<script lang="ts">
  import { appState } from '../../stores/app.svelte';
  import { srsManager } from '../../services/srs';
  import { deckCounts } from '../../data';
  import type { CurriculumDeck } from '../../types/kanji';
  import { Download, Upload, Trash2, Sun, Moon, Laptop } from '@lucide/svelte';

  const decks: { id: CurriculumDeck; label: string; sub: string; tag?: string }[] = [
    { id: 'N5', label: 'JLPT N5', sub: '初級入門', tag: 'N5' },
    { id: 'N4', label: 'JLPT N4', sub: '初級', tag: 'N4' },
    { id: 'N3', label: 'JLPT N3', sub: '中級', tag: 'N3' },
    { id: 'N2', label: 'JLPT N2', sub: '中上級', tag: 'N2' },
    { id: 'N1', label: 'JLPT N1', sub: '上級', tag: 'N1' },
    { id: 'freq250', label: 'FREQ 250', sub: '最頻出', tag: '頻度' },
    { id: 'freq500', label: 'FREQ 500', sub: '頻出', tag: '頻度' },
    { id: 'freq1000', label: 'FREQ 1000', sub: '中頻度', tag: '頻度' },
    { id: 'freq2500', label: 'FREQ 2500', sub: '全頻度', tag: '頻度' },
  ];

  let fileInput = $state<HTMLInputElement | null>(null);
  let importSuccess = $state(false);

  let hasInteracted = $state(false);

  function handleToggle() {
    hasInteracted = true;
    appState.toggleTheme();
  }

  function exportBackup() {
    const json = srsManager.exportData();
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `kansu-backup-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function handleImport(e: Event) {
    const files = (e.target as HTMLInputElement).files;
    if (!files || files.length === 0) return;
    const file = files[0];
    const reader = new FileReader();
    reader.onload = () => {
      const content = reader.result as string;
      const ok = srsManager.importData(content);
      if (ok) {
        importSuccess = true;
        appState.refreshStats();
        setTimeout(() => (importSuccess = false), 3000);
      } else {
        alert('Invalid backup file format');
      }
    };
    reader.readAsText(file);
  }
</script>

<div class="max-w-2xl mx-auto space-y-6">
  <!-- curriculum level -->
  <div class="bg-white dark:bg-[#1F2421] rounded-3xl p-6 sm:p-8 border border-[#E8E5DC] dark:border-[#28322B] shadow-xs">
    <div class="flex items-center gap-2 mb-1">
      <h3 class="text-lg font-bold text-[#1A1C1A] dark:text-[#EAE6DE]">
        Curriculum Deck
      </h3>
    </div>
    <p class="text-xs text-[#50514F] dark:text-[#9E9D95] mb-5">
      Select your primary study deck. Review progress is tracked independently per kanji.
    </p>

    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
      {#each decks as d}
        <button
          type="button"
          onclick={() => appState.setDeck(d.id)}
          class="p-3.5 rounded-2xl border text-left transition cursor-pointer flex flex-col justify-between {appState.currentDeck === d.id ? 'bg-[#273B2E] text-white border-[#273B2E] shadow-xs' : 'bg-[#FBF9F3] dark:bg-[#252A27] border-[#E8E5DC] dark:border-[#2F332F] text-[#1A1C1A] dark:text-[#B4B3AC] hover:bg-[#F5F2EB] dark:hover:bg-[#2C332E] dark:hover:text-[#EAE6DE]'}"
        >
          <div class="flex items-center justify-between">
            <div class="text-xs font-bold">{d.label}</div>
            {#if appState.currentDeck === d.id}
              <span class="w-1.5 h-1.5 rounded-full bg-[#7A9A83]"></span>
            {:else if d.tag}
              <span class="text-[10px] font-mono text-[#1A1C1A]/50 dark:text-[#6E736E]">{d.tag}</span>
            {/if}
          </div>
          <div class="flex items-center justify-between mt-3 text-[11px] {appState.currentDeck === d.id ? 'text-white/80' : 'text-[#1A1C1A]/60 dark:text-[#6E736E]'}">
            <span>{deckCounts[d.id]} cards</span>
            <span class="font-normal">{d.sub}</span>
          </div>
        </button>
      {/each}
    </div>
  </div>

  <!-- appearance / theme toggle -->
  <div class="bg-white dark:bg-[#1F2421] rounded-3xl p-6 sm:p-8 border border-[#E8E5DC] dark:border-[#28322B] shadow-xs flex items-center justify-between">
    <div>
      <h3 class="text-lg font-bold text-[#1A1C1A] dark:text-[#EAE6DE] mb-1">
        Theme
      </h3>
      <p class="text-xs text-[#50514F] dark:text-[#9E9D95]">
        Toggle between light and dark display modes.
      </p>
    </div>

    <div class="flex items-center gap-3">
      <span class="text-xs font-semibold text-[#1A1C1A] dark:text-[#EAE6DE] capitalize flex items-center gap-1.5">
        {#if appState.theme === 'dark'}
          <Moon class="w-3.5 h-3.5 text-[#7A9A83]" />
          <span></span>
        {:else}
          <Sun class="w-3.5 h-3.5 text-[#8C6D58]" />
          <span></span>
        {/if}
      </span>

      <button
        type="button"
        role="switch"
        aria-checked={appState.theme === 'dark'}
        aria-label="Toggle theme"
        data-on={appState.theme === 'dark' ? 'true' : 'false'}
        class="t-toggle {hasInteracted ? 'is-init' : ''} relative inline-flex items-center w-[38px] h-[22px] rounded-full p-[2.5px] cursor-pointer transition-colors border {appState.theme === 'dark' ? 'bg-[#2A332C] border-[#38453B]' : 'bg-[#DFD7C5] border-[#D0C7B3]'}"
        onclick={handleToggle}
      >
        <span class="t-toggle-thumb block w-[17px] h-[17px] rounded-full shadow-xs {appState.theme === 'dark' ? 'bg-[#7A9A83]' : 'bg-white'}"></span>
      </button>
    </div>
  </div>

  <!-- backup & restore -->
  <div class="bg-white dark:bg-[#1F2421] rounded-3xl p-6 sm:p-8 border border-[#E8E5DC] dark:border-[#28322B] shadow-xs">
    <h3 class="text-lg font-bold text-[#1A1C1A] dark:text-[#EAE6DE] mb-1">
      Data Backup & Sync
    </h3>
    <p class="text-xs text-[#50514F] dark:text-[#9E9D95] mb-5">
      Export your FSRS intervals and review history to JSON, or restore progress across devices.
    </p>

    <div class="flex flex-wrap items-center gap-3">
      <button
        type="button"
        onclick={exportBackup}
        class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#FDFCFB] hover:bg-[#F5F3ED] text-xs font-semibold text-[#1A1C1A] border border-[#DFD7C5] dark:bg-[#252A27] dark:hover:bg-[#2C332E] dark:text-[#EAE6DE] dark:border-[#2F332F] transition cursor-pointer"
      >
        <Download class="w-4 h-4" />
        <span>Export JSON Backup</span>
      </button>

      <button
        type="button"
        onclick={() => fileInput?.click()}
        class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#273B2E] hover:bg-[#354E3E] text-xs font-semibold text-white dark:bg-[#7A9A83] dark:hover:bg-[#8CB399] dark:text-[#111412] shadow-xs transition cursor-pointer"
      >
        <Upload class="w-4 h-4" />
        <span>Import Backup</span>
      </button>

      <input
        bind:this={fileInput}
        type="file"
        accept=".json"
        onchange={handleImport}
        class="hidden"
      />

      {#if importSuccess}
        <span class="text-xs font-semibold text-emerald-600 dark:text-emerald-400">
          ✓ Restored successfully!
        </span>
      {/if}
    </div>
  </div>
</div>
