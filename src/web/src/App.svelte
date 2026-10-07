<script lang="ts">
  import { appState } from './lib/stores/app.svelte';
  import Header from './lib/components/layout/Header.svelte';
  import HotkeyBar from './lib/components/layout/HotkeyBar.svelte';
  import BentoDashboard from './lib/components/dashboard/BentoDashboard.svelte';
  import StudyScreen from './lib/components/study/StudyScreen.svelte';
  import QuizScreen from './lib/components/quiz/QuizScreen.svelte';
  import ReviewScreen from './lib/components/review/ReviewScreen.svelte';
  import SettingsScreen from './lib/components/settings/SettingsScreen.svelte';
  import DictionaryScreen from './lib/components/dictionary/DictionaryScreen.svelte';
  import CommandPalette from './lib/components/common/CommandPalette.svelte';

  function handleKeydown(e: KeyboardEvent) {
    const activeEl = document.activeElement;
    const isInput = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA');

    // global search hotkeys: ctrl+k, cmd+k, or / when not focused in an input
    if ((e.key === 'k' && (e.ctrlKey || e.metaKey)) || (!isInput && e.key === '/')) {
      e.preventDefault();
      if (appState.isSearchOpen) {
        appState.closeSearch();
      } else {
        appState.openSearch();
      }
      return;
    }

    if (e.key === 'Escape') {
      if (appState.isSearchOpen) {
        appState.closeSearch();
        return;
      }
      if (isInput) (activeEl as HTMLElement).blur();
      if (appState.currentScreen !== 'menu') {
        appState.setScreen('menu');
      }
      return;
    }

    if (isInput || appState.isSearchOpen) return;

    if (appState.currentScreen === 'menu') {
      if (e.key === '1') appState.setScreen('study');
      if (e.key === '2') appState.setScreen('quiz');
      if (e.key === '3') appState.setScreen('quiz');
      if (e.key === '4') appState.setScreen('review');
      if (e.key === '5') appState.setScreen('dictionary');
      if (e.key === '6') appState.setScreen('settings');
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="min-h-screen bg-[#F5F3ED] dark:bg-[#111412] dark:dark-grid-bg text-[#1A1C1A] dark:text-[#EAE6DE] flex flex-col font-sans transition-colors antialiased pb-20">
  <Header />

  <main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 sm:py-8">
    {#if appState.currentScreen === 'menu'}
      <BentoDashboard />
    {:else if appState.currentScreen === 'dictionary'}
      <DictionaryScreen />
    {:else if appState.currentScreen === 'study'}
      <StudyScreen />
    {:else if appState.currentScreen === 'quiz'}
      <QuizScreen />
    {:else if appState.currentScreen === 'review'}
      <ReviewScreen />
    {:else if appState.currentScreen === 'settings'}
      <SettingsScreen />
    {/if}
  </main>

  <HotkeyBar />
  <CommandPalette />
</div>
