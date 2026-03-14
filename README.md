# VectorSearch

A simple semantic search engine for legal documents using embeddings and
vector similarity.

The system converts legal articles into embeddings and allows users to
search them using natural language queries. Results are ranked by
semantic similarity.

------------------------------------------------------------------------

# Features

-   Semantic search over legal text
-   Arabic and English article support
-   Embedding generation using SentenceTransformers
-   Fast nearest‑neighbor search with HNSW
-   Simple web interface for querying

------------------------------------------------------------------------

# Running Locally

## 1 Clone the repository

``` bash
git clone https://github.com/RamezEssam/VectorSearch.git
cd VectorSearch
```

------------------------------------------------------------------------

## 2 Create a Python environment

``` bash
python -m venv venv
source venv/bin/activate
```

Windows:

``` powershell
venv\Scripts\activate.ps1
```

------------------------------------------------------------------------

## 3 Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 4 Set your HuggingFace token

Some embedding models require authentication.

Linux / Mac:

``` bash
export HF_TOKEN=your_token_here
```

Windows PowerShell:

``` powershell
$env:HF_TOKEN="your_token_here"
```

------------------------------------------------------------------------

## 5 Build the vector index (first time only)

If embeddings and index files are not present, generate them:

``` bash
python embed.py
```

This will create:

    embeddings.bin
    metadata.json


------------------------------------------------------------------------

## 6 Start the API server

``` bash
python query.py
```
This will create or load the index: hnsw_index.bin

The server will start on:

    http://localhost:6969

------------------------------------------------------------------------

## 7 Open the search interface

Open the frontend in your browser:

    index.html

Enter a query and view the most relevant legal articles.

------------------------------------------------------------------------

# Example Query

    What rights does a tenant have to sublease an apartment?

The system returns the most semantically relevant legal articles ranked
by similarity.

------------------------------------------------------------------------

# Notes

-   The first run may take time while downloading embedding models.
-   Large embedding files are excluded from Git using `.gitignore`.

------------------------------------------------------------------------

# License

This project is provided for educational and experimentation purposes.
