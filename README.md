# 🧠 ChatGPT Knowledge Base

**RAG System für 2.927 ChatGPT Conversations**

Durchsuche deine ChatGPT History mit verschiedenen Analyse-Perspektiven!

---

## ✨ Features

- 🔍 **6 Query-Modi**: Analytiker, Coach, Kritiker, Zusammenfassung, Handlung, Beziehungen
- 📱 **Mobile-optimiert**: Läuft auf iPhone/Android
- 🆓 **100% kostenlos**: Hosted auf Hugging Face
- 🔒 **Privat & sicher**: Deine Daten bleiben bei dir

---

## 🚀 Live Demo

**Deployed auf Hugging Face Spaces:**

👉 **[https://huggingface.co/spaces/Benjieboy/RAG](https://huggingface.co/spaces/Benjieboy/RAG)**

---

## 🎯 Verwendung

### Query-Modi wählen:

Jeder Modus gibt eine andere Perspektive:

- **🔍 Analytiker**: Objektive Fakten & Muster
- **💭 Coach**: Einfühlsames, konstruktives Feedback
- **⚡ Kritiker**: Kritisches Hinterfragen
- **📝 Zusammenfassung**: Kompakter Überblick
- **🎯 Handlung**: Konkrete nächste Schritte
- **🔮 Beziehungen**: Analyse sozialer Dynamiken

---

## 🛠️ Tech Stack

- **Frontend**: Gradio
- **Vector DB**: ChromaDB  
- **Embeddings**: sentence-transformers
- **LLM**: Mistral 7B (HF Inference API)
- **Hosting**: Hugging Face Spaces

---

## 📦 Deployment

Siehe **[SETUP.md](SETUP.md)** für Schritt-für-Schritt Anleitung!

---

## 🧰 Eigenen RAG-Index bauen

Du willst die Inhalte dieses Repos oder deine eigenen Dateien in einen frischen Chroma-Vektorstore schreiben? Mit dem neuen Helper-Script geht das in Sekunden – inklusive automatischem Chunking für bessere Embeddings:

```bash
pip install -r requirements.txt
python build_repo_rag.py --persist-dir local_chroma
```

Was passiert dabei?

- Alle Text-, Markdown-, HTML-, JSON- und Python-Dateien im Repo werden eingelesen (weitere Endungen steuerbar über `--extensions`)
- Dateien größer als 2 MB werden standardmäßig übersprungen
- Die Inhalte werden in überlappende Chunks (900 Zeichen, 200 Zeichen Overlap) aufgeteilt, damit die Embeddings fokussiert bleiben
- Es wird ein Chroma-Index in `local_chroma/` angelegt
- Metadaten enthalten den relativen Dateipfad und die Chunk-Nummer, damit du später die Herkunft nachvollziehen kannst

Du kannst Dateiendungen anpassen, z. B. nur Markdown indizieren:

```bash
python build_repo_rag.py --extensions .md --persist-dir local_chroma
```

Chunking und File-Filter kannst du ebenfalls tunen, z. B. kleinere Chunks und zusätzlich Logs von Unterordnern ausschließen:

```bash
python build_repo_rag.py \
  --persist-dir local_chroma \
  --chunk-size 600 \
  --chunk-overlap 150 \
  --exclude-dirs .git venv logs
```

Den entstandenen Vektorstore kannst du in deinem eigenen RAG-Workflow weiterverwenden oder in deine Streamlit/Gradio-App einbinden.

---

**⭐ Star das Repo wenn es dir hilft!**
