import random

from database import get_all_kanji, get_vocabulary


def get_kanji_card(kanji):
    vocabulary = get_vocabulary(kanji["id"])

    return {
        "id": kanji["id"],
        "character": kanji["character"],
        "meaning": kanji["meaning"],
        "onyomi": kanji["onyomi"],
        "kunyomi": kanji["kunyomi"],
        "vocabulary": vocabulary,
    }


class StudyScreen:
    def __init__(self, ui):
        self.ui = ui
        self.kanji_list = get_all_kanji()
        self.index = 0

        if not self.kanji_list:
            ui.show_review_result("No kanji found.")
            return

        self.show()

    def show(self):
        kanji = self.kanji_list[self.index]
        card = get_kanji_card(kanji)

        self.ui.show_study(
            card,
            self.previous,
            self.next,
        )

    def previous(self, event=None):
        self.index = (self.index - 1) % len(self.kanji_list)
        self.show()

    def next(self, event=None):
        self.index = (self.index + 1) % len(self.kanji_list)
        self.show()