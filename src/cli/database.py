import os
from pathlib import Path
import sqlite3


def _resolve_db_path() -> Path:
    env_path = os.environ.get("KANJI_DB_PATH")
    if env_path:
        return Path(env_path)
    cli_db = Path(__file__).resolve().parent / "kanji.db"
    if cli_db.exists():
        return cli_db
    src_db = Path(__file__).resolve().parent.parent / "kanji.db"
    if src_db.exists():
        return src_db
    return cli_db


DATABASE = _resolve_db_path()


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# sql shits
def initialize_database():
    connection = get_connection()
    
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kanji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character TEXT NOT NULL UNIQUE,
            meaning TEXT NOT NULL,
            onyomi TEXT,
            kunyomi TEXT,
            level TEXT,
            strokes INTEGER,
            grade INTEGER,
            frequency INTEGER
        )
    """)

    try:
        cursor.execute("ALTER TABLE kanji ADD COLUMN frequency INTEGER")
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kanji_id INTEGER,
            word TEXT NOT NULL UNIQUE,
            reading TEXT,
            meaning TEXT NOT NULL,
            level TEXT,
            FOREIGN KEY (kanji_id) REFERENCES kanji(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS examples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vocabulary_id INTEGER NOT NULL,
            japanese TEXT NOT NULL,
            english TEXT NOT NULL,
            FOREIGN KEY (vocabulary_id) REFERENCES vocabulary(id),
            UNIQUE (vocabulary_id, japanese)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS srs_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT NOT NULL,
            item_id INTEGER NOT NULL,
            card TEXT NOT NULL,
            UNIQUE (item_type, item_id)
        )
    """)

    connection.commit()
    connection.close()


def add_kanji(character, meaning, onyomi=None, kunyomi=None, level=None, strokes=None, grade=None, frequency=None):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO kanji (character, meaning, onyomi, kunyomi, level, strokes, grade, frequency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(character) DO UPDATE SET
            meaning = excluded.meaning,
            onyomi = excluded.onyomi,
            kunyomi = excluded.kunyomi,
            level = excluded.level,
            strokes = excluded.strokes,
            grade = excluded.grade,
            frequency = excluded.frequency
    """, (character, meaning, onyomi, kunyomi, level, strokes, grade, frequency))

    connection.commit()

    kanji_id = cursor.execute(
        "SELECT id FROM kanji WHERE character = ?", (character,)
    ).fetchone()["id"]

    connection.close()
    return kanji_id


def add_vocabulary(word, reading, meaning, level=None, kanji_id=None):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO vocabulary (word, reading, meaning, level, kanji_id)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(word) DO UPDATE SET
            reading = excluded.reading,
            meaning = excluded.meaning,
            level = excluded.level,
            kanji_id = excluded.kanji_id
    """, (word, reading, meaning, level, kanji_id))

    connection.commit()

    vocabulary_id = cursor.execute(
        "SELECT id FROM vocabulary WHERE word = ?", (word,)
    ).fetchone()["id"]

    connection.close()
    return vocabulary_id


def add_example(vocabulary_id, japanese, english):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO examples (vocabulary_id, japanese, english)
        VALUES (?, ?, ?)
    """, (vocabulary_id, japanese, english))

    connection.commit()
    connection.close()


def get_all_kanji():
    connection = get_connection()

    rows = connection.execute("""
        SELECT id, character, meaning, onyomi, kunyomi, level, strokes, grade, frequency
        FROM kanji
        ORDER BY character
    """).fetchall()
    connection.close()
    return rows


def get_vocabulary(kanji_id):
    connection = get_connection()

    rows = connection.execute("""
        SELECT id, word, reading, meaning, level
        FROM vocabulary
        WHERE kanji_id = ?
        ORDER BY word
    """, (kanji_id,)).fetchall()
    connection.close()
    return rows


def get_all_vocabulary():
    connection = get_connection()

    rows = connection.execute("""
        SELECT id, word, reading, meaning, level, kanji_id
        FROM vocabulary
        ORDER BY word
    """).fetchall()
    connection.close()
    return rows


def get_examples(vocabulary_id):
    connection = get_connection()

    rows = connection.execute("""
        SELECT id, japanese, english
        FROM examples
        WHERE vocabulary_id = ?
    """, (vocabulary_id,)).fetchall()
    connection.close()
    return rows


def get_srs_card(item_type, item_id):
    connection = get_connection()
    row = connection.execute("""
        SELECT card
        FROM srs_cards
        WHERE item_type = ? AND item_id = ?
    """, (item_type, item_id)).fetchone()
    connection.close()
    return row["card"] if row else None


def save_srs_card(item_type, item_id, card):
    connection = get_connection()

    connection.execute("""
        INSERT INTO srs_cards (item_type, item_id, card)
        VALUES (?, ?, ?)
        ON CONFLICT(item_type, item_id) DO UPDATE SET
            card = excluded.card
    """, (item_type, item_id, card))

    connection.commit()
    connection.close()


# review & deck section
def get_kanji_by_level(level):
    connection = get_connection()

    level_str = str(level).strip() if level else "All"

    if level_str == "All":
        rows = connection.execute("""
            SELECT id, character, meaning, onyomi, kunyomi, level, strokes, grade, frequency
            FROM kanji
            ORDER BY character
        """).fetchall()
    elif level_str.startswith("Top "):
        try:
            rank_limit = int(level_str.replace("Top ", "").strip())
        except ValueError:
            rank_limit = 2500
        rows = connection.execute("""
            SELECT id, character, meaning, onyomi, kunyomi, level, strokes, grade, frequency
            FROM kanji
            WHERE frequency IS NOT NULL AND frequency <= ?
            ORDER BY frequency ASC
        """, (rank_limit,)).fetchall()
    else:
        rows = connection.execute("""
            SELECT id, character, meaning, onyomi, kunyomi, level, strokes, grade, frequency
            FROM kanji
            WHERE level = ?
            ORDER BY character
        """, (level_str,)).fetchall()

    connection.close()
    return rows


def get_all_srs_cards():
    connection = get_connection()

    rows = connection.execute("""
        SELECT item_type, item_id, card
        FROM srs_cards
    """).fetchall()

    connection.close()
    return rows


def clear_srs_cards():
    connection = get_connection()
    connection.execute("DELETE FROM srs_cards")
    connection.commit()
    connection.close()


def get_kanji_counts():
    connection = get_connection()
    rows = connection.execute("""
        SELECT level, COUNT(*) as count
        FROM kanji
        GROUP BY level
    """).fetchall()
    total = connection.execute("SELECT COUNT(*) FROM kanji").fetchone()[0]

    counts = {"All": total}
    for row in rows:
        if row["level"]:
            counts[row["level"]] = row["count"]

    for tier in [250, 500, 1000, 2500]:
        tier_count = connection.execute("""
            SELECT COUNT(*) FROM kanji
            WHERE frequency IS NOT NULL AND frequency <= ?
        """, (tier,)).fetchone()[0]
        counts[f"Top {tier}"] = tier_count

    connection.close()
    return counts