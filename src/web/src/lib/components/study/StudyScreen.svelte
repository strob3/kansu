<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { getDeck } from '../../data';
  import { ArrowLeft, ArrowRight } from '@lucide/svelte';

  const deck = $derived(getDeck(appState.currentDeck));
  let currentIndex = $state(0);

  // sync card index when jumping from search palette
  $effect(() => {
    if (appState.targetKanjiId !== null) {
      const idx = deck.findIndex(k => k.id === appState.targetKanjiId);
      if (idx !== -1) {
        currentIndex = idx;
      }
      appState.targetKanjiId = null;
    }
  });

  const currentKanji = $derived(deck[currentIndex] || deck[0]);

  function prev() {
    if (currentIndex > 0) currentIndex--;
  }

  function next() {
    if (currentIndex < deck.length - 1) currentIndex++;
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'ArrowLeft' || e.key === 'h') prev();
    if (e.key === 'ArrowRight' || e.key === 'l') next();
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="max-w-3xl mx-auto space-y-6">
  <!-- nav header -->
  <div class="flex items-center justify-between bg-white dark:bg-[#1F2421] p-3 sm:p-4 rounded-2xl border border-[#E8E5DC] dark:border-[#28322B] shadow-xs">
    <button
      type="button"
      onclick={prev}
      disabled={currentIndex === 0}
      class="inline-flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold bg-[#273B2E] hover:bg-[#354E3E] text-white dark:bg-[#252A27] dark:text-[#EAE6DE] dark:border dark:border-[#2F332F] dark:hover:bg-[#2C332E] disabled:opacity-30 transition cursor-pointer"
    >
      <ArrowLeft class="w-4 h-4" />
      <span>Previous</span>
      <kbd class="hidden sm:inline-block px-1.5 py-0.5 rounded bg-[#354E3E] text-white dark:bg-[#1F2421] dark:text-[#8E8D84] text-[10px] font-mono ml-1">←</kbd>
    </button>

    <div class="text-xs sm:text-sm font-medium text-[#1A1C1A]/70 dark:text-[#8E8D84] font-mono">
      Card {currentIndex + 1} of {deck.length}
    </div>

    <button
      type="button"
      onclick={next}
      disabled={currentIndex === deck.length - 1}
      class="inline-flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold bg-[#273B2E] hover:bg-[#354E3E] text-white dark:bg-[#252A27] dark:text-[#EAE6DE] dark:border dark:border-[#2F332F] dark:hover:bg-[#2C332E] disabled:opacity-30 transition cursor-pointer"
    >
      <span>Next</span>
      <kbd class="hidden sm:inline-block px-1.5 py-0.5 rounded bg-[#354E3E] text-white dark:bg-[#1F2421] dark:text-[#8E8D84] text-[10px] font-mono mr-1">→</kbd>
      <ArrowRight class="w-4 h-4" />
    </button>
  </div>

  {#if currentKanji}
    <!-- main card -->
    <div class="bg-white dark:bg-[#1F2421] rounded-3xl p-8 sm:p-10 border border-[#E8E5DC] dark:border-[#28322B] shadow-sm relative">
      <!-- glyph & meaning -->
      <div class="text-center my-4">
        <div class="text-8xl sm:text-9xl font-black font-serif text-[#1A1C1A] dark:text-[#EAE6DE] tracking-tight mb-4 select-all">
          {currentKanji.character}
        </div>
        <div class="text-xl sm:text-2xl font-bold text-[#1A1C1A]/90 dark:text-[#D1CCC2]">
          {currentKanji.meaning}
        </div>
      </div>

      <!-- readings matrix -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 my-8">
        <div class="p-4 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F] text-center">
          <div class="text-[11px] font-bold uppercase tracking-wider text-[#755844] dark:text-[#8E8D84] mb-1">On'yomi</div>
          <div class="text-base font-semibold text-[#1A1C1A] dark:text-[#EAE6DE]">
            {currentKanji.onyomi || '—'}
          </div>
        </div>

        <div class="p-4 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F] text-center">
          <div class="text-[11px] font-bold uppercase tracking-wider text-[#755844] dark:text-[#8E8D84] mb-1">Kun'yomi</div>
          <div class="text-base font-semibold text-[#1A1C1A] dark:text-[#EAE6DE]">
            {currentKanji.kunyomi || '—'}
          </div>
        </div>

        <div class="p-4 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F] text-center">
          <div class="text-[11px] font-bold uppercase tracking-wider text-[#755844] dark:text-[#8E8D84] mb-1">Strokes / Level</div>
          <div class="text-base font-semibold text-[#1A1C1A] dark:text-[#EAE6DE]">
            {currentKanji.strokes} 画 · {currentKanji.level}
          </div>
        </div>
      </div>

      <!-- associated vocabulary -->
      <div class="pt-6 border-t border-[#E8E5DC] dark:border-[#28322B]">
        <h4 class="text-xs font-bold uppercase tracking-wider text-[#1A1C1A]/60 dark:text-[#6E736E] mb-3">
          Associated Vocabulary ({currentKanji.vocabulary.length})
        </h4>

        {#if currentKanji.vocabulary.length > 0}
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {#each currentKanji.vocabulary.slice(0, 6) as v}
              <div class="p-3.5 rounded-xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F]">
                <div class="flex items-baseline gap-2">
                  <span class="font-bold text-base text-[#1A1C1A] dark:text-[#EAE6DE]">{v.word}</span>
                  <span class="text-xs text-[#755844] dark:text-[#7A9A83] font-semibold">({v.reading})</span>
                </div>
                <div class="text-xs text-[#50514F] dark:text-[#9E9D95] mt-0.5">{v.meaning}</div>
              </div>
            {/each}
          </div>
        {:else}
          <p class="text-xs text-[#1A1C1A]/50 dark:text-[#6E736E] italic">No associated vocabulary entries available.</p>
        {/if}
      </div>
    </div>
  {/if}
</div>
