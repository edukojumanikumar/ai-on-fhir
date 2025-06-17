from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_parser import extract_entities
from fhir_mapper import build_fhir_query
import json

app = Flask(__name__)
CORS(app)

# Store latest query result (in-memory)
latest_result = {}

# Homepage route
@app.route("/")
def index():
    if latest_result:
        pretty_json = json.dumps(latest_result, indent=2)
        return f"""
        <html>
          <head>
            <title>AI on FHIR Backend</title>
            <meta http-equiv="refresh" content="5"> <!-- Refresh every 5 seconds -->
            <style>
              body {{ font-family: Segoe UI, sans-serif; padding: 20px; background: #f9f9fb; }}
              pre {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }}
              h2 {{ color: #007bff; }}
            </style>
          </head>
          <body>
            <h2>✅ AI on FHIR Backend is Running</h2>
            <p>use the <strong>React frontend</strong> at <code>http://localhost:3000</code>.</p>
            <hr>
            <h3>📤 Latest Query Result:</h3>
            <pre>{pretty_json}</pre>
          </body>
        </html>
        """
    else:
        return """
        <html>
          <head>
            <title>AI on FHIR Backend</title>
            <meta http-equiv="refresh" content="5">
            <style>
              body { font-family: Segoe UI, sans-serif; padding: 20px; background: #f9f9fb; }
              h2 { color: #007bff; }
            </style>
          </head>
          <body>
            <h2>✅ AI on FHIR Backend is Running</h2>
            <p>No query received yet. Waiting for input...</p>
          </body>
        </html>
        """


# Query processing route
@app.route("/query", methods=["POST"])
def query():
    global latest_result
    data = request.get_json()
    query_text = data.get("query", "")

    entities = extract_entities(query_text)
    fhir_query = build_fhir_query(entities)
    condition = entities.get("condition", "Unknown")
    age_threshold = entities.get("age")

    # Simulate mock patient filtering
    mock_pool = [
        {"name": "Alice", "age": 61}, {"name": "Bob", "age": 72}, {"name": "Charlie", "age": 75},
        {"name": "David", "age": 68}, {"name": "Eva", "age": 80}, {"name": "Frank", "age": 65},
        {"name": "Grace", "age": 70}, {"name": "Helen", "age": 55}, {"name": "Isaac", "age": 69},
        {"name": "Judy", "age": 74}, {"name": "Kyle", "age": 59}, {"name": "Laura", "age": 77},
        {"name": "Mike", "age": 62}, {"name": "Nina", "age": 67}, {"name": "Omar", "age": 71},
        {"name": "Priya", "age": 66}, {"name": "Quinn", "age": 58}, {"name": "Rita", "age": 73},
        {"name": "Steve", "age": 69}, {"name": "Tina", "age": 64}
    ]

    filtered_results = [
        {**p, "condition": condition}
        for p in mock_pool
        if age_threshold is None or p["age"] >= age_threshold
    ]

    latest_result = {
        "input": query_text,
        "entities": entities,
        "fhir_simulation": fhir_query,
        "results": filtered_results
    }

    print("\nQuery received and stored for frontend and backend UI.\n")
    return jsonify(latest_result)

if __name__ == "__main__":
    app.run(debug=True)
