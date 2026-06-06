import argparse
import json
import os
from pathlib import Path
from typing import List, Dict

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def load_json_file(file_path: Path) -> List[Dict]:
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print(f"Warning: {file_path} does not contain a JSON array. Skipping.")
                return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Ingest ChatGPT JSON exports into ChromaDB.")
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory containing ChatGPT JSON export files.",
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="./chroma_db",
        help="Path to the local ChromaDB directory (default: ./chroma_db)",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="chatgpt_conversations",
        help="Name of the ChromaDB collection (default: chatgpt_conversations)",
    )

    args = parser.parse_args()
    input_dir = Path(args.directory)

    if not input_dir.is_dir():
        print(f"Error: Directory not found: {input_dir}")
        return

    # Initialize ChromaDB client
    db_path = Path(args.db_path).resolve()
    print(f"Connecting to ChromaDB at: {db_path}")
    db_path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_path))
    embedder = SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

    collection = client.get_or_create_collection(
        name=args.collection,
        embedding_function=embedder,
        metadata={"description": "ChatGPT Export Conversations"}
    )

    json_files = list(input_dir.glob("*.json"))
    if not json_files:
        print(f"No .json files found in {input_dir}")
        return

    print(f"Found {len(json_files)} JSON files to process.")

    total_added = 0
    for file_path in json_files:
        print(f"Processing {file_path.name}...")
        records = load_json_file(file_path)

        ids = []
        texts = []
        metadatas = []

        for i, record in enumerate(records):
            # Extract relevant fields
            content = record.get("content")
            if not content:
                continue

            conv_id = record.get("conversation_id", f"unknown-{file_path.stem}")
            msg_idx = record.get("message_index", i)
            role = record.get("role", "unknown")
            created_at = record.get("created_at", "")

            # Create a unique ID
            doc_id = f"{conv_id}-{msg_idx}-{role}"

            ids.append(doc_id)
            texts.append(content)
            metadatas.append({
                "conversation_id": conv_id,
                "role": role,
                "source_file": file_path.name,
                "created_at": created_at
            })

        if ids:
            try:
                # Upsert to handle duplicates gracefully
                collection.upsert(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas
                )
                total_added += len(ids)
                print(f"  Added/Updated {len(ids)} records from {file_path.name}")
            except Exception as e:
                print(f"  Error inserting records from {file_path.name}: {e}")

    print(f"\nIngestion complete. Added/Updated a total of {total_added} records.")
    print(f"Total documents in collection '{args.collection}': {collection.count()}")

if __name__ == "__main__":
    main()
