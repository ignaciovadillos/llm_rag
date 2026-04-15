from loader import load_all_books, chunk_book_chapters

chapters = load_all_books("data/")
docs, metas, ids = chunk_book_chapters(chapters)

print(f"Total chapters: {len(chapters)}")
print(f"Total chunked docs: {len(docs)}")
print(f"Total metadata rows: {len(metas)}")
print(f"Total ids: {len(ids)}")

print("\nFIRST CHUNK:\n")
print(docs[0])

print("\nFIRST META:\n")
print(metas[0])

print("\nFIRST ID:\n")
print(ids[0])