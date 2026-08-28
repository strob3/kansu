from pathlib import Path
import sqlite3


DATABASE = Path(__file__).resolve().parent / "kanji.db"


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
            grade INTEGER
        )
    """)

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

    connection.commit()
    connection.close()


def add_kanji(character, meaning, onyomi=None, kunyomi=None, level=None, strokes=None, grade=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO kanji (character, meaning, onyomi, kunyomi, level, strokes, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(character) DO UPDATE SET
            meaning = excluded.meaning,
            onyomi = excluded.onyomi,
            kunyomi = excluded.kunyomi,
            level = excluded.level,
            strokes = excluded.strokes,
            grade = excluded.grade
    """, (character, meaning, onyomi, kunyomi, level, strokes, grade))

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
        SELECT id, character, meaning, onyomi, kunyomi, level, strokes, grade
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