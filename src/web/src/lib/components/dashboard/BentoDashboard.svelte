<script lang="ts">
  import HeroStudyCard from './HeroStudyCard.svelte';
  import SrsMasteryCard from './SrsMasteryCard.svelte';
  import ReviewDueCard from './ReviewDueCard.svelte';
  import QuizModeCard from './QuizModeCard.svelte';
  import StatisticsCard from './StatisticsCard.svelte';
  import DictionaryCard from './DictionaryCard.svelte';
  import SettingsCard from './SettingsCard.svelte';
</script>

<div class="grid grid-cols-1 lg:grid-cols-3 gap-5 sm:gap-6">
  <!-- row 1: hero study (2 cols) + srs mastery (1 col) -->
  <HeroStudyCard />
  <SrsMasteryCard />

  <!-- row 2: quiz mode (1 col) + review due (1 col) + statistics (1 col) -->
  <QuizModeCard />
  <ReviewDueCard />
  <StatisticsCard />

  <!-- row 3: dictionary (2 cols) + settings (1 col) -->
  <DictionaryCard />
  <SettingsCard />
</div>
