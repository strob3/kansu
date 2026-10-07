<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { getDeck } from '../../data';
  import { ChevronRight } from '@lucide/svelte';

  const deck = $derived(getDeck(appState.currentDeck));
  const previewKanji = $derived(deck[1] || deck[0]);
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
        2
      </span>
      <span class="px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-[#E8EFE9] text-[#273B2E] border border-[#D2DDD4] dark:bg-[#293232] dark:text-[#8CB3A8] dark:border-[#354545]">
        Acc: 94.2%
      </span>
    </div>

    <!-- title & desc -->
    <h3 class="text-xl font-bold text-[#1A1C1A] dark:text-[#EAE6DE] flex items-baseline gap-2 mb-1">
      Quiz Mode <span class="text-sm font-normal text-[#1A1C1A]/60 dark:text-[#6E736E]">「試験」</span>
    </h3>
    <p class="text-xs text-[#50514F] dark:text-[#9E9D95] mb-5 leading-relaxed">
      Active recall test with dynamic FSRS interval weighting.
    </p>

    <!-- interactive prompt preview box -->
    {#if previewKanji}
      <div class="rounded-xl p-3.5 bg-[#FBF9F3] dark:bg-[#252A27] border border-[#E8E5DC] dark:border-[#2F332F] flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-white dark:bg-[#181C1A] border border-[#DFD7C5] dark:border-[#2F332F] font-bold text-xl flex items-center justify-center text-[#1A1C1A] dark:text-[#EAE6DE] shadow-2xs">
            {previewKanji.character}
          </div>
          <div>
            <div class="text-[10px] text-[#1A1C1A]/60 dark:text-[#6E736E] uppercase tracking-wider font-semibold">Prompt: Onyomi</div>
            <div class="text-xs font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">
              {previewKanji.onyomi || previewKanji.meaning.split('/')[0]}
            </div>
          </div>
        </div>

        <span class="text-[11px] font-semibold text-[#50514F] bg-[#F4F2EC] border border-[#DFD7C5] dark:text-[#9E9D95] dark:bg-[#252A27] dark:border-[#38433C] px-2 py-1 rounded">
          Quick Test
        </span>
      </div>
    {/if}
  </div>

  <!-- bottom link -->
  <div class="pt-4 mt-4 flex items-center justify-between text-xs text-[#1A1C1A] dark:text-[#9E9D95] group-hover:underline dark:group-hover:text-[#EAE6DE] font-semibold">
    <span>Launch quiz test</span>
    <ChevronRight class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
  </div>
</div>
