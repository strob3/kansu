import curses
import random

from database import get_all_kanji
from ui import continue_menu, get_text_input


def display_quiz(stdscr, kanji):
    stdscr.clear()
    _, width = stdscr.getmaxyx()

    title = "quiz"
    stdscr.addstr(2, max(0, (width - len(title)) // 2), title, curses.A_BOLD)

    question = f"What does {kanji['character']} mean?"
    stdscr.addstr(6, max(0, (width - len(question)) // 2), question)
    stdscr.addstr(8, 4, "answer:")
    stdscr.refresh()

    return get_text_input(stdscr, 10, 4)


def quiz_mode(stdscr):
    kanji_list = get_all_kanji()

    if not kanji_list:
        return

    while True:
        kanji = random.choice(kanji_list)
        answer = display_quiz(stdscr, kanji)

        correct_answers = [
            meaning.strip().lower()
            for meaning in kanji["meaning"].split("/")
        ]

        result = "✓" if answer.lower() in correct_answers else f"✗ answer: {kanji['meaning']}"

        if continue_menu(stdscr, result) == 1:
            return