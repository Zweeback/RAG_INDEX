#!/usr/bin/env python3
"""
ChatGPT RAG API Server
Läuft auf deinem MSI PC oder Google Cloud Run
ChatGPT kann dann über Actions dein RAG abfragen!
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
import os

app = Flask(__name__)
CORS(app)

# ChromaDB laden (von Google Drive gemountet)
CHROMA_PATH = "./chroma_db"  # Passe an!
client = None
collection = None

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def init_rag():
    global client, collection
    if client is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        embedder = SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
        collection = client.get_collection("chatgpt_conversations", embedding_function=embedder)
    return collection

@app.route('/search', methods=['POST'])
def search():
    """RAG Suche Endpoint für ChatGPT"""
    try:
        data = request.json
        query = data.get('query', '')
        n_results = data.get('n_results', 5)
        
        coll = init_rag()
        results = coll.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Formatiere für ChatGPT
        formatted = []
        for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            formatted.append({
                'title': meta.get('title', meta.get('source_file', 'Unknown')),
                'relevance': f"{(1-dist)*100:.1f}%",
                'messages': meta.get('message_count', 1),
                'content': doc[:2000]  # Erste 2000 Zeichen
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': formatted,
            'total_found': len(formatted)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """RAG Statistiken"""
    try:
        coll = init_rag()
        return jsonify({
            'total_chatgpt_conversations': coll.count(),
            'status': 'online'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_conversation():
    """Neue Conversation hinzufügen"""
    try:
        data = request.json
        title = data.get('title', 'Untitled')
        content = data.get('content', '')
        
        coll = init_rag()
        conv_id = f"manual_{coll.count() + 1}"
        
        coll.add(
            documents=[content],
            metadatas=[{
                'title': title,
                'message_count': 1,
                'conv_index': coll.count(),
                'source': 'manual'
            }],
            ids=[conv_id]
        )
        
        return jsonify({
            'success': True,
            'message': f'Added conversation: {title}',
            'id': conv_id
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Für lokalen Test
    print("🚀 Starting RAG API Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    # Für Production (MSI PC oder Cloud):
    # gunicorn -w 4 -b 0.0.0.0:5000 chatgpt_rag_server:app
