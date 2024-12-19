from notion import get_vocabs
from anki import create_anki_deck

if __name__ == "__main__":
    vocab_list: list = get_vocabs()
    create_anki_deck(vocab_list)