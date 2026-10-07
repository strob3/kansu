<script lang="ts">
  import { appState, type ScreenName } from '../../stores/app.svelte';
  import { formatDeckLabel } from '../../types/kanji';

  const screens: { id: ScreenName; label: string }[] = [
    { id: 'menu', label: 'Menu' },
    { id: 'study', label: 'Study' },
    { id: 'quiz', label: 'Quiz' },
    { id: 'review', label: 'Review' },
    { id: 'dictionary', label: 'Dictionary' },
    { id: 'settings', label: 'Settings' },
  ];
</script>

<header class="w-full bg-[#F5F3ED]/90 dark:bg-[#151A18]/90 backdrop-blur-md border-b border-[#E5E2D9] dark:border-[#232A26] sticky top-0 z-40 transition-colors">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
    <!-- brand & deck badge -->
    <div class="flex items-center gap-3">
      <button
        onclick={() => appState.setScreen('menu')}
        class="flex items-center gap-2.5 font-bold text-lg tracking-tight hover:opacity-85 transition cursor-pointer text-[#1A1C1A] dark:text-[#EAE6DE]"
      >
        <img src="/assets/logo.svg" alt="Kansu logo" class="w-8 h-8 rounded-lg shrink-0 object-contain" />
        <span class="hidden sm:inline">kansu</span>
        <span class="text-[#1A1C1A]/60 dark:text-[#8E8D84] font-normal text-sm">カンス</span>
      </button>

      <div class="h-4 w-px bg-[#E5E2D9] dark:bg-[#2A322C] hidden sm:block"></div>

      <!-- current deck pill -->
      <button
        onclick={() => appState.setScreen('settings')}
        class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-[#E8EFE9] hover:bg-[#DCE7DE] dark:bg-[#1F2421] dark:hover:bg-[#252A27] text-[#273B2E] dark:text-[#B4B3AC] transition cursor-pointer border border-[#D2DDD4] dark:border-[#2A322C]"
        title="Change curriculum deck"
      >
        <span>{formatDeckLabel(appState.currentDeck)}</span>
      </button>
    </div>

    <!-- navigation tabs & external links -->
    <div class="flex items-center gap-2 sm:gap-3">
      <nav class="flex items-center gap-1 text-xs sm:text-sm font-medium">
        <!-- search trigger in navbar -->
        <button
          type="button"
          onclick={() => appState.openSearch()}
          class="p-1 sm:p-1.5 rounded-lg text-[#50514F] hover:text-[#1A1C1A] dark:text-[#8E8D84] dark:hover:text-[#EAE6DE] hover:bg-[#EBE7DF] dark:hover:bg-[#252A27] transition cursor-pointer"
          title="Search kanji (Ctrl+K or /)"
          aria-label="Search kanji"
        >
          <svg class="w-4 h-4 stroke-current" fill="none" viewBox="0 0 24 24" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </svg>
        </button>

        {#each screens as s}
          <button
            class="px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-lg transition-all cursor-pointer {appState.currentScreen === s.id ? 'bg-[#273B2E] text-white dark:bg-[#425347] dark:text-[#EAE6DE] shadow-xs font-medium' : 'text-[#50514F] dark:text-[#8E8D84] hover:text-[#1A1C1A] dark:hover:text-[#EAE6DE] hover:bg-[#EBE7DF] dark:hover:bg-[#252A27]'}"
            onclick={() => appState.setScreen(s.id)}
          >
            {s.label}
          </button>
        {/each}
      </nav>

      <a
        href="https://github.com/strob3/kansu"
        target="_blank"
        rel="noopener noreferrer"
        class="p-2 text-[#50514F] hover:text-[#1A1C1A] dark:text-[#8E8D84] dark:hover:text-[#EAE6DE] transition rounded-lg hover:bg-[#EBE7DF] dark:hover:bg-[#252A27]"
        aria-label="GitHub Repository"
      >
        <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
          <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
        </svg>
      </a>
    </div>
  </div>
</header>
