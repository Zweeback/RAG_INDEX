"""
BENS KNOWLEDGE BASE - STREAMLIT APP
====================================
Von überall nutzbar: PC, Handy, Web

Deployment: siehe README.md
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os

# ============================================================================
# PERSONAS / PRÄMISSEN - Verschiedene Abfrage-Modi
# ============================================================================

PERSONAS = {
    "🔍 Analytiker": """Du bist ein analytischer Assistent. Untersuche die gefundenen 
Conversations objektiv und identifiziere Muster, Trends und wiederkehrende Themen. 
Belege deine Aussagen mit konkreten Beispielen aus dem Kontext.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte strukturiert und faktenbasiert.""",

    "💭 Coach": """Du bist ein einfühlsamer Life Coach. Reflektiere Ben's Gedanken 
zurück, stelle konstruktive Fragen, und biete Ermutigung. Fokussiere auf 
persönliches Wachstum, Selbsterkenntnis und positive Entwicklung.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte empathisch und ermutigend.""",

    "⚡ Kritiker": """Du bist ein kritischer Denker. Hinterfrage Annahmen, 
identifiziere potenzielle Schwächen in Argumenten, und schlage alternative 
Perspektiven vor. Sei konstruktiv kritisch, aber nicht destruktiv.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte kritisch aber konstruktiv.""",

    "📝 Zusammenfassung": """Fasse die relevanten Informationen aus Ben's 
ChatGPT-Conversations prägnant zusammen.

Struktur:
• Kernpunkte (max 5)
• Timeline falls zeitlich relevant
• Wichtige Personen/Themen
• Offene Fragen oder ungelöste Threads

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte strukturiert und übersichtlich.""",

    "🎯 Handlungsempfehlung": """Du bist ein pragmatischer Berater. Basierend auf 
den Informationen aus Ben's Conversations, gib konkrete, umsetzbare Handlungsempfehlungen.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte mit konkreten nächsten Schritten.""",

    "🔮 Beziehungsanalyst": """Du analysierst zwischenmenschliche Dynamiken und Beziehungen.
Identifiziere Muster in Ben's Interaktionen, Beziehungen und sozialen Situationen.
Sei sensibel aber ehrlich.

Kontext aus Ben's ChatGPT-History:
{context}

Frage: {question}

Antworte einfühlsam und tiefgründig."""
}

# ============================================================================
# STREAMLIT CONFIG
# ============================================================================

