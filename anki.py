import genanki
from anki_config import FIELDS, TEMPLATES

def create_anki_deck(vocab_list: list) -> None:
    my_model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=FIELDS,
        templates=TEMPLATES
    )

    my_deck = genanki.Deck(
        2059400110,
        'Vocabulary Deck'
    )

    for vocab in vocab_list:
        my_note = genanki.Note(
            model=my_model,
            fields=[
                vocab['name'], vocab['meaning'], vocab['sentence_1'], vocab['translation_1'],
                vocab['sentence_2'], vocab['translation_2'], vocab['sentence_3'], vocab['translation_3'],
                vocab['compare_word_1'], vocab['compare_meaning_1'], vocab['compare_word_2'], vocab['compare_meaning_2'],
                vocab['compare_word_3'], vocab['compare_meaning_3'], vocab['root']
            ]
        )
        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file('output.apkg')