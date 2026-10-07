<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { getDeck } from '../../data';
  import { srsManager, Rating } from '../../services/srs';
  import { CheckCircle2, XCircle } from '@lucide/svelte';
  import type { KanjiItem } from '../../types/kanji';

  let deck = $derived(getDeck(appState.currentDeck));
  let dueQueue = $state<KanjiItem[]>([]);
  let currentIdx = $state(0);
  let userInput = $state('');
  let isAnswered = $state(false);
  let isCorrect = $state(false);
  let inputEl = $state<HTMLInputElement | null>(null);

  // initialize or reset queue
  $effect(() => {
    // pick queue based on due or all deck
    const dueIds = new Set(srsManager.getAllDueKanjiIds(appState.currentDeck));
    const items = dueIds.size > 0 
      ? deck.filter(k => dueIds.has(k.id)) 
      : [...deck].sort(() => 0.5 - Math.random()).slice(0, 20);
    dueQueue = items;
    currentIdx = 0;
    resetStep();
  });

  const currentCard = $derived(dueQueue[currentIdx]);

  function resetStep() {
    userInput = '';
    isAnswered = false;
    isCorrect = false;
    setTimeout(() => inputEl?.focus(), 50);
  }

  function handleInput(e: Event) {
    userInput = (e.target as HTMLInputElement).value;
  }

  function checkAnswer() {
    if (!currentCard || isAnswered) return;
    const cleanInput = userInput.trim().toLowerCase();
    const accepted = currentCard.meaning.toLowerCase().split('/').map(s => s.trim());
    isCorrect = accepted.some(m => m === cleanInput || cleanInput.includes(m));
    isAnswered = true;
  }

  function submitRating(rating: Rating) {
    if (!currentCard) return;
    srsManager.rateCard(currentCard.id, rating);
    appState.refreshStats();

    if (currentIdx < dueQueue.length - 1) {
      currentIdx++;
      resetStep();
    } else {
      // quiz complete
      appState.setScreen('menu');
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (!isAnswered) {
      if (e.key === 'Enter') checkAnswer();
    } else {
      if (e.key === '1') submitRating(Rating.Again);
      if (e.key === '2') submitRating(Rating.Hard);
      if (e.key === '3') submitRating(Rating.Good);
      if (e.key === '4') submitRating(Rating.Easy);
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="max-w-xl mx-auto space-y-6">
  <!-- quiz header status -->
  <div class="flex items-center justify-between bg-white dark:bg-[#1F2421] px-4 py-3 rounded-2xl border border-[#E8E5DC] dark:border-[#28322B] shadow-xs">
    <div class="text-xs font-semibold text-[#1A1C1A] dark:text-[#EAE6DE]">
      Meaning Recall Quiz
    </div>

    <div class="text-xs font-mono text-[#1A1C1A]/60 dark:text-[#8E8D84]">
      {dueQueue.length > 0 ? `${currentIdx + 1} / ${dueQueue.length}` : '0 / 0'}
    </div>
  </div>

  {#if currentCard}
    <!-- question card -->
    <div class="bg-white dark:bg-[#1F2421] rounded-3xl p-8 sm:p-10 border border-[#E8E5DC] dark:border-[#28322B] shadow-sm text-center relative">
      <!-- kanji character -->
      <div class="text-8xl sm:text-9xl font-black font-serif text-[#1A1C1A] dark:text-[#EAE6DE] mb-6">
        {currentCard.character}
      </div>

      {#if !isAnswered}
        <!-- input area -->
        <div class="max-w-xs mx-auto space-y-3">
          <input
            bind:this={inputEl}
            type="text"
            value={userInput}
            oninput={handleInput}
            placeholder="Enter English meaning..."
            class="w-full text-center text-lg font-medium px-4 py-3 rounded-2xl bg-[#FBF9F3] dark:bg-[#252A27] border border-[#DFD7C5] dark:border-[#2F332F] text-[#1A1C1A] dark:text-[#EAE6DE] placeholder:text-[#1A1C1A]/40 dark:placeholder:text-[#6E736E] focus:outline-none focus:ring-2 focus:ring-[#273B2E]/30 dark:focus:ring-[#7A9A83]/30"
          />
          <button
            type="button"
            onclick={checkAnswer}
            class="w-full py-2.5 rounded-xl bg-[#273B2E] hover:bg-[#354E3E] text-white dark:bg-[#7A9A83] dark:hover:bg-[#8CB399] dark:text-[#111412] font-semibold text-sm shadow-xs cursor-pointer transition"
          >
            Check Answer (Enter)
          </button>
        </div>
      {:else}
        <!-- answer reveal & srs buttons -->
        <div class="space-y-6">
          <div class="p-4 rounded-2xl {isCorrect ? 'bg-[#E8EFE9] dark:bg-[#1E2B22] border border-[#D2DDD4] dark:border-[#2D3E32] text-[#273B2E] dark:text-[#7A9A83]' : 'bg-[#F5ECE5] dark:bg-[#383229] border border-[#E8D9CE] dark:border-[#543F32] text-[#755844] dark:text-[#D59B6A]'}">
            <div class="flex items-center justify-center gap-2 font-bold text-base mb-1">
              {#if isCorrect}
                <CheckCircle2 class="w-5 h-5 text-[#273B2E] dark:text-[#7A9A83]" />
                <span>Correct!</span>
              {:else}
                <XCircle class="w-5 h-5 text-[#8C6D58] dark:text-[#D59B6A]" />
                <span>Revealed</span>
              {/if}
            </div>
            <div class="text-lg font-bold text-[#1A1C1A] dark:text-[#EAE6DE] mt-2">
              {currentCard.meaning}
            </div>
            <div class="text-xs text-[#50514F] dark:text-[#8E8D84] mt-1 font-mono">
              On: {currentCard.onyomi || '—'}  |  Kun: {currentCard.kunyomi || '—'}
            </div>
          </div>

          <!-- 4-button fsrs rating bar -->
          <div>
            <div class="text-xs font-semibold uppercase tracking-wider text-[#1A1C1A]/70 dark:text-[#8E8D84] mb-2">
              Rate your recall (1 - 4):
            </div>
            <div class="grid grid-cols-4 gap-2">
              <button
                type="button"
                onclick={() => submitRating(Rating.Again)}
                class="p-2.5 rounded-xl bg-[#FBF0ED] hover:bg-[#F5DFDA] dark:bg-[#382725] dark:hover:bg-[#483230] text-[#8F3528] dark:text-[#E58B82] border border-[#EFC6BF] dark:border-[#543936] text-xs font-bold cursor-pointer transition"
              >
                <div>[1] Again</div>
                <div class="text-[10px] font-normal opacity-70">1 min</div>
              </button>
              <button
                type="button"
                onclick={() => submitRating(Rating.Hard)}
                class="p-2.5 rounded-xl bg-[#FDF4EB] hover:bg-[#F8E7D6] dark:bg-[#382F24] dark:hover:bg-[#483D2F] text-[#8C5D2C] dark:text-[#E5B676] border border-[#F2D7BE] dark:border-[#544634] text-xs font-bold cursor-pointer transition"
              >
                <div>[2] Hard</div>
                <div class="text-[10px] font-normal opacity-70">5 min</div>
              </button>
              <button
                type="button"
                onclick={() => submitRating(Rating.Good)}
                class="p-2.5 rounded-xl bg-[#EDF5F0] hover:bg-[#DCEDE1] dark:bg-[#213328] dark:hover:bg-[#2C4436] text-[#27613D] dark:text-[#7EB893] border border-[#BEDEC8] dark:border-[#344F3F] text-xs font-bold cursor-pointer transition"
              >
                <div>[3] Good</div>
                <div class="text-[10px] font-normal opacity-70">1 day</div>
              </button>
              <button
                type="button"
                onclick={() => submitRating(Rating.Easy)}
                class="p-2.5 rounded-xl bg-[#EBF3F5] hover:bg-[#D7E9EC] dark:bg-[#1E3038] dark:hover:bg-[#273E48] text-[#245D69] dark:text-[#78B4C4] border border-[#BFDFE5] dark:border-[#2F4A57] text-xs font-bold cursor-pointer transition"
              >
                <div>[4] Easy</div>
                <div class="text-[10px] font-normal opacity-70">4 days</div>
              </button>
            </div>
          </div>
        </div>
      {/if}
    </div>
  {:else}
    <div class="text-center py-16 bg-white dark:bg-[#1F2421] rounded-3xl border border-[#E8E5DC] dark:border-[#28322B] p-8">
      <h3 class="text-xl font-bold text-[#1A1C1A] dark:text-[#EAE6DE] mb-2">No Cards Due!</h3>
      <p class="text-sm text-[#50514F] dark:text-[#9E9D95] mb-6">You are completely caught up on your SRS reviews.</p>
      <button
        type="button"
        onclick={() => appState.setScreen('menu')}
        class="px-5 py-2.5 rounded-xl bg-[#273B2E] hover:bg-[#354E3E] text-white dark:bg-[#7A9A83] dark:hover:bg-[#8CB399] dark:text-[#111412] font-semibold text-sm cursor-pointer shadow-xs"
      >
        Return to Menu
      </button>
    </div>
  {/if}
</div>
