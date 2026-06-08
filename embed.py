import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, chunk_text

DOCS_DIR = "documents"
DB_DIR = "chroma_db"
COLLECTION_NAME = "utd_housing"
TOP_K = 5

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store():
    docs = load_documents(DOCS_DIR)
    chunks = chunk_text(docs)

    client = chromadb.PersistentClient(path=DB_DIR)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]
    ids = [f"{c['source']}_{c['chunk_index']}" for c in chunks]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    print(f"\nStored {len(chunks)} chunks in ChromaDB.")
    return collection


def get_collection():
    client = chromadb.PersistentClient(path=DB_DIR)
    return client.get_collection(COLLECTION_NAME)


def retrieve(query, k=TOP_K):
    collection = get_collection()
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance": round(distance, 4),
        })
    return chunks


if __name__ == "__main__":
    print("Building vector store...\n")
    build_vector_store()

    test_queries = [
        "Are Canyon Creek Heights apartments furnished?",
        "Are the UTD dorms single occupancy or shared rooms?",
        "Do the Canyon Creek Heights apartments include utilities in rent?",
        "Is Canyon Creek Heights safe?",
        "Are there any problems with maintenance or insects?",
    ]

    for query in test_queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print(f"{'=' * 60}")
        results = retrieve(query)
        for i, r in enumerate(results, 1):
            print(f"\n[Result {i} — {r['source']}, chunk {r['chunk_index']} | distance: {r['distance']}]")
            print(r["text"])
