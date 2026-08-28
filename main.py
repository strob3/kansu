kanji = {
    "character": "日",
    "meaning": "day / sun",
    "onyomi": "ニチ / ジツ",
    "kunyomi": "ひ / か",
    "vocabulary": [
        {
            "word": "日本",
            "reading": "にほん",
            "meaning": "Japan",
        },
        {
            "word": "今日",
            "reading": "きょう",
            "meaning": "today",
        },
    ],
}


def show_kanji():
    print("\n" + "=" * 40)
    print("              KANJI STUDY")
    print("=" * 40)

    print(f"\nKanji:\n\n        {kanji['character']}")

    print(f"\nMeaning:\n{kanji['meaning']}")

    print(f"\nOn'yomi:\n{kanji['onyomi']}")

    print(f"\nKun'yomi:\n{kanji['kunyomi']}")

    print("\nVocabulary:")

    for word in kanji["vocabulary"]:
        print(f"\n{word['word']}")
        print(f"{word['reading']}")
        print(f"{word['meaning']}")

    input("\nPress ENTER to continue...")


def quiz():
    print("\n" + "=" * 40)
    print("                 QUIZ")
    print("=" * 40)

    print(f"\nWhat does {kanji['character']} mean?")

    answer = input("> ").strip().lower()

    correct_answers = [
        "day",
        "sun",
        "day / sun",
    ]

    if answer in correct_answers:
        print("\n✓ Correct!")
    else:
        print(f"\n✗ Incorrect.")
        print(f"The answer is: {kanji['meaning']}")

    input("\nPress ENTER to continue...")


def main():
    while True:
        print("\n" + "=" * 40)
        print("              KANJI STUDY")
        print("=" * 40)

        print("\n1. Study")
        print("2. Quiz")
        print("3. Quit")

        choice = input("\n> ").strip()

        if choice == "1":
            show_kanji()

        elif choice == "2":
            quiz()

        elif choice == "3":
            print("\nGoodbye.")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()