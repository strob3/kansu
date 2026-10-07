<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { searchKanji, type SearchResult } from '../../services/search';
  import { Search, X, CornerDownLeft, ArrowUp, ArrowDown } from '@lucide/svelte';

  let query = $state('');
  let selectedIndex = $state(0);
  let inputEl = $state<HTMLInputElement | null>(null);

  const results = $derived(searchKanji(query, 25));

  // focus input when palette opens
  $effect(() => {
    if (appState.isSearchOpen) {
      query = '';
      selectedIndex = 0;
      setTimeout(() => inputEl?.focus(), 50);
    }
  });

  // keep selectedIndex in bounds
  $effect(() => {
    if (selectedIndex >= results.length) {
      selectedIndex = Math.max(0, results.length - 1);
    }
  });

  function selectResult(item: SearchResult) {
    appState.jumpToKanji(item.kanji.id, item.kanji.level);
  }

  let resultsContainer = $state<HTMLDivElement | null>(null);

  function scrollSelectedIntoView() {
    if (!resultsContainer) return;
    const items = resultsContainer.querySelectorAll<HTMLButtonElement>('button[data-idx]');
    const activeItem = items[selectedIndex];
    if (activeItem) {
      activeItem.scrollIntoView({ block: 'nearest' });
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (!appState.isSearchOpen) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      e.stopPropagation();
      appState.closeSearch();
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (selectedIndex < results.length - 1) {
        selectedIndex++;
        scrollSelectedIntoView();
      }
      return;
    }

    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (selectedIndex > 0) {
        selectedIndex--;
        scrollSelectedIntoView();
      }
      return;
    }

    if (e.key === 'Enter') {
      e.preventDefault();
      if (results[selectedIndex]) {
        selectResult(results[selectedIndex]);
      }
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

{#if appState.isSearchOpen}
  <!-- backdrop modal -->
  <div
    role="presentation"
    onclick={(e) => { if (e.target === e.currentTarget) appState.closeSearch(); }}
    class="fixed inset-0 z-50 bg-zinc-950/50 backdrop-blur-xs flex items-start justify-center pt-16 sm:pt-24 px-4 p-4"
  >
    <!-- palette modal box -->
    <div
      role="dialog"
      aria-modal="true"
      tabindex="-1"
      class="w-full max-w-xl bg-white dark:bg-[#1F2421] rounded-2xl shadow-2xl border border-[#E8E5DC] dark:border-[#28322B] overflow-hidden flex flex-col max-h-[75vh]"
    >
      <!-- search bar input -->
      <div class="flex items-center gap-3 px-4 py-3.5 border-b border-[#E8E5DC] dark:border-[#28322B]">
        <Search class="w-5 h-5 text-[#50514F] dark:text-[#8E8D84] shrink-0" />
        <input
          bind:this={inputEl}
          type="text"
          bind:value={query}
          placeholder="Search by kanji (水), meaning (water), or reading (mizu)"
          class="flex-1 bg-transparent text-sm sm:text-base font-medium text-[#1A1C1A] dark:text-[#EAE6DE] placeholder:text-[#1A1C1A]/40 dark:placeholder:text-[#6E736E] focus:outline-none"
        />
        {#if query}
          <button
            type="button"
            onclick={() => { query = ''; inputEl?.focus(); }}
            class="p-1 rounded-md text-[#50514F] hover:text-[#1A1C1A] dark:text-[#8E8D84] dark:hover:text-[#EAE6DE] cursor-pointer"
          >
            <X class="w-4 h-4" />
          </button>
        {/if}
        <kbd class="hidden sm:inline-block px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#F4F2EC] dark:bg-[#252A27] text-[#50514F] dark:text-[#8E8D84] border border-[#DFD7C5] dark:border-[#38433C]">
          ESC
        </kbd>
      </div>

      <!-- search results list -->
      {#if results.length > 0}
        <div
          bind:this={resultsContainer}
          class="flex-1 overflow-y-auto divide-y divide-[#E8E5DC]/70 dark:divide-[#28322B] p-2 border-b border-[#E8E5DC] dark:border-[#28322B]"
        >
          {#each results as res, idx}
            <button
              type="button"
              data-idx={idx}
              onclick={() => selectResult(res)}
              onmouseenter={() => (selectedIndex = idx)}
              class="w-full text-left p-3 rounded-xl flex items-center justify-between gap-3 transition cursor-pointer {selectedIndex === idx ? 'bg-[#273B2E] text-white dark:bg-[#252A27] dark:text-[#EAE6DE] dark:border dark:border-[#38433C] shadow-xs' : 'hover:bg-[#FBF9F3] dark:hover:bg-[#252A27] text-[#1A1C1A] dark:text-[#B4B3AC]'}"
            >
              <div class="flex items-center gap-3 min-w-0">
                <!-- glyph badge -->
                <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xl font-bold font-serif shrink-0 border {selectedIndex === idx ? 'bg-[#354E3E] text-white border-[#456651] dark:bg-[#181C1A] dark:text-[#7A9A83] dark:border-[#38433C]' : 'bg-[#F4F2EC] dark:bg-[#181C1A] text-[#1A1C1A] dark:text-[#EAE6DE] border-[#E8E5DC] dark:border-[#28322B]'}">
                  {res.kanji.character}
                </div>

                <!-- meaning and readings -->
                <div class="min-w-0">
                  <div class="font-semibold text-sm truncate flex items-center gap-2">
                    <span>{res.kanji.meaning}</span>
                    <span class="px-1.5 py-0.5 rounded text-[10px] font-mono font-medium shrink-0 {selectedIndex === idx ? 'bg-[#E8EFE9] text-[#273B2E] dark:bg-[#181C1A] dark:text-[#7A9A83]' : 'bg-[#E8EFE9] text-[#273B2E] dark:bg-[#181C1A] dark:text-[#8E8D84] dark:border dark:border-[#28322B]'}">
                      {res.kanji.level}
                    </span>
                  </div>
                  <div class="text-xs truncate mt-0.5 {selectedIndex === idx ? 'text-white/80 dark:text-[#8E8D84]' : 'text-[#50514F] dark:text-[#8E8D84]'}">
                    On: {res.kanji.onyomi || '—'} · Kun: {res.kanji.kunyomi || '—'}
                  </div>
                </div>
              </div>

              {#if selectedIndex === idx}
                <div class="flex items-center gap-1 text-[11px] text-[#7A9A83] dark:text-[#7A9A83] font-medium shrink-0">
                  <span>Open</span>
                  <CornerDownLeft class="w-3.5 h-3.5" />
                </div>
              {/if}
            </button>
          {/each}       
        </div>
      {/if}

      <!-- palette footer instructions -->
      <div class="px-4 py-2.5 bg-[#FBF9F3] dark:bg-[#181C1A] flex items-center justify-between text-[11px] text-[#50514F] dark:text-[#6E736E]">
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1">
            <kbd class="px-1 py-0.5 rounded bg-[#F4F2EC] dark:bg-[#252A27] border border-[#DFD7C5] dark:border-[#38433C] font-mono text-[9px] text-[#1A1C1A] dark:text-[#EAE6DE]">↑</kbd>
            <kbd class="px-1 py-0.5 rounded bg-[#F4F2EC] dark:bg-[#252A27] border border-[#DFD7C5] dark:border-[#38433C] font-mono text-[9px] text-[#1A1C1A] dark:text-[#EAE6DE]">↓</kbd>
            <span>Navigate</span>
          </div>
          <div class="flex items-center gap-1">
            <kbd class="px-1 py-0.5 rounded bg-[#F4F2EC] dark:bg-[#252A27] border border-[#DFD7C5] dark:border-[#38433C] font-mono text-[9px] text-[#1A1C1A] dark:text-[#EAE6DE]">↵</kbd>
            <span>Select</span>
          </div>
        </div>

        <div>
          <span>{results.length} results</span>
        </div>
      </div>
    </div>
  </div>
{/if}
