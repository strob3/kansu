<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { deckCounts } from '../../data';
  import { formatDeckLabel } from '../../types/kanji';
  import { ArrowRight } from '@lucide/svelte';

  const stats = $derived(appState.stats);
  const total = $derived(deckCounts[appState.currentDeck]);
</script>

<div class="max-w-2xl mx-auto space-y-6">
  <div class="bg-white dark:bg-[#1F2421] rounded-3xl p-6 sm:p-8 border border-[#E8E5DC] dark:border-[#28322B] shadow-xs">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-xl font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">
        Curriculum Mastery: {formatDeckLabel(appState.currentDeck)}
      </h3>
      <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#E8EFE9] text-[#273B2E] border border-[#D2DDD4] dark:bg-[#232C26] dark:text-[#7A9A83] dark:border-[#334137]">
        {stats.retentionRate}% Retained
      </span>
    </div>

    <!-- stat grid -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 my-6">
      <div class="p-4 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F]">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#273B2E] dark:text-[#7A9A83]">Mature</div>
        <div class="text-2xl font-black text-[#1A1C1A] dark:text-[#EAE6DE] font-mono mt-1">{stats.mature}</div>
      </div>

      <div class="p-4 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F]">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#456651] dark:text-[#687E96]">Learning</div>
        <div class="text-2xl font-black text-[#1A1C1A] dark:text-[#EAE6DE] font-mono mt-1">{stats.learning}</div>
      </div>

      <div class="p-4 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F]">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#8C6D58] dark:text-[#C87D55]">Due Now</div>
        <div class="text-2xl font-black text-[#1A1C1A] dark:text-[#EAE6DE] font-mono mt-1">{stats.due}</div>
      </div>

      <div class="p-4 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F]">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#50514F] dark:text-[#8E8D84]">Unseen</div>
        <div class="text-2xl font-black text-[#1A1C1A] dark:text-[#EAE6DE] font-mono mt-1">{stats.unseen}</div>
      </div>
    </div>

    <div class="pt-4 border-t border-[#E8E5DC] dark:border-[#28322B] flex items-center justify-between">
      <span class="text-xs text-[#1A1C1A]/70 dark:text-[#8E8D84]">Total in deck: {total} Kanji</span>
      <button
        type="button"
        onclick={() => appState.setScreen('quiz')}
        class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#273B2E] hover:bg-[#354E3E] text-white dark:bg-[#7A9A83] dark:hover:bg-[#8CB399] dark:text-[#111412] text-xs font-semibold shadow-xs transition cursor-pointer"
      >
        <span>Start Review Queue</span>
        <ArrowRight class="w-4 h-4" />
      </button>
    </div>
  </div>
</div>
