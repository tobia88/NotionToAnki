from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import yaml

import os

load_dotenv()
client = OpenAI()
client.api_key = os.environ.get("OPENAI_API_KEY")

class VocabularyExtraction(BaseModel):
    name: str
    language: str
    meaning: str
    rate_of_use: str
    manual_root: str
    sentence_1: str
    translation_1: str
    sentence_2: str
    translation_2: str
    sentence_3: str
    translation_3: str
    compare_word_1: str
    compare_meaning_1: str
    compare_word_2: str
    compare_meaning_2: str
    compare_word_3: str
    compare_meaning_3: str

def process_entries(entries):
    sys_content = ""

    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as file:
            sys_content = yaml.safe_load(file)
    except FileNotFoundError:
        print("File not found")
        return

    parsed_entries = []
    for entry in entries:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system",
                    "content": sys_content
                },
                {
                    "role": "user",
                    "content": entry["name"]
                }
            ],
            response_format=VocabularyExtraction,
            temperature=0.3,
            max_tokens=2048,
            top_p=1
        )
        parsed_message = response.choices[0].message.parsed
        parsed_entries.append({"id": entry["id"], "parsed_message": parsed_message})

    return parsed_entries


if __name__ == "__main__":
    entries = []
    process_entries(entries)