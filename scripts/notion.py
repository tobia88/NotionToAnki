import os
import httpx
import configparser
from config_loader import config_loader
from dotenv import load_dotenv

config = configparser.ConfigParser()
config.read('config.ini')

load_dotenv()

NOTION_API_URL = 'https://api.notion.com/v1/databases'
NOTION_VERSION = '2022-06-28'
TOKEN = os.environ.get('NOTION_API_KEY')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')
TARGET_LANGUAGE = config_loader.language
NOTION_QUERY_URL = f"{NOTION_API_URL}/{DATABASE_ID}/query"
NOTION_API_HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}


def get_empty_meaning_entries() -> list[dict[str, any]]:
    query_data = {
        "filter": {
            "and": [
                {
                    "property": "Language",
                    "select": {
                        "equals": TARGET_LANGUAGE
                    }
                },
                {
                    "property": "Meaning",
                    "rich_text": {
                        "is_empty": True
                    }
                }
            ]
        }
    }

    try:
        response = httpx.post(NOTION_QUERY_URL, headers=NOTION_API_HEADERS, json=query_data)
        response.raise_for_status()

    except httpx.HTTPStatusError as err:
        print(f"HTTP error occurred: {err}")
        return []

    except Exception as err:
        print(f"An error occurred: {err}")
        return []

    data = response.json()
    entries = [{"id": result["id"], "name": result["properties"]["Name"]["title"][0]["text"]["content"]} for result in data["results"]]
    if entries:
        for entry in entries:
            print(f"Empty meaning entry found: {entry['name']}")
    else:
        print("No empty meaning entries found.")

    return entries


def get_vocabs() -> list:
    query_data = {
        "filter": {
            "and": [
                {
                    "property": "Language",
                    "select": {
                        "equals": TARGET_LANGUAGE
                    }
                },
                {
                    "property": "Meaning",
                    "rich_text": {
                        "is_not_empty": True
                    }
                }
            ]
        }
    }

    try:
        response = httpx.post(NOTION_QUERY_URL, headers=NOTION_API_HEADERS, json=query_data)
        response.raise_for_status()

    except httpx.HTTPStatusError as err:
        print(f"HTTP error occurred: {err}")
        return

    except Exception as err:
        print(f"An error occurred: {err}")
        return

    result_dict = response.json()
    vocab_list_results = result_dict.get('results', [])
    vocab_list = []
    for result in vocab_list_results:
        vocab = map_notion_result_to_vocabulary(result, TARGET_LANGUAGE)
        vocab_list.append(vocab)

    return vocab_list


def map_notion_result_to_vocabulary(result, target_language):
    properties = result.get('properties', {})
    name = properties.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')

    print(f"Processing vocabulary: {name}")

    meaning = properties.get('Meaning', {}).get('rich_text', [])[0].get('text', {}).get('content', '')
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

    return {
        'name': name,
        'language': TARGET_LANGUAGE,
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
        'root': root,
        'illustration_url': illustration_url
    }


if __name__ == "__main__":
    get_empty_meaning_entries()
    get_vocabs()