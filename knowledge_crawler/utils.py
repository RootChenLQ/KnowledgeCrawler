# -*- coding: utf-8 -*-
"""
Utility functions for the Knowledge Crawler project.

This module contains helper functions for tasks such as reading input files,
assembling final JSON objects, and saving data to files.
"""
import json
import pandas as pd
import re
import pinyin

def load_all_entities_from_excel(filepath: str) -> list[str]:
    """
    Loads entity names from a specified column in an Excel file.

    Args:
        filepath: The path to the .xlsx file.

    Returns:
        A list of entity names. Returns an empty list if file cannot be read.
    """
    print(f"--- Loading entities from: {filepath} ---")
    try:
        # Assuming the entities are in the first column of the first sheet.
        # This can be made more robust if the column name is known.
        df = pd.read_excel(filepath, header=None)
        entities = df[0].dropna().astype(str).tolist()
        print(f"--- Found {len(entities)} entities. ---")
        return entities
    except FileNotFoundError:
        print(f"Error: The file was not found at {filepath}")
        return []
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return []

def standardize_entity_id(entity_name: str) -> str:
    """
    Creates a standardized, machine-readable entity ID from its name
    by converting it to CamelCase Pinyin.
    Example: "重力坝" -> "ZhongLiBa"
    """
    # Remove special characters that are not part of the name
    entity_name = re.sub(r'[·-]', '', entity_name)
    # Get pinyin, separated by spaces
    pinyin_str = pinyin.get(entity_name, format="strip", delimiter=" ")
    # Capitalize each word and join to form CamelCase
    camel_case_id = "".join(word.capitalize() for word in pinyin_str.split())
    # Remove any remaining non-alphanumeric characters
    return re.sub(r'[^a-zA-Z0-9]', '', camel_case_id)


def assemble_json(entity_name: str, source_file: str, info: dict, relations: list) -> dict:
    """
    Assembles the final JSON object for an entity.

    Args:
        entity_name: The original name of the entity.
        source_file: The source file the entity came from.
        info: A dict containing structured info like description, type, etc.
        relations: A list of relation objects.

    Returns:
        A complete JSON object for the entity.
    """
    print(f"--- Assembling final JSON for: {entity_name} ---")

    # In a real implementation, you would need to handle aliases.
    # For now, we'll use an empty list.
    aliases = []
    if "aliases" in info:
        aliases = info["aliases"]

    assembled_obj = {
        "entity_id": standardize_entity_id(entity_name),
        "label": entity_name,
        "aliases": aliases,
        "source_file": source_file,
        "description": info.get("description", ""),
        "background_context": info.get("background_context", ""),
        "entity_type": info.get("entity_type", {}),
        "attributes": info.get("attributes", {}),
        "relations": relations
    }
    return assembled_obj


def save_json_to_file(json_data: dict, output_dir: str = "output"):
    """
    Saves a JSON object to a file in a specified directory.
    The filename is derived from the entity_id.
    """
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    entity_id = json_data.get('entity_id', 'unknown_entity')
    filepath = os.path.join(output_dir, f"{entity_id}.json")

    print(f"--- Saving JSON to: {filepath} ---")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print("--- Save successful. ---")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
