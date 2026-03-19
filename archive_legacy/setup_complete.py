"""
RAG SYSTEM - KOMPLETTES SETUP
==============================
Führe dieses Script aus, um ALLES einzurichten!

Voraussetzungen:
1. chroma_db.zip im gleichen Ordner
2. Python 3.8+
3. pip installiert

Das Script macht:
✓ Entpackt ChromaDB
✓ Installiert alle Pakete
✓ Testet die Verbindung
✓ Zeigt Statistiken
"""

import os
import sys
import zipfile
import subprocess
from pathlib import Path

def print_status(msg, status="INFO"):
    symbols = {"INFO": "ℹ️", "OK": "✅", "ERROR": "❌", "WAIT": "⏳"}
    print(f"\n{symbols.get(status, '•')} {msg}")

def install_packages():
    """Installiert benötigte Pakete"""
    print_status("Installiere Pakete...", "WAIT")
    
    packages = [
        "chromadb",
        "sentence-transformers",
        "pandas",
        "tqdm"
    ]
    
    for pkg in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
            print(f"  ✓ {pkg}")
        except:
            print(f"  ✗ {pkg} (Fehler - bitte manuell installieren)")
    
    print_status("Pakete installiert!", "OK")

def extract_chromadb():
    """Entpackt chroma_db.zip"""
    zip_path = "chroma_db.zip"
    extract_path = "./chroma_db"
    
    if not os.path.exists(zip_path):
        print_status(f"chroma_db.zip nicht gefunden!", "ERROR")
        print("Bitte lege chroma_db.zip in diesen Ordner:")
        print(f"  {os.getcwd()}")
        return False
    
    if os.path.exists(extract_path):
        print_status("ChromaDB bereits entpackt", "INFO")
        return True
    
    print_status("Entpacke ChromaDB...", "WAIT")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # Größe berechnen
        size_mb = sum(f.stat().st_size for f in Path(extract_path).rglob('*')) / 1024 / 1024
        print_status(f"ChromaDB entpackt! ({size_mb:.1f} MB)", "OK")
        return True
    except Exception as e:
        print_status(f"Fehler beim Entpacken: {e}", "ERROR")
        return False

def test_connection():
    """Testet ChromaDB Verbindung"""
    print_status("Teste ChromaDB Verbindung...", "WAIT")
    
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(
            name="chatgpt_conversations",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )
        
        count = collection.count()
        print_status(f"Verbindung OK! {count} Conversations gefunden!", "OK")
        
        # Erste Conversation als Test
        sample = collection.get(limit=1, include=["documents", "metadatas"])
        if sample['documents']:
            print("\n📄 Beispiel-Conversation:")
            print(f"   {sample['documents'][0][:200]}...")
        
        return True
    except Exception as e:
        print_status(f"Verbindungsfehler: {e}", "ERROR")
        return False

def create_folder_structure():
    """Erstellt Ordnerstruktur"""
    folders = ["backups", "exports", "scripts"]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    print_status("Ordnerstruktur erstellt", "OK")

def main():
    print("=" * 60)
    print("  RAG SYSTEM - KOMPLETTES SETUP")
    print("=" * 60)
    
    # Schritt 1: Pakete installieren
    install_packages()
    
    # Schritt 2: ChromaDB entpacken
    if not extract_chromadb():
        return
    
    # Schritt 3: Ordner erstellen
    create_folder_structure()
    
    # Schritt 4: Verbindung testen
    if not test_connection():
        return
    
    # Fertig!
    print("\n" + "=" * 60)
    print_status("SETUP ABGESCHLOSSEN!", "OK")
    print("=" * 60)
    print("\n📋 NÄCHSTE SCHRITTE:")
    print("   1. Führe 'python query_simple.py' aus zum Suchen")
    print("   2. Oder öffne 'RAG_COMPLETE_GUIDE.md' für mehr Infos")
    print("\n💡 TIPP: Nutze 'python extract_relationships.py' für Beziehungsanalyse!")
    print()

if __name__ == "__main__":
    main()
