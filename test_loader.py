from loader import load_all_books

chapters = load_all_books("data/")
print(chapters[0])
print(chapters[1])
print(f"Parsed chapters: {len(chapters)}")