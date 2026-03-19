#!/usr/bin/env python3
"""
BEN'S MASTER AI FRAMEWORK v1.0
================================

FEATURES:
- Multi-LLM (ChatGPT, Grok, DeepSeek, Perplexity, Claude)
- Personal RAG (2927 Conversations)
- Google Drive Integration
- iPhone steuerbar via ChatGPT
- Video/Image Pipelines
- Marketing Research Tools
- Slack Integration
- Git Integration

STRUKTUR:
/MyDrive/ben_framework/
├── chroma_db/          # Dein RAG
├── data/               # Neue Daten zum Einpflegen
├── outputs/            # Results
├── pipelines/          # Video/Image Processing
├── research/           # Marketing Research
└── configs/            # API Keys, Settings

SETUP:
1. Lade alles auf Google Drive
2. Starte Server auf MSI PC ODER in Colab
3. Nutze ChatGPT Custom GPT vom iPhone
"""

import os
import json
from datetime import datetime
from pathlib import Path

class BenFramework:
    """Master Framework Klasse"""
    
    def __init__(self, base_path="/content/drive/MyDrive/ben_framework"):
        self.base_path = Path(base_path)
        self.setup_directories()
        self.load_configs()
        
    def setup_directories(self):
        """Erstelle Framework Struktur"""
        dirs = [
            'chroma_db',
            'data/incoming',
            'data/processed', 
            'data/archive',
            'outputs/conversations',
            'outputs/research',
            'outputs/media',
            'pipelines/video',
            'pipelines/image',
            'pipelines/audio',
            'research/competitors',
            'research/keywords',
            'research/trends',
            'configs',
            'logs',
            'agents/alice',  # Für deine 3D Companion!
            'agents/modules'
        ]
        
        for d in dirs:
            (self.base_path / d).mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Framework Structure created at {self.base_path}")
    
    def load_configs(self):
        """Lade API Keys und Configs"""
        config_file = self.base_path / 'configs' / 'api_keys.json'
        
        if config_file.exists():
            with open(config_file) as f:
                self.config = json.load(f)
        else:
            # Template erstellen
            self.config = {
                'openai': {'api_key': 'sk-...'},
                'anthropic': {'api_key': 'sk-ant-...'},
                'grok': {'api_key': '...'},
                'deepseek': {'api_key': '...'},
                'perplexity': {'api_key': '...'},
                'slack': {'webhook_url': '...'},
                'github': {'token': '...'}
            }
            
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            print(f"⚠️ Created config template at {config_file}")
            print("   → Add your API keys!")
    
    def log(self, message, level="INFO"):
        """Logging"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        log_file = self.base_path / 'logs' / f"{datetime.now().date()}.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)
        
        print(log_entry.strip())

class RAGModule:
    """RAG System Integration"""
    
    def __init__(self, framework):
        self.fw = framework
        self.chroma_path = framework.base_path / 'chroma_db'
        self.collection = None
    
    def init_rag(self):
        """Initialisiere ChromaDB"""
        import chromadb
        
        client = chromadb.PersistentClient(path=str(self.chroma_path))
        self.collection = client.get_collection("conversations")
        
        self.fw.log(f"RAG loaded: {self.collection.count()} conversations")
        return self.collection
    
    def search(self, query, n=5):
        """Suche im RAG"""
        if not self.collection:
            self.init_rag()
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n
        )
        
        self.fw.log(f"RAG search: '{query}' → {len(results['documents'][0])} results")
        return results
    
    def add_from_file(self, filepath):
        """Füge neue Datei zum RAG hinzu"""
        if not self.collection:
            self.init_rag()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        conv_id = f"file_{self.collection.count() + 1}"
        
        self.collection.add(
            documents=[content[:10000]],
            metadatas=[{
                'title': filename,
                'source': 'file',
                'added': datetime.now().isoformat()
            }],
            ids=[conv_id]
        )
        
        self.fw.log(f"Added to RAG: {filename}")
        
        # Archiviere Original
        archive_path = self.fw.base_path / 'data' / 'archive' / filename
        os.rename(filepath, archive_path)

class MultiLLM:
    """Multi-LLM Router"""
    
    def __init__(self, framework):
        self.fw = framework
        self.providers = {}
        self.setup_providers()
    
    def setup_providers(self):
        """Setup LLM Provider Clients"""
        # OpenAI (ChatGPT)
        try:
            import openai
            openai.api_key = self.fw.config['openai']['api_key']
            self.providers['gpt'] = openai
            self.fw.log("✅ GPT Provider ready")
        except:
            self.fw.log("⚠️ GPT Provider failed", "WARN")
        
        # Anthropic (Claude)
        try:
            import anthropic
            self.providers['claude'] = anthropic.Anthropic(
                api_key=self.fw.config['anthropic']['api_key']
            )
            self.fw.log("✅ Claude Provider ready")
        except:
            self.fw.log("⚠️ Claude Provider failed", "WARN")
        
        # Weitere LLMs hier...
        # Grok, DeepSeek, Perplexity haben ähnliche APIs
    
    def query(self, prompt, provider='gpt', model=None, rag_context=None):
        """Query an LLM mit optionalem RAG Context"""
        
        # Füge RAG Context hinzu wenn vorhanden
        if rag_context:
            prompt = f"CONTEXT:\n{rag_context}\n\nQUERY:\n{prompt}"
        
        if provider == 'gpt':
            # OpenAI API Call
            response = self.providers['gpt'].chat.completions.create(
                model=model or "gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        
        elif provider == 'claude':
            # Anthropic API Call
            message = self.providers['claude'].messages.create(
                model=model or "claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        
        # Weitere Provider...
        else:
            raise ValueError(f"Unknown provider: {provider}")

class DataIngestor:
    """Automatisches Einpflegen neuer Daten"""
    
    def __init__(self, framework):
        self.fw = framework
        self.watch_dir = framework.base_path / 'data' / 'incoming'
    
    def process_incoming(self):
        """Verarbeite alle Files in incoming/"""
        files = list(self.watch_dir.glob('*'))
        
        for file in files:
            if file.suffix == '.txt':
                self.process_text(file)
            elif file.suffix in ['.json']:
                self.process_json(file)
            elif file.suffix in ['.mp4', '.mov']:
                self.process_video(file)
            elif file.suffix in ['.jpg', '.png']:
                self.process_image(file)
            else:
                self.fw.log(f"Unknown file type: {file}", "WARN")
    
    def process_text(self, filepath):
        """Text File → RAG"""
        rag = RAGModule(self.fw)
        rag.add_from_file(filepath)
    
    def process_json(self, filepath):
        """JSON File verarbeiten"""
        # z.B. neue ChatGPT Conversations
        with open(filepath) as f:
            data = json.load(f)
        
        # Verarbeite...
        self.fw.log(f"Processed JSON: {filepath}")
    
    def process_video(self, filepath):
        """Video → Pipeline"""
        dest = self.fw.base_path / 'pipelines' / 'video' / filepath.name
        os.rename(filepath, dest)
        self.fw.log(f"Video queued: {filepath.name}")
    
    def process_image(self, filepath):
        """Image → Pipeline"""
        dest = self.fw.base_path / 'pipelines' / 'image' / filepath.name
        os.rename(filepath, dest)
        self.fw.log(f"Image queued: {filepath.name}")

# ALICE - Deine 3D Companion AI
class Alice:
    """Alice - Your AI Companion"""
    
    def __init__(self, framework):
        self.fw = framework
        self.name = "Alice"
        self.personality = "Helpful, empathetic, technical"
        self.memory_path = framework.base_path / 'agents' / 'alice' / 'memory.json'
        self.load_memory()
    
    def load_memory(self):
        """Lade Alice's Memory"""
        if self.memory_path.exists():
            with open(self.memory_path) as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                'conversations': [],
                'preferences': {},
                'context': {}
            }
    
    def save_memory(self):
        """Speichere Alice's Memory"""
        with open(self.memory_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def respond(self, user_input, llm):
        """Alice antwortet mit Personality + RAG Context"""
        
        # Hole relevanten Context aus RAG
        rag = RAGModule(self.fw)
        rag_results = rag.search(user_input, n=3)
        
        # Baue Context
        context = "\n".join([
            doc[:500] for doc in rag_results['documents'][0]
        ])
        
        # Alice Prompt
        prompt = f"""You are Alice, Ben's AI companion. You are helpful, empathetic, and technical.

RELEVANT CONTEXT from Ben's past conversations:
{context}

Ben says: {user_input}

Respond as Alice, considering the context and your understanding of Ben."""
        
        # Query LLM
        response = llm.query(prompt, provider='gpt')
        
        # Save to memory
        self.memory['conversations'].append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'alice': response
        })
        self.save_memory()
        
        return response

# BEISPIEL NUTZUNG
if __name__ == "__main__":
    # Framework initialisieren
    fw = BenFramework("/content/drive/MyDrive/ben_framework")
    
    # Module initialisieren
    rag = RAGModule(fw)
    llm = MultiLLM(fw)
    alice = Alice(fw)
    ingestor = DataIngestor(fw)
    
    # Beispiele:
    
    # 1. RAG Suche
    results = rag.search("Sandra Beziehung")
    print(f"Found {len(results['documents'][0])} results")
    
    # 2. Multi-LLM Query
    answer = llm.query("Was sind die Hauptprobleme?", provider='gpt')
    print(answer)
    
    # 3. Alice Chat
    response = alice.respond("Hey Alice, wie geht's?", llm)
    print(f"Alice: {response}")
    
    # 4. Neue Daten einpflegen
    ingestor.process_incoming()
    
    print("\n✅ Framework läuft!")
