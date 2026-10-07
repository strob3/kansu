## [1.2.0] - 2026-10-08

### Added
- **Web Svelte 5 & TypeScript**: Rebuilt web application using Svelte 5 runes, TypeScript, and Tailwind CSS v4.
- **Grid Dashboard**: Implemented bento grid style layout.
- **Dictionary Explorer**: Added dictionary to easily explore all kanji.
- **Command Palette**: Search kanji characters, English meanings, and On/Kun readings via `Ctrl+K` or `/` with direct card jump.
- **Data**: JSON backup export and import for FSRS card states.

### Changed
- **Quick Select 1–6**: Assigned shortcut key 6 to Settings on menu screen; updated hotkey bar to display 1–6.
- **Topbar Refinement**: Removed level status dot and search keybind badge, aligned search pill height with navigation bar, and updated tab ordering to Menu > Study > Quiz > Review > Dictionary > Settings.
- **Hotkey Bar**: Dynamic footer keyboard shortcuts reflecting only actions applicable to the active screen.
- **Theme Switcher**: Replaced 3-button theme selector with animated 2-state toggle switch.
- **Color Palette**: Implemented zen design system palette across kansu.
- **Logo**: Recolored logo SVG to website forest green palette.

## [1.1.0] - 2026-10-03

### Added
- **1-Line CLI Curl Installation**: Direct installation via `curl -fsSL https://raw.githubusercontent.com/strob3/kansu/main/install.sh | bash` with automatic fallback to standard XDG data directory (`~/.local/share/kansu`).
- **Dynamic Module Resolution**: Configured `sys.path` dynamically in `src/main.py` so `kansu` can be invoked from any working directory.
- **Offline Resilience**: Optimized database provisioning in `install.sh` to verify existing records in `src/kanji.db` before attempting remote downloads.

### Changed
- **Installer Overhaul (`install.sh`)**:
  - Automatically resolves local repository paths when run from a clone or downloaded standalone.
  - Automatically adds `~/.local/bin` to existing shell configs (`~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, `~/.profile`) without creating unwanted new dotfiles.
  - Refreshes shell binary hash lookup caches (`hash -r` / `rehash`) for immediate availability.

## [1.0.0] - 2026-10-02

### Added
- **Kansu Web Version**: Full-featured web application deployed at [https://kansu.vercel.app](https://kansu.vercel.app).
- ~~**REST API Backend**: FastAPI service exposing `/api/kanji`, `/api/quiz`, `/api/review`, `/api/stats`, and `/api/levels`.~~
- **FSRS Spaced Repetition on Web**: Interactive flashcards powered by FSRS scheduling algorithms with Again, Hard, Good, and Easy card ratings.

## [0.2.0] - 2026-08-28

### Added
- **Textual Terminal User Interface (TUI)**: Interactive terminal application with custom styling and keyboard-first navigation.
- **High-Resolution Kanji Renderer**: Terminal glyph rendering supporting Braille and Unicode half-block characters using system CJK fonts.
- **Review & Stats Screen**: Deck breakdown displaying Due, New, Learning, and Total card counts with mastery progression.
- **Settings Screen**: In-app configuration for deck level selection and study preferences.

## [0.1.0] - 2026-08-28

### Added
- Initial project prototype.
- SQLite database schema for kanji, vocabulary, and example sentences.
- FSRS algorithm integration for study and quiz tracking.
- OpenJLPT dataset importer.
