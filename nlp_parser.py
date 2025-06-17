import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Canonical condition keywords and their synonyms
CONDITION_MAP = {
    "diabetes": ["diabetes", "diabetic"],
    "asthma": ["asthma"],
    "hypertension": ["hypertension", "high blood pressure"],
    "cancer": ["cancer"],
    "covid": ["covid", "corona", "covid-19"],
    "flu": ["flu", "influenza"]
}

def extract_entities(query):
    query = query.lower()
    doc = nlp(query)
    tokens = [token.text for token in doc]

    # Match any known condition
    matched_conditions = []
    for canonical, synonyms in CONDITION_MAP.items():
        if any(word in tokens for word in synonyms):
            matched_conditions.append(canonical)

    # Just use the first condition for now (can be expanded)
    condition = matched_conditions[0] if matched_conditions else None

    # Match age with flexible pattern support
    age_match = re.search(r"(?:over|older than|age above|>|≥|\+)?\s*(\d{2,3})", query)
    age = int(age_match.group(1)) if age_match else None

    # Detect gender (optional)
    gender = None
    if "female" in tokens or "woman" in tokens:
        gender = "female"
    elif "male" in tokens or "man" in tokens:
        gender = "male"

    return {
        "age": age,
        "condition": condition,
        "gender": gender
    }
