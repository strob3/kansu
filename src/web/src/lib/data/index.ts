import type { KanjiItem, CurriculumDeck, JLPTLevel } from '../types/kanji';
import rawKanji from './kanji.json';

export const allKanji: KanjiItem[] = rawKanji as KanjiItem[];

// fast lookup map by id and character
export const kanjiById = new Map<number, KanjiItem>(allKanji.map(k => [k.id, k]));
export const kanjiByChar = new Map<string, KanjiItem>(allKanji.map(k => [k.character, k]));

// pre-sorted frequency kanji list
const freqSorted = allKanji
  .filter(k => k.frequency !== null && k.frequency > 0)
  .sort((a, b) => (a.frequency ?? 99999) - (b.frequency ?? 99999));

// precomputed deck lists
export const decks: Record<CurriculumDeck, KanjiItem[]> = {
  N5: allKanji.filter(k => k.level === 'N5'),
  N4: allKanji.filter(k => k.level === 'N4'),
  N3: allKanji.filter(k => k.level === 'N3'),
  N2: allKanji.filter(k => k.level === 'N2'),
  N1: allKanji.filter(k => k.level === 'N1'),
  freq250: freqSorted.filter(k => (k.frequency ?? 99999) <= 250),
  freq500: freqSorted.filter(k => (k.frequency ?? 99999) <= 500),
  freq1000: freqSorted.filter(k => (k.frequency ?? 99999) <= 1000),
  freq2500: freqSorted.filter(k => (k.frequency ?? 99999) <= 2500),
};

export const deckCounts: Record<CurriculumDeck, number> = {
  N5: decks.N5.length,
  N4: decks.N4.length,
  N3: decks.N3.length,
  N2: decks.N2.length,
  N1: decks.N1.length,
  freq250: decks.freq250.length,
  freq500: decks.freq500.length,
  freq1000: decks.freq1000.length,
  freq2500: decks.freq2500.length,
};

export function getDeck(deck: CurriculumDeck): KanjiItem[] {
  return decks[deck] || decks.N5;
}
