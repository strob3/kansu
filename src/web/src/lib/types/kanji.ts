export interface ExampleItem {
  japanese: string;
  english: string;
}

export interface VocabItem {
  id: number;
  word: string;
  reading: string;
  meaning: string;
  examples: ExampleItem[];
}

export interface KanjiItem {
  id: number;
  character: string;
  meaning: string;
  onyomi: string;
  kunyomi: string;
  level: 'N5' | 'N4' | 'N3' | 'N2' | 'N1';
  strokes: number;
  grade: number | null;
  frequency: number | null;
  vocabulary: VocabItem[];
}

export type JLPTLevel = 'N5' | 'N4' | 'N3' | 'N2' | 'N1';
export type FrequencyDeck = 'freq250' | 'freq500' | 'freq1000' | 'freq2500';
export type CurriculumDeck = JLPTLevel | FrequencyDeck;

export function formatDeckLabel(deck: CurriculumDeck): string {
  if (deck.startsWith('freq')) {
    return `FREQ ${deck.slice(4)}`;
  }
  return `JLPT ${deck}`;
}
