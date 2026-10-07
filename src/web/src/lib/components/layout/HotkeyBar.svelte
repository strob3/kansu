<script lang="ts">
  import { appState, type ScreenName } from '../../stores/app.svelte';

  interface Hotkey {
    key: string;
    label: string;
  }

  // screen-specific footer shortcuts mapping
  const shortcutsByScreen: Record<ScreenName, Hotkey[]> = {
    menu: [
      { key: '1-6', label: 'Quick Select' },
      { key: '/', label: 'Search' },
    ],
    dictionary: [
      { key: '/', label: 'Search' },
      { key: 'Enter', label: 'Open' },
      { key: 'Esc', label: 'Menu' },
    ],
    study: [
      { key: '/', label: 'Search' },
      { key: 'Esc', label: 'Menu' },
    ],
    quiz: [
      { key: '/', label: 'Search' },
      { key: 'Esc', label: 'Menu' },
    ],
    review: [
      { key: '/', label: 'Search' },
      { key: 'Esc', label: 'Menu' },
    ],
    settings: [
      { key: '/', label: 'Search' },
      { key: 'Esc', label: 'Menu' },
    ],
  };

  const currentShortcuts = $derived(shortcutsByScreen[appState.currentScreen] || []);
</script>

{#if currentShortcuts.length > 0}
  <div class="fixed bottom-4 left-1/2 -translate-x-1/2 z-30 pointer-events-none">
    <div class="pointer-events-auto flex items-center gap-2 sm:gap-4 px-3 sm:px-4 py-2 rounded-full bg-white dark:bg-[#1F2421] backdrop-blur-md shadow-md border border-[#E5E2D9] dark:border-[#2F332F] text-[11px] sm:text-xs text-[#50514F] dark:text-[#8E8D84] font-medium">
      {#each currentShortcuts as item, i}
        {#if i > 0}
          <span class="text-[#1A1C1A]/20 dark:text-[#38433C]">|</span>
        {/if}
        <div class="flex items-center gap-1.5">
          <kbd class="px-1.5 py-0.5 rounded bg-[#F4F2EC] dark:bg-[#252A27] border border-[#DFD7C5] dark:border-[#38433C] font-mono text-[10px] text-[#1A1C1A] dark:text-[#EAE6DE]">{item.key}</kbd>
          <span>{item.label}</span>
        </div>
      {/each}
    </div>
  </div>
{/if}
