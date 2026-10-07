import {
  fsrs,
  createEmptyCard,
  Rating,
  State,
  type Card,
  type RecordLogItem,
} from 'ts-fsrs';
import type { CurriculumDeck } from '../types/kanji';
import { getDeck } from '../data';

export { Rating, State, type Card };

export interface SavedCardData {
  id: number;
  card: Card;
  lastReview?: string;
}

export interface DeckStats {
  total: number;
  mature: number;
  learning: number;
  due: number;
  unseen: number;
  retentionRate: number;
}

class SrsManager {
  private f = fsrs();
  private storageKey = 'kansu_srs_cards_v2';
  private legacyKey = 'kansu_srs_cards';
  private cards: Map<number, Card> = new Map();

  constructor() {
    this.loadCards();
  }

  private loadCards() {
    try {
      // 1. try modern ts-fsrs storage
      const raw = localStorage.getItem(this.storageKey);
      if (raw) {
        const parsed: Record<string, any> = JSON.parse(raw);
        for (const [idStr, c] of Object.entries(parsed)) {
          const id = Number(idStr);
          this.cards.set(id, {
            ...c,
            due: new Date(c.due),
            last_review: c.last_review ? new Date(c.last_review) : undefined,
          });
        }
        return;
      }

      // 2. fallback migrate from legacy storage
      const legacyRaw = localStorage.getItem(this.legacyKey);
      if (legacyRaw) {
        const legacyParsed = JSON.parse(legacyRaw);
        for (const [idStr, lc] of Object.entries(legacyParsed as Record<string, any>)) {
          const id = Number(idStr);
          const card = createEmptyCard(new Date());
          if (lc.due) card.due = new Date(lc.due);
          if (lc.last_review) card.last_review = new Date(lc.last_review);
          if (lc.reps) card.reps = lc.reps;
          card.state = lc.state === 2 ? State.Review : (lc.state === 1 ? State.Learning : State.New);
          this.cards.set(id, card);
        }
        this.save();
      }
    } catch (e) {
      console.warn('Failed to parse SRS cards, resetting to empty:', e);
    }
  }

  private save() {
    try {
      const obj: Record<number, Card> = {};
      for (const [id, card] of this.cards.entries()) {
        obj[id] = card;
      }
      localStorage.setItem(this.storageKey, JSON.stringify(obj));
    } catch (e) {
      console.error('Failed to save SRS data to localStorage:', e);
    }
  }

  getCard(kanjiId: number): Card {
    const existing = this.cards.get(kanjiId);
    if (existing) return existing;
    const fresh = createEmptyCard(new Date());
    this.cards.set(kanjiId, fresh);
    return fresh;
  }

  isDue(kanjiId: number): boolean {
    const card = this.cards.get(kanjiId);
    if (!card || !card.last_review) return false;
    return new Date(card.due).getTime() <= Date.now();
  }

  isUnseen(kanjiId: number): boolean {
    const card = this.cards.get(kanjiId);
    return !card || !card.last_review;
  }

  rateCard(kanjiId: number, rating: Rating, now: Date = new Date()): RecordLogItem {
    const current: Card = this.getCard(kanjiId);
    const scheduling = this.f.repeat(current, now);
    let record: RecordLogItem;

    switch (rating) {
      case Rating.Again:
        record = scheduling[Rating.Again];
        break;
      case Rating.Hard:
        record = scheduling[Rating.Hard];
        break;
      case Rating.Good:
        record = scheduling[Rating.Good];
        break;
      case Rating.Easy:
        record = scheduling[Rating.Easy];
        break;
      default:
        record = scheduling[Rating.Good];
    }

    this.cards.set(kanjiId, record.card);
    this.save();
    return record;
  }

  getDeckStats(deckName: CurriculumDeck): DeckStats {
    const items = getDeck(deckName);
    const now = Date.now();
    let mature = 0;
    let learning = 0;
    let due = 0;
    let unseen = 0;

    for (const item of items) {
      const card = this.cards.get(item.id);
      if (!card || !card.last_review) {
        unseen++;
      } else {
        if (new Date(card.due).getTime() <= now) {
          due++;
        }
        if (card.state === State.Review) {
          mature++;
        } else {
          learning++;
        }
      }
    }

    const reviewedCount = mature + learning;
    const retentionRate = reviewedCount > 0 ? (mature / reviewedCount) * 100 : 100;

    return {
      total: items.length,
      mature,
      learning,
      due,
      unseen,
      retentionRate: Math.round(retentionRate * 10) / 10,
    };
  }

  getAllDueKanjiIds(deckName: CurriculumDeck): number[] {
    const items = getDeck(deckName);
    const now = Date.now();
    return items
      .filter(item => {
        const card = this.cards.get(item.id);
        return card && card.last_review && new Date(card.due).getTime() <= now;
      })
      .map(item => item.id);
  }

  exportData(): string {
    const obj: Record<number, Card> = {};
    for (const [id, card] of this.cards.entries()) {
      obj[id] = card;
    }
    return JSON.stringify({
      version: 2,
      algorithm: 'FSRS-v5',
      exportedAt: new Date().toISOString(),
      cards: obj,
    }, null, 2);
  }

  importData(jsonString: string): boolean {
    try {
      const data = JSON.parse(jsonString);
      if (!data.cards || typeof data.cards !== 'object') return false;

      this.cards.clear();
      for (const [idStr, c] of Object.entries(data.cards as Record<string, any>)) {
        this.cards.set(Number(idStr), {
          ...c,
          due: new Date(c.due),
          last_review: c.last_review ? new Date(c.last_review) : undefined,
        });
      }
      this.save();
      return true;
    } catch {
      return false;
    }
  }
}

export const srsManager = new SrsManager();
