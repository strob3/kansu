<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { allKanji } from '../../data';
  import type { JLPTLevel } from '../../types/kanji';
  import { Search, X } from '@lucide/svelte';

  type FilterLevel = 'all' | JLPTLevel;

  const levelRank: Record<JLPTLevel, number> = {
    N5: 1,
    N4: 2,
    N3: 3,
    N2: 4,
    N1: 5,
  };

  // kanji pre-sorted from n5 going down to n1
  const sortedKanji = [...allKanji].sort((a, b) => {
    const rankDiff = (levelRank[a.level] || 99) - (levelRank[b.level] || 99);
    if (rankDiff !== 0) return rankDiff;
    return a.id - b.id;
  });

  const levelCounts: Record<FilterLevel, number> = {
    all: sortedKanji.length,
    N5: sortedKanji.filter(k => k.level === 'N5').length,
    N4: sortedKanji.filter(k => k.level === 'N4').length,
    N3: sortedKanji.filter(k => k.level === 'N3').length,
    N2: sortedKanji.filter(k => k.level === 'N2').length,
    N1: sortedKanji.filter(k => k.level === 'N1').length,
  };

  let activeFilter = $state<FilterLevel>('all');
  let searchQuery = $state('');

  const filterButtons: { id: FilterLevel; label: string }[] = [
    { id: 'all', label: 'All' },
    { id: 'N5', label: 'N5' },
    { id: 'N4', label: 'N4' },
    { id: 'N3', label: 'N3' },
    { id: 'N2', label: 'N2' },
    { id: 'N1', label: 'N1' },
  ];

  // filter by level and query
  const filteredList = $derived(
    sortedKanji.filter(k => {
      if (activeFilter !== 'all' && k.level !== activeFilter) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.trim().toLowerCase();
        return (
          k.character.includes(q) ||
          k.meaning.toLowerCase().includes(q) ||
          k.onyomi.toLowerCase().includes(q) ||
          k.kunyomi.toLowerCase().includes(q)
        );
      }
      return true;
    })
  );

  function handleTileClick(id: number, level: JLPTLevel) {
    appState.jumpToKanji(id, level);
  }
</script>

<div class="space-y-6">
  <!-- header control bar -->
  <div class="bg-white dark:bg-[#1F2421] rounded-2xl p-4 border border-[#E8E5DC] dark:border-[#28322B] shadow-xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
    <!-- level filter pills -->
    <div class="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
      {#each filterButtons as btn}
        <button
          type="button"
          onclick={() => (activeFilter = btn.id)}
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition cursor-pointer border {activeFilter === btn.id ? 'bg-[#273B2E] text-white border-[#273B2E] dark:bg-[#7A9A83] dark:text-[#111412] dark:border-[#7A9A83] shadow-xs' : 'bg-[#FBF9F3] dark:bg-[#252A27] hover:bg-[#F5F2EB] dark:hover:bg-[#2C332E] text-[#1A1C1A] dark:text-[#B4B3AC] dark:hover:text-[#EAE6DE] border-[#E8E5DC] dark:border-[#2F332F]'}"
        >
          <span>{btn.label}</span>
          <span class="text-[10px] opacity-70 font-mono">
            {levelCounts[btn.id]}
          </span>
        </button>
      {/each}
    </div>

    <!-- instant search input -->
    <div class="relative w-full sm:w-64">
      <Search class="w-4 h-4 text-[#50514F] dark:text-[#8E8D84] absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Filter by kanji, meaning..."
        class="w-full pl-9 pr-8 py-1.5 rounded-xl text-xs bg-[#FBF9F3] dark:bg-[#252A27] border border-[#DFD7C5] dark:border-[#2F332F] text-[#1A1C1A] dark:text-[#EAE6DE] placeholder:text-[#1A1C1A]/40 dark:placeholder:text-[#6E736E] focus:outline-none focus:ring-2 focus:ring-[#273B2E]/30 dark:focus:ring-[#7A9A83]/30"
      />
      {#if searchQuery}
        <button
          type="button"
          onclick={() => (searchQuery = '')}
          class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#50514F] hover:text-[#1A1C1A] dark:text-[#8E8D84] dark:hover:text-[#EAE6DE] cursor-pointer"
        >
          <X class="w-3.5 h-3.5" />
        </button>
      {/if}
    </div>
  </div>

  <!-- total count indicator -->
  <div class="flex items-center justify-between text-xs text-[#1A1C1A]/60 dark:text-[#8E8D84] px-1">
    <span>Showing {filteredList.length} of {sortedKanji.length} kanji</span>
    <span>Click any tile to open in Study Mode</span>
  </div>

  <!-- kanji tiles grid -->
  {#if filteredList.length > 0}
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
      {#each filteredList as item (item.id)}
        <button
          type="button"
          onclick={() => handleTileClick(item.id, item.level)}
          class="group p-4 rounded-2xl bg-white dark:bg-[#1F2421] border border-[#E8E5DC] dark:border-[#28322B] hover:border-[#4A6B56]/50 dark:hover:border-[#7A9A83]/50 shadow-xs hover:shadow-md transition-all text-left flex flex-col justify-between cursor-pointer"
        >
          <!-- top row: kanji character and level -->
          <div class="flex items-start justify-between gap-2 mb-2">
            <span class="text-3xl font-black font-serif text-[#1A1C1A] dark:text-[#EAE6DE] group-hover:opacity-80 transition-opacity">
              {item.character}
            </span>
            <span class="px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-[#E8EFE9] text-[#273B2E] border border-[#D2DDD4] dark:bg-[#181C1A] dark:text-[#7A9A83] dark:border-[#28322B]">
              {item.level}
            </span>
          </div>

          <!-- bottom row: meaning only -->
          <div class="text-xs text-[#50514F] dark:text-[#9E9D95] line-clamp-2 leading-snug">
            {item.meaning}
          </div>
        </button>
      {/each}
    </div>
  {:else}
    <div class="text-center py-20 bg-white dark:bg-[#1F2421] rounded-3xl border border-[#E8E5DC] dark:border-[#28322B] p-8">
      <div class="text-sm font-semibold text-[#1A1C1A] dark:text-[#EAE6DE] mb-1">No kanji matched your search</div>
      <div class="text-xs text-[#50514F] dark:text-[#9E9D95]">Try searching for a different character or English meaning.</div>
    </div>
  {/if}
</div>
