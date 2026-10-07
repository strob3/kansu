<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { allKanji, deckCounts } from '../../data';
  import { ArrowRight } from '@lucide/svelte';

  const levels = [
    { label: 'N5', count: deckCounts.N5 },
    { label: 'N4', count: deckCounts.N4 },
    { label: 'N3', count: deckCounts.N3 },
    { label: 'N2', count: deckCounts.N2 },
    { label: 'N1', count: deckCounts.N1 },
  ];
</script>

<div
  role="button"
  tabindex="0"
  onclick={() => appState.setScreen('dictionary')}
  onkeydown={(e) => e.key === 'Enter' && appState.setScreen('dictionary')}
  class="group col-span-1 lg:col-span-2 rounded-2xl p-6 bg-white dark:bg-[#1F2421] border border-[#E8E5DC] dark:border-[#28322B] shadow-xs hover:border-[#4A6B56]/50 dark:hover:border-[#7A9A83]/50 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
>
  <div>
    <!-- top badge bar -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center justify-center w-6 h-6 rounded-md bg-[#F4F2EC] text-[#50514F] dark:bg-[#252A27] dark:text-[#A5A49B] border border-[#DFD7C5] dark:border-[#2F332F] text-xs font-semibold font-mono">
          5
        </span>
      </div>
      <span class="text-xs font-mono uppercase tracking-wider text-[#1A1C1A]/60 dark:text-[#6E736E]">
        {allKanji.length} Kanji Catalog
      </span>
    </div>

    <!-- title & desc -->
    <h3 class="text-xl sm:text-2xl font-bold tracking-tight text-[#1A1C1A] dark:text-[#EAE6DE] flex items-baseline gap-2 mb-1">
      Dictionary <span class="text-base font-normal text-[#1A1C1A]/60 dark:text-[#6E736E]">「辞書」</span>
    </h3>
    <p class="text-xs sm:text-sm text-[#50514F] dark:text-[#9E9D95] mb-4 leading-relaxed max-w-xl">
      Browse complete kanji catalog across all JLPT levels with instant search, stroke counts, and readings.
    </p>

  </div>

  <!-- bottom cta bar -->
  <div class="pt-4 mt-4 flex items-center justify-between text-xs text-[#50514F] dark:text-[#8E8D84] font-semibold">
    <div class="inline-flex items-center gap-1.5 text-[#273B2E] dark:text-[#7A9A83] group-hover:underline transition-transform">
      <span>Browse Dictionary</span>
      <ArrowRight class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
    </div>
  </div>
</div>
