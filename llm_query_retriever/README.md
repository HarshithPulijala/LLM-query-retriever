# LLM-Powered Intelligent Query–Retrieval System

## 🧠 Objective
Build a system that uses a Large Language Model (LLM) like Google Gemini Pro to answer user questions based on the contents of long unstructured documents such as policy documents, legal contracts, or emails.

## ⚙️ Tech Stack
- **Backend:** Python
- **LLM:** Gemini 2.5 Pro via Google Generative AI SDK
- **Document Parsing:** PyMuPDF or unstructured
- **Embeddings + Vector DB:** SentenceTransformers + FAISS
- **Retrieval Pipeline:** RAG (Retrieval-Augmented Generation)
- **Frontend:** Streamlit Web App
- **Deployment:** Streamlit Cloud or Hugging Face Spaces

## 📦 Folder Structure
```
llm_query_retriever/
├── app.py                      # Streamlit app
├── docs/                       # Uploaded documents
├── src/
│   ├── extract_text.py         # Parses PDF/DOCX/TXT
│   ├── embedding_store.py      # Vector DB setup (FAISS)
│   ├── query_answer.py         # LLM-based answer generation
│   ├── query_parser.py         # Query entity extraction
│   └── decision_logic.py       # LLM-based decision logic
├── requirements.txt
└── README.md
```

## 🧩 Features
- Upload PDF, DOCX, or TXT files
- **Immediate LLM-powered summary and five key topics** after upload
- Extract and chunk document text
- Store and search embeddings in a vector DB
- RAG pipeline with Gemini Pro for answers
- **Decision (claim/approval) and Explanation (general question) modes**
- Display source snippets and confidence scores
- **Chat history of previous questions only**
- Debug output for LLM summary response (for troubleshooting)
- Error handling for long/empty files and LLM quota issues

## 🚀 Setup Instructions
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your Google Generative AI API key in a `.env` file:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## 📝 Add-ons
- Chat history context
- Option to reprocess new documents
- Error handling for long/empty files
- **Debug: Shows raw LLM summary response after upload for troubleshooting**

## 🧪 Evaluation
- Display confidence score or source snippets
- Show retrieved chunks alongside the answer
- **If summary is not shown:**
  - Check for LLM quota or API key issues
  - See the raw LLM summary response for debugging
  - Try with a different document or check error messages in the UI

## 🧠 Usage Flow
1. **Upload a document** (PDF, DOCX, or TXT)
2. **See immediate summary and five key topics** (LLM-generated)
3. **Ask a question** about the document
4. **Choose mode:**
   - Decision (claim/approval): get structured JSON with decision, amount, justification, and referenced clauses
   - Explanation (general question): get a detailed, document-grounded answer with referenced clauses
5. **Review chat history of previous questions**

## 🛠️ Troubleshooting
- If you see `[Error from Gemini Pro: ...]`, check your API key, quota, or billing status.
- If summary is missing, check the debug output for the raw LLM response.
- For further help, see the Google Gemini API documentation or contact the maintainer. 