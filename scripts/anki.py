import genanki
from anki_config import FIELDS, TEMPLATES
from config_loader import config_loader
import utils
import yaml


with open('config.yaml') as f:
    config = yaml.safe_load(f)

DECK_NAME = config_loader.anki.output_deck_name
PACKAGE_NAME = f'{config_loader.output_dir}\\{config_loader.anki.output_package_name}.apkg'

# Define the model so we can use a custom guid
class VocabularyNode(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[0])

def create_anki_deck(vocab_list: list) -> None:
    my_model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=FIELDS,
        templates=TEMPLATES
    )

    my_deck = genanki.Deck(
        2059400110,
        DECK_NAME
    )

    media_file_paths = []
    for vocab in vocab_list:
        img_src = utils.get_image_url(vocab['id'])

        anki_fields =[
            vocab['id'],
            vocab['name'], vocab['meaning'], vocab['sentence_1'], vocab['translation_1'],
            vocab['sentence_2'], vocab['translation_2'], vocab['sentence_3'], vocab['translation_3'],
            vocab['compare_word_1'], vocab['compare_meaning_1'], vocab['compare_word_2'], vocab['compare_meaning_2'],
            vocab['compare_word_3'], vocab['compare_meaning_3'], vocab['root'], f"<img src='{img_src}'>",
            str(vocab['rate_of_use'])
        ]

        print(f"Anki:::Creating note for {vocab['name']}")

        if img_src:
            media_file_paths.append(utils.get_absolute_image_url(vocab['id']))

        my_note = VocabularyNode(
            model=my_model,
            fields=anki_fields
        )
        my_deck.add_note(my_note)

    package = genanki.Package(my_deck)
    package.media_files = media_file_paths
    package.write_to_file(PACKAGE_NAME)

    print(f"Anki deck '{DECK_NAME}' has been exported to '{PACKAGE_NAME}'")


if __name__ == '__main__':
    print(PACKAGE_NAME)