# -*- coding: utf-8 -*-
"""
Module for JSON schema definition and validation.

This module defines the master schema for the knowledge graph entities and
provides functions to validate JSON objects against that schema.
"""

# The master schema defines the expected structure of the final JSON object.
MASTER_SCHEMA = {
    "type": "object",
    "properties": {
        "entity_id": {"type": "string"},
        "label": {"type": "string"},
        "aliases": {"type": "array", "items": {"type": "string"}},
        "source_file": {"type": "string"},
        "description": {"type": "string"},
        "background_context": {"type": "string"},
        "entity_type": {
            "type": "object",
            "properties": {
                "primary_type": {"type": "string"},
                "sub_type": {"type": "string"}
            },
            "required": ["primary_type", "sub_type"]
        },
        "attributes": {"type": "object"},
        "relations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "target_entity_id": {"type": "string"},
                    "target_label": {"type": "string"},
                    "relationship_type": {"type": "string"}
                },
                "required": ["target_entity_id", "target_label", "relationship_type"]
            }
        }
    },
    "required": [
        "entity_id", "label", "aliases", "source_file", "description",
        "background_context", "entity_type", "attributes", "relations"
    ]
}

def validate_schema(json_obj: dict) -> bool:
    """
    Validates a JSON object against the MASTER_SCHEMA.

    This is a basic validator. For more complex scenarios, a library like
    jsonschema would be more robust.

    Args:
        json_obj: The JSON object (as a Python dict) to validate.

    Returns:
        True if the object is valid, False otherwise.
    """
    print(f"--- Validating schema for entity: {json_obj.get('label', 'N/A')} ---")

    # Check for required top-level fields
    for key in MASTER_SCHEMA["required"]:
        if key not in json_obj:
            print(f"Validation Error: Missing required key '{key}'")
            return False

    # Check types of properties
    for key, schema_props in MASTER_SCHEMA["properties"].items():
        if key in json_obj:
            if schema_props["type"] == "string" and not isinstance(json_obj[key], str):
                print(f"Validation Error: Key '{key}' should be a string.")
                return False
            if schema_props["type"] == "array" and not isinstance(json_obj[key], list):
                print(f"Validation Error: Key '{key}' should be a list.")
                return False
            if schema_props["type"] == "object" and not isinstance(json_obj[key], dict):
                print(f"Validation Error: Key '{key}' should be a dict.")
                return False

    # Deeper validation for nested objects can be added here.
    # For example, checking the structure of entity_type or relations array.

    print("--- Schema validation successful. ---")
    return True
