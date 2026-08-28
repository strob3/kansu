# run only once
# imports all n5 material only

import json
import urllib.request

from database import (
    initialize_database,
    add_kanji,
    add_vocabulary,
    add_example,
    get_all_kanji,
)


KANJI_URL = (
    "https://raw.githubusercontent.com/"
    "evanclan/OpenJLPT/main/data/json/kanji/n5.json"
)

VOCABULARY_URL = (
    "https://raw.githubusercontent.com/"
    "evanclan/OpenJLPT/main/data/json/vocab/n5.json"
)


def download_json(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()

    return json.loads(data)


def import_kanji(data):
    imported = 0

    for entry in data:
        meanings = entry.get("meanings", [])
        onyomi = entry.get("onyomi", [])
        kunyomi = entry.get("kunyomi", [])

        add_kanji(
            character=entry["character"],
            meaning=" / ".join(meanings),
            onyomi=" / ".join(onyomi),
            kunyomi=" / ".join(kunyomi),
            level=entry.get("level"),
            strokes=entry.get("strokes"),
            grade=entry.get("grade"),
        )

        imported += 1
    return imported


def build_kanji_lookup():
    kanji_rows = get_all_kanji()
    return {
        row["character"]: row["id"]
        for row in kanji_rows
    }


def find_kanji_id(word, kanji_lookup):
    """
    Finds the first kanji in a vocabulary word
    that exists in our kanji database.
    """

    for character in word:
        if character in kanji_lookup:
            return kanji_lookup[character]

    return None


def import_vocabulary(data):
    kanji_lookup = build_kanji_lookup()

    imported = 0
    example_count = 0

    for entry in data:
        word = entry["word"]
        reading = entry.get("reading", "")
        meanings = entry.get("meanings", [])

        meaning = " / ".join(meanings)

        kanji_id = find_kanji_id(
            word,
            kanji_lookup,
        )

        vocabulary_id = add_vocabulary(
            word=word,
            reading=reading,
            meaning=meaning,
            level=entry.get("level"),
            kanji_id=kanji_id,
        )

        for example in entry.get("examples", []):
            japanese = example.get("ja")
            english = example.get("en")

            if japanese and english:
                add_example(
                    vocabulary_id,
                    japanese,
                    english,
                )

                example_count += 1

        imported += 1
    return imported, example_count


def main():
    initialize_database()
    kanji_data = download_json(KANJI_URL)
    vocabulary_data = download_json(VOCABULARY_URL)

    print(f"Kanji found:       {len(kanji_data)}")
    print(f"Vocabulary found:  {len(vocabulary_data)}")
    print()

    kanji_count = import_kanji(kanji_data)

    print(f"Imported kanji:       {kanji_count}")

    vocabulary_count, example_count = import_vocabulary(
        vocabulary_data
    )

    print(f"Imported vocabulary:  {vocabulary_count}")
    print(f"Imported examples:    {example_count}")
    print()
    print("Done")


if __name__ == "__main__":
    main()