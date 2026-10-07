import { allKanji } from '../data';
import type { KanjiItem } from '../types/kanji';

export interface SearchResult {
  kanji: KanjiItem;
  matchType: 'character' | 'meaning' | 'reading';
}

// pre-normalize kanji for fast multi-field matching
const searchIndex = allKanji.map(item => ({
  item,
  charLower: item.character.toLowerCase(),
  meaningLower: item.meaning.toLowerCase(),
  onyomiLower: item.onyomi.toLowerCase(),
  kunyomiLower: item.kunyomi.toLowerCase(),
}));

export function searchKanji(query: string, limit: number = 20): SearchResult[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];

  const results: SearchResult[] = [];

  for (const entry of searchIndex) {
    if (entry.charLower === q) {
      results.unshift({ kanji: entry.item, matchType: 'character' });
    } else if (entry.charLower.includes(q)) {
      results.push({ kanji: entry.item, matchType: 'character' });
    } else if (entry.meaningLower.includes(q)) {
      results.push({ kanji: entry.item, matchType: 'meaning' });
    } else if (entry.onyomiLower.includes(q) || entry.kunyomiLower.includes(q)) {
      results.push({ kanji: entry.item, matchType: 'reading' });
    }

    if (results.length >= limit) break;
  }

  return results;
}
