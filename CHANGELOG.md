# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-03

### Added
- **1-Line CLI Curl Installation**: Direct installation via `curl -fsSL https://raw.githubusercontent.com/strob3/kansu/main/install.sh | bash` with automatic fallback to standard XDG data directory (`~/.local/share/kansu`).
- **Dynamic Module Resolution**: Configured `sys.path` dynamically in `src/main.py` so `kansu` can be invoked from any working directory.
- **Offline Resilience**: Optimized database provisioning in `install.sh` to verify existing records in `src/kanji.db` before attempting remote downloads, avoiding network timeouts when offline.

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
