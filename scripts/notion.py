import os
import httpx
from config_loader import config_loader
from dotenv import load_dotenv
import utils

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


def get_response(query_data: dict) -> any:
    try:
        response = httpx.post(NOTION_QUERY_URL, headers=NOTION_API_HEADERS, json=query_data)
        response.raise_for_status()

    except httpx.HTTPStatusError as err:
        print(f"Notion:::HTTP error occurred: {err}")
        return

    except Exception as err:
        print(f"Notion:::An error occurred: {err}")
        return

    return response.json()


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

    data = get_response(query_data)
    entries = [{"id": result["id"], "name": result["properties"]["Name"]["title"][0]["text"]["content"]} for result in data["results"]]
    if entries:
        for entry in entries:
            print(f"Notion:::Empty meaning entry found: {entry['name']}")
    else:
        print("Notion:::No empty meaning entries found.")

    return entries


def get_empty_illustration_entries() -> any:
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
                },
                {
                    "property": "Illustration",
                    "files": {
                        "is_empty": True
                    }
                }
            ]
        }
    }

    data = get_response(query_data)
    return data


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
        print(f"Notion:::HTTP error occurred: {err}")
        return

    except Exception as err:
        print(f"Notion:::An error occurred: {err}")
        return

    result_dict = response.json()
    vocab_list_results = result_dict.get('results', [])
    vocab_list = []
    for result in vocab_list_results:
        vocab = map_notion_result_to_vocabulary(result)
        vocab_list.append(vocab)

    return vocab_list

def get_property_value(properties: dict, property_key: str) -> str:
    retval: str = ''

    property = properties[property_key]
    property_type = property.get('type')

    try:
        if property_type == 'title':
            retval = property.get('title', [{}])[0].get('text', {}).get('content', '')
        elif property_type == 'rich_text':
            retval = property.get('rich_text', [{}])[0].get('text', {}).get('content', '')
        elif property_type == 'select':
            retval = property.get('select', {}).get('name', '')
        elif property_type == 'formula':
            retval = property.get('formula', {}).get('string', '')
        elif property_type == 'files':
            retval = property.get('files', [{}])[0].get('file', {}).get('url', '')

    except Exception as err:
        print(f"Error===> Notion:::Key={property_key}::Type={property_type}::An error occurred: {err}")

    return retval


def map_notion_result_to_vocabulary(result: any) -> dict[str, str]:
    properties = result.get('properties', {})
    name = properties.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')

    print(f"Notion:::Processing vocabulary: {name}")

    # meaning = properties.get('Meaning', {}).get('rich_text', [])[0].get('text', {}).get('content', '')
    # sentence_1 = properties.get('Sentence 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    # translation_1 = properties.get('Translation 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    # sentence_2 = properties.get('Sentence 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    # translation_2 = properties.get('Translation 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    # sentence_3 = properties.get('Sentence 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    # translation_3 = properties.get('Translation 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    # compare_word_1 = properties.get('Compare Word 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    # compare_meaning_1 = properties.get('Compare Meaning 1', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    # compare_word_2 = properties.get('Compare Word 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    # compare_meaning_2 = properties.get('Compare Meaning 2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    # compare_word_3 = properties.get('Compare Word 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
    # compare_meaning_3 = properties.get('Compare Meaning 3', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')

    # root = properties.get('Root', {}).get('formula', {}).get('string', '')

    # files = properties.get('Illustration', {}).get('files', [])
    # illustration_url = files[0].get('file', {}).get('url', '') if files else ''
    # rate_of_use = properties.get('Rate of Usage', {}).get('select', {}).get('name', '')

    return {
        'id': result['id'],
        'name': name,
        'language': TARGET_LANGUAGE,
        'meaning': get_property_value(properties, 'Meaning'),
        'sentence_1': get_property_value(properties, 'Sentence 1'),
        'translation_1': get_property_value(properties, 'Translation 1'),
        'sentence_2': get_property_value(properties, 'Sentence 2'),
        'translation_2': get_property_value(properties, 'Translation 2'),
        'sentence_3': get_property_value(properties, 'Sentence 3'),
        'translation_3': get_property_value(properties, 'Translation 3'),
        'compare_word_1': get_property_value(properties, 'Compare Word 1'),
        'compare_meaning_1': get_property_value(properties, 'Compare Meaning 1'),
        'compare_word_2': get_property_value(properties, 'Compare Word 2'),
        'compare_meaning_2': get_property_value(properties, 'Compare Meaning 2'),
        'compare_word_3': get_property_value(properties, 'Compare Word 3'),
        'compare_meaning_3': get_property_value(properties, 'Compare Meaning 3'),
        'root': get_property_value(properties, 'Manual Root'),
        'illustration_url': get_property_value(properties, 'Illustration'),
        'rate_of_use': get_property_value(properties, 'Rate of Usage')
    }

def update_notion_page(entry_id, data: dict):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    print(data)

    page_data = {
        "properties": {
            "Meaning": {"rich_text": [{"text": {"content": data["meaning"]}}]},
            "Manual Root": {"rich_text": [{"text": {"content": data["manual_root"]}}]},
            "Sentence 1": {"rich_text": [{"text": {"content": data["sentence_1"]}}]},
            "Translation 1": {"rich_text": [{"text": {"content": data["translation_1"]}}]},
            "Sentence 2": {"rich_text": [{"text": {"content": data["sentence_2"]}}]},
            "Translation 2": {"rich_text": [{"text": {"content": data["translation_2"]}}]},
            "Sentence 3": {"rich_text": [{"text": {"content": data["sentence_3"]}}]},
            "Translation 3": {"rich_text": [{"text": {"content": data["translation_3"]}}]},
            "Compare Word 1": {"rich_text": [{"text": {"content": data["compare_word_1"]}}]},
            "Compare Meaning 1": {"rich_text": [{"text": {"content": data["compare_meaning_1"]}}]},
            "Compare Word 2": {"rich_text": [{"text": {"content": data["compare_word_2"]}}]},
            "Compare Meaning 2": {"rich_text": [{"text": {"content": data["compare_meaning_2"]}}]},
            "Compare Word 3": {"rich_text": [{"text": {"content": data["compare_word_3"]}}]},
            "Compare Meaning 3": {"rich_text": [{"text": {"content": data["compare_meaning_3"]}}]},
            "Rate of Usage": {"select": {"name": data["rate_of_use"]}}
        }
    }

    url = f"https://api.notion.com/v1/pages/{entry_id}"

    try:
        response = httpx.patch(url, headers=headers, json=page_data)
        response.raise_for_status()
        print(f"Notion:::Page updated: {entry_id}")
        return response.json()
    except httpx.HTTPStatusError as err:
        print(f"Notion:::HTTP error occurred: {err}")
    except Exception as err:
        print(f"Notion:::An error occurred: {err}")

    return None


if __name__ == "__main__":
    get_empty_meaning_entries()
    get_empty_illustration_entries()
    get_vocabs()