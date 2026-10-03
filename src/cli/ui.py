# main ui application 

from typing import List, Optional
import re

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Container, Horizontal, Middle, Vertical
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Static

try:
    import database
    from kanji_renderer import render_braille, render_halfblock
    from quiz_engine import check_answer, choose_next_quiz_kanji, get_quiz_candidates
    import srs
except ImportError:
    from . import database, srs
    from .kanji_renderer import render_braille, render_halfblock
    from .quiz_engine import check_answer, choose_next_quiz_kanji, get_quiz_candidates


KANSU_CSS = """
Screen {
    background: #09090b;
    color: #f8fafc;
}

KansuHeader {
    dock: top;
    height: 0;
    width: 100%;
    display: none;
}

#header-title {
    width: auto;
    padding-left: 1;
}

#header-shortcuts {
    width: 1fr;
    text-align: right;
    padding-right: 1;
}

#menu-shortcuts {
    width: 100%;
    text-align: center;
    color: #94a3b8;
    margin-top: 1;
}

#app-container {
    width: 100%;
    height: 1fr;
    align: center middle;
    overflow-y: auto;
}

.card-panel {
    width: 86;
    max-width: 96%;
    height: auto;
    border: round #272732;
    background: #121217;
    padding: 1 2;
    align: center middle;
}

.title-text {
    text-align: center;
    text-style: bold;
    color: #818cf8;
    margin-bottom: 1;
}

.subtitle-text {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 1;
}

.big-kanji {
    text-align: center;
    color: #f8fafc;
    text-style: bold;
    margin: 1 0;
    min-height: 9;
}

.meaning-text {
    text-align: center;
    text-style: bold;
    color: #f8fafc;
    margin-top: 1;
}

.meta-text {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 1;
}

.vocab-section {
    border-top: solid #272732;
    padding-top: 1;
    margin-top: 1;
    width: 100%;
}

.vocab-item {
    color: #f8fafc;
    margin-bottom: 0;
}

.vocab-reading {
    color: #06b6d4;
}

.vocab-meaning {
    color: #94a3b8;
}

.menu-button {
    width: 34;
    height: 1;
    min-height: 1;
    margin-bottom: 0;
    padding: 0 1;
    border: none;
    background: #1c1c24;
    color: #f8fafc;
}

.menu-button:hover, .menu-button:focus {
    background: #262633;
    color: #818cf8;
    text-style: bold;
}

.menu-options {
    margin: 0;
    align: center middle;
    width: 100%;
    height: auto;
}

#quiz-input {
    width: 48;
    margin: 1 0;
    border: round #272732;
    background: #09090b;
    color: #f8fafc;
    text-align: center;
}

#quiz-input:focus {
    border: round #6366f1;
}

.correct-badge {
    text-align: center;
    color: #10b981;
    text-style: bold;
    margin-bottom: 1;
}

.incorrect-badge {
    text-align: center;
    color: #f43f5e;
    text-style: bold;
    margin-bottom: 1;
}

.rating-row {
    margin-top: 1;
    align: center middle;
    width: 100%;
    height: auto;
}

.rating-btn {
    min-width: 12;
    height: 1;
    min-height: 1;
    margin: 0 1;
    padding: 0 1;
    border: none;
    background: #1c1c24;
}

.rating-btn:hover, .rating-btn:focus {
    background: #262633;
    text-style: bold;
}

.rating-btn-1 {
    color: #f43f5e;
}

.rating-btn-2 {
    color: #f59e0b;
}

.rating-btn-3 {
    color: #10b981;
}

.rating-btn-4 {
    color: #06b6d4;
}

.stat-row {
    width: 40;
    height: 1;
    margin-bottom: 1;
}

.stat-label {
    width: 24;
    color: #94a3b8;
}

.stat-val {
    width: 16;
    text-align: right;
    text-style: bold;
    color: #818cf8;
}

.section-label {
    color: #94a3b8;
    text-style: bold;
    margin-top: 1;
    margin-bottom: 0;
    width: 100%;
    text-align: center;
}

.btn-row {
    height: 1;
    width: 100%;
    align: center middle;
    margin-bottom: 0;
}

.opt-btn {
    min-width: 1;
    width: auto;
    height: 1;
    min-height: 1;
    margin: 0 1;
    padding: 0 1;
    border: none;
    background: #1c1c24;
    color: #94a3b8;
}

.opt-btn:hover, .opt-btn:focus {
    background: #262633;
    color: #f8fafc;
}

.opt-btn.active {
    background: #818cf8;
    color: #09090b;
    text-style: bold;
}
"""


