import os
import random
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = "documents"

# 350 tokens * 4 chars/token = 1400 chars; 50 tokens * 4 chars/token = 200 chars
CHUNK_SIZE = 1400
CHUNK_OVERLAP = 200


def load_documents(docs_dir):
    docs = []
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith(".txt"):
            path = os.path.join(docs_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if text:
                docs.append({"source": filename, "text": text})
    return docs


def chunk_text(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = []
    for doc in docs:
        splits = splitter.split_text(doc["text"])
        for i, split in enumerate(splits):
            if split.strip():
                chunks.append({
                    "source": doc["source"],
                    "chunk_index": i,
                    "text": split.strip(),
                })
    return chunks


if __name__ == "__main__":
    docs = load_documents(DOCS_DIR)
    print(f"Loaded {len(docs)} documents\n")

    chunks = chunk_text(docs)
    print(f"Total chunks: {len(chunks)}")
    print(f"(Expected range: 50–2000 chunks across 10 documents)\n")

    print("--- 5 Random Chunks ---\n")
    for i, chunk in enumerate(random.sample(chunks, min(5, len(chunks))), 1):
        print(f"[Chunk {i} — {chunk['source']}, index {chunk['chunk_index']}]")
        print(chunk["text"])
        print()
