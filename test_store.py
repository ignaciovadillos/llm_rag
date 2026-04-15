from rag import load_collection, retrieve

collection = load_collection("owl_db")

query = "What is the name of Harry's owl?"
results = retrieve(query, collection, k=3)

for i, (chunk, meta, distance) in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print(f"Book: {meta['book']}")
    print(f"Chapter: {meta['chapter_number']} - {meta['chapter_title']}")
    print(f"Distance: {distance}")
    print(chunk[:300])