class KansuHeader(Widget):
    """Top bar widget."""

    DEFAULT_CSS = """
    KansuHeader {
        dock: top;
        height: 0;
        width: 100%;
        display: none;
    }
    """

    def __init__(self, shortcuts: str = "", id: Optional[str] = None):
        super().__init__(id=id)
        self.shortcuts = shortcuts

    def compose(self) -> ComposeResult:
        yield Label("", id="header-title")
        yield Label("", id="header-shortcuts")

    def update_shortcuts(self, text: str) -> None:
        self.shortcuts = text
        try:
            lbl = self.query_one("#header-shortcuts", Label)
            lbl.update(text)
        except Exception:
            pass


class MenuScreen(Screen):
    """Main menu navigation screen."""

    BINDINGS = [
        Binding("up", "nav_up", "Up", show=False),
        Binding("k", "nav_up", "Up", show=False),
        Binding("down", "nav_down", "Down", show=False),
        Binding("j", "nav_down", "Down", show=False),
        Binding("1", "select_study", "Study", show=False),
        Binding("2", "select_quiz", "Quiz", show=False),
        Binding("3", "select_review", "Review", show=False),
        Binding("4", "select_settings", "Settings", show=False),
        Binding("5", "quit_app", "Quit", show=False),
        Binding("q", "quit_app", "Quit", show=False),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="app-container"):
            with Vertical(classes="card-panel"):
                yield Label("kansu  |  カンス", classes="title-text")
                yield Label(
                    f"[ {self.app.current_level} ]",
                    markup=False,
                    classes="subtitle-text",
                    id="menu-deck-label",
                )
                with Vertical(classes="menu-options"):
                    yield Button("1. Study Kanji Cards", id="btn-study", classes="menu-button")
                    yield Button("2. Quiz (Active Recall)", id="btn-quiz", classes="menu-button")
                    yield Button("3. Review Statistics", id="btn-review", classes="menu-button")
                    yield Button("4. Settings", id="btn-settings", classes="menu-button")
                    yield Button("5. Quit Kansu", id="btn-quit", classes="menu-button")
                yield Label(
                    "[#818cf8]↑ / ↓[/#818cf8] [dim]navigate[/dim]  •  [#818cf8]enter[/#818cf8] [dim]select[/dim]  •  [#818cf8]1-5[/#818cf8] [dim]jump[/dim]  •  [#818cf8]q[/#818cf8] [dim]quit[/dim]",
                    id="menu-shortcuts",
                )

    def on_mount(self) -> None:
        self.query_one("#btn-study", Button).focus()

    def on_screen_resume(self) -> None:
        try:
            self.query_one("#menu-deck-label", Label).update(f"[ {self.app.current_level} ]")
        except Exception:
            pass

    def action_nav_down(self) -> None:
        buttons = [
            self.query_one("#btn-study", Button),
            self.query_one("#btn-quiz", Button),
            self.query_one("#btn-review", Button),
            self.query_one("#btn-settings", Button),
            self.query_one("#btn-quit", Button),
        ]
        current = self.focused
        if current in buttons:
            idx = buttons.index(current)
            buttons[(idx + 1) % len(buttons)].focus()
        else:
            buttons[0].focus()

    def action_nav_up(self) -> None:
        buttons = [
            self.query_one("#btn-study", Button),
            self.query_one("#btn-quiz", Button),
            self.query_one("#btn-review", Button),
            self.query_one("#btn-settings", Button),
            self.query_one("#btn-quit", Button),
        ]
        current = self.focused
        if current in buttons:
            idx = buttons.index(current)
            buttons[(idx - 1) % len(buttons)].focus()
        else:
            buttons[-1].focus()

    def on_screen_resume(self) -> None:
        deck_label = self.query_one("#menu-deck-label", Label)
        deck_label.update(f"[ {self.app.current_level} ]")
        buttons = [
            self.query_one("#btn-study", Button),
            self.query_one("#btn-quiz", Button),
            self.query_one("#btn-review", Button),
            self.query_one("#btn-settings", Button),
            self.query_one("#btn-quit", Button),
        ]
        if self.focused not in buttons:
            buttons[0].focus()

    @on(Button.Pressed, "#btn-study")
    def action_select_study(self) -> None:
        self.app.push_screen(StudyScreen())

    @on(Button.Pressed, "#btn-quiz")
    def action_select_quiz(self) -> None:
        self.app.push_screen(QuizScreen())

    @on(Button.Pressed, "#btn-review")
    def action_select_review(self) -> None:
        self.app.push_screen(ReviewScreen())

    @on(Button.Pressed, "#btn-settings")
    def action_select_settings(self) -> None:
        self.app.push_screen(SettingsScreen())

    @on(Button.Pressed, "#btn-quit")
    def action_quit_app(self) -> None:
        self.app.exit()


