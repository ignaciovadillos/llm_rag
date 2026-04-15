from loader import load_all_books, chunk_book_chapters
from store import build_vector_store

chapters = load_all_books("../data/")
docs, metas, ids = chunk_book_chapters(chapters)

build_vector_store(docs, metas, ids, persist_dir=".")
print("Indexing complete. You can now run app.py")