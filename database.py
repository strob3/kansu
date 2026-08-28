import sqlite3


DATABASE = "kanji.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


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
            kanji_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            reading TEXT NOT NULL,
            meaning TEXT NOT NULL,

            FOREIGN KEY (kanji_id)
                REFERENCES kanji(id),

            UNIQUE (kanji_id, word)
        )
    """)

    connection.commit()
    connection.close()


def add_kanji(
    character,
    meaning,
    onyomi=None,
    kunyomi=None,
    level=None,
    strokes=None,
    grade=None,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO kanji (
            character,
            meaning,
            onyomi,
            kunyomi,
            level,
            strokes,
            grade
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(character) DO UPDATE SET
            meaning = excluded.meaning,
            onyomi = excluded.onyomi,
            kunyomi = excluded.kunyomi,
            level = excluded.level,
            strokes = excluded.strokes,
            grade = excluded.grade
    """, (
        character,
        meaning,
        onyomi,
        kunyomi,
        level,
        strokes,
        grade,
    ))

    connection.commit()

    kanji_id = cursor.execute("""
        SELECT id
        FROM kanji
        WHERE character = ?
    """, (character,)).fetchone()["id"]

    connection.close()

    return kanji_id


def add_vocabulary(
    kanji_id,
    word,
    reading,
    meaning,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO vocabulary (
            kanji_id,
            word,
            reading,
            meaning
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(kanji_id, word) DO UPDATE SET
            reading = excluded.reading,
            meaning = excluded.meaning
    """, (
        kanji_id,
        word,
        reading,
        meaning,
    ))

    connection.commit()
    connection.close()


def get_all_kanji():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            character,
            meaning,
            onyomi,
            kunyomi,
            level,
            strokes,
            grade
        FROM kanji
        ORDER BY character
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_vocabulary(kanji_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            word,
            reading,
            meaning
        FROM vocabulary
        WHERE kanji_id = ?
        ORDER BY word
    """, (kanji_id,))

    rows = cursor.fetchall()

    connection.close()

    return rows