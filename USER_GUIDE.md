# ChatGPT Export Ingestion Guide

## What are these JSON files?
Die Dateien, die du in deinem Ordner (z.B. `C:\Users\derzw\Desktop\STATE_BASE_AUDIT\OVERSIGHT_CORE\02_ARCHIVE_RAW\ChatGPT_Exports_Raw_2026-05\`) hast, sind aufgeteilte Exporte deiner ChatGPT-Historie. Da der gesamte Export oft sehr groß ist, wurde er in mehrere kleine `conversations-xxx.json` Dateien zerlegt. Diese enthalten deine bisherigen Chats, aufbereitet als JSON-Format.

## How to add them to your Knowledge Base (RAG)
Um diese Chats in dein RAG-System (Ben's Knowledge Base) zu laden, musst du sie in die lokale ChromaDB importieren. Dafür haben wir ein Skript vorbereitet.

### Schritt-für-Schritt Anleitung (Windows)

1. Öffne ein Terminal (Eingabeaufforderung / PowerShell).
2. Navigiere in das Verzeichnis deines RAG-Projekts (dort wo dieses `USER_GUIDE.md` liegt).
3. Führe das Ingestion-Skript aus und übergebe den Pfad zu deinem Ordner mit den JSON-Dateien als Argument.

**Befehl:**
```bash
python scripts\ingest_chatgpt_exports.py "C:\Users\derzw\Desktop\STATE_BASE_AUDIT\OVERSIGHT_CORE\02_ARCHIVE_RAW\ChatGPT_Exports_Raw_2026-05"
```

Das Skript wird alle `.json` Dateien in diesem Ordner lesen, die Texte extrahieren und in deine lokale `chroma_db` Datenbank einfügen, sodass sie von deinem RAG System (z.B. dem Flask Server oder der Streamlit App) gefunden werden können.
