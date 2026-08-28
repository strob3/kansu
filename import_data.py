# run only once
# imports kanji material 

import json
import sys
import urllib.request

from database import (
    initialize_database,
    add_kanji,
    add_vocabulary,
    add_example,
    get_all_kanji,
)


BASE_URL = "https://raw.githubusercontent.com/evanclan/OpenJLPT/main/data/json"


def download_json(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


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

        vocabulary_id = add_vocabulary(
            word=word,
            reading=reading,
            meaning=" / ".join(meanings),
            level=entry.get("level"),
            kanji_id=find_kanji_id(word, kanji_lookup),
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
    level = sys.argv[1].lower() if len(sys.argv) > 1 else "n5"

    if level not in ("n5", "n4"):
        print("usage: python import_data.py [n5|n4]")
        return

    initialize_database()

    kanji_url = f"{BASE_URL}/kanji/{level}.json"
    vocabulary_url = f"{BASE_URL}/vocab/{level}.json"

    print(f"Importing {level.upper()}...")
    print()

    kanji_data = download_json(kanji_url)
    vocabulary_data = download_json(vocabulary_url)

    print(f"kanji found:       {len(kanji_data)}")
    print(f"vocabulary found:  {len(vocabulary_data)}")
    print()

    kanji_count = import_kanji(kanji_data)

    print(f"imported kanji:       {kanji_count}")

    vocabulary_count, example_count = import_vocabulary(
        vocabulary_data
    )

    print(f"imported vocabulary:  {vocabulary_count}")
    print(f"imported examples:    {example_count}")
    print()
    print("done")


if __name__ == "__main__":
    main()