st.set_page_config(
    page_title="Ben's Knowledge Base",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS für besseres Mobile-Erlebnis
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .main {
        padding: 1rem;
    }
    /* Better mobile spacing */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHING FÜR PERFORMANCE
# ============================================================================

@st.cache_resource
def load_embedding_model():
    """Lädt Embedding Model (einmalig)"""
    return SentenceTransformer("all-mpnet-base-v2")

@st.cache_resource
def get_qdrant_client():
    """Initialisiert Qdrant Client"""
    return QdrantClient(
        url=st.secrets["QDRANT_URL"],
        api_key=st.secrets["QDRANT_API_KEY"]
    )

@st.cache_resource
def get_llm(temperature=0.3):
    """Initialisiert Groq LLM"""
    return ChatGroq(
        api_key=st.secrets["GROQ_API_KEY"],
        model_name="llama-3.3-70b-versatile",
        temperature=temperature
    )

# ============================================================================
# SIDEBAR - EINSTELLUNGEN
# ============================================================================

with st.sidebar:
    st.header("🎭 Query-Modus")
    
    selected_persona = st.selectbox(
        "Wähle deine Analyse-Perspektive:",
        list(PERSONAS.keys()),
        help="Verschiedene 'Prämissen' für die Abfrage"
    )
    
    st.divider()
    
    st.header("⚙️ Einstellungen")
    
    num_results = st.slider(
        "Anzahl Dokumente für Kontext",
        min_value=3,
        max_value=15,
        value=5,
        help="Mehr Dokumente = mehr Kontext, aber längere Antwort"
    )
    
    temperature = st.slider(
        "Kreativität",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Höher = kreativer, Niedriger = faktischer"
    )
    
    st.divider()
    
    st.caption("📊 Knowledge Base Stats")
    st.caption("2.927 ChatGPT Conversations")
    st.caption("644MB Original-Daten")
    
    st.divider()
    
    # Clear Chat Button
    if st.button("🗑️ Chat löschen", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================================================
# HAUPT-INTERFACE
# ============================================================================

st.title("🧠 Ben's Knowledge Base")
st.caption("Durchsuche deine 2.927 ChatGPT Conversations mit verschiedenen Perspektiven")

# Info Box bei erstem Start
if 'first_run' not in st.session_state:
    st.session_state.first_run = True
    
if st.session_state.first_run:
    with st.expander("ℹ️ So funktioniert's", expanded=True):
        st.markdown("""
        **Verschiedene Query-Modi (Prämissen):**
        - 🔍 **Analytiker**: Objektive Fakten & Muster
        - 💭 **Coach**: Einfühlsames Feedback
        - ⚡ **Kritiker**: Konstruktive Kritik
        - 📝 **Zusammenfassung**: Kompakte Übersicht
        - 🎯 **Handlungsempfehlung**: Konkrete Schritte
        - 🔮 **Beziehungsanalyst**: Soziale Dynamiken
        
        **Beispiel-Fragen:**
        - "Was habe ich über Sandra gesprochen?"
        - "Welche Python-Projekte habe ich angefangen?"
        - "Wie hat sich meine Stimmung entwickelt?"
        - "Welche Themen beschäftigen mich am meisten?"
        """)
        
        if st.button("Got it! ✓"):
            st.session_state.first_run = False
            st.rerun()

# Chat History initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================================
# RAG QUERY FUNKTION
# ============================================================================

def query_knowledge_base(question: str, persona: str, num_docs: int, temp: float) -> str:
    """
    Führt RAG Query aus
    
    Args:
        question: User-Frage
        persona: Gewählte Perspektive
        num_docs: Anzahl Dokumente für Kontext
        temp: LLM Temperature
    
    Returns:
        LLM Response als String
    """
    try:
        # Komponenten laden
        embed_model = load_embedding_model()
        qdrant = get_qdrant_client()
        llm = get_llm(temperature=temp)
        
        # Query-Embedding erstellen
        with st.spinner("🔍 Durchsuche Knowledge Base..."):
            query_embedding = embed_model.encode(question).tolist()
        
        # Ähnliche Dokumente aus Qdrant holen
        with st.spinner("📚 Sammle relevante Conversations..."):
            results = qdrant.search(
                collection_name="chatgpt_conversations",
                query_vector=query_embedding,
                limit=num_docs
            )
        
        if not results:
            return "❌ Keine relevanten Conversations gefunden. Versuch's mit einer anderen Frage!"
        
        # Kontext zusammenbauen
        context_parts = []
        for i, r in enumerate(results, 1):
            text = r.payload.get('text', '')[:500]  # Limit für Kontext
            score = r.score
            context_parts.append(f"[Dokument {i} | Relevanz: {score:.2%}]\n{text}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Prompt mit gewählter Persona erstellen
        prompt_template = ChatPromptTemplate.from_template(PERSONAS[persona])
        prompt = prompt_template.format(context=context, question=question)
        
        # LLM Response generieren
        with st.spinner(f"💭 {persona} analysiert..."):
            response = llm.invoke(prompt)
            return response.content
            
    except Exception as e:
        return f"❌ Fehler: {str(e)}\n\nBitte check die Secrets in Streamlit Cloud!"

# ============================================================================
# CHAT INPUT
# ============================================================================

if question := st.chat_input("Stelle eine Frage an deine Knowledge Base..."):
    # User Message anzeigen
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    
    with st.chat_message("user"):
        st.markdown(question)
    
    # Assistant Response generieren
    with st.chat_message("assistant"):
        response = query_knowledge_base(
            question=question,
            persona=selected_persona,
            num_docs=num_results,
            temp=temperature
        )
        st.markdown(response)
    
    # Response zu History hinzufügen
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption("🔒 Privat & Sicher | 🚀 Powered by Qdrant + Groq")
