import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from pathlib import Path

hf_token = os.getenv("HF_TOKEN")

# Load strong Arabic embedding model
model = SentenceTransformer(
    "BAAI/bge-m3",
    token=hf_token
)


folder = "extracted_articles"

texts = []
ids = []

for fname in sorted(os.listdir(folder)):
    if fname.endswith(".txt"):
        path = os.path.join(folder, fname)
        file = Path(path)
        if file.stat().st_size == 0:
            continue
        with open(path, "r", encoding="utf8") as f:
            text = f.read()

        ids.append(fname)
        texts.append(text)

print("Embedding", len(texts), "articles")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True
)

embeddings = embeddings.astype("float32")

count = embeddings.shape[0]
dim = embeddings.shape[1]

print("dimension:", dim)

# Save embeddings
with open("embeddings.bin", "wb") as f:
    f.write(np.int32(count))
    f.write(np.int32(dim))
    embeddings.tofile(f)

# Save metadata
with open("metadata.json", "w", encoding="utf8") as f:
    json.dump(ids, f, ensure_ascii=False)

print("Done")