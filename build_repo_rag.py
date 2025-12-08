"""Utility to build a local Chroma vector store from this repository's content.

Run this script to transform the repository files into your own RAG-ready index.
The resulting Chroma database is stored in the directory you pass via
``--persist-dir`` (defaults to ``local_chroma``).

Example:
    python build_repo_rag.py --persist-dir local_chroma
"""

import argparse
import os
from pathlib import Path
from typing import Iterable, List, Tuple

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# File types that typically contain relevant textual content
DEFAULT_EXTENSIONS = {".md", ".txt", ".py", ".html", ".json"}
DEFAULT_EXCLUDE_DIRS = {".git", "__pycache__", "venv", "env"}


def iter_text_files(
    root: Path, extensions: Iterable[str], exclude_dirs: Iterable[str], max_file_mb: int
) -> Iterable[Tuple[Path, str]]:
    """Yield (path, content) for files under ``root`` with matching extensions."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories and virtual envs/git metadata
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in exclude_dirs]

        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() not in extensions:
                continue

            if path.stat().st_size > max_file_mb * 1024 * 1024:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            yield path, text


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> Iterable[str]:
    """Split text into overlapping chunks to keep embeddings focused."""
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        yield text[start:end]
        if end == text_length:
            break

        start += chunk_size - chunk_overlap


def build_chroma_index(
    documents: List[Tuple[Path, int, str]], persist_dir: Path, repo_root: Path
) -> None:
    """Create a Chroma collection from the provided documents."""
    persist_dir.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(persist_dir))
    embedder = SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
    collection = client.get_or_create_collection(
        name="repo_documents",
        embedding_function=embedder,
        metadata={"source": "rag_index_repo"},
    )

    ids: List[str] = []
    texts: List[str] = []
    metadatas: List[dict] = []

    for path, chunk_index, content in documents:
        relative = path.relative_to(repo_root)
        chunk_id = f"{relative}::chunk-{chunk_index:04d}"

        ids.append(chunk_id)
        texts.append(content)
        metadatas.append({"path": str(relative), "chunk": chunk_index})

    if ids:
        collection.upsert(documents=texts, ids=ids, metadatas=metadatas)



def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Chroma index from this repo.")
    parser.add_argument(
        "--persist-dir",
        type=Path,
        default=Path("local_chroma"),
        help="Directory where the Chroma DB will be stored.",
    )
    parser.add_argument(
        "--extensions",
        type=str,
        nargs="*",
        default=sorted(DEFAULT_EXTENSIONS),
        help="File extensions to index (include the dot).",
    )
    parser.add_argument(
        "--exclude-dirs",
        type=str,
        nargs="*",
        default=sorted(DEFAULT_EXCLUDE_DIRS),
        help="Folder names to skip while crawling.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=900,
        help="Number of characters per text chunk.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Overlap between consecutive chunks (characters).",
    )
    parser.add_argument(
        "--max-file-mb",
        type=int,
        default=2,
        help="Skip files larger than this size (in megabytes).",
    )

    args = parser.parse_args()

    extensions = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in args.extensions}
    exclude_dirs = set(args.exclude_dirs)
    repo_root = Path.cwd()
    documents: List[Tuple[Path, int, str]] = []

    for path, raw_text in iter_text_files(repo_root, extensions, exclude_dirs, args.max_file_mb):
        for chunk_index, chunk in enumerate(
            chunk_text(raw_text, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
        ):
            documents.append((path, chunk_index, chunk))

    print(f"🗂️  Found {len(documents)} documents to index.")
    if not documents:
        return

    build_chroma_index(documents, args.persist_dir, repo_root)
    print(f"✅ Chroma index created at: {args.persist_dir}")


if __name__ == "__main__":
    main()
