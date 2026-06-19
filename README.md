# 🌟 SupportSphere AI

An intelligent, persona-aware AI customer support system powered by **RAG (Retrieval-Augmented Generation)**, **Gemini LLM**, **ChromaDB vector search**, and **Streamlit UI**, designed to simulate real-world enterprise support automation.

---

##  Key Features

### Persona-Aware Intelligence
Automatically detects user intent and adapts responses for:
- Technical Experts (detailed debugging & logs)
- Frustrated Users (empathetic support)
- Business Executives (concise impact-focused answers)

---

### RAG-Based Knowledge Engine
- Uses **ChromaDB vector database**
- Embeds documents using **Sentence Transformers**
- Retrieves most relevant context before generating answers

---

### 🤖 LLM Integration (Gemini AI)
- Generates human-like responses using Google Gemini
- Context-aware prompt engineering
- Safe fallback handling when API limits are reached

---

### ⚠️ Smart Escalation System
Automatically escalates cases when:
- Sensitive keywords are detected
- Low retrieval confidence
- No relevant knowledge found

---

### Conversation Memory
Maintains session-based chat history for contextual continuity.

---

### Analytics & Feedback
- Stores user interactions in SQLite database
- Tracks escalation patterns
- Supports feedback logging

---

## System Architecture
```
User Query
↓
Persona Detector
↓
RAG Pipeline (ChromaDB)
↓
Escalation Manager
↓
Gemini LLM (Response Generator)
↓
Streamlit UI Output
```
---
## 📁 Project Structure
```
Adsparkx-AI-Agent/
│
├── app.py
├── build_kb.py
├── requirements.txt
├── data/
├── chroma_db/
├── database/
│
├── src/
│ ├── rag_pipeline.py
│ ├── response_generator.py
│ ├── persona_detector.py
│ ├── escalation_manager.py
│ ├── database.py
│ ├── analytics.py
│ ├── feedback_manager.py
│ ├── conversation_memory.py
│ ├── config.py
│ ├── handoff_generator.py
│ ├── sentiment_analyzer.py
│ ├── utils.py
│
├── ui/
└── test_*.py
```

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/RohitKr-codes/SupportSphere-AI.git
cd SupportSphere-AI
```
2. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate   # Windows
```
3. Install Dependencies
```
pip install -r requirements.txt
```
---
# Build Knowledge Base
```
python build_kb.py
```
### Expected output:
```
Indexed XX chunks
```
---
## Run Application
```
streamlit run app.py
```

## Environment Variables

Create .env file:
```
GEMINI_API_KEY=your_api_key_here
```
---

## Tech Stack
* Python
* Streamlit
* Google Gemini API
* ChromaDB
* Sentence Transformers
* SQLite
* LangChain (light usage)
---
## ⚠️ Fallback Handling
If Gemini API quota is exceeded:
* System automatically uses RAG-based fallback responses
* Ensures zero downtime experience
---
## Real-World Use Cases
* Customer Support Automation
* IT Helpdesk Systems
* SaaS Support Bots
* Enterprise Ticket Resolution Systems
---
## Author
* Rohit Kumar Rai
---
### License
* This project is part of an AI Engineering assignment and is intended for educational & demonstration purposes.
