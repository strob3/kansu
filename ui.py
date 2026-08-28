import curses


def is_enter(key):
    return key in (10, 13)

def is_up(key):
    return key == curses.KEY_UP

def is_down(key):
    return key == curses.KEY_DOWN

def is_escape(key):
    return key == 27

def is_quit(key):
    return key in (ord("q"), ord("Q"))


def menu(stdscr, title, options):
    selected = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(2, max(0, (width - len(title)) // 2), title, curses.A_BOLD)

        for i, option in enumerate(options):
            text = ("> " if i == selected else "  ") + option
            x = max(0, (width - len(text)) // 2)

            attr = curses.A_REVERSE if i == selected else curses.A_NORMAL
            stdscr.addstr(5 + i, x, text, attr)

        stdscr.addstr(height - 2, 2, "↑/↓ navigate    ENTER select    Q quit")
        stdscr.refresh()

        key = stdscr.getch()

        if is_up(key):
            selected = (selected - 1) % len(options)

        elif is_down(key):
            selected = (selected + 1) % len(options)

        elif is_enter(key):
            return selected
        
        elif is_quit(key):
            return len(options) - 1


def navigation_menu(stdscr):
    return menu(stdscr, "kansu", ["study", "quiz", "quit"])


def continue_menu(stdscr, message=None):
    return menu(stdscr, message or "what next?", ["continue", "back to menu"])


def get_text_input(stdscr, y, x, max_length=40):
    curses.echo()

    try:
        value = stdscr.getstr(y, x, max_length)

    finally:
        curses.noecho()

    return value.decode("utf-8", errors="replace").strip()


def wait_for_enter(stdscr):
    while True:
        key = stdscr.getch()
        
        if is_enter(key):
            return