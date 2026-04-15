from loader import BOOK_SOURCES

for filename, info in BOOK_SOURCES.items():
    print(filename, "->", info["title"], "|", info["type"])