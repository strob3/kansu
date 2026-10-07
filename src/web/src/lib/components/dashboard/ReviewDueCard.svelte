<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { ChevronRight, Check } from '@lucide/svelte';

  const stats = $derived(appState.stats);
  const isUpToDate = $derived(stats.due === 0);
</script>

<div
  role="button"
  tabindex="0"
  onclick={() => appState.setScreen('quiz')}
  onkeydown={(e) => e.key === 'Enter' && appState.setScreen('quiz')}
  class="group col-span-1 rounded-2xl p-6 bg-white dark:bg-[#1F2421] border border-[#E8E5DC] dark:border-[#28322B] shadow-xs hover:border-[#4A6B56]/50 dark:hover:border-[#7A9A83]/50 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
>
  <div>
    <!-- top badge bar -->
    <div class="flex items-center justify-between mb-4">
      <span class="inline-flex items-center justify-center w-6 h-6 rounded-md bg-[#F4F2EC] text-[#50514F] dark:bg-[#252A27] dark:text-[#A5A49B] border border-[#DFD7C5] dark:border-[#2F332F] text-xs font-semibold font-mono">
        3
      </span>
      {#if isUpToDate}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-[#E8EFE9] text-[#273B2E] border border-[#D2DDD4] dark:bg-[#232C26] dark:text-[#7A9A83] dark:border-[#334137]">
          <Check class="w-3 h-3" />
          <span>Up to date</span>
        </span>
      {:else}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-[#F5ECE5] text-[#755844] border border-[#E8D9CE] dark:bg-[#383229] dark:text-[#D59B6A] dark:border-[#543F32]">
          <span>{stats.due} Due</span>
        </span>
      {/if}
    </div>

    <!-- title & desc -->
    <h3 class="text-xl font-bold text-[#1A1C1A] dark:text-[#EAE6DE] mb-1">
      Review Due
    </h3>
    <p class="text-xs text-[#50514F] dark:text-[#9E9D95] mb-5 leading-relaxed">
      Check and reinforce cards scheduled for review today.
    </p>

    <!-- center status callout -->
    <div class="rounded-xl p-4 bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F] flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg {isUpToDate ? 'bg-[#E8EFE9] text-[#273B2E] dark:bg-[#232C26] dark:text-[#7A9A83]' : 'bg-[#E8D9CE] text-[#755844] dark:bg-[#463B30] dark:text-[#D59B6A]'} font-bold flex items-center justify-center text-lg font-mono">
        {stats.due}
      </div>
      <div>
        <div class="text-xs font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">
          {isUpToDate ? 'All caught up!' : `${stats.due} Cards Pending`}
        </div>
        <div class="text-[11px] text-[#50514F] dark:text-[#8E8D84]">
          {isUpToDate ? 'No cards pending review' : 'Ready for active recall'}
        </div>
      </div>
    </div>
  </div>

  <!-- bottom link -->
  <div class="pt-4 mt-4 flex items-center justify-between text-xs text-[#1A1C1A] dark:text-[#9E9D95] group-hover:underline dark:group-hover:text-[#EAE6DE] font-semibold">
    <span>Open review queue</span>
    <ChevronRight class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
  </div>
</div>
