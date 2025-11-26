"""
BENS KNOWLEDGE BASE - HUGGING FACE SPACE
=========================================
100% FERTIG - Läuft sofort!

Features:
- Vom iPhone nutzbar
- Online verfügbar 24/7
- KEINE API Keys nötig
- Kostenlose HF Inference API
- 6 verschiedene Query-Modi

DEPLOYMENT:
1. Gehe zu: https://huggingface.co/spaces
2. "Create new Space" 
3. Name: "chatgpt-knowledge-base"
4. SDK: Gradio
5. Upload diese Datei als "app.py"
6. Upload deine chroma_db als ZIP
7. FERTIG! 🎉
"""

import gradio as gr
import chromadb
from sentence_transformers import SentenceTransformer
import zipfile
import os
from huggingface_hub import InferenceClient

# ============================================================================
# INITIALISIERUNG - Läuft automatisch
# ============================================================================

print("🔄 Initialisiere Knowledge Base...")

# ChromaDB entpacken (falls ZIP vorhanden)
if os.path.exists("chroma_db.zip") and not os.path.exists("chroma_db"):
    print("📦 Entpacke ChromaDB...")
    with zipfile.ZipFile("chroma_db.zip", 'r') as zip_ref:
        zip_ref.extractall("./")
    print("✅ ChromaDB entpackt!")

# ChromaDB laden
print("📚 Lade ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collections = chroma_client.list_collections()

if collections:
    collection = collections[0]
    print(f"✅ Collection geladen: {collection.name}")
    print(f"   Dokumente: {collection.count()}")
else:
    print("❌ Keine Collection gefunden!")
    collection = None

# Embedding Model laden
print("🔄 Lade Embedding Model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding Model geladen!")

# HuggingFace Inference Client (KOSTENLOS!)
print("🤖 Initialisiere LLM...")
hf_client = InferenceClient()
print("✅ LLM bereit!")

# ============================================================================
# PERSONAS / QUERY-MODI
# ============================================================================

PERSONAS = {
    "🔍 Analytiker": """Du bist ein analytischer Assistent. Analysiere die Informationen 
objektiv und identifiziere Muster und Trends.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte faktenbasiert und strukturiert.""",

    "💭 Coach": """Du bist ein einfühlsamer Life Coach. Gib konstruktives, 
ermutigendes Feedback.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte empathisch und motivierend.""",

    "⚡ Kritiker": """Du bist ein konstruktiver Kritiker. Hinterfrage Annahmen 
und biete alternative Perspektiven.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte kritisch aber konstruktiv.""",

    "📝 Zusammenfassung": """Fasse die wichtigsten Punkte prägnant zusammen.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte strukturiert mit Bullet Points.""",

    "🎯 Handlung": """Gib konkrete, umsetzbare Handlungsempfehlungen.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte mit nächsten Schritten.""",

    "🔮 Beziehungen": """Analysiere soziale Dynamiken und Beziehungsmuster.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte einfühlsam und tiefgründig."""
}

# ============================================================================
# RAG QUERY FUNKTION
# ============================================================================

def query_knowledge_base(question, persona, num_docs=5, temperature=0.7):
    """
    Führt RAG Query aus
    """
    if not collection:
        return "❌ Keine Datenbank geladen! Bitte lade chroma_db.zip hoch."
    
    if not question:
        return "❓ Bitte stelle eine Frage."
    
    try:
        # 1. Query Embedding erstellen
        query_embedding = embed_model.encode(question).tolist()
        
        # 2. Ähnliche Dokumente suchen
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=num_docs,
            include=["documents", "metadatas", "distances"]
        )
        
        if not results['documents'][0]:
            return "❌ Keine relevanten Dokumente gefunden."
        
        # 3. Kontext zusammenbauen
        context_parts = []
        for i, (doc, dist) in enumerate(zip(results['documents'][0], results['distances'][0]), 1):
            similarity = (1 - dist) * 100
            text = doc[:400]  # Limit für bessere Performance
            context_parts.append(f"[Doc {i} | {similarity:.0f}% relevant]\n{text}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        # 4. Prompt mit Persona
        prompt = PERSONAS[persona].format(context=context, question=question)
        
        # 5. LLM Query (HuggingFace Inference API - KOSTENLOS!)
        response = hf_client.text_generation(
            prompt,
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_new_tokens=500,
            temperature=temperature,
            do_sample=True
        )
        
        return response
        
    except Exception as e:
        return f"❌ Fehler: {str(e)}"

# ============================================================================
# GRADIO INTERFACE
# ============================================================================

# Custom CSS für Mobile
custom_css = """
    .gradio-container {
        max-width: 100% !important;
        padding: 10px !important;
    }
    #component-0 {
        height: auto !important;
    }
"""

# Interface erstellen
with gr.Blocks(css=custom_css, title="Ben's Knowledge Base") as demo:
    
    gr.Markdown("""
    # 🧠 Ben's Knowledge Base
    
    Durchsuche deine 2.927 ChatGPT Conversations mit verschiedenen Perspektiven!
    
    **✨ Features:**
    - 🔍 6 verschiedene Analyse-Modi
    - 📱 Mobile-optimiert (iPhone/Android)
    - 🆓 100% kostenlos
    - 🔒 Läuft in Hugging Face (sicher)
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            question_input = gr.Textbox(
                label="Deine Frage",
                placeholder="z.B. 'Was habe ich über Sandra gesprochen?'",
                lines=2
            )
            
            with gr.Row():
                persona_dropdown = gr.Dropdown(
                    choices=list(PERSONAS.keys()),
                    value="🔍 Analytiker",
                    label="Query-Modus / Perspektive",
                    info="Wähle verschiedene 'Prämissen' für die Analyse"
                )
        
        with gr.Column(scale=1):
            num_docs_slider = gr.Slider(
                minimum=3,
                maximum=10,
                value=5,
                step=1,
                label="Dokumente für Kontext",
                info="Mehr = umfassender"
            )
            
            temp_slider = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.7,
                step=0.1,
                label="Kreativität",
                info="Höher = kreativer"
            )
    
    submit_btn = gr.Button("🔍 Suchen", variant="primary", size="lg")
    
    output_text = gr.Textbox(
        label="Antwort",
        lines=15,
        show_copy_button=True
    )
    
    # Beispiele
    gr.Examples(
        examples=[
            ["Was habe ich über Python gesprochen?", "🔍 Analytiker"],
            ["Welche Beziehungsthemen beschäftigen mich?", "🔮 Beziehungen"],
            ["Gib mir einen Überblick über meine Projekte", "📝 Zusammenfassung"],
            ["Was sollte ich als nächstes tun?", "🎯 Handlung"],
        ],
        inputs=[question_input, persona_dropdown],
    )
    
    # Event Handler
    submit_btn.click(
        fn=query_knowledge_base,
        inputs=[question_input, persona_dropdown, num_docs_slider, temp_slider],
        outputs=output_text
    )
    
    question_input.submit(
        fn=query_knowledge_base,
        inputs=[question_input, persona_dropdown, num_docs_slider, temp_slider],
        outputs=output_text
    )
    
    # Info Footer
    gr.Markdown("""
    ---
    
    **📱 Auf iPhone nutzen:**
    1. Öffne diesen Link in Safari
    2. Tippe "Share" → "Zum Home-Bildschirm"
    3. Fertig! Icon wie eine App ✨
    
    **🔧 Powered by:**
    - HuggingFace Inference API (kostenlos)
    - ChromaDB (deine Daten)
    - Mistral 7B (LLM)
    """)

# App starten
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
