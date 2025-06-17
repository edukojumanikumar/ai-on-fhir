# test_nlp.py

from nlp_parser import extract_entities
from fhir_mapper import build_fhir_query

query = "Show me all diabetic patients over 50"
entities = extract_entities(query)
fhir_query = build_fhir_query(entities)

print("Entities:", entities)
print("Simulated FHIR Query:", fhir_query)
