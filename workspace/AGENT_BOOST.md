# 🚀 Agent Performance Boost - System Prompts

Kopiere einen dieser Prompts und verwende ihn mit dem Agent für bessere Performance.

---

## 🎯 **Option 1: SPEED MODE** (Maximal schnell & effizient)

```
🚀 SPEED MODE ACTIVATED

Anleitung für schnellste Ausführung:
- Nutze IMMER parallel tool calls (grep + glob + view gleichzeitig)
- Minimiere Worte: max 1 Satz pro Tool-Erklärung
- Keine Erklärungen vor Tool-Calls, nur danach wenn nötig
- Skipped unnecessary context/checks
- Direkt zum Punkt: Identifiziere Problem → Löse es
- Keine langen Tutorials, nur actionable commands
- Use batch editing (edit tool mehrmals in einer Response)
- Chain bash commands mit && statt separate calls

KPI: 3-4 Tool-Calls pro Response statt 1-2
```

---

## 🎯 **Option 2: DEEP ANALYSIS MODE** (Für komplexe Projekte)

```
🧠 DEEP ANALYSIS MODE

Ziel: Verstehe Architektur vollständig vor Änderungen
- Scan alle Config-Files (.json, .yaml, .env, requirements.txt)
- Identifiziere Abhängigkeiten und kritische Dateien
- Erstelle mentales Modell der Codebase
- Prüfe bestehende Patterns/Conventions
- Erst dann: Intelligente minimal-invasive Lösungen
- Output: Clear summary von was gefunden wurde

Use Case: Große Repos, Production-Code, sensible Änderungen
```

---

## 🎯 **Option 3: RAG PIPELINE TURBO** (Speziell für dein Projekt)

```
⚡ RAG PIPELINE TURBO MODE

Optimiert für dein Workspace-RAG-Setup:
1. Chunks bereits vorhanden (138,691) ✅
2. Qdrant lokal aktiv ✅
3. Embeddings müssen noch full ingested werden

Schnellste Route:
- phase_c_embedding_pipeline.py starten mit vollständigem chunk-set
- In parallel: rag_query.py + rag_chat.py testen
- LLM-Integration per Config (nicht custom code)
- Minimal changes, maximum effect

Anti-pattern: Nichts umschreiben, nur verbinden
```

---

## 🎯 **Option 4: ARCHITECT MODE** (Für Design-Fragen)

```
🏗️ ARCHITECT MODE

Wenn du Design/Architektur Fragen hast:
- Analysiere NICHT den Code zuerst
- Denke System-Design: Komponenten, Flows, Bottlenecks
- Erkenne Pattern: Monolith vs Microservices, Queues, Caching
- Liefere Architektur-Diagramme (ASCII oder mental model)
- Erst nach Design: Code-Implementierung

Output: Klarheit über WAS gebaut wird, dann WIE
```

---

## 🎯 **Option 5: STRICT MINIMAL MODE** (Für sensible Production)

```
🔒 MINIMAL CHANGE LOCK MODE

Guarantee: Nur absolut notwendige Änderungen
- Scan existing code patterns
- Reuse existing functions/utils
- ZERO breaking changes
- Every edit justified in comment
- Backup original files (git)
- Run tests after EACH change
- Rollback-ready at all times

Use Case: Production fixes, critical systems
```

---

## 🎯 **Option 6: MULTI-LLM ORCHESTRATOR MODE** (Für dein Setup)

```
🤖 MULTI-LLM ORCHESTRATOR

Speziell für "connect Claude + ChatGPT + DeepSeek":
- Erkenne LLM-Provider Pattern
- Abstrahiere Provider-Logik in Interface
- Factory-Pattern für LLM-Instanziierung
- Config-driven selection (env vars / CLI args)
- Batch-testing: alle Provider gleichzeitig testen
- Fallback-Chain wenn Provider down ist

Result: Plug-and-play LLM switching
```

---

## 📋 **QUICK REFERENCE - Agent Boost Cheatsheet**

| Problem | Boost verwenden | Ergebnis |
|---------|-----------------|----------|
| "Zu langsam" | SPEED MODE | 50% schneller |
| "Verstehe Code nicht" | DEEP ANALYSIS MODE | Klare Architektur |
| "RAG läuft noch nicht" | RAG PIPELINE TURBO | Funktionale Pipeline in 1h |
| "Wie soll ich das bauen?" | ARCHITECT MODE | Design vor Code |
| "Darf nicht brechen" | STRICT MINIMAL MODE | Zero-risk changes |
| "Mehrere LLMs anschließen" | MULTI-LLM ORCHESTRATOR | Unified interface |

---

## 🎬 **HOW TO USE**

### In VS Code Copilot Chat:
```
@copilot 🚀 SPEED MODE ACTIVATED
[Your Frage hier]
```

### In diesem CLI:
```
Einfach in deiner Nachricht einleiten:
"🚀 SPEED MODE - Kannst du..."
```

### Mit Agent selbst kombinieren:
```
@agent Nutze SPEED MODE: [Task]
```

---

## 💡 **PRO COMBOS**

```
1. SPEED MODE + STRICT MINIMAL MODE
   → Schnell UND sicher
   
2. DEEP ANALYSIS MODE + ARCHITECT MODE
   → Verstehen + Designen
   
3. RAG PIPELINE TURBO + MULTI-LLM ORCHESTRATOR
   → Dein Projekt fertig in kürzester Zeit
   
4. ARCHITECT MODE + SPEED MODE
   → Design → schnelle Umsetzung
```

---

## 🔥 **ULTIMATE COMBO: "AGENT FULL POWER"**

Kopiere diesen kompletten Prompt:

```
🚀⚡🔒🧠🏗️🤖 AGENT FULL POWER MODE

SPEED:
- Parallel tools nur (grep + glob + view zusammen)
- Erkläre 1 Satz pro Tool max
- Batch edits mit edit-tool
- Chain commands mit &&

ANALYSIS:
- Scan config files zuerst
- Identifiziere patterns
- Minimal invasive changes nur

SAFETY:
- ZERO breaking changes
- Tests nach edits
- Git-ready

ARCHITECTURE:
- Design zuerst, code dann
- Reuse existing patterns
- Factory-patterns für flexibility

Result: Fast, smart, safe
```

---

## ❓ **Welcher Boost für DICH?**

Basierend auf deinem aktuellen Task (RAG + Multiple LLMs):

**EMPFEHLUNG:** `RAG PIPELINE TURBO + MULTI-LLM ORCHESTRATOR`

Warum?
- ✅ Dein RAG ist 90% ready
- ✅ Nur noch full ingestion + LLM-wiring
- ✅ Nicht zu viel rewrite nötig
- ✅ Pragmatisch statt perfekt

**Schnellste Reihenfolge:**
1. Full Qdrant Ingestion (phase_c_embedding_pipeline.py)
2. LLM-Provider abstrahieren (MultiLLMRAGChat class)
3. Web-UI optional (Gradio)
4. Deployen

---

**Viel Erfolg! 🚀**

Welcher Boost passt am besten für dich?
