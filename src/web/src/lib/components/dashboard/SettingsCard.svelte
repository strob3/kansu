<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { ChevronRight } from '@lucide/svelte';
</script>

<div
  role="button"
  tabindex="0"
  onclick={() => appState.setScreen('settings')}
  onkeydown={(e) => e.key === 'Enter' && appState.setScreen('settings')}
  class="group col-span-1 rounded-2xl p-6 bg-white dark:bg-[#1F2421] border border-[#E8E5DC] dark:border-[#28322B] shadow-xs hover:border-[#4A6B56]/50 dark:hover:border-[#7A9A83]/50 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
>
  <div>
    <!-- top badge bar -->
    <div class="flex items-center justify-between mb-4">
      <span class="inline-flex items-center justify-center w-6 h-6 rounded-md bg-[#F4F2EC] text-[#50514F] dark:bg-[#252A27] dark:text-[#A5A49B] border border-[#DFD7C5] dark:border-[#2F332F] text-xs font-semibold font-mono">
        6
      </span>
    </div>

    <!-- title & desc -->
    <h3 class="text-xl font-bold text-[#1A1C1A] dark:text-[#EAE6DE] mb-1">
      Settings & Hotkeys
    </h3>
    <p class="text-xs text-[#50514F] dark:text-[#9E9D95] mb-4 leading-relaxed">
      Configure JLPT level, frequency tiers, and FSRS algorithm options.
    </p>
  </div>

  <!-- bottom link -->
  <div class="pt-4 mt-4 flex items-center justify-between text-xs text-[#1A1C1A] dark:text-[#9E9D95] group-hover:underline dark:group-hover:text-[#EAE6DE] font-semibold">
    <span>Open preferences</span>
    <ChevronRight class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
  </div>
</div>
