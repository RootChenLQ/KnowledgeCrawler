# -*- coding: utf-8 -*-
"""
Module for interacting with Large Language Models (LLMs).

This module contains functions to get responses from an LLM and stores the
detailed prompt templates required for the knowledge extraction pipeline.

NOTE: This is a placeholder module. The actual implementation will require
integrating an LLM SDK (e.g., OpenAI, Anthropic, or a self-hosted model)
and managing API keys and request/response logic.
"""
import json

# --- Prompt Templates (from the technical document) ---

# 4.2.1: Query Augmentation
QUERY_AUGMENTATION_PROMPT = """
I am building a knowledge graph about smart water conservancy. For the core entity "{entity_name}", please generate 5 specific and technical search engine queries to find expert-level information about its principles, methods, models, and application cases. Please focus on terms used in academic and engineering fields, and include queries in both Chinese and English.
"""

# 4.2.2: Entity Typing and Definition
TYPING_AND_DEFINITION_PROMPT = """
Based on the following aggregated text about "{entity_name}":
--- TEXT START ---
{raw_text}
--- TEXT END ---

Please perform the following tasks:
1.  **Classification**: Choose the most precise sub-type for "{entity_name}" from the following `DomainConcept` sub-types: `PhysicalObject`, `PhysicalPhenomenon`, `EngineeringProcess`, `AbstractConcept`, `EconomicTerm`, `Property`. (Note: The full list of types should be used here in a real implementation).
2.  **Definition**: Write an accurate, objective, encyclopedia-style definition (`description`) summarizing the core meaning of "{entity_name}".
3.  **Background**: Write a more detailed background information section (`background_context`) explaining its role, historical development, and importance in water conservancy engineering.

Please return the result in JSON format, containing the keys `entity_type` (which should be an object with `primary_type` and `sub_type`), `description`, and `background_context`.
"""

# 4.2.3: Attribute Extraction
ATTRIBUTE_EXTRACTION_PROMPT = """
Given that "{entity_name}" is an `{entity_type}`. Please extract its key structured attributes from the same text provided previously. The attributes to look for include, but are not limited to:
- `objectives`: e.g., flood control, power generation, irrigation, ecological protection.
- `input_data`: e.g., real-time hydrological data, weather forecasts, water demand plans.
- `key_constraints`: e.g., flood control limited water level, minimum downstream discharge, navigation requirements.
- `scheduling_rules`: e.g., scheduling chart, dispatching regulations.

Please format the extracted information as a JSON object to be used as the value for the `attributes` field. If an attribute is not found in the text, do not include its key.
"""

# 4.2.4: Relation Inference
RELATION_INFERENCE_PROMPT = """
Please re-analyze the text about "{entity_name}" and refer to the following complete list of entities in the water conservancy domain:
{all_entities_list}

Identify and list all explicit or strongly implied relationships between "{entity_name}" and other entities in the master list. For each relationship, provide it in the following JSON format:
`{{ "target_entity_id": "...", "target_label": "...", "relationship_type": "..." }}`

Focus on identifying relationship types such as:
- `uses_method`: Does it apply a certain mathematical method (e.g., `OptimizationAlgorithm`, `LinearProgramming`)?
- `governed_by`: Is it constrained by a regulation or technical standard (e.g., `FloodDispatchPlanPreparationGuide`)?
- `mitigates`: Is it used to mitigate a natural phenomenon or disaster (e.g., `Flood`, `Drought`)?
- `enables`: Does it support or enable a certain goal (e.g., `HydropowerGeneration`, `Irrigation`)?

Please ensure you only output high-confidence relationships that are supported by the text.
"""

# 4.2.5: Final Validation
FINAL_VALIDATION_PROMPT = """
You are a senior expert in water conservancy engineering. Please review the following complete JSON data generated for the entity "{entity_name}". Evaluate its accuracy, logic, and completeness within the professional context of water conservancy engineering.

- Is the classification correct?
- Are the attributes comprehensive and accurate?
- Are the relationships reasonable? For example, does the relationship `uses_method: OptimizationAlgorithm` align with engineering practice?

If the data is completely correct, return it as is. If there are any inaccuracies or omissions, please provide the corrected, final version of the complete JSON.

JSON_DATA:
{json_data}
"""

def get_llm_response(prompt: str) -> str:
    """
    Simulates getting a response from an LLM.

    Args:
        prompt: The prompt to send to the LLM.

    Returns:
        A simulated response string from the LLM.
    """
    print("--- [Placeholder] Sending prompt to LLM ---")
    # In a real implementation, you would use an LLM API client here.
    # The response will be a dummy JSON string based on the prompt.

    # This is a very basic router to provide different dummy responses
    # based on the prompt content for demonstration purposes.
    if "generate 5 specific and technical search engine queries" in prompt:
        return json.dumps([
            "水库调度 优化算法 应用",
            "reservoir scheduling optimization models",
            "水库调度 防洪兴利 联合调度",
            "水库调度 随机动态规划",
            "reservoir operation rules extraction"
        ])
    elif "Classification" in prompt and "Definition" in prompt:
        return json.dumps({
            "entity_type": {"primary_type": "DomainConcept", "sub_type": "EngineeringProcess"},
            "description": "这是由LLM生成的对'水库调度'的模拟描述。",
            "background_context": "这是由LLM生成的关于'水库调度'的模拟背景信息。"
        })
    elif "extract its key structured attributes" in prompt:
        return json.dumps({
            "objectives": ["防洪", "发电", "灌溉"],
            "key_constraints": ["防洪限制水位", "下游最小生态流量"]
        })
    elif "re-analyze the text about" in prompt:
        return json.dumps([
            {"target_entity_id": "OptimizationAlgorithm", "target_label": "优化算法", "relationship_type": "uses_method"},
            {"target_entity_id": "FloodControlLawOfPRC", "target_label": "中华人民共和国防洪法", "relationship_type": "governed_by"}
        ])
    elif "You are a senior expert" in prompt:
        # The self-correction prompt just returns the received data for now
        start_index = prompt.find('{')
        end_index = prompt.rfind('}') + 1
        return prompt[start_index:end_index]

    return "{}"
