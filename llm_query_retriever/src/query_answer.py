import os
import google.generativeai as genai
from typing import List, Tuple

def get_answer(query: str, retrieved_chunks: List[Tuple[str, float]], chat_history=None):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "[Google API key not set]", [], None
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-pro')
    context = "\n\n".join([f"Clause: {chunk}" for chunk, _ in retrieved_chunks])
    prompt = f"""
You are an expert assistant. Given the following user question and the most relevant policy clauses, provide a clear, concise explanation based only on the document. Reference the specific clauses used.

User Question: {query}

Relevant Clauses:
{context}

Respond with a detailed answer and reference the clauses.
"""
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        # Reference the actual retrieved chunks for transparency
        referenced = [chunk for chunk, _ in retrieved_chunks]
        confidence = getattr(response, 'safety_ratings', None)
        return answer, referenced, confidence
    except Exception as e:
        return f"[Error from Gemini Pro: {e}]", [], None 