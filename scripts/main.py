import notion
import anki
import openai_utils
import utils


def fill_empty_meaning_entries() -> None:
    empty_items: list = notion.get_empty_meaning_entries()

    if empty_items:
        openai_utils.interpret_vocabulary_items(empty_items, callback=notion.update_notion_page)


def fill_empty_illustration_entries() -> None:
    result: list = notion.get_empty_illustration_entries()
    items = [{'id': result['id'],
              'name': result["properties"]["Name"]["title"][0]["text"]["content"],
              'meaning': result["properties"]["Meaning"]["rich_text"][0]["plain_text"]} for result in result["results"]]

    empty_items_without_images = [item for item in items if not utils.is_image_downloaded(item['id'])]

    if not empty_items_without_images:
        return

    openai_utils.generate_images_url(empty_items_without_images, callback=utils.download_image)


def notion_to_anki_deck() -> None:
    vocab_list: list = notion.get_vocabs()
    vocab_without_images = [vocab for vocab in vocab_list if vocab['illustration_url'] and not utils.is_image_downloaded(vocab['id'])]
    # download images if image url is valid
    for vocab in vocab_without_images:
        file_name = f'{vocab["id"]}_{vocab["name"]}'
        utils.download_image(vocab['illustration_url'], file_name)

    anki.create_anki_deck(vocab_list)


def main() -> None:
    # fill_empty_meaning_entries()
    # fill_empty_illustration_entries() /* This cost too much money */
    notion_to_anki_deck()


if __name__ == "__main__":
    main()