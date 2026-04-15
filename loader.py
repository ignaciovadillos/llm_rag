import re
from dataclasses import dataclass
from typing import List

# Map filenames to book titles
BOOK_TITLES = {
    "hp1.txt": "Harry Potter and the Philosopher's Stone",
    "hp2.txt": "Harry Potter and the Chamber of Secrets",
    "hp3.txt": "Harry Potter and the Prisoner of Azkaban",
    "hp4.txt": "Harry Potter and the Goblet of Fire",
    "hp5.txt": "Harry Potter and the Order of the Phoenix",
    "hp6.txt": "Harry Potter and the Half-Blood Prince",
    "hp7.txt": "Harry Potter and the Deathly Hallows",
}

# Data structure for chapters
@dataclass
class TextChunk:
    text: str
    book: str
    chapter_number: int
    chapter_title: str


# Regex to match different chapter formats
CHAPTER_PATTERN = re.compile(
    r'(?i)^chapter\s+(\w+)\s*[:\-\s]*(.*)$',
    re.MULTILINE
)


def parse_book(filepath: str, book_title: str) -> List[TextChunk]:
    """Split a book into chapters and return labelled chunks."""

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    matches = list(CHAPTER_PATTERN.finditer(text))
    chunks = []

    for i, match in enumerate(matches):
        chapter_num_str = match.group(1).strip()
        chapter_title = match.group(2).strip()

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        chapter_text = text[start:end].strip()

        # Try to convert chapter number
        try:
            chapter_num = int(chapter_num_str)
        except ValueError:
            chapter_num = i + 1  # fallback

        chunks.append(
            TextChunk(
                text=chapter_text,
                book=book_title,
                chapter_number=chapter_num,
                chapter_title=chapter_title
            )
        )

    return chunks


def load_all_books(data_dir: str = "data/") -> List[TextChunk]:
    """Load all books and parse them into chapters."""

    all_chunks = []

    for filename, title in BOOK_TITLES.items():
        path = f"{data_dir}{filename}"
        print(f"Loading: {title}")

        book_chunks = parse_book(path, title)
        all_chunks.extend(book_chunks)

    print(f"Total chapters parsed: {len(all_chunks)}")
    return all_chunks

from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)


def chunk_book_chapters(chapters):
    """Split chapters into smaller chunks, preserving metadata."""

    all_docs = []
    all_metas = []
    all_ids = []

    for ch in chapters:
        sub_chunks = splitter.split_text(ch.text)

        for j, sub in enumerate(sub_chunks):
            all_docs.append(sub)

            all_metas.append({
                "book": ch.book,
                "chapter_number": ch.chapter_number,
                "chapter_title": ch.chapter_title,
                "chunk_index": j
            })

            # Create unique ID
            safe_book = ch.book.replace(" ", "_").replace("'", "")
            chunk_id = f"{safe_book}_ch{ch.chapter_number}_p{j}"
            all_ids.append(chunk_id)

    print(f"Total chunks created: {len(all_docs)}")
    return all_docs, all_metas, all_ids