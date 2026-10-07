import type { CurriculumDeck } from '../types/kanji';
import { srsManager, type DeckStats } from '../services/srs';

export type ScreenName = 'menu' | 'study' | 'quiz' | 'review' | 'settings' | 'dictionary';

class AppState {
  currentScreen = $state<ScreenName>('menu');
  currentDeck = $state<CurriculumDeck>('N5');
  theme = $state<'light' | 'dark'>('dark');
  revision = $state(0); // bump to trigger reactive re-computation of srs stats
  isSearchOpen = $state(false);
  targetKanjiId = $state<number | null>(null);

  constructor() {
    if (typeof window !== 'undefined') {
      let savedDeck = localStorage.getItem('kansu_level');
      if (savedDeck) {
        if (savedDeck === 'Top 250') savedDeck = 'freq250';
        else if (savedDeck === 'Top 500') savedDeck = 'freq500';
        else if (savedDeck === 'Top 1000') savedDeck = 'freq1000';
        else if (savedDeck === 'Top 2500') savedDeck = 'freq2500';
        this.currentDeck = savedDeck as CurriculumDeck;
      }

      const savedTheme = localStorage.getItem('kansu_theme') as 'light' | 'dark';
      const initialTheme = savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      this.setTheme(initialTheme);
    }
  }

  setScreen(screen: ScreenName) {
    this.currentScreen = screen;
  }

  openSearch() {
    this.isSearchOpen = true;
  }

  closeSearch() {
    this.isSearchOpen = false;
  }

  jumpToKanji(id: number, deck?: CurriculumDeck) {
    if (deck) {
      this.currentDeck = deck;
    }
    this.targetKanjiId = id;
    this.currentScreen = 'study';
    this.isSearchOpen = false;
  }

  setDeck(deck: CurriculumDeck) {
    this.currentDeck = deck;
    if (typeof window !== 'undefined') {
      localStorage.setItem('kansu_level', deck);
    }
    this.revision++;
  }

  setTheme(theme: 'light' | 'dark') {
    this.theme = theme;
    if (typeof window !== 'undefined') {
      localStorage.setItem('kansu_theme', theme);
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
        document.documentElement.setAttribute('data-theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        document.documentElement.setAttribute('data-theme', 'light');
      }
    }
  }

  toggleTheme() {
    this.setTheme(this.theme === 'dark' ? 'light' : 'dark');
  }

  refreshStats() {
    this.revision++;
  }

  get stats(): DeckStats {
    // reading this.revision establishes reactivity
    void this.revision;
    return srsManager.getDeckStats(this.currentDeck);
  }
}

export const appState = new AppState();
