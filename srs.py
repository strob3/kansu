import json
from datetime import datetime, timezone

from fsrs import Card, Rating, Scheduler

from database import get_srs_card, save_srs_card


scheduler = Scheduler()


def load_card(item_type, item_id):
    data = get_srs_card(item_type, item_id)

    if data is None:
        return Card()

    return Card.from_dict(json.loads(data))


def save_card(item_type, item_id, card):
    save_srs_card(item_type, item_id, json.dumps(card.to_dict()))


def review_card(item_type, item_id, rating):
    card = load_card(item_type, item_id)
    card, review_log = scheduler.review_card(card, rating)
    save_card(item_type, item_id, card)
    return card, review_log


def is_due(card):
    return card.due <= datetime.now(timezone.utc)