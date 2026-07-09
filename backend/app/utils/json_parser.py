import json
import re


def extract_json(text: str) -> dict:
    """
    Extracts the first valid JSON object from an LLM response.

    Handles:
    - Markdown code blocks
    - Extra explanations
    - Leading/trailing text
    """

    text = text.strip()

    # Remove markdown fences
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No valid JSON found in LLM response.")

    return json.loads(match.group())