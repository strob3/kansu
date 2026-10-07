<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { getDeck, deckCounts } from '../../data';
  import { ArrowRight, BookOpen } from '@lucide/svelte';

  const deck = $derived(getDeck(appState.currentDeck));
  const count = $derived(deckCounts[appState.currentDeck]);
  // sample kanji preview items from current deck
  const sampleKanji = $derived(deck.slice(0, 3));
</script>

<div
  role="button"
  tabindex="0"
  onclick={() => appState.setScreen('study')}
  onkeydown={(e) => e.key === 'Enter' && appState.setScreen('study')}
  class="group relative col-span-1 lg:col-span-2 rounded-2xl p-6 sm:p-7 bg-white dark:bg-[#1F2421] border border-[#E8E5DC] dark:border-[#28322B] shadow-xs hover:border-[#4A6B56]/50 dark:hover:border-[#7A9A83]/50 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
>
  <div>
    <!-- top badge bar -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center justify-center w-6 h-6 rounded-md bg-[#F4F2EC] text-[#50514F] dark:bg-[#252A27] dark:text-[#A5A49B] border border-[#DFD7C5] dark:border-[#2F332F] text-xs font-semibold font-mono">
          1
        </span>
      </div>
      <span class="text-xs font-mono uppercase tracking-wider text-[#1A1C1A]/60 dark:text-[#6E736E]">
        {count} Kanji Loaded
      </span>
    </div>

    <!-- main title & desc -->
    <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-[#1A1C1A] dark:text-[#EAE6DE] flex items-baseline gap-2 mb-2">
      Study Mode <span class="text-base sm:text-lg font-normal text-[#1A1C1A]/60 dark:text-[#6E736E]">「学習」</span>
    </h2>
    <p class="text-sm text-[#50514F] dark:text-[#9E9D95] max-w-lg mb-6 leading-relaxed">
      Browse kanji, onyomi & kunyomi readings, stroke orders, and high-frequency contextual vocabulary.
    </p>

    <!-- kanji pill previews -->
    <div class="flex flex-wrap items-center gap-2 sm:gap-3 mb-6">
      {#each sampleKanji as k}
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#FBF9F3] dark:bg-[#181C1A] border border-[#E8E5DC] dark:border-[#28322B] text-xs">
          <span class="font-bold text-sm text-[#1A1C1A] dark:text-[#EAE6DE]">{k.character}</span>
          <span class="text-[#50514F] dark:text-[#8E8D84]">
            {k.kunyomi || k.onyomi || k.meaning.split('/')[0]}
          </span>
        </div>
      {/each}
    </div>
  </div>

  <!-- bottom cta bar -->
  <div class="pt-4 flex items-center justify-start">
    <button
      type="button"
      onclick={(e) => { e.stopPropagation(); appState.setScreen('study'); }}
      class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#273B2E] hover:bg-[#354E3E] text-white dark:bg-[#7A9A83] dark:hover:bg-[#8CB399] dark:text-[#111412] text-xs sm:text-sm font-semibold shadow-xs hover:shadow transition cursor-pointer"
    >
      <span>Start Browsing</span>
      <ArrowRight class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
    </button>
  </div>
</div>
