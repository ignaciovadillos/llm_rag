# The Know-It Owl

The Know-It Owl is a Harry Potter RAG chatbot built with `ChromaDB`, `sentence-transformers`, `Ollama`, and `Streamlit`.
It retrieves passages from the book corpus, answers in character, and shows chapter-level source citations in the UI.

## What This Repo Contains

- `loader.py`: parses book files into chapter chunks, then sub-chunks them for retrieval
- `store.py`: builds the Chroma vector store
- `rag.py`: retrieves relevant chunks and calls the local Ollama model
- `index.py`: indexing entry point that creates `owl_db/`
- `app.py`: Streamlit chat app
- `test_*.py`: small manual test scripts for checking parsing, chunking, retrieval, and generation

## Current Scope

Right now the retriever indexes the seven main Harry Potter novels listed in `loader.py`:

- `HP1.txt`
- `HP2.txt`
- `HP3.txt`
- `HP4.txt`
- `HP5.txt`
- `HP6.txt`
- `HP7.txt`

The `data/` folder in this workspace also contains supplementary Wizarding World texts, but they are not loaded by the current `BOOK_TITLES` mapping, so they are not part of the indexed corpus unless you extend `loader.py`.

## Requirements

- Python 3.10+
- `pip`
- Ollama installed locally
- The Ollama model used by `rag.py`: `qwen2.5:7b`

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Pull the local Ollama model:

```bash
ollama pull qwen2.5:7b
```

## Data Layout

Place the source text files in `data/`.
This repo already ignores `data/*.txt`, so large book files stay out of version control.

Expected working structure:

```text
hm_harry_potter/
├── app.py
├── index.py
├── loader.py
├── rag.py
├── requirements.txt
├── store.py
├── data/
│   ├── HP1.txt
│   ├── HP2.txt
│   ├── ...
│   └── HP7.txt
└── owl_db/
```

## Build The Vector Store

From the project root, run:

```bash
python index.py
```

This will:

- load the Harry Potter text files from `data/`
- split them into chunks
- embed them with `all-MiniLM-L6-v2`
- create or replace the Chroma collection in `owl_db/`

You only need to rebuild the index when the corpus changes.

## Run The App

Start the Streamlit interface with:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit, usually `http://localhost:8501`.

## How Answering Works

1. The app loads the persisted Chroma collection from `owl_db/`.
2. A user question is used to retrieve the most relevant chunks.
3. The retrieved context is sent to Ollama with the owl system prompt.
4. The response is shown in character, followed by a list of cited sources.

## Useful Test Scripts

These are simple manual checks rather than a full automated test suite:

- `python test_loader.py`
- `python test_chunking.py`
- `python test_store.py`
- `python test_rag.py`
- `python test_generation.py`

They assume the required data files and, for retrieval/generation checks, a built `owl_db/`.

## Notes

- The app expects a local vector store in `owl_db/`.
- `rag.py` currently defaults to `qwen2.5:7b`.
- The chatbot is designed to stay in the Wizarding World voice and avoid unsupported claims.
- If you want the extra texts in `data/` to be searchable, update `BOOK_TITLES` in `loader.py` and rebuild the index.
