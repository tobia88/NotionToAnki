import os
import httpx
from typing import Any, Dict, Optional
import configparser
from dotenv import load_dotenv

config = configparser.ConfigParser()
config.read('config.ini')

load_dotenv()

NOTION_API_URL = 'https://api.notion.com/v1/databases'
NOTION_VERSION = '2022-06-28'
TOKEN = os.environ.get('NOTION_API_KEY')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')
TARGET_LANGUAGE = config['notion']['language']
IMAGES_DIR = 'images'

def get_vocabs() -> list:
    url = f'{NOTION_API_URL}/{DATABASE_ID}/query'
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Notion-Version": NOTION_VERSION
    }

    try:
        response = httpx.post(url, headers=headers)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    result_dict = response.json()
    vocab_list_results = result_dict.get('results', [])
    vocab_list = []
    for result in vocab_list_results:
        vocab = map_notion_result_to_vocabulary(result, TARGET_LANGUAGE)
        if vocab:
            vocab_list.append(vocab)

    return vocab_list



def map_notion_result_to_vocabulary(result: Dict[str, Any], target_language: str) -> Optional[Dict[str, Any]]:
    properties = result.get('properties', {})
    name = properties.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
    language = properties.get('Language', {}).get('select', {}).get('name', '')

    if language != target_language:
        return None

    print(f"Processing vocabulary: {name}")

    meaning_rich_text = properties.get('Meaning', {}).get('rich_text', [])
    if not meaning_rich_text:
        return None

    meaning = meaning_rich_text[0].get('text', {}).get('content', '')
    sentence_1 = properties.get('Sentence 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    translation_1 = properties.get('Translation 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    sentence_2 = properties.get('Sentence 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    translation_2 = properties.get('Translation 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    sentence_3 = properties.get('Sentence 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    translation_3 = properties.get('Translation 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    compare_word_1 = properties.get('Compare Word 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    compare_meaning_1 = properties.get('Compare Meaning 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    compare_word_2 = properties.get('Compare Word 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    compare_meaning_2 = properties.get('Compare Meaning 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    compare_word_3 = properties.get('Compare Word 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    compare_meaning_3 = properties.get('Compare Meaning 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    root = properties.get('Root', {}).get('formula', {}).get('string', '')

    files = properties.get('Illustration', {}).get('files', [])
    illustration_url = files[0].get('file', {}).get('url', '') if files else ''

    if illustration_url:
        download_image(illustration_url, name)

    return {
        'name': name,
        'language': language,
        'meaning': meaning,
        'sentence_1': sentence_1,
        'translation_1': translation_1,
        'sentence_2': sentence_2,
        'translation_2': translation_2,
        'sentence_3': sentence_3,
        'translation_3': translation_3,
        'compare_word_1': compare_word_1,
        'compare_meaning_1': compare_meaning_1,
        'compare_word_2': compare_word_2,
        'compare_meaning_2': compare_meaning_2,
        'compare_word_3': compare_word_3,
        'compare_meaning_3': compare_meaning_3,
        'root': root
    }

def download_image(url: str, name: str) -> None:
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    image_path = os.path.join(IMAGES_DIR, f"{name}.jpg")
    if os.path.exists(image_path):
        print(f"Image already exists for: {name}, skipping download.")
        return

    print(f"Downloading image for: {name}")

    with httpx.stream("GET", url) as response:
        response.raise_for_status()
        total = int(response.headers["Content-Length"])
        with open(image_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_bytes():
                f.write(chunk)
                downloaded += len(chunk)
                percentage = (downloaded / total) * 100
                print(f"Downloading {name}: {percentage:.2f}% complete", end='\r')

    print(f"\nImage saved to: {image_path}")


if __name__ == "__main__":
    get_vocabs()