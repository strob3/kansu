<div align="center">
  <img src="src/web/assets/logo.svg" width="140" alt="Kansu logo">
  <h1>
    Kansu (カンス)
  </h1>
  <p>
    A Japanese <strong>kan</strong>ji <strong>stu</strong>dy application for learning and practicing kanji and related vocabulary with FSRS spaced repetition, available as both a TUI and a web app.
  </p>
</div>

## Features

* **Study**: Browse kanji glyphs, On'yomi and Kun'yomi readings, stroke counts, and related vocabulary with example sentences.
* **Quiz**: Interactive flashcard quizzes with the **FSRS spaced repetition algorithm** (Again, Hard, Good, Easy ratings).
* **Review & Statistics**: Deck breakdown (Due, New, Learning, Total) and visual mastery progress.
* **Keyboard-centric**: Keyboard-first shortcuts (`↑`/`↓`, `←`/`→`, `Enter`, `Esc`, `1`-`4` ratings) paired with touch/mouse-friendly on-screen controls.
* **Level Selection**: Switch between N5-N1 or real-world usage frequency. 
* **Terminal & Web Interfaces**: Run in your terminal via `kansu` or in your browser.

## Web Version

* **Live Web App**: [https://kansu.vercel.app](https://kansu.vercel.app)

The web version is a pure client-side web app. Runs entirely in the browser with offline support and local storage persistence, no server setup or local dependencies required.

## TUI Version

### Installation

Install directly from your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/strob3/kansu/main/install.sh | bash
```

You can also clone the repo and run the install script:

```bash
git clone https://github.com/strob3/kansu.git
cd kansu
./install.sh
```

### Launch Kansu

After installation, run in your terminal:

```bash
kansu
```

## Keyboard Shortcuts

| Shortcut | Context | Action |
| :--- | :--- | :--- |
| `↑` / `↓` or `k` / `j` | Menu | Navigate menu options |
| `1` - `5` | Menu | Directly open option 1 to 5 |
| `Enter` | Menu / Forms | Select menu item / Submit quiz answer |
| `←` / `→` or `h` / `l` | Study Mode | Previous / Next kanji card |
| `1`, `2`, `3`, `4` | Quiz Result | Rate card: `[1] Again`, `[2] Hard`, `[3] Good`, `[4] Easy` |
| `Esc` | Anywhere | Return to Main Menu / Exit active mode |

## Roadmap (planned features)

- Quick kanji search & dictionary explorer (Ctrl+K / /)
- Reading quiz mode & romaji-to-kana auto-transliteration
- SRS progress backup & restore (JSON Export / Import)
- Study streak & daily review tracker
- Animated kanji stroke order
- Backend feature overhaul including:
    - authentication
    - user accounts
    - synchronization
    - progress
    - FSRS state
    - settings
    - custom decks
    - API authorization
- Mobile version

## License & Attribution

Kansu source code is licensed under the [MIT License](LICENSE).

The OpenJLPT-derived data included in Kansu is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

See [NOTICE.md](NOTICE.md) for attribution and upstream data sources.
