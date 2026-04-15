import re
from dataclasses import dataclass
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

BOOK_TITLES = {
    "HP1.txt": "Harry Potter and the Philosopher's Stone",
    "HP2.txt": "Harry Potter and the Chamber of Secrets",
    "HP3.txt": "Harry Potter and the Prisoner of Azkaban",
    "HP4.txt": "Harry Potter and the Goblet of Fire",
    "HP5.txt": "Harry Potter and the Order of the Phoenix",
    "HP6.txt": "Harry Potter and the Half-Blood Prince",
    "HP7.txt": "Harry Potter and the Deathly Hallows",
}


@dataclass
class TextChunk:
    text: str
    book: str
    chapter_number: int
    chapter_title: str


CHAPTER_PATTERN = re.compile(
    r'(?i)^chapter\s+(\w+)\s*[:\-\s]*(.*)$',
    re.MULTILINE
)


def parse_book(filepath: str, book_title: str) -> List[TextChunk]:
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

        try:
            chapter_num = int(chapter_num_str)
        except ValueError:
            chapter_num = i + 1

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
    all_chunks = []

    for filename, title in BOOK_TITLES.items():
        path = f"{data_dir}{filename}"
        print(f"Loading: {title}")
        all_chunks.extend(parse_book(path, title))

    print(f"Total chapters parsed: {len(all_chunks)}")
    return all_chunks


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)


def chunk_book_chapters(chapters):
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

            safe_book = ch.book.replace(" ", "_").replace("'", "")
            all_ids.append(f"{safe_book}_ch{ch.chapter_number}_p{j}")

    print(f"Total chunks created: {len(all_docs)}")
    return all_docs, all_metas, all_ids