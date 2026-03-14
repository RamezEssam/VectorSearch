import os
import json
import numpy as np
import hnswlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from sentence_transformers import SentenceTransformer

# -----------------------------
# Config
# -----------------------------
EMBEDDINGS_FILE = "embeddings.bin"
METADATA_FILE = "metadata.json"
HNSW_INDEX_FILE = "hnsw_index.bin"
EMBEDDING_MODEL = "BAAI/bge-m3"
ARTICLES_DIR = "extracted_articles"
DEFAULT_TOP_K = 5
hf_token = os.getenv("HF_TOKEN")

# -----------------------------
# Load embeddings
# -----------------------------
print("Loading embeddings...")

with open(EMBEDDINGS_FILE, "rb") as f:
    count = np.frombuffer(f.read(4), dtype=np.int32)[0]
    dim = np.frombuffer(f.read(4), dtype=np.int32)[0]
    embeddings = np.frombuffer(f.read(), dtype=np.float32).reshape(count, dim)

print(f"Loaded {count} embeddings")

# -----------------------------
# Load metadata
# -----------------------------
with open(METADATA_FILE, "r", encoding="utf8") as f:
    metadata = json.load(f)

# -----------------------------
# Load index
# -----------------------------
index = hnswlib.Index(space='cosine', dim=dim)

if os.path.exists(HNSW_INDEX_FILE):
    print("Loading HNSW index...")
    index.load_index(HNSW_INDEX_FILE)
    index.set_ef(50)
else:
    index.init_index(max_elements=count, ef_construction=200, M=16)
    index.add_items(embeddings, np.arange(count))
    index.set_ef(50)
    index.save_index(HNSW_INDEX_FILE)

# -----------------------------
# Load embedding model
# -----------------------------
print("Loading model...")
model = SentenceTransformer(
    EMBEDDING_MODEL,
    token=hf_token
)

# -----------------------------
# HTTP Handler
# -----------------------------
class SearchHandler(BaseHTTPRequestHandler):

    # Handle CORS preflight
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

    def do_POST(self):

        if self.path != "/search":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        query = data.get("query", "").strip()
        top_k = data.get("top_k", DEFAULT_TOP_K)

        if not query:
            results = []
        else:
            query_emb = model.encode([query], normalize_embeddings=True).astype("float32")
            labels, distances = index.knn_query(query_emb, k=top_k)

            results = []
            for idx, dist in zip(labels[0], distances[0]):
                filename = metadata[idx]
                filepath = os.path.join(ARTICLES_DIR, filename)
                text = ""
                if os.path.exists(filepath):
                    with open(filepath, "r", encoding="utf8") as f:
                        text = f.read()
                results.append({"title": filename, "text": text, "score": float(1 - dist)})

        response = json.dumps({"results": results}).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(response)

# -----------------------------
# Run server
# -----------------------------
PORT = 6969

server = HTTPServer(("localhost", PORT), SearchHandler)

print(f"Server running on http://localhost:{PORT}")

server.serve_forever()