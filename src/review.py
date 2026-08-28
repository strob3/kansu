import json

from database import get_all_kanji, get_all_srs_cards
from fsrs import Card
from srs import is_due


class ReviewScreen:
    def __init__(self, ui):
        self.ui = ui
        self.show()

    def get_stats(self):
        kanji = get_all_kanji()
        cards = get_all_srs_cards()

        cards_by_id = {}

        for row in cards:
            if row["item_type"] != "kanji":
                continue

            try:
                card = Card.from_dict(
                    json.loads(row["card"])
                )
                cards_by_id[row["item_id"]] = card
            except Exception:
                continue

        new = 0
        due = 0
        learning = 0

        for kanji in kanji:
            card = cards_by_id.get(kanji["id"])

            if card is None:
                new += 1
            elif is_due(card):
                due += 1
            else:
                learning += 1

        return {
            "new": new,
            "due": due,
            "learning": learning,
            "total": len(kanji),
        }

    def show(self):
        stats = self.get_stats()
        self.ui.show_review(
            stats,
            self.back,
        )

    def back(self, event=None):
        self.ui.show_menu()