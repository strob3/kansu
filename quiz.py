import random

from database import get_all_kanji
from fsrs import Rating
from srs import review_card


class QuizScreen:
    def __init__(self, ui):
        self.ui = ui
        self.kanji_list = get_all_kanji()
        self.kanji = None

        if not self.kanji_list:
            ui.show_review_result("No kanji found.")
            return

        self.next_question()

    def next_question(self):
        available = [
            kanji
            for kanji in self.kanji_list
            if self.kanji is None or kanji["id"] != self.kanji["id"]
        ]

        self.kanji = random.choice(available)

        self.ui.show_quiz(
            self.kanji,
            self.submit,
        )

    def submit(self, answer):
        correct_answers = [
            meaning.strip().lower()
            for meaning in self.kanji["meaning"].split("/")
        ]

        correct = answer.strip().lower() in correct_answers

        self.ui.show_quiz_result(
            correct,
            answer,
            self.kanji["meaning"],
            self.rate,
        )

    def rate(self, rating):
        review_card(
            "kanji",
            self.kanji["id"],
            Rating(rating),
        )

        self.next_question()
