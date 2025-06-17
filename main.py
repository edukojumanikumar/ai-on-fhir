# main.py

from nlp_parser import extract_entities
from fhir_mapper import build_fhir_query

def handle_query(query):
    entities = extract_entities(query)
    fhir_query = build_fhir_query(entities)

    return {
        "input": query,
        "entities": entities,
        "fhir_simulation": fhir_query
    }

if __name__ == "__main__":
    # You can change this input for testing
    query = input("Enter your healthcare query: ")
    result = handle_query(query)
    print("\n--- Result ---")
    print(result)
