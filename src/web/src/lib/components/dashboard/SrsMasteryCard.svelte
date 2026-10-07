<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { formatDeckLabel } from '../../types/kanji';

  const stats = $derived(appState.stats);
  const progressPercent = $derived(
    stats.total > 0 ? Math.min(100, Math.round(((stats.mature + stats.learning) / stats.total) * 100)) : 0
  );
</script>

<div class="col-span-1 rounded-2xl p-6 sm:p-7 bg-white dark:bg-[#1F2421] border border-[#E8E5DC] dark:border-[#28322B] shadow-xs flex flex-col justify-between">
  <div>
    <!-- top badge row -->
    <div class="flex items-center justify-between mb-4">
      <span class="text-xs font-bold uppercase tracking-wider text-[#1A1C1A]/70 dark:text-[#6E736E]">
        SRS Mastery
      </span>
      <div class="flex items-center gap-1.5">
        <span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-[#E8EFE9] text-[#273B2E] border border-[#D2DDD4] dark:bg-[#232C26] dark:text-[#7A9A83] dark:border-[#334137]">
          {stats.retentionRate}% Retained
        </span>
        <span class="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-[#F4F2EC] text-[#50514F] border border-[#DFD7C5] dark:bg-[#252A27] dark:text-[#8E8D84] dark:border-[#2F332F]">
          FSRS-v5
        </span>
      </div>
    </div>

    <!-- progress numbers -->
    <div class="flex items-baseline justify-between mb-2">
      <div>
        <span class="text-xs text-[#1A1C1A]/60 dark:text-[#6E736E]">Deck Progress ({formatDeckLabel(appState.currentDeck)})</span>
        <div class="flex items-baseline gap-1 mt-1">
          <span class="text-3xl font-extrabold text-[#1A1C1A] dark:text-[#EAE6DE] tracking-tight">
            {stats.mature + stats.learning}
          </span>
          <span class="text-xs text-[#1A1C1A]/60 dark:text-[#6E736E]">/ {stats.total} Kanji</span>
        </div>
      </div>
      <div class="text-right">
        <span class="text-[11px] text-[#1A1C1A]/60 dark:text-[#6E736E]">Target Retention</span>
        <div class="text-base font-bold text-[#273B2E] dark:text-[#7A9A83]">90.0%</div>
      </div>
    </div>

    <!-- multi-segment progress bar -->
    <div class="w-full h-2 rounded-full bg-[#F4F2EC] dark:bg-[#252A27] overflow-hidden flex my-4">
      {#if stats.total > 0}
        <div
          class="bg-[#273B2E] dark:bg-[#7A9A83] h-full transition-all duration-500"
          style="width: {(stats.mature / stats.total) * 100}%"
          title="Mature: {stats.mature}"
        ></div>
        <div
          class="bg-[#456651] dark:bg-[#687E96] h-full transition-all duration-500"
          style="width: {(stats.learning / stats.total) * 100}%"
          title="Learning: {stats.learning}"
        ></div>
        <div
          class="bg-[#8C6D58] dark:bg-[#C87D55] h-full transition-all duration-500"
          style="width: {(stats.due / stats.total) * 100}%"
          title="Due Now: {stats.due}"
        ></div>
      {/if}
    </div>

    <!-- 4 stats pips -->
    <div class="grid grid-cols-2 gap-y-2.5 gap-x-2 text-xs pt-1">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-[#273B2E] dark:bg-[#7A9A83]"></span>
        <span class="text-[#1A1C1A]/70 dark:text-[#8E8D84]">Mature:</span>
        <span class="font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">{stats.mature}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-[#456651] dark:bg-[#687E96]"></span>
        <span class="text-[#1A1C1A]/70 dark:text-[#8E8D84]">Learning:</span>
        <span class="font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">{stats.learning}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-[#8C6D58] dark:bg-[#C87D55]"></span>
        <span class="text-[#1A1C1A]/70 dark:text-[#8E8D84]">Due Now:</span>
        <span class="font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">{stats.due}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-[#DFD7C5] dark:bg-[#505551]"></span>
        <span class="text-[#1A1C1A]/70 dark:text-[#8E8D84]">Unseen:</span>
        <span class="font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">{stats.unseen}</span>
      </div>
    </div>
  </div>

  <div class="pt-4 mt-4 border-t border-[#E8E5DC] dark:border-[#28322B] flex items-center justify-between text-[11px] text-[#1A1C1A]/60 dark:text-[#6E736E]">
    <span class="font-mono">Next interval: +4.2d</span>
  </div>
</div>
