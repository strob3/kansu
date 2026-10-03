import random
import re
try:
    from database import get_kanji_by_level
    from srs import load_card, is_due, is_new
except ImportError:
    from .database import get_kanji_by_level
    from .srs import load_card, is_due, is_new


def normalize_text(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"[^\w\s]", "", text.strip().lower())
    return " ".join(cleaned.split())


def check_answer(user_answer: str, meaning_str: str):
    norm_user = normalize_text(user_answer)
    meanings = [m.strip() for m in meaning_str.split("/") if m.strip()]
    if not norm_user:
        return False, meanings

    for m in meanings:
        if norm_user == normalize_text(m):
            return True, meanings
        clean_m = re.sub(r"\(.*?\)", "", m).strip()
        if clean_m and norm_user == normalize_text(clean_m):
            return True, meanings

    return False, meanings


def get_quiz_candidates(level="All", mode="all"):
    kanji_list = get_kanji_by_level(level)
    new_cards = []
    due_cards = []
    future_cards = []

    for kanji in kanji_list:
        card = load_card("kanji", kanji["id"])
        if is_new(card):
            new_cards.append(kanji)
        elif is_due(card):
            due_cards.append(kanji)
        else:
            future_cards.append(kanji)

    counts = {
        "due": len(due_cards),
        "new": len(new_cards),
        "learning": len(future_cards),
        "total": len(kanji_list),
    }

    if mode == "due_only":
        return due_cards, counts

    if due_cards:
        candidates = due_cards + (new_cards[:5] if new_cards else [])
    elif new_cards:
        candidates = new_cards
    else:
        candidates = future_cards

    return candidates, counts


def choose_next_quiz_kanji(level="All", mode="all", previous_id=None):
    candidates, counts = get_quiz_candidates(level=level, mode=mode)
    if not candidates:
        return None, counts

    if len(candidates) > 1 and previous_id is not None:
        filtered = [k for k in candidates if k["id"] != previous_id]
        if filtered:
            candidates = filtered

    chosen = random.choice(candidates)
    card = load_card("kanji", chosen["id"])
    return {
        "id": chosen["id"],
        "character": chosen["character"],
        "meaning": chosen["meaning"],
        "onyomi": chosen["onyomi"],
        "kunyomi": chosen["kunyomi"],
        "level": chosen["level"],
        "strokes": chosen["strokes"],
        "grade": chosen["grade"],
        "is_new": is_new(card),
        "is_due": is_due(card),
    }, counts
