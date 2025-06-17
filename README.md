# AI on FHIR – Part 1: Backend & NLP Integration

This service accepts natural language queries and simulates a FHIR API request by extracting healthcare-related entities like age and condition using NLP.

## 🧠 How It Works

1. `nlp_parser.py`: Uses spaCy and fuzzy matching to extract medical conditions and age constraints from natural language input.
2. `fhir_mapper.py`: Builds a mock FHIR query using `Patient` and `Condition` resources.
3. `main.py`: Central script to run and test everything interactively.

## 🚀 Getting Started

1. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

3. Run the app:
    ```bash
    python main.py
    ```

## ✅ Sample Queries

See `examples.json` for 5 test cases including:
- "Show me all diabetic patients over 50"
- "List asthma patients over 60"
- "Give me hypertension patients older than 45"

## 📂 Files

- `nlp_parser.py` – NLP logic
- `fhir_mapper.py` – FHIR query generator
- `main.py` – Entry point
- `examples.json` – Sample queries and expected output
