import re
import spacy
from typing import Dict

nlp = spacy.load("en_core_web_sm")

AGE_PATTERN = re.compile(r"(\d{2})[- ]?(year[- ]old|y/o|M|F|male|female)?", re.I)
DURATION_PATTERN = re.compile(r"(\d+)[- ]?(month|year)[- ]?(old|policy)?", re.I)

# Extend this as needed for more robust extraction

def parse_query(query: str) -> Dict:
    doc = nlp(query)
    result = {}
    # Age
    age_match = AGE_PATTERN.search(query)
    if age_match:
        result["age"] = int(age_match.group(1))
    # Gender
    if "male" in query.lower() or "m," in query.lower():
        result["gender"] = "male"
    elif "female" in query.lower() or "f," in query.lower():
        result["gender"] = "female"
    # Procedure (naive: first noun chunk)
    for chunk in doc.noun_chunks:
        if "surgery" in chunk.text.lower() or "procedure" in chunk.text.lower():
            result["procedure"] = chunk.text
            break
    # Location (naive: proper noun)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            result["location"] = ent.text
            break
    # Policy duration
    duration_match = DURATION_PATTERN.search(query)
    if duration_match:
        result["policy_duration"] = duration_match.group(0)
    return result 