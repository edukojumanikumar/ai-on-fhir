# fhir_mapper.py

def build_fhir_query(entities):
    """
    Build a simulated FHIR-like query object based on extracted entities.
    
    Args:
        entities (dict): Dictionary containing 'age' and 'condition' keys.

    Returns:
        dict: Simulated FHIR query representation.
    """
    age = entities.get("age")
    condition = entities.get("condition")

    simulated_query = {
        "resourceType": "FHIR_Query",
        "Patient": {},
        "Condition": {}
    }

    # Add age filter if found
    if age is not None:
        simulated_query["Patient"]["age"] = f">={age}"

    # Add condition filter if found
    if condition:
        simulated_query["Condition"]["code"] = condition

    return simulated_query
