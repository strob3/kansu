# unit tests for kansu cli 

import sys
import unittest
from pathlib import Path

# add src and src/cli to python path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
CLI_DIR = SRC_DIR / "cli"
for p in (CLI_DIR, SRC_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from kanji_renderer import find_cjk_font, render_halfblock, render_braille
from ui import KansuApp, KansuHeader, MenuScreen, StudyScreen, QuizScreen, ReviewScreen, SettingsScreen
from textual.widgets import Static, Label, Button, Input


class TestKanjiRenderer(unittest.TestCase):
    def test_find_cjk_font(self):
        font = find_cjk_font()
        self.assertIsNotNone(font, "A CJK font should be discovered on system")

    def test_render_halfblock_simple(self):
        glyph = render_halfblock("日", size=18)
        lines = glyph.splitlines()
        self.assertGreaterEqual(len(lines), 7)
        self.assertLessEqual(len(lines), 11)
        self.assertTrue(any("█" in line or "▀" in line or "▄" in line for line in lines))

    def test_render_halfblock_complex(self):
        glyph = render_halfblock("漢", size=18)
        lines = glyph.splitlines()
        self.assertGreaterEqual(len(lines), 7)
        self.assertLessEqual(len(lines), 11)

    def test_render_braille(self):
        glyph = render_braille("日", size=24)
        lines = glyph.splitlines()
        self.assertGreaterEqual(len(lines), 5)
        self.assertLessEqual(len(lines), 9)


class TestKansuTUI(unittest.IsolatedAsyncioTestCase):
    async def test_app_lifecycle_and_menu(self):
        app = KansuApp()
        async with app.run_test() as pilot:
            self.assertIsInstance(app.screen, MenuScreen)
            title_lbl = app.screen.query_one(".title-text", Label)
            self.assertIn("kansu", str(title_lbl.render()).lower())

            # deck render
            deck_lbl = app.screen.query_one("#menu-deck-label", Label)
            self.assertIn("N5", str(deck_lbl.render()))

            shortcuts_lbl = app.screen.query_one("#menu-shortcuts", Label)
            self.assertIsNotNone(shortcuts_lbl)
            self.assertIn("navigate", str(shortcuts_lbl.render()).lower())
            panel = app.screen.query_one(".card-panel")
            self.assertEqual(list(panel.children)[-1], shortcuts_lbl)

            # arrow navigation
            self.assertEqual(app.screen.focused.id, "btn-study")
            await pilot.press("down")
            await pilot.pause()
            self.assertEqual(app.screen.focused.id, "btn-quiz")
            await pilot.press("down")
            await pilot.pause()
            self.assertEqual(app.screen.focused.id, "btn-review")
            await pilot.press("up")
            await pilot.pause()
            self.assertEqual(app.screen.focused.id, "btn-quiz")

    async def test_navigate_to_study_screen(self):
        app = KansuApp()
        async with app.run_test() as pilot:
            await pilot.press("1")
            await pilot.pause()
            self.assertIsInstance(app.screen, StudyScreen)

            kanji_static = app.screen.query_one("#study-kanji", Static)
            rendered_text = str(kanji_static.render())
            self.assertTrue(any(c in rendered_text for c in ("█", "▀", "▄")))

            initial_idx = app.screen.current_index
            await pilot.press("right")
            await pilot.pause()
            self.assertEqual(app.screen.current_index, initial_idx + 1)

            await pilot.press("left")
            await pilot.pause()
            self.assertEqual(app.screen.current_index, initial_idx)

            await pilot.press("escape")
            await pilot.pause()
            self.assertIsInstance(app.screen, MenuScreen)

    async def test_navigate_to_quiz_and_submit(self):
        app = KansuApp()
        async with app.run_test() as pilot:
            await pilot.press("2")
            await pilot.pause()
            self.assertIsInstance(app.screen, QuizScreen)

            quiz_screen: QuizScreen = app.screen
            self.assertEqual(quiz_screen.phase, "question")

            inp = quiz_screen.query_one("#quiz-input", Input)
            self.assertTrue(inp.display)

            # q/a
            quiz_screen.submit_answer("sun")
            await pilot.pause()

            self.assertEqual(quiz_screen.phase, "result")
            self.assertFalse(inp.display)

            # rate card
            await pilot.press("3")
            await pilot.pause()
            self.assertEqual(quiz_screen.phase, "question")

            await pilot.press("escape")
            await pilot.pause()
            self.assertIsInstance(app.screen, MenuScreen)

    async def test_navigate_to_review(self):
        app = KansuApp()
        async with app.run_test() as pilot:
            await pilot.press("3")
            await pilot.pause()
            self.assertIsInstance(app.screen, ReviewScreen)

            total_lbl = app.screen.query_one("#stat-total", Label)
            total_val = int(str(total_lbl.render()))
            self.assertGreater(total_val, 0)

            await pilot.press("escape")
            await pilot.pause()
            self.assertIsInstance(app.screen, MenuScreen)

    async def test_settings_screen_deck_change(self):
        app = KansuApp()
        async with app.run_test() as pilot:
            await pilot.press("4")
            await pilot.pause()
            self.assertIsInstance(app.screen, SettingsScreen)

            # test direct jlpt selection via hotkey
            await pilot.press("3")
            await pilot.pause()
            self.assertEqual(app.current_level, "N4")

            # test direct frequency selection via hotkey
            await pilot.press("8")
            await pilot.pause()
            self.assertEqual(app.current_level, "Top 500")

            # test button click for jlpt level
            n5_btn = app.screen.query_one("#lvl-N5", Button)
            n5_btn.press()
            await pilot.pause()
            self.assertEqual(app.current_level, "N5")

            # test button click for frequency tier
            top250_btn = app.screen.query_one("#lvl-Top-250", Button)
            top250_btn.press()
            await pilot.pause()
            self.assertEqual(app.current_level, "Top 250")

            # test cycle with right arrow
            await pilot.press("right")
            await pilot.pause()
            self.assertEqual(app.current_level, "Top 500")

            initial_mode = app.kanji_render_mode
            await pilot.press("m")
            await pilot.pause()
            self.assertNotEqual(app.kanji_render_mode, initial_mode)

            await pilot.press("escape")
            await pilot.pause()
            self.assertIsInstance(app.screen, MenuScreen)


if __name__ == "__main__":
    unittest.main()
