<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { ChevronRight } from '@lucide/svelte';

  const stats = $derived(appState.stats);
</script>

<div
  role="button"
  tabindex="0"
  onclick={() => appState.setScreen('review')}
  onkeydown={(e) => e.key === 'Enter' && appState.setScreen('review')}
  class="group col-span-1 rounded-2xl p-6 bg-white dark:bg-[#1F2421] border border-[#E8E5DC] dark:border-[#28322B] shadow-xs hover:border-[#4A6B56]/50 dark:hover:border-[#7A9A83]/50 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
>
  <div>
    <!-- top badge bar -->
    <div class="flex items-center justify-between mb-4">
      <span class="inline-flex items-center justify-center w-6 h-6 rounded-md bg-[#F4F2EC] text-[#50514F] dark:bg-[#252A27] dark:text-[#A5A49B] border border-[#DFD7C5] dark:border-[#2F332F] text-xs font-semibold font-mono">
        4
      </span>
    </div>

    <!-- title & desc -->
    <h3 class="text-xl font-bold text-[#1A1C1A] dark:text-[#EAE6DE] mb-1">
      Deck Statistics
    </h3>
    <p class="text-xs text-[#50514F] dark:text-[#9E9D95] mb-5 leading-relaxed">
      Visual SRS learning curves, stability, and difficulty scores.
    </p>

    <!-- visual sparkline / bar graph mockup -->
    <div class="rounded-xl p-3 bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F] flex items-center justify-between">
      <div class="flex items-end gap-1.5 h-10 px-2">
        <div class="w-2 rounded-t bg-[#273B2E]/30 dark:bg-[#252A27] h-4"></div>
        <div class="w-2 rounded-t bg-[#273B2E]/50 dark:bg-[#292F2B] h-7"></div>
        <div class="w-2 rounded-t bg-[#273B2E]/70 dark:bg-[#7A9A83] h-9"></div>
        <div class="w-2 rounded-t bg-[#273B2E] dark:bg-[#9BB8A4] h-6"></div>
        <div class="w-2 rounded-t bg-[#4A6B56] dark:bg-[#7A9A83] h-8"></div>
      </div>
      <div class="text-right">
        <div class="text-[10px] uppercase font-semibold text-[#1A1C1A]/60 dark:text-[#6E736E]">Total Kanji</div>
        <div class="text-sm font-extrabold text-[#1A1C1A] dark:text-[#EAE6DE] font-mono">
          {stats.total} <span class="text-xs font-normal text-[#1A1C1A]/60 dark:text-[#6E736E]">Cards</span>
        </div>
      </div>
    </div>
  </div>

  <!-- bottom link -->
  <div class="pt-4 mt-4 flex items-center justify-between text-xs text-[#1A1C1A] dark:text-[#9E9D95] group-hover:underline dark:group-hover:text-[#EAE6DE] font-semibold">
    <span>Statistics</span>
    <ChevronRight class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
  </div>
</div>
