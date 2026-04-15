from rag import load_collection, ask_owl

collection = load_collection("owl_db")
history = []

query = "What is the name of Harry's owl?"
answer, sources = ask_owl(query, collection, history)

print("\nANSWER:\n")
print(answer)

print("\nSOURCES:\n")
for _, meta, dist in sources:
    print(f"{meta['book']} | Chapter {meta['chapter_number']} | {meta['chapter_title']} | distance={dist}")