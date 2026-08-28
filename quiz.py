import random

from database import get_all_kanji
from fsrs import Rating

from srs import is_due, load_card, review_card


class QuizScreen:
    def __init__(self, ui):
        self.ui = ui
        self.kanji_list = get_all_kanji()
        self.previous_id = None

        if not self.kanji_list:
            self.ui.back()
            return

        self.next_question()

    def get_candidates(self):
        new_cards = []
        due_cards = []
        future_cards = []

        for kanji in self.kanji_list:
            card = load_card("kanji", kanji["id"])

            if card.reps == 0:
                new_cards.append(kanji)
            elif is_due(card):
                due_cards.append(kanji)
            else:
                future_cards.append(kanji)

        return new_cards, due_cards, future_cards

    def choose_kanji(self):
        new_cards, due_cards, future_cards = self.get_candidates()

        candidates = due_cards + new_cards

        if not candidates:
            candidates = future_cards

        if len(candidates) > 1:
            candidates = [
                kanji
                for kanji in candidates
                if kanji["id"] != self.previous_id
            ]

        kanji = random.choice(candidates)
        self.previous_id = kanji["id"]

        return kanji

    def next_question(self):
        kanji = self.choose_kanji()
        self.current_kanji = kanji

        self.ui.show_quiz(
            kanji,
            self.submit_answer,
        )

    def submit_answer(self, answer):
        correct_answers = [
            meaning.strip().lower()
            for meaning in self.current_kanji["meaning"].split("/")
        ]

        correct = answer.strip().lower() in correct_answers

        self.ui.show_quiz_result(
            correct,
            answer,
            self.current_kanji["meaning"],
            self.rate,
        )

    def rate(self, rating):
        card, _ = review_card(
            "kanji",
            self.current_kanji["id"],
            Rating(rating),
        )

        self.next_question()