class StudyScreen(Screen):
    """Card study screen with big kanji, readings, and vocabulary."""

    BINDINGS = [
        Binding("left", "prev_card", "Previous", show=True),
        Binding("h", "prev_card", "Previous", show=False),
        Binding("p", "prev_card", "Previous", show=False),
        Binding("right", "next_card", "Next", show=True),
        Binding("l", "next_card", "Next", show=False),
        Binding("n", "next_card", "Next", show=False),
        Binding("space", "next_card", "Next", show=False),
        Binding("escape", "back_to_menu", "Menu", show=True),
        Binding("backspace", "back_to_menu", "Menu", show=False),
        Binding("q", "back_to_menu", "Menu", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.kanji_list: List[dict] = []
        self.current_index: int = 0

    def compose(self) -> ComposeResult:
        yield KansuHeader(
            "[#818cf8]← / →[/#818cf8] [dim]cards[/dim]  •  [#818cf8]space[/#818cf8] [dim]next[/dim]  •  [#818cf8]esc[/#818cf8] [dim]menu[/dim]"
        )
        with Container(id="app-container"):
            with Vertical(classes="card-panel"):
                yield Label("STUDY", classes="title-text", id="study-header")
                yield Static("", id="study-kanji", classes="big-kanji")
                yield Label("", id="study-meaning", classes="meaning-text")
                yield Label("", id="study-readings", classes="meta-text")
                yield Label("", id="study-meta", classes="meta-text")
                with Vertical(classes="vocab-section", id="study-vocab-box"):
                    yield Label("Vocabulary Examples:", classes="meta-text")
                    yield Static("", id="study-vocab-list")

    def on_mount(self) -> None:
        self.kanji_list = database.get_kanji_by_level(self.app.current_level)
        self.current_index = 0
        if not self.kanji_list:
            self.query_one("#study-header", Label).update("No Kanji Found")
            self.query_one("#study-kanji", Static).update("No cards in deck")
            return
        self.update_card()

    def update_card(self) -> None:
        if not self.kanji_list:
            return

        kanji = dict(self.kanji_list[self.current_index])
        vocab = database.get_vocabulary(kanji["id"])

        rendered_glyph = self.app.render_kanji(kanji["character"])
        self.query_one("#study-header", Label).update(
            f"STUDY  •  Card {self.current_index + 1} of {len(self.kanji_list)}  [ {self.app.current_level} ]"
        )
        self.query_one("#study-kanji", Static).update(rendered_glyph)
        self.query_one("#study-meaning", Label).update(kanji["meaning"])

        onyomi = kanji.get("onyomi") or "-"
        kunyomi = kanji.get("kunyomi") or "-"
        self.query_one("#study-readings", Label).update(f"On'yomi: {onyomi}    Kun'yomi: {kunyomi}")

        strokes = f"Strokes: {kanji['strokes']}" if kanji.get("strokes") else ""
        freq = f"Frequency: #{kanji['frequency']}" if kanji.get("frequency") else ""
        meta_str = "    ".join(filter(None, [strokes, freq]))
        self.query_one("#study-meta", Label).update(meta_str)

        if vocab:
            vocab_lines = []
            for v_row in vocab[:4]:
                v = dict(v_row)
                word = v.get("word", "")
                reading = f"({v['reading']})" if v.get("reading") else ""
                meaning = v.get("meaning", "")
                vocab_lines.append(f"• [bold #818cf8]{word}[/bold #818cf8] [cyan]{reading}[/cyan]  [#94a3b8]{meaning}[/#94a3b8]")
            self.query_one("#study-vocab-list", Static).update("\n".join(vocab_lines))
        else:
            self.query_one("#study-vocab-list", Static).update("No vocabulary entries.")

    def action_next_card(self) -> None:
        if not self.kanji_list:
            return
        self.current_index = (self.current_index + 1) % len(self.kanji_list)
        self.update_card()

    def action_prev_card(self) -> None:
        if not self.kanji_list:
            return
        self.current_index = (self.current_index - 1) % len(self.kanji_list)
        self.update_card()

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()


class QuizScreen(Screen):
    """Quiz screen with big kanji prompt, typing input, and FSRS rating phase."""

    BINDINGS = [
        Binding("escape", "back_to_menu", "Menu", show=True),
        Binding("1", "rate_1", "Again", show=False),
        Binding("2", "rate_2", "Hard", show=False),
        Binding("3", "rate_3", "Good", show=False),
        Binding("4", "rate_4", "Easy", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.phase: str = "question"  # 'question' or 'result'
        self.current_kanji: Optional[dict] = None
        self.last_kanji_id: Optional[int] = None
        self.is_correct: bool = False
        self.user_answer: str = ""
        self.expected_meanings: List[str] = []

    def compose(self) -> ComposeResult:
        yield KansuHeader(
            "[#818cf8]enter[/#818cf8] [dim]submit[/dim]  •  [#818cf8]esc[/#818cf8] [dim]menu[/dim]",
            id="quiz-header-bar",
        )
        with Container(id="app-container"):
            with Vertical(classes="card-panel"):
                yield Label("QUIZ", classes="title-text", id="quiz-header")
                yield Label("", classes="subtitle-text", id="quiz-stats")
                yield Static("", id="quiz-kanji", classes="big-kanji")
                yield Label("what does this mean?", classes="subtitle-text", id="quiz-prompt")
                yield Input(placeholder="Type English meaning and press Enter...", id="quiz-input")

                with Vertical(id="quiz-result-box"):
                    yield Label("", id="quiz-result-badge")
                    yield Label("", id="quiz-user-answer", classes="meaning-text")
                    yield Label("", id="quiz-expected-answer", classes="meta-text")
                    yield Label("Rate retention to schedule next review:", classes="subtitle-text")
                    with Horizontal(classes="rating-row"):
                        yield Button("[1] Again", id="rate-1", classes="rating-btn rating-btn-1")
                        yield Button("[2] Hard", id="rate-2", classes="rating-btn rating-btn-2")
                        yield Button("[3] Good", id="rate-3", classes="rating-btn rating-btn-3")
                        yield Button("[4] Easy", id="rate-4", classes="rating-btn rating-btn-4")

    def on_mount(self) -> None:
        self.next_question()

    def next_question(self) -> None:
        kanji, counts = choose_next_quiz_kanji(
            level=self.app.current_level,
            mode="all",
            previous_id=self.last_kanji_id,
        )
        hdr = self.query_one("#quiz-header-bar", KansuHeader)
        if not kanji:
            self.phase = "empty"
            self.query_one("#quiz-header", Label).update("Quiz Complete")
            self.query_one("#quiz-kanji", Static).update("No due cards.")
            self.query_one("#quiz-prompt", Label).update("Check back later or choose another level in Settings.")
            self.query_one("#quiz-input", Input).display = False
            self.query_one("#quiz-result-box", Vertical).display = False
            if hdr:
                hdr.update_shortcuts("[#818cf8]esc[/#818cf8] [dim]menu[/dim]")
            return

        self.current_kanji = kanji
        self.last_kanji_id = kanji["id"]
        self.phase = "question"

        self.query_one("#quiz-stats", Label).update(
            f"[ {self.app.current_level} ]  •  Due: {counts['due']}  |  New: {counts['new']}  |  Learning: {counts['learning']}"
        )

        rendered_glyph = self.app.render_kanji(kanji["character"])
        self.query_one("#quiz-kanji", Static).update(rendered_glyph)
        self.query_one("#quiz-prompt", Label).update("what does this mean?")

        inp = self.query_one("#quiz-input", Input)
        inp.value = ""
        inp.display = True
        inp.focus()

        self.query_one("#quiz-result-box", Vertical).display = False

        if hdr:
            hdr.update_shortcuts("[#818cf8]enter[/#818cf8] [dim]submit[/dim]  •  [#818cf8]esc[/#818cf8] [dim]menu[/dim]")

    @on(Input.Submitted, "#quiz-input")
    def handle_submit(self, event: Input.Submitted) -> None:
        self.submit_answer(event.value)

    def submit_answer(self, answer: str) -> None:
        if self.phase != "question" or not self.current_kanji:
            return

        clean_answer = answer.strip()
        correct, meanings = check_answer(clean_answer, self.current_kanji["meaning"])
        self.is_correct = correct
        self.user_answer = clean_answer or "(no answer)"
        self.expected_meanings = meanings
        self.phase = "result"

        self.query_one("#quiz-input", Input).display = False
        result_box = self.query_one("#quiz-result-box", Vertical)
        result_box.display = True

        badge = self.query_one("#quiz-result-badge", Label)
        if correct:
            badge.update("✓  CORRECT!")
            badge.remove_class("incorrect-badge")
            badge.add_class("correct-badge")
        else:
            badge.update("✗  INCORRECT")
            badge.remove_class("correct-badge")
            badge.add_class("incorrect-badge")

        self.query_one("#quiz-user-answer", Label).update(f"Your answer: {self.user_answer}")
        self.query_one("#quiz-expected-answer", Label).update(f"Accepted: {', '.join(meanings)}")
        self.query_one("#rate-3", Button).focus()

        hdr = self.query_one("#quiz-header-bar", KansuHeader)
        if hdr:
            hdr.update_shortcuts(
                "[#f43f5e]1[/#f43f5e] [dim]again[/dim]  [#f59e0b]2[/#f59e0b] [dim]hard[/dim]  [#10b981]3[/#10b981] [dim]good[/dim]  [#06b6d4]4[/#06b6d4] [dim]easy[/dim]  •  [#818cf8]esc[/#818cf8] [dim]menu[/dim]"
            )

    def apply_rating(self, rating: int) -> None:
        if self.phase != "result" or not self.current_kanji:
            return

        srs.review_card("kanji", self.current_kanji["id"], rating)
        self.next_question()

    @on(Button.Pressed, "#rate-1")
    def handle_btn_rate_1(self) -> None:
        self.apply_rating(1)

    @on(Button.Pressed, "#rate-2")
    def handle_btn_rate_2(self) -> None:
        self.apply_rating(2)

    @on(Button.Pressed, "#rate-3")
    def handle_btn_rate_3(self) -> None:
        self.apply_rating(3)

    @on(Button.Pressed, "#rate-4")
    def handle_btn_rate_4(self) -> None:
        self.apply_rating(4)

    def action_rate_1(self) -> None:
        if self.phase == "result":
            self.apply_rating(1)

    def action_rate_2(self) -> None:
        if self.phase == "result":
            self.apply_rating(2)

    def action_rate_3(self) -> None:
        if self.phase == "result":
            self.apply_rating(3)

    def action_rate_4(self) -> None:
        if self.phase == "result":
            self.apply_rating(4)

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()


class ReviewScreen(Screen):
    """SRS review stats screen."""

    BINDINGS = [
        Binding("escape", "back_to_menu", "Menu", show=True),
        Binding("backspace", "back_to_menu", "Menu", show=False),
        Binding("q", "back_to_menu", "Menu", show=False),
        Binding("enter", "back_to_menu", "Menu", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield KansuHeader("[#818cf8]esc / enter / q[/#818cf8] [dim]menu[/dim]")
        with Container(id="app-container"):
            with Vertical(classes="card-panel"):
                yield Label("REVIEW STATISTICS", classes="title-text")
                yield Label("Spaced Repetition (FSRS) Status", classes="subtitle-text", id="rev-sub")
                yield Static("", classes="meta-text")
                with Vertical(classes="rating-row"):
                    with Horizontal(classes="stat-row"):
                        yield Label("Due for Review:", classes="stat-label")
                        yield Label("0", id="stat-due", classes="stat-val")
                    with Horizontal(classes="stat-row"):
                        yield Label("New (Unlearned):", classes="stat-label")
                        yield Label("0", id="stat-new", classes="stat-val")
                    with Horizontal(classes="stat-row"):
                        yield Label("Learning / Retained:", classes="stat-label")
                        yield Label("0", id="stat-learning", classes="stat-val")
                    with Horizontal(classes="stat-row"):
                        yield Label("Total Kanji:", classes="stat-label")
                        yield Label("0", id="stat-total", classes="stat-val")
                yield Static("", classes="meta-text")
                yield Button("Return to Menu (Esc)", id="btn-rev-back", classes="menu-button")

    def on_mount(self) -> None:
        _, counts = get_quiz_candidates(self.app.current_level, mode="all")
        self.query_one("#rev-sub", Label).update(
            f"[ {self.app.current_level} ]"
        )
        self.query_one("#stat-due", Label).update(str(counts["due"]))
        self.query_one("#stat-new", Label).update(str(counts["new"]))
        self.query_one("#stat-learning", Label).update(str(counts["learning"]))
        self.query_one("#stat-total", Label).update(str(counts["total"]))
        self.query_one("#btn-rev-back", Button).focus()

    @on(Button.Pressed, "#btn-rev-back")
    def handle_back_click(self) -> None:
        self.action_back_to_menu()

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()


class SettingsScreen(Screen):
    """Level, frequency, and render mode configuration screen."""

    JLPT_LEVELS = [("1", "All"), ("2", "N5"), ("3", "N4"), ("4", "N3"), ("5", "N2"), ("6", "N1")]
    FREQ_LEVELS = [("7", "Top 250"), ("8", "Top 500"), ("9", "Top 1000"), ("0", "Top 2500")]
    ALL_LEVELS = ["All", "N5", "N4", "N3", "N2", "N1", "Top 250", "Top 500", "Top 1000", "Top 2500"]
    MODES = ["halfblock", "braille", "standard"]

    BINDINGS = [
        Binding("left", "prev_deck", "Prev Level", show=False),
        Binding("h", "prev_deck", "Prev Level", show=False),
        Binding("right", "next_deck", "Next Level", show=False),
        Binding("l", "next_deck", "Next Level", show=False),
        Binding("m", "toggle_mode", "Toggle Mode", show=False),
        Binding("1", "set_lvl_all", "All", show=False),
        Binding("2", "set_lvl_n5", "N5", show=False),
        Binding("3", "set_lvl_n4", "N4", show=False),
        Binding("4", "set_lvl_n3", "N3", show=False),
        Binding("5", "set_lvl_n2", "N2", show=False),
        Binding("6", "set_lvl_n1", "N1", show=False),
        Binding("7", "set_lvl_t250", "Top 250", show=False),
        Binding("8", "set_lvl_t500", "Top 500", show=False),
        Binding("9", "set_lvl_t1000", "Top 1000", show=False),
        Binding("0", "set_lvl_t2500", "Top 2500", show=False),
        Binding("escape", "back_to_menu", "Save & Menu", show=False),
        Binding("backspace", "back_to_menu", "Save & Menu", show=False),
        Binding("q", "back_to_menu", "Save & Menu", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield KansuHeader(
            "[#818cf8]1-6[/#818cf8] [dim]jlpt[/dim]  •  [#818cf8]7-0[/#818cf8] [dim]freq[/dim]  •  [#818cf8]← / →[/#818cf8] [dim]cycle[/dim]  •  [#818cf8]m[/#818cf8] [dim]mode[/dim]  •  [#818cf8]esc[/#818cf8] [dim]save[/dim]"
        )
        with Container(id="app-container"):
            with Vertical(classes="card-panel"):
                yield Label("SETTINGS", classes="title-text")
                yield Label("", classes="subtitle-text", id="set-status")

                yield Label("Study by JLPT Level (Keys 1-6):", classes="section-label")
                with Horizontal(classes="btn-row"):
                    for key, lvl in self.JLPT_LEVELS:
                        yield Button(f"[{key}] {lvl}", id=f"lvl-{lvl.replace(' ', '-')}", classes="opt-btn")

                yield Label("Study by Real-World Frequency (Keys 7-0):", classes="section-label")
                with Horizontal(classes="btn-row"):
                    for key, lvl in self.FREQ_LEVELS:
                        yield Button(f"[{key}] {lvl}", id=f"lvl-{lvl.replace(' ', '-')}", classes="opt-btn")

                yield Label("Terminal Render Style (Key m):", classes="section-label")
                with Horizontal(classes="btn-row"):
                    yield Button("Half-Block", id="mode-halfblock", classes="opt-btn")
                    yield Button("Braille", id="mode-braille", classes="opt-btn")
                    yield Button("Standard", id="mode-standard", classes="opt-btn")

                yield Static("", id="set-preview", classes="big-kanji")
                yield Button("Save & Return to Menu (Esc)", id="btn-set-save", classes="menu-button")

    def on_mount(self) -> None:
        self.update_display()
        self.query_one("#btn-set-save", Button).focus()

    def update_display(self) -> None:
        counts = database.get_kanji_counts()
        count = counts.get(self.app.current_level, 0)
        self.query_one("#set-status", Label).update(
            f"Active: [bold #818cf8][ {self.app.current_level} ][/bold #818cf8]  •  {count} Kanji"
        )

        for _, lvl in self.JLPT_LEVELS + self.FREQ_LEVELS:
            try:
                btn = self.query_one(f"#lvl-{lvl.replace(' ', '-')}", Button)
                if lvl == self.app.current_level:
                    btn.add_class("active")
                else:
                    btn.remove_class("active")
            except Exception:
                pass

        for m in self.MODES:
            try:
                btn = self.query_one(f"#mode-{m}", Button)
                if m == self.app.kanji_render_mode:
                    btn.add_class("active")
                else:
                    btn.remove_class("active")
            except Exception:
                pass

        self.query_one("#set-preview", Static).update(self.app.render_kanji("漢"))

    def select_level(self, level: str) -> None:
        self.app.current_level = level
        self.update_display()

    def action_set_lvl_all(self) -> None: self.select_level("All")
    def action_set_lvl_n5(self) -> None: self.select_level("N5")
    def action_set_lvl_n4(self) -> None: self.select_level("N4")
    def action_set_lvl_n3(self) -> None: self.select_level("N3")
    def action_set_lvl_n2(self) -> None: self.select_level("N2")
    def action_set_lvl_n1(self) -> None: self.select_level("N1")
    def action_set_lvl_t250(self) -> None: self.select_level("Top 250")
    def action_set_lvl_t500(self) -> None: self.select_level("Top 500")
    def action_set_lvl_t1000(self) -> None: self.select_level("Top 1000")
    def action_set_lvl_t2500(self) -> None: self.select_level("Top 2500")

    def action_prev_deck(self) -> None:
        idx = self.ALL_LEVELS.index(self.app.current_level) if self.app.current_level in self.ALL_LEVELS else 0
        self.select_level(self.ALL_LEVELS[(idx - 1) % len(self.ALL_LEVELS)])

    def action_next_deck(self) -> None:
        idx = self.ALL_LEVELS.index(self.app.current_level) if self.app.current_level in self.ALL_LEVELS else 0
        self.select_level(self.ALL_LEVELS[(idx + 1) % len(self.ALL_LEVELS)])

    def action_toggle_mode(self) -> None:
        idx = self.MODES.index(self.app.kanji_render_mode) if self.app.kanji_render_mode in self.MODES else 0
        self.app.kanji_render_mode = self.MODES[(idx + 1) % len(self.MODES)]
        self.update_display()

    @on(Button.Pressed)
    def handle_button_press(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ""
        if btn_id == "btn-set-save":
            self.action_back_to_menu()
        elif btn_id.startswith("lvl-"):
            lvl_name = btn_id[4:].replace("-", " ")
            self.select_level(lvl_name)
        elif btn_id.startswith("mode-"):
            mode_name = btn_id[5:]
            self.app.kanji_render_mode = mode_name
            self.update_display()

    def action_back_to_menu(self) -> None:
        self.app.pop_screen()


class KansuApp(App):
    """Main Textual Application for Kansu."""

    TITLE = "kansu | カンス"
    CSS = KANSU_CSS
    ENABLE_COMMAND_PALETTE = False

    def __init__(self) -> None:
        super().__init__()
        self.current_level: str = "N5"
        self.kanji_render_mode: str = "halfblock"  # 'halfblock', 'braille', 'standard'
        self.kanji_size: int = 18

    def render_kanji(self, char: str) -> str:
        """Renders Kanji according to user's selected render style."""
        if self.kanji_render_mode == "halfblock":
            return render_halfblock(char, size=self.kanji_size)
        elif self.kanji_render_mode == "braille":
            return render_braille(char, size=24)
        else:
            return f"\n\n    {char}    \n\n"

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())


KansuUI = KansuApp


if __name__ == "__main__":
    app = KansuApp()
    app.run()
