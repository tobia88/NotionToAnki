from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from config_loader import config_loader
import httpx

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

def interpret_vocabulary_items(entries: list) -> list:
    parsed_entries = []
    for entry in entries:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system",
                    "content": config_loader.openai.prompt_system_content
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


def generate_images_url(entires: list, callback) -> list[dict[any]]:
    """
    return {'id': str, 'name': str, 'url': str}
    """
    url_list = []
    for entry in entires:
        prompt: str = config_loader.openai.prompt_image_format\
            .replace('%name%', entry['name'])\
            .replace('%meaning%', entry['meaning'])
        try:
            print (f"Generating image for {entry['name']} with prompt: {prompt}")
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
        except Exception as e:
            print(f"Error generating image for {entry['name']}: {e}")
            continue

        output_image_path = f'{entry["id"]}_{entry["name"]}'

        callback(response.data[0].url, output_image_path)
        url_list.append({'id': entry['id'], 'name': entry['name'], 'url': response.data[0].url})
        print(f"Generated image for {entry['name']} at {response.data[0].url}")

    return url_list


if __name__ == "__main__":
    entries = [{'name':'test'}]
    # interpret_vocabulary_items(entries)
    generate_images_url(entries)