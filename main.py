import curses

from database import initialize_database
from quiz import quiz_mode
from study import study_mode
from ui import navigation_menu


def application(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(False)

    while True:
        selection = navigation_menu(stdscr)

        if selection == 0:
            study_mode(stdscr)

        elif selection == 1:
            quiz_mode(stdscr)
            
        elif selection == 2:
            break


def main():
    initialize_database()
    curses.wrapper(application)


if __name__ == "__main__":
    main()