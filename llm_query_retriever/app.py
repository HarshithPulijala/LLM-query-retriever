import streamlit as st
import os
from dotenv import load_dotenv
from src import extract_text, embedding_store, query_answer
from src import query_parser, decision_logic

load_dotenv()

st.set_page_config(page_title="LLM-Powered Intelligent Query–Retrieval System")
st.title("LLM-Powered Intelligent Query–Retrieval System")

os.makedirs("docs", exist_ok=True)

# Initialize session state for embedding store and chat history
if 'embed_store' not in st.session_state:
    st.session_state.embed_store = embedding_store.EmbeddingStore()
if 'doc_loaded' not in st.session_state:
    st.session_state.doc_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_path = os.path.join("docs", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded {uploaded_file.name}")
    with st.spinner("Extracting text..."):
        text = extract_text.extract_text(file_path)
    if not text or text.startswith("[Error"):
        st.error(f"Failed to extract text: {text}")
        st.session_state.doc_loaded = False
    elif len(text) < 100:
        st.warning("Document is too short for meaningful retrieval.")
        st.session_state.doc_loaded = False
    else:
        # Generate document summary and bullet points using LLM immediately after upload
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.5-pro')
            summary_prompt = f"""
You are an expert assistant. Read the following document and:
1. Give a brief summary (2-3 sentences).
2. List five important topics or sections as bullet points.

Document:
{text[:6000]}

Respond in this format:
Summary: <summary here>
Bullet Points:
- <point 1>
- <point 2>
- <point 3>
- <point 4>
- <point 5>
"""
            try:
                response = model.generate_content(summary_prompt)
                st.write(f"Raw LLM Summary Response: {response.text}")  # Debug output
                lines = response.text.strip().split('\n')
                summary = ''
                bullets = []
                for line in lines:
                    if line.lower().startswith('summary:'):
                        summary = line[len('summary:'):].strip()
                    elif line.strip().startswith('-'):
                        bullets.append(line.strip())
                if summary:
                    st.info(f"**Document Summary:** {summary}")
                if bullets:
                    st.markdown("**Important Topics:**")
                    for bullet in bullets[:5]:
                        st.markdown(bullet)
            except Exception as e:
                st.warning(f"Could not generate summary: {e}")
        with st.spinner("Indexing document..."):
            st.session_state.embed_store.clear()
            st.session_state.embed_store.add_document(text)
        st.session_state.doc_loaded = True
        st.success("Document processed and indexed!")
        st.session_state.chat_history = []

st.markdown("---")
question = st.text_input("Ask a question about your document:")
mode = st.radio("Choose mode:", ["Decision (Claim/Approval)", "Explanation (General Question)"])

if st.button("Get Answer") and question:
    if not st.session_state.doc_loaded:
        st.warning("Please upload and process a valid document first.")
    else:
        with st.spinner("Retrieving relevant clauses..."):
            retrieved = st.session_state.embed_store.search(question, top_k=5)
        if mode == "Decision (Claim/Approval)":
            with st.spinner("Parsing query and evaluating decision..."):
                parsed_query = query_parser.parse_query(question)
                decision_json = decision_logic.evaluate_decision(parsed_query, retrieved)
            st.session_state.chat_history.append({"question": question, "decision_json": decision_json})
            st.subheader("Decision (Structured JSON):")
            st.json(decision_json)
            st.subheader("Explanation:")
            st.write(f"Decision: {decision_json['decision']}")
            st.write(f"Amount: {decision_json['amount']}")
            st.write(f"Justification: {decision_json['justification']}")
            st.markdown("**Referenced Clauses:**")
            for clause in decision_json['referenced_clauses']:
                st.markdown(f"- {clause}")
        else:
            with st.spinner("Generating explanation with LLM..."):
                answer, referenced, confidence = query_answer.get_answer(question, retrieved, st.session_state.chat_history)
            st.session_state.chat_history.append({"question": question, "answer": answer})
            st.subheader("Answer:")
            st.write(answer)
            if confidence:
                st.caption(f"Confidence/Rating: {confidence}")
            st.markdown("**Referenced Clauses:**")
            for i, clause in enumerate(referenced):
                st.markdown(f"**Clause {i+1}:**\n> {clause[:300]}{'...' if len(clause) > 300 else ''}")
    st.markdown("---")
    st.markdown("**Chat History (Questions Only):**")
    for entry in st.session_state.chat_history:
        st.markdown(f"- {entry['question']}") 