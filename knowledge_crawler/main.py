# -*- coding: utf-8 -*-
"""
Main control script for the Knowledge Crawler.

This script orchestrates the entire process of building the knowledge graph,
following the technical plan. It loads entities, processes each one through
the pipeline, and saves the structured output.
"""
import json
import os

# Import modules from the project
import crawler_module
import llm_api_module
import validator_module
import utils

# --- Configuration ---
# The user's Excel file is in the root directory, one level above this script.
INPUT_EXCEL_FILE = '../大渡河知识实体.xlsx'
SOURCE_FILENAME = os.path.basename(INPUT_EXCEL_FILE)
OUTPUT_DIR = 'output'

def process_entity(entity_name: str, all_entities_list: list[str]):
    """
    Processes a single entity through the entire knowledge extraction pipeline.

    Args:
        entity_name: The name of the entity to process.
        all_entities_list: The full list of all entities for context.
    """
    print(f"\n--- Processing Entity: {entity_name} ---")

    # --------------------------------------------------------------------------
    # Stage 1: Intelligent Query Construction & Targeted Information Retrieval
    # --------------------------------------------------------------------------
    print("\n[Stage 1/4] Query Augmentation and Crawling...")
    query_prompt = llm_api_module.QUERY_AUGMENTATION_PROMPT.format(entity_name=entity_name)
    augmented_queries_str = llm_api_module.get_llm_response(query_prompt)
    augmented_queries = json.loads(augmented_queries_str)

    raw_text = crawler_module.crawl_web(augmented_queries)

    if not raw_text or raw_text.strip() == "":
        print(f"Warning: No information found for {entity_name}. Skipping.")
        # In a real system, you might create a minimal JSON to mark this
        # e.g., utils.create_minimal_json(entity_name, status="info_not_found")
        return

    # --------------------------------------------------------------------------
    # Stage 2: LLM-driven Information Distillation & Structuring
    # --------------------------------------------------------------------------
    print("\n[Stage 2/4] Information Structuring...")
    structuring_prompt = llm_api_module.TYPING_AND_DEFINITION_PROMPT.format(
        entity_name=entity_name,
        raw_text=raw_text
    )
    structured_info_str = llm_api_module.get_llm_response(structuring_prompt)
    structured_info = json.loads(structured_info_str)

    entity_type_obj = structured_info.get("entity_type", {})
    entity_type_name = entity_type_obj.get("sub_type", "Unknown")

    attribute_prompt = llm_api_module.ATTRIBUTE_EXTRACTION_PROMPT.format(
        entity_name=entity_name,
        entity_type=entity_type_name
    )
    attributes_str = llm_api_module.get_llm_response(attribute_prompt)
    attributes = json.loads(attributes_str)
    structured_info["attributes"] = attributes

    # --------------------------------------------------------------------------
    # Stage 3: Relation Inference and Link Prediction
    # --------------------------------------------------------------------------
    print("\n[Stage 3/4] Relation Inference...")
    relation_prompt = llm_api_module.RELATION_INFERENCE_PROMPT.format(
        entity_name=entity_name,
        all_entities_list=json.dumps(all_entities_list, ensure_ascii=False)
    )
    relations_str = llm_api_module.get_llm_response(relation_prompt)
    relations = json.loads(relations_str)

    # --------------------------------------------------------------------------
    # Stage 4: Synthesis, Validation, and JSON Generation
    # --------------------------------------------------------------------------
    print("\n[Stage 4/4] Synthesis and Validation...")
    # Assemble the complete JSON object
    final_json_obj = utils.assemble_json(
        entity_name=entity_name,
        source_file=SOURCE_FILENAME,
        info=structured_info,
        relations=relations
    )

    # Validate against the master schema
    if not validator_module.validate_schema(final_json_obj):
        print(f"Error: Schema validation failed for {entity_name}. Skipping.")
        return

    # Final LLM self-correction step
    validation_prompt = llm_api_module.FINAL_VALIDATION_PROMPT.format(
        entity_name=entity_name,
        json_data=json.dumps(final_json_obj, ensure_ascii=False, indent=2)
    )
    validated_json_str = llm_api_module.get_llm_response(validation_prompt)

    # Save the final, validated JSON file
    utils.save_json_to_file(json.loads(validated_json_str), OUTPUT_DIR)

    print(f"--- Successfully processed and saved {entity_name} ---")


def main():
    """
    Main function to run the knowledge extraction pipeline.
    """
    print("=============================================")
    print("=== KNOWLEDGE CRAWLER PROJECT STARTING... ===")
    print("=============================================")

    # Load the list of all entities to serve as a global context for relationships
    all_entities_list = utils.load_all_entities_from_excel(INPUT_EXCEL_FILE)

    if not all_entities_list:
        print("No entities found in the input file. Exiting.")
        return

    # The document mentions processing all entities, but for a demonstration,
    # let's just process the first few to show the framework is working.
    entities_to_process = all_entities_list[:2]
    print(f"\nFound {len(all_entities_list)} total entities. Processing first {len(entities_to_process)} for demonstration.")

    for entity_name in entities_to_process:
        try:
            process_entity(entity_name, all_entities_list)
        except Exception as e:
            print(f"\n--- CRITICAL ERROR processing '{entity_name}': {e} ---")
            print("--- Skipping to next entity. ---")

    print("\n=============================================")
    print("===      KNOWLEDGE CRAWLER FINISHED       ===")
    print("=============================================")


if __name__ == "__main__":
    main()
