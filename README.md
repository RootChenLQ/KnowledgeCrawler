# Knowledge Crawler for Smart Water Conservancy

This project is an implementation of the "Strategic Blueprint for Building a Smart Water Conservancy Knowledge Graph". It provides a complete, end-to-end pipeline for automatically extracting structured knowledge from unstructured text and building a knowledge graph.

The pipeline is driven by a series of Large Language Model (LLM) prompts and is designed to be modular and extensible.

## Project Structure

The project is organized into the following components:

- **`大渡河知识实体.xlsx`**: The input Excel file containing the list of seed entities for the knowledge graph.
- **`requirements.txt`**: A list of all the Python dependencies required to run the project.
- **`knowledge_crawler/`**: The main directory for the Python source code.
  - **`main.py`**: The main control script that orchestrates the entire knowledge extraction pipeline.
  - **`utils.py`**: Contains helper functions for loading data, standardizing IDs, assembling JSON objects, and saving files.
  - **`crawler_module.py`**: A **placeholder module** for web crawling. It needs to be integrated with a real web scraping library.
  - **`llm_api_module.py`**: A **placeholder module** for interacting with a Large Language Model (LLM). It contains all the necessary prompt templates but needs to be connected to an actual LLM API.
  - **`validator_module.py`**: Contains the master JSON schema and a function to validate the output against it.
  - **`output/`**: The directory where the final, structured JSON files for each entity are saved. This directory is created automatically when the script is run.

## How to Run

1.  **Install Dependencies:**
    Make sure you have Python 3 installed. Then, install the required libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Placeholder Modules (Crucial Step):**
    This framework is fully built but requires you to connect it to your specific web crawling and LLM services.

    -   **LLM API (`knowledge_crawler/llm_api_module.py`):**
        -   Open this file and locate the `get_llm_response` function.
        -   Replace the placeholder logic with actual calls to your chosen LLM API (e.g., OpenAI's `client.chat.completions.create`, Anthropic's client, etc.).
        -   You will need to manage your API keys securely, for example, by using environment variables.

    -   **Web Crawler (`knowledge_crawler/crawler_module.py`):**
        -   Open this file and locate the `crawl_web` function.
        -   Replace the placeholder logic with a real web crawling implementation. You can use libraries like `requests` and `BeautifulSoup` for simple cases, or a more robust framework like `Scrapy`.
        -   The function should take a list of search queries and return a single string of clean, aggregated text content.

3.  **Run the Pipeline:**
    Once the placeholder modules are configured, you can run the main script from the project's root directory:
    ```bash
    python3 knowledge_crawler/main.py
    ```
    By default, the script is configured to process the first two entities from the Excel file as a demonstration. You can change this by editing the `entities_to_process` variable in `main.py`.

## Output

The script will generate one `.json` file for each processed entity inside the `knowledge_crawler/output/` directory. The filename will be the CamelCase Pinyin version of the entity's name (e.g., `ShuiZiYuan.json`).

Each JSON file will be structured according to the master schema defined in `validator_module.py`, containing the entity's description, attributes, relationships, and other metadata.
