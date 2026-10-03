import json
from datetime import datetime, timezone
from fsrs import Card, Rating, Scheduler
try:
    from database import get_srs_card, save_srs_card
except ImportError:
    from .database import get_srs_card, save_srs_card


scheduler = Scheduler()


def load_card(item_type, item_id):
    data = get_srs_card(item_type, item_id)

    if data is None:
        return Card()

    try:
        return Card.from_dict(json.loads(data))
    except Exception:
        return Card()


def save_card(item_type, item_id, card):
    save_srs_card(item_type, item_id, json.dumps(card.to_dict()))


def review_card(item_type, item_id, rating):
    card = load_card(item_type, item_id)
    if isinstance(rating, int):
        rating = Rating(rating)
    card, review_log = scheduler.review_card(card, rating)
    save_card(item_type, item_id, card)
    return card, review_log


def is_new(card):
    return card.last_review is None


def is_due(card):
    if card.last_review is None:
        return False
    due = card.due
    if isinstance(due, str):
        due = datetime.fromisoformat(due)
    if hasattr(due, "tzinfo") and due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    return due <= datetime.now(timezone.utc)


def get_card_info(item_type, item_id):
    card = load_card(item_type, item_id)
    state_val = card.state.value if hasattr(card.state, "value") else int(card.state)
    return {
        "is_new": is_new(card),
        "is_due": is_due(card),
        "state": state_val,
        "step": card.step,
        "due": card.due.isoformat() if isinstance(card.due, datetime) else str(card.due),
        "last_review": (
            card.last_review.isoformat()
            if isinstance(card.last_review, datetime)
            else (str(card.last_review) if card.last_review else None)
        ),
        "stability": card.stability,
        "difficulty": card.difficulty,
    }