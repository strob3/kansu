import curses
import random

from database import get_all_kanji, get_vocabulary
from ui import continue_menu, wait_for_enter


def get_kanji_card(kanji):
    vocabulary = get_vocabulary(kanji["id"])

    return {
        "character": kanji["character"],
        "meaning": kanji["meaning"],
        "onyomi": kanji["onyomi"],
        "kunyomi": kanji["kunyomi"],
        "vocabulary": vocabulary,
    }


def display_kanji(stdscr, kanji):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    title = "study"
    stdscr.addstr(1, max(0, (width - len(title)) // 2), title, curses.A_BOLD)

    character = kanji["character"]
    stdscr.addstr(4, max(0, (width - 1) // 2), character, curses.A_BOLD)

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

    stdscr.addstr(height - 2, 2, "press ENTER to continue")
    stdscr.refresh()


def study_mode(stdscr):
    kanji_list = get_all_kanji()

    if not kanji_list:
        return

    while True:
        kanji = random.choice(kanji_list)
        display_kanji(stdscr, get_kanji_card(kanji))
        wait_for_enter(stdscr)

        if continue_menu(stdscr) == 1:
            return