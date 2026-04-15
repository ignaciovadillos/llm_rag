import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

EMBED_MODEL = "all-MiniLM-L6-v2"

embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)


def build_vector_store(docs, metas, ids, persist_dir="owl_db"):
    client = chromadb.PersistentClient(path=persist_dir)

    try:
        client.delete_collection("harry_potter")
        print("Deleted existing collection: harry_potter")
    except Exception:
        print("No existing collection to delete")

    collection = client.create_collection(
        name="harry_potter",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )

    batch_size = 500

    for i in range(0, len(docs), batch_size):
        collection.add(
            documents=docs[i:i + batch_size],
            metadatas=metas[i:i + batch_size],
            ids=ids[i:i + batch_size]
        )
        print(f"Indexed {min(i + batch_size, len(docs))}/{len(docs)} chunks")

    print(f"Vector store built at: {persist_dir}")
    return collection