import curses
import random

from database import (
    initialize_database,
    get_all_kanji,
    get_vocabulary,
)


def draw_menu(stdscr, selected):
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    title = "KANJI STUDY"
    options = [
        "Study",
        "Quiz",
        "Quit",
    ]

    # Title
    stdscr.addstr(
        2,
        max(0, (width - len(title)) // 2),
        title,
        curses.A_BOLD,
    )

    # Menu
    start_y = 5

    for index, option in enumerate(options):
        prefix = "> " if index == selected else "  "

        if index == selected:
            stdscr.addstr(
                start_y + index,
                max(0, (width - len(option) - 2) // 2),
                prefix + option,
                curses.A_REVERSE,
            )
        else:
            stdscr.addstr(
                start_y + index,
                max(0, (width - len(option) - 2) // 2),
                prefix + option,
            )

    stdscr.addstr(
        height - 2,
        2,
        "↑/↓ Navigate    ENTER Select",
    )

    stdscr.refresh()


def navigation_menu(stdscr):
    selected = 0

    while True:
        draw_menu(stdscr, selected)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % 3

        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % 3

        elif key in (curses.KEY_ENTER, 10, 13):
            return selected


def draw_continue_menu(stdscr, selected):
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    options = [
        "Continue",
        "Back to menu",
    ]

    title = "What next?"

    stdscr.addstr(
        2,
        max(0, (width - len(title)) // 2),
        title,
        curses.A_BOLD,
    )

    start_y = 5

    for index, option in enumerate(options):
        prefix = "> " if index == selected else "  "

        if index == selected:
            stdscr.addstr(
                start_y + index,
                max(0, (width - len(option) - 2) // 2),
                prefix + option,
                curses.A_REVERSE,
            )
        else:
            stdscr.addstr(
                start_y + index,
                max(0, (width - len(option) - 2) // 2),
                prefix + option,
            )

    stdscr.addstr(
        height - 2,
        2,
        "↑/↓ Navigate    ENTER Select",
    )

    stdscr.refresh()


def continue_menu(stdscr, message=None):
    selected = 0

    while True:
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        if message:
            stdscr.addstr(
                3,
                max(0, (width - len(message)) // 2),
                message,
                curses.A_BOLD,
            )

        title = "What next?"

        stdscr.addstr(
            6,
            max(0, (width - len(title)) // 2),
            title,
            curses.A_BOLD,
        )

        options = [
            "Continue",
            "Back to menu",
        ]

        start_y = 9

        for index, option in enumerate(options):
            prefix = "> " if index == selected else "  "

            if index == selected:
                stdscr.addstr(
                    start_y + index,
                    max(0, (width - len(option) - 2) // 2),
                    prefix + option,
                    curses.A_REVERSE,
                )
            else:
                stdscr.addstr(
                    start_y + index,
                    max(0, (width - len(option) - 2) // 2),
                    prefix + option,
                )

        stdscr.addstr(
            height - 2,
            2,
            "↑/↓ Navigate    ENTER Select",
        )

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % 2

        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % 2

        elif key in (curses.KEY_ENTER, 10, 13):
            return selected


def display_kanji(stdscr, kanji):
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    title = "KANJI STUDY"

    stdscr.addstr(
        1,
        max(0, (width - len(title)) // 2),
        title,
        curses.A_BOLD,
    )

    character = kanji["character"]

    stdscr.addstr(
        4,
        max(0, (width - 1) // 2),
        character,
        curses.A_BOLD,
    )

    y = 7

    stdscr.addstr(y, 4, "Meaning:")
    stdscr.addstr(y + 1, 6, kanji["meaning"])

    stdscr.addstr(y + 3, 4, "On'yomi:")
    stdscr.addstr(y + 4, 6, kanji["onyomi"] or "-")

    stdscr.addstr(y + 6, 4, "Kun'yomi:")
    stdscr.addstr(y + 7, 6, kanji["kunyomi"] or "-")

    y += 10

    stdscr.addstr(y, 4, "Vocabulary:", curses.A_BOLD)

    y += 2

    for word in kanji["vocabulary"]:
        if y + 3 >= height - 2:
            break

        stdscr.addstr(y, 6, word["word"])
        stdscr.addstr(y + 1, 8, word["reading"])
        stdscr.addstr(y + 2, 8, word["meaning"])

        y += 4

    stdscr.addstr(
        height - 2,
        2,
        "Press ENTER to continue",
    )

    stdscr.refresh()


def get_kanji_card(kanji):
    vocabulary = get_vocabulary(kanji["id"])

    return {
        "character": kanji["character"],
        "meaning": kanji["meaning"],
        "onyomi": kanji["onyomi"],
        "kunyomi": kanji["kunyomi"],
        "vocabulary": [
            {
                "word": word["word"],
                "reading": word["reading"],
                "meaning": word["meaning"],
            }
            for word in vocabulary
        ],
    }


def study_mode(stdscr):
    kanji_list = get_all_kanji()

    if not kanji_list:
        return

    while True:
        kanji = random.choice(kanji_list)
        kanji_card = get_kanji_card(kanji)

        display_kanji(stdscr, kanji_card)

        key = stdscr.getch()

        if key not in (curses.KEY_ENTER, 10, 13):
            continue

        choice = continue_menu(stdscr)

        if choice == 0:
            continue

        elif choice == 1:
            return


def display_quiz(stdscr, kanji):
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    title = "QUIZ"

    stdscr.addstr(
        2,
        max(0, (width - len(title)) // 2),
        title,
        curses.A_BOLD,
    )

    question = f"What does {kanji['character']} mean?"

    stdscr.addstr(
        6,
        max(0, (width - len(question)) // 2),
        question,
    )

    stdscr.addstr(
        8,
        4,
        "Type your answer:",
    )

    stdscr.refresh()

    curses.echo()

    answer = stdscr.getstr(
        10,
        4,
        40,
    ).decode("utf-8").strip().lower()

    curses.noecho()

    correct_answers = kanji["meaning"].lower().split(" / ")

    if answer in correct_answers:
        result = "✓ Correct!"
    else:
        result = f"✗ Incorrect. Answer: {kanji['meaning']}"

    stdscr.addstr(
        13,
        4,
        result,
        curses.A_BOLD,
    )

    stdscr.refresh()

    return result


def quiz_mode(stdscr):
    kanji_list = get_all_kanji()

    if not kanji_list:
        return

    while True:
        kanji = random.choice(kanji_list)

        quiz_data = {
            "character": kanji["character"],
            "meaning": kanji["meaning"],
        }

        result = display_quiz(stdscr, quiz_data)

        choice = continue_menu(stdscr, result)

        if choice == 0:
            continue

        elif choice == 1:
            return


def application(stdscr):
    curses.curs_set(0)

    while True:
        selection = navigation_menu(stdscr)

        if selection == 0:
            study_mode(stdscr)

        elif selection == 1:
            quiz_mode(stdscr)

        elif selection == 2:
            break


if __name__ == "__main__":
    initialize_database()

    curses.wrapper(application)