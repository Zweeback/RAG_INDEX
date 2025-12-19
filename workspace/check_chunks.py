#!/usr/bin/env python3
import json

try:
    with open('data/processed_chunks.json', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if it's a list or dict
    if isinstance(data, list):
        print(f"✓ processed_chunks.json ist eine Liste")
        print(f"  Anzahl Chunks: {len(data)}")
        if len(data) > 0:
            print(f"  Erstes Chunk: {data[0][:80] if isinstance(data[0], str) else data[0]}")
    elif isinstance(data, dict):
        print(f"✓ processed_chunks.json ist ein Dict")
        if 'chunks' in data:
            chunks = data['chunks']
            print(f"  Anzahl Chunks: {len(chunks)}")
            if len(chunks) > 0:
                print(f"  Erstes Chunk: {chunks[0][:80] if isinstance(chunks[0], str) else chunks[0]}")
        else:
            print(f"  Keys: {data.keys()}")
except Exception as e:
    print(f"✗ Fehler: {e}")
