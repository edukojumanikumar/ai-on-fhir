from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_parser import extract_entities
from fhir_mapper import build_fhir_query
import logging

app = Flask(__name__)
CORS(app)

# Set up logging to console
logging.basicConfig(level=logging.INFO)

# Simulated mock patient pool (for demo purposes)
mock_pool = [
    {"name": "Alice", "age": 61},
    {"name": "Bob", "age": 72},
    {"name": "Charlie", "age": 75},
    {"name": "David", "age": 68},
    {"name": "Eva", "age": 80},
    {"name": "Frank", "age": 65},
    {"name": "Grace", "age": 70},
    {"name": "Helen", "age": 55},
    {"name": "Isaac", "age": 69},
    {"name": "Judy", "age": 74},
    {"name": "Kyle", "age": 59},
    {"name": "Laura", "age": 77},
    {"name": "Mike", "age": 62},
    {"name": "Nina", "age": 67},
    {"name": "Omar", "age": 71},
    {"name": "Priya", "age": 66},
    {"name": "Quinn", "age": 58},
    {"name": "Rita", "age": 73},
    {"name": "Steve", "age": 69},
    {"name": "Tina", "age": 64}
]

@app.route("/", methods=["GET"])
def health_check():
    """Health check route to verify server is running."""
    return jsonify({"status": "OK", "message": "FHIR backend is live!"}), 200

@app.route("/query", methods=["POST"])
def query():
    """Handle natural language queries and simulate FHIR-style response."""
    data = request.get_json()
    query_text = data.get("query", "")

    logging.info(f"Received query: {query_text}")

    # Extract entities from natural language query
    entities = extract_entities(query_text)
    logging.info(f"Extracted entities: {entities}")

    # Build simulated FHIR query from extracted entities
    fhir_query = build_fhir_query(entities)

    condition = entities.get("condition", "Unknown")
    age_threshold = entities.get("age")

    # Filter mock patients by age and attach condition
    mock_results = []
    for person in mock_pool:
        if age_threshold is None or person["age"] >= age_threshold:
            mock_results.append({**person, "condition": condition})

    return jsonify({
        "input": query_text,
        "entities": entities,
        "fhir_simulation": fhir_query,
        "results": mock_results
    })

if __name__ == "__main__":
    app.run(debug=True)
