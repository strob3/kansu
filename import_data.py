import json
import urllib.request

from database import (
    initialize_database,
    add_kanji,
)


KANJI_URL = (
    "https://raw.githubusercontent.com/"
    "evanclan/OpenJLPT/main/data/json/kanji/n5.json"
)


def download_kanji_data():
    print("Downloading N5 kanji data...")

    with urllib.request.urlopen(KANJI_URL) as response:
        data = response.read()

    return json.loads(data)


def import_kanji(data):
    imported = 0

    for entry in data:
        meanings = entry.get("meanings", [])

        onyomi = entry.get("onyomi", [])
        kunyomi = entry.get("kunyomi", [])

        meaning = " / ".join(meanings)
        onyomi_text = " / ".join(onyomi)
        kunyomi_text = " / ".join(kunyomi)

        add_kanji(
            character=entry["character"],
            meaning=meaning,
            onyomi=onyomi_text,
            kunyomi=kunyomi_text,
            level=entry.get("level"),
            strokes=entry.get("strokes"),
            grade=entry.get("grade"),
        )

        imported += 1

    return imported


def main():
    initialize_database()

    data = download_kanji_data()

    print(f"Found {len(data)} N5 kanji.")

    imported = import_kanji(data)

    print(f"Imported {imported} kanji.")
    print("Import complete.")


if __name__ == "__main__":
    main()