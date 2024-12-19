from notion import get_vocabs
from anki import create_anki_deck
from utils import download_image


def main() -> None:
    vocab_list: list = get_vocabs()

    # download images if image url is valid
    for vocab in vocab_list:
        if vocab['illustration_url']:
            download_image(vocab['illustration_url'], vocab['name'])

    create_anki_deck(vocab_list)


if __name__ == "__main__":
    main()