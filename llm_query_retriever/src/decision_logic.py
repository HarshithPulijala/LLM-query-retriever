import os
import google.generativeai as genai
from typing import List, Tuple, Dict
import re

def evaluate_decision(parsed_query: Dict, retrieved_clauses: List[Tuple[str, float]]) -> Dict:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "decision": "error",
            "amount": 0,
            "justification": "[Google API key not set]",
            "referenced_clauses": []
        }
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-pro')
    # Prepare context for the LLM
    context = "\n\n".join([f"Clause: {clause}" for clause, _ in retrieved_clauses])
    prompt = f"""
You are an expert insurance policy decision assistant. Given the following user query and extracted entities, and the most relevant policy clauses, make a decision (approved/rejected), payout amount (if any), and provide a justification. Reference the specific clauses used. Return your answer as a JSON object with keys: decision, amount, justification, referenced_clauses (list of clause texts used).

User Query: {parsed_query}

Relevant Clauses:
{context}

Respond ONLY with a valid JSON object.
"""
    try:
        response = model.generate_content(prompt)
        import json
        # Remove code block markers if present
        text = response.text.strip()
        text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
        text = re.sub(r"```$", "", text)
        try:
            result = json.loads(text)
        except Exception:
            # If not valid JSON, return as error
            return {
                "decision": "error",
                "amount": 0,
                "justification": f"LLM did not return valid JSON: {response.text.strip()}",
                "referenced_clauses": []
            }
        # Ensure all required keys are present
        for key in ["decision", "amount", "justification", "referenced_clauses"]:
            if key not in result:
                result[key] = None
        return result
    except Exception as e:
        return {
            "decision": "error",
            "amount": 0,
            "justification": f"[Error from Gemini Pro: {e}]",
            "referenced_clauses": []
        } 