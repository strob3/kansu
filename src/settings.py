class SettingsScreen:
    levels = ["All", "N5", "N4"]
    # levels = ["All", "N5", "N4", "N3", "N2", "N1"]

    def __init__(self, ui):
        self.ui = ui
        self.level_index = self.levels.index(
            ui.nlevel
        ) if ui.nlevel in self.levels else 0

        self.show()

    def show(self):
        self.ui.show_settings(
            self.levels[self.level_index],
            self.previous,
            self.next,
            self.back,
        )

    def previous(self, event=None):
        self.level_index = (
            self.level_index - 1
        ) % len(self.levels)

        self.ui.nlevel = self.levels[self.level_index]
        self.show()

    def next(self, event=None):
        self.level_index = (
            self.level_index + 1
        ) % len(self.levels)

        self.ui.nlevel = self.levels[self.level_index]
        self.show()

    def back(self, event=None):
        self.ui.show_menu()