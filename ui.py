import tkinter as tk
from tkinter import font


BG = "#151819"
FG = "#fbf1c7"
MUTED = "#928374"
ACCENT = "#bbfff2"
ERROR = "#ff8173"
BORDER = "#665c54"


class KansuUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("kansu")
        self.root.geometry("800x600")
        self.root.minsize(600, 450)
        self.root.configure(bg=BG)

        self.title_font = font.Font(
            family="Noto Sans",
            size=20,
            weight="bold",
        )
        self.kanji_font = font.Font(
            family="Noto Sans CJK JP",
            size=96,
        )
        self.text_font = font.Font(
            family="Noto Sans",
            size=14,
        )

        self.screen = "menu"
        self.menu_index = 0
        self.quiz_kanji = ""

        self.root.bind("q", self.handle_q)
        self.root.bind("<BackSpace>", self.handle_backspace)

        self.build_ui()

    def build_ui(self):
        self.outer = tk.Frame(
            self.root,
            bg=BORDER,
        )
        self.outer.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18,
        )

        self.inner = tk.Frame(
            self.outer,
            bg=BG,
        )
        self.inner.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1,
        )

        self.header = tk.Frame(
            self.inner,
            bg=BG,
            height=55,
        )
        self.header.pack(
            fill="x",
            padx=22,
            pady=(10, 0),
        )
        self.header.pack_propagate(False)

        self.header_right = tk.Label(
            self.header,
            bg=BG,
            fg=MUTED,
            font=self.text_font,
        )
        self.header_right.pack(side="right")

        self.top_border = tk.Frame(
            self.inner,
            bg=BORDER,
            height=1,
        )
        self.top_border.pack(fill="x")

        self.content = tk.Frame(
            self.inner,
            bg=BG,
        )
        self.content.pack(
            fill="both",
            expand=True,
        )

        self.bottom_border = tk.Frame(
            self.inner,
            bg=BORDER,
            height=1,
        )
        self.bottom_border.pack(fill="x")

        self.footer = tk.Frame(
            self.inner,
            bg=BG,
            height=45,
        )
        self.footer.pack(
            fill="x",
            padx=22,
            pady=(5, 5),
        )
        self.footer.pack_propagate(False)

        self.footer_left = tk.Label(
            self.footer,
            bg=BG,
            fg=MUTED,
            font=self.text_font,
        )
        self.footer_left.pack(side="left")

        self.footer_right = tk.Label(
            self.footer,
            bg=BG,
            fg=MUTED,
            font=self.text_font,
        )
        self.footer_right.pack(side="right")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def set_footer(self, left="", right=""):
        self.footer_left.config(text=left)
        self.footer_right.config(text=right)

    def reset_bindings(self):
        for sequence in (
            "<Up>",
            "<Down>",
            "<Left>",
            "<Right>",
            "<Return>",
            "1",
            "2",
            "3",
            "4",
        ):
            self.root.unbind(sequence)

    def handle_q(self, event=None):
        if isinstance(self.root.focus_get(), tk.Entry):
            return
        self.quit()

    def handle_backspace(self, event=None):
        if isinstance(self.root.focus_get(), tk.Entry):
            return
        self.back()

    def run(self):
        self.show_menu()
        self.root.mainloop()

    def show_menu(self):
        self.screen = "menu"
        self.reset_bindings()
        self.clear_content()

        self.header_right.config(text="menu")

        container = tk.Frame(
            self.content,
            bg=BG,
        )
        container.place(
            relx=0.5,
            rely=0.45,
            anchor="center",
        )

        tk.Label(
            container,
            text="kansu | カンス",
            bg=BG,
            fg=FG,
            font=self.title_font,
        ).pack(pady=(0, 30))

        self.menu_labels = []

        for _ in range(3):
            label = tk.Label(
                container,
                bg=BG,
                fg=FG,
                font=self.text_font,
                width=20,
                anchor="center",
                highlightthickness=0,
                bd=0,
            )
            label.pack(pady=5)
            self.menu_labels.append(label)

        self.update_menu()

        self.set_footer(
            "↑ ↓ navigate    enter select",
        )

        self.root.bind("<Up>", self.menu_up)
        self.root.bind("<Down>", self.menu_down)
        self.root.bind("<Right>", self.menu_down)
        self.root.bind("<Left>", self.menu_up)
        self.root.bind("<Return>", self.menu_select)

    def update_menu(self):
        items = [
            "study",
            "quiz",
            "quit",
        ]

        for i, label in enumerate(self.menu_labels):
            label.config(
                text=f"> {items[i]}" if i == self.menu_index else f"  {items[i]}",
                fg=ACCENT if i == self.menu_index else FG,
            )

    def menu_up(self, event=None):
        self.menu_index = (self.menu_index - 1) % 3
        self.update_menu()

    def menu_down(self, event=None):
        self.menu_index = (self.menu_index + 1) % 3
        self.update_menu()

    def menu_select(self, event=None):
        if self.menu_index == 0:
            from study import StudyScreen
            StudyScreen(self)
        elif self.menu_index == 1:
            from quiz import QuizScreen
            QuizScreen(self)
        else:
            self.quit()

    def show_study(self, card, previous, next_card):
        self.screen = "study"
        self.reset_bindings()
        self.clear_content()

        self.header_right.config(text="study")

        content = tk.Frame(
            self.content,
            bg=BG,
        )
        content.place(
            relx=0.5,
            rely=0.45,
            anchor="center",
        )

        tk.Label(
            content,
            text=card["character"],
            bg=BG,
            fg=FG,
            font=self.kanji_font,
        ).pack()

        tk.Label(
            content,
            text=card["meaning"],
            bg=BG,
            fg=FG,
            font=self.text_font,
        ).pack(pady=(15, 0))

        tk.Label(
            content,
            text=f"On'yomi: {card['onyomi'] or '-'}",
            bg=BG,
            fg=MUTED,
            font=self.text_font,
        ).pack(pady=(10, 0))

        tk.Label(
            content,
            text=f"Kun'yomi: {card['kunyomi'] or '-'}",
            bg=BG,
            fg=MUTED,
            font=self.text_font,
        ).pack()

        vocabulary = card["vocabulary"]

        if vocabulary:
            tk.Label(
                content,
                text="Vocabulary",
                bg=BG,
                fg=FG,
                font=self.text_font,
            ).pack(pady=(20, 5))

            for word in vocabulary:
                tk.Label(
                    content,
                    text=(
                        f"{word['word']}  "
                        f"{word['reading']}  "
                        f"{word['meaning']}"
                    ),
                    bg=BG,
                    fg=MUTED,
                    font=self.text_font,
                ).pack()

        self.set_footer(
            "← previous    → next",
            "backspace back    q quit",
        )

        self.root.bind("<Left>", previous)
        self.root.bind("<Right>", next_card)

    def show_quiz(self, kanji, submit):
        self.screen = "quiz"
        self.reset_bindings()
        self.clear_content()

        self.quiz_kanji = kanji["character"]

        self.header_right.config(text="quiz")

        content = tk.Frame(
            self.content,
            bg=BG,
        )
        content.place(
            relx=0.5,
            rely=0.45,
            anchor="center",
        )

        tk.Label(
            content,
            text=kanji["character"],
            bg=BG,
            fg=FG,
            font=self.kanji_font,
        ).pack()

        tk.Label(
            content,
            text="what does this mean?",
            bg=BG,
            fg=FG,
            font=self.text_font,
        ).pack(pady=(20, 10))

        entry = tk.Entry(
            content,
            bg="#1d2021",
            fg=FG,
            insertbackground=FG,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            font=self.text_font,
            width=30,
            justify="center",
        )
        entry.pack(ipady=5)
        entry.focus_set()

        entry.bind(
            "<Return>",
            lambda event: submit(entry.get()),
        )

        self.set_footer(
            "enter submit",
        )

    def show_quiz_result(
        self,
        correct,
        answer,
        expected,
        rating_callback,
    ):
        self.screen = "quiz_result"
        self.reset_bindings()
        self.clear_content()

        self.header_right.config(text="quiz")

        content = tk.Frame(
            self.content,
            bg=BG,
        )
        content.place(
            relx=0.5,
            rely=0.45,
            anchor="center",
        )

        tk.Label(
            content,
            text="✓" if correct else "✗",
            bg=BG,
            fg=ACCENT if correct else ERROR,
            font=self.title_font,
        ).pack(pady=(0, 20))

        tk.Label(
            content,
            text=self.quiz_kanji,
            bg=BG,
            fg=FG,
            font=self.kanji_font,
        ).pack()

        tk.Label(
            content,
            text=f"your answer:   {answer}",
            bg=BG,
            fg=FG,
            font=self.text_font,
        ).pack(pady=(20, 5))

        if not correct:
            tk.Label(
                content,
                text=f"correct answer:   {expected}",
                bg=BG,
                fg=FG,
                font=self.text_font,
            ).pack(pady=5)

        tk.Label(
            content,
            text="1 again    2 hard    3 good    4 easy",
            bg=BG,
            fg=MUTED,
            font=self.text_font,
        ).pack(pady=(25, 10))

        self.set_footer(
            "",
            "backspace back",
        )

        self.root.bind(
            "1",
            lambda event: rating_callback(1),
        )
        self.root.bind(
            "2",
            lambda event: rating_callback(2),
        )
        self.root.bind(
            "3",
            lambda event: rating_callback(3),
        )
        self.root.bind(
            "4",
            lambda event: rating_callback(4),
        )

    def show_review_result(self, message):
        self.screen = "review_result"
        self.reset_bindings()
        self.clear_content()

        self.header_right.config(text="review")

        tk.Label(
            self.content,
            text=message,
            bg=BG,
            fg=FG,
            font=self.text_font,
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        self.set_footer(
            "backspace back",
            "q quit",
        )

    def back(self, event=None):
        if self.screen != "menu":
            self.menu_index = 0
            self.show_menu()

    def quit(self, event=None):
        self.root.destroy()