

class KansuApp {
  constructor() {
    this.currentScreen = 'menu';
    this.currentLevel = localStorage.getItem('kansu_level') || 'N5';
    this.theme = localStorage.getItem('kansu_theme') || 'system';
    this.menuIndex = 0;
    this.studyList = [];
    this.studyIndex = 0;
    this.currentKanjiDetail = null;
    this.quizMode = 'all'; // 'all' or 'due_only'
    this.currentQuiz = null;
    this.quizPhase = 'question'; // 'question', 'result', 'empty'
    this.lastKanjiId = null;

    this.init();
  }

  init() {
    const connEl = document.getElementById('footer-connection');
    if (connEl) {
      connEl.textContent = 'Client-Side (Offline Ready)';
    }

    this.bindEvents();
    this.applyTheme(this.theme);
    this.syncLevelUI();
    this.syncThemeUI();
    this.updateFooterShortcuts();
    this.updateMenuStats();
  }

  bindEvents() {
    window.addEventListener('keydown', (e) => this.handleKeyDown(e));
  }

  handleKeyDown(e) {
    const activeEl = document.activeElement;
    const isInput = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA');

    if (e.key === 'Escape') {
      if (isInput) activeEl.blur();
      if (this.currentScreen !== 'menu') {
        this.showScreen('menu');
      }
      return;
    }

    if (isInput) return;

    switch (this.currentScreen) {
      case 'menu':
        if (e.key === 'ArrowUp' || e.key === 'k') {
          e.preventDefault();
          this.menuUp();
        } else if (e.key === 'ArrowDown' || e.key === 'j') {
          e.preventDefault();
          this.menuDown();
        } else if (e.key === 'Enter') {
          e.preventDefault();
          this.menuSelect();
        } else if (e.key >= '1' && e.key <= '5') {
          e.preventDefault();
          this.menuSelectIndex(parseInt(e.key, 10) - 1);
        }
        break;

      case 'study':
        if (e.key === 'ArrowLeft' || e.key === 'h') {
          e.preventDefault();
          this.studyPrev();
        } else if (e.key === 'ArrowRight' || e.key === 'l') {
          e.preventDefault();
          this.studyNext();
        }
        break;

      case 'quiz':
        if (this.quizPhase === 'result') {
          if (['1', '2', '3', '4'].includes(e.key)) {
            e.preventDefault();
            this.submitRating(parseInt(e.key, 10));
          }
        }
        break;

      case 'review':
        if (e.key === 'Enter') {
          e.preventDefault();
          this.startQuiz('due_only');
        }
        break;
    }
  }

  showScreen(screenName) {
    this.currentScreen = screenName;

    document.querySelectorAll('.screen').forEach((el) => {
      el.classList.remove('active');
    });
    const target = document.getElementById(`screen-${screenName}`);
    if (target) {
      target.classList.add('active');
    }

    // sync nav buttons
    document.querySelectorAll('.nav-btn, .footer-nav-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.screen === screenName);
    });

    this.updateFooterShortcuts();

    if (screenName === 'study') {
      this.loadStudyDeck();
    } else if (screenName === 'review') {
      this.loadReviewStats();
    } else if (screenName === 'menu') {
      this.updateMenuStats();
    }
  }

  updateFooterShortcuts() {
    const footer = document.getElementById('footer-shortcuts');
    if (!footer) return;

    switch (this.currentScreen) {
      case 'menu':
        footer.textContent = '[↑/↓] Navigate | [1-5] Quick Select | [Enter] Open';
        break;
      case 'study':
        footer.textContent = '[←] Previous  [→] Next | [Esc] Menu';
        break;
      case 'quiz':
        if (this.quizPhase === 'result') {
          footer.textContent = '[1] Again  [2] Hard  [3] Good  [4] Easy | [Esc] Menu';
        } else {
          footer.textContent = '[Enter] Submit | [Esc] Menu';
        }
        break;
      case 'review':
        footer.textContent = '[Enter] Start Due Reviews | [Esc] Menu';
        break;
      case 'settings':
        footer.textContent = '[Esc] Menu';
        break;
    }
  }

  changeLevel(level) {
    this.currentLevel = level;
    localStorage.setItem('kansu_level', level);
    this.syncLevelUI();
    this.studyList = [];
    this.studyIndex = 0;

    if (this.currentScreen === 'study') {
      this.loadStudyDeck();
    } else if (this.currentScreen === 'review') {
      this.loadReviewStats();
    } else if (this.currentScreen === 'menu') {
      this.updateMenuStats();
    }
  }

  syncLevelUI() {
    const headerSelect = document.getElementById('header-level-select');
    if (headerSelect) {
      headerSelect.value = this.currentLevel;
    }
    const radio = document.querySelector(
      `input[name="deck-radio"][value="${this.currentLevel}"], input[name="level-radio"][value="${this.currentLevel}"]`
    );
    if (radio) {
      radio.checked = true;
    }
    const reviewLevel = document.getElementById('review-level-name');
    if (reviewLevel) {
      reviewLevel.textContent = this.currentLevel;
    }
  }

  setTheme(theme) {
    this.theme = theme;
    localStorage.setItem('kansu_theme', theme);
    this.applyTheme(theme);
    this.syncThemeUI();
  }

  applyTheme(theme) {
    if (theme === 'system') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', theme);
    }
  }

  syncThemeUI() {
    const radio = document.querySelector(`input[name="theme-radio"][value="${this.theme}"]`);
    if (radio) {
      radio.checked = true;
    }
  }

  menuUp() {
    const items = document.querySelectorAll('.menu-item');
    this.menuIndex = (this.menuIndex - 1 + items.length) % items.length;
    this.updateMenuHighlight();
  }

  menuDown() {
    const items = document.querySelectorAll('.menu-item');
    this.menuIndex = (this.menuIndex + 1) % items.length;
    this.updateMenuHighlight();
  }

  menuSelect() {
    this.menuSelectIndex(this.menuIndex);
  }

  menuSelectIndex(index) {
    this.menuIndex = index;
    this.updateMenuHighlight();
    const items = document.querySelectorAll('.menu-item');
    if (items[index]) {
      items[index].click();
    }
  }

  updateMenuHighlight() {
    const items = document.querySelectorAll('.menu-item');
    items.forEach((item, i) => {
      item.classList.toggle('active', i === this.menuIndex);
    });
  }

  // data and SRS helper methods

  getAllKanji() {
    if (window.KANSU_DATA && Array.isArray(window.KANSU_DATA)) {
      return window.KANSU_DATA;
    }
    return [];
  }

  getKanjiForLevel(level) {
    const all = this.getAllKanji();
    if (!level || level === 'All') return all;
    if (String(level).startsWith('Top ')) {
      const limit = parseInt(String(level).replace('Top ', ''), 10) || 2500;
      return all
        .filter((k) => k.frequency != null && k.frequency <= limit)
        .sort((a, b) => (a.frequency || 9999) - (b.frequency || 9999));
    }
    return all.filter((k) => k.level === level);
  }

  getLocalCards() {
    try {
      return JSON.parse(localStorage.getItem('kansu_srs_cards') || '{}');
    } catch (e) {
      return {};
    }
  }

  saveLocalCards(cards) {
    localStorage.setItem('kansu_srs_cards', JSON.stringify(cards));
  }

  getLocalCard(kanjiId) {
    const cards = this.getLocalCards();
    return cards[kanjiId] || null;
  }

  isLocalCardDue(card) {
    if (!card || !card.due) return false;
    return new Date(card.due) <= new Date();
  }

  getLocalStats(level) {
    const kanjiList = this.getKanjiForLevel(level);
    const cards = this.getLocalCards();
    let due = 0;
    let newCards = 0;
    let learning = 0;

    for (const k of kanjiList) {
      const card = cards[k.id];
      if (!card || !card.last_review) {
        newCards++;
      } else if (this.isLocalCardDue(card)) {
        due++;
      } else {
        learning++;
      }
    }

    return {
      due,
      new: newCards,
      learning,
      total: kanjiList.length,
    };
  }

  updateMenuStats() {
    const dueCount = this.getLocalStats(this.currentLevel).due;
    const dueDesc = document.getElementById('menu-due-count');
    if (dueDesc) {
      if (dueCount > 0) {
        dueDesc.textContent = `${dueCount} card${dueCount === 1 ? '' : 's'} ready for review`;
        dueDesc.style.color = 'var(--vibrant-danger)';
      } else {
        dueDesc.textContent = 'All caught up! (0 due)';
        dueDesc.style.color = 'var(--text-muted)';
      }
    }
  }

  // study mode

  loadStudyDeck() {
    const glyph = document.getElementById('study-glyph');
    if (glyph) glyph.textContent = '...';

    this.studyList = this.getKanjiForLevel(this.currentLevel);

    if (this.studyList.length === 0) {
      if (glyph) glyph.textContent = '-';
      document.getElementById('study-meaning').textContent = 'No kanji found for this level.';
      return;
    }

    if (this.studyIndex >= this.studyList.length) {
      this.studyIndex = 0;
    }
    this.renderStudyCard();
  }

  renderStudyCard() {
    if (!this.studyList || this.studyList.length === 0) return;
    const kanji = this.studyList[this.studyIndex];

    const cardEl = document.getElementById('study-card');
    if (cardEl) {
      cardEl.classList.remove('content-fade');
      void cardEl.offsetWidth;
      cardEl.classList.add('content-fade');
    }

    document.getElementById('study-counter').textContent = `Card ${this.studyIndex + 1} of ${this.studyList.length}`;
    document.getElementById('study-glyph').textContent = kanji.character;
    document.getElementById('study-meaning').textContent = kanji.meaning;
    document.getElementById('study-onyomi').textContent = kanji.onyomi || 'None';
    document.getElementById('study-kunyomi').textContent = kanji.kunyomi || 'None';
    const freqStr = kanji.frequency ? `Rank #${kanji.frequency}` : 'Unranked';
    const levelStr = kanji.level ? kanji.level : 'Unknown';
    document.getElementById('study-meta').textContent = `${kanji.strokes || '-'} strokes | ${levelStr} | ${freqStr}`;

    const vocabListEl = document.getElementById('study-vocab-list');
    const vocabulary = kanji.vocabulary || [];

    if (!vocabulary || vocabulary.length === 0) {
      vocabListEl.innerHTML = '<p class="empty-hint">No vocabulary entries found for this kanji.</p>';
      return;
    }

    vocabListEl.innerHTML = vocabulary.map((v) => {
      let examplesHtml = '';
      if (v.examples && v.examples.length > 0) {
        examplesHtml = `
          <div class="vocab-examples">
            <div class="vocab-example-ja">${this.escapeHtml(v.examples[0].japanese)}</div>
            <div class="vocab-example-en">${this.escapeHtml(v.examples[0].english)}</div>
          </div>
        `;
      }
      return `
        <div class="vocab-item">
          <div class="vocab-header">
            <span class="vocab-word">${this.escapeHtml(v.word)}</span>
            <span class="vocab-reading">${this.escapeHtml(v.reading || '')}</span>
          </div>
          <div class="vocab-meaning">${this.escapeHtml(v.meaning)}</div>
          ${examplesHtml}
        </div>
      `;
    }).join('');
  }

  studyNext() {
    if (!this.studyList.length) return;
    this.studyIndex = (this.studyIndex + 1) % this.studyList.length;
    this.renderStudyCard();
  }

  studyPrev() {
    if (!this.studyList.length) return;
    this.studyIndex = (this.studyIndex - 1 + this.studyList.length) % this.studyList.length;
    this.renderStudyCard();
  }

  // quiz mode

  startQuiz(mode = 'all') {
    this.quizMode = mode;
    this.showScreen('quiz');
    this.nextQuizQuestion();
  }

  async nextQuizQuestion() {
    this.quizPhase = 'question';
    this.updateFooterShortcuts();

    const qBox = document.getElementById('quiz-question-box');
    const rBox = document.getElementById('quiz-result-box');
    const eBox = document.getElementById('quiz-empty-box');

    qBox.classList.remove('hidden');
    rBox.classList.add('hidden');
    eBox.classList.add('hidden');

    const modeLabel = document.getElementById('quiz-mode-label');
    const deckName = this.currentLevel === 'All' ? 'All Kanji' : this.currentLevel;
    modeLabel.textContent = `${this.quizMode === 'due_only' ? 'Due Reviews Only' : 'All Cards'} • ${deckName}`;

    const input = document.getElementById('quiz-input');
    input.value = '';

    const local = this.chooseLocalNextQuiz(this.currentLevel, this.quizMode, this.lastKanjiId);
    const chosen = local.kanji;
    const counts = local.counts;

    if (!chosen) {
      this.quizPhase = 'empty';
      qBox.classList.add('hidden');
      eBox.classList.remove('hidden');
      const emptyMsg = document.getElementById('quiz-empty-message');
      if (this.quizMode === 'due_only') {
        emptyMsg.textContent = 'All scheduled reviews are complete! No cards are due right now.';
      } else {
        emptyMsg.textContent = 'No kanji found in this level to quiz.';
      }
      return;
    }

    this.currentQuiz = chosen;
    this.lastKanjiId = chosen.id;

    const glyphEl = document.getElementById('quiz-glyph');
    if (glyphEl) {
      glyphEl.textContent = chosen.character;
      glyphEl.classList.remove('glyph-fade');
      void glyphEl.offsetWidth;
      glyphEl.classList.add('glyph-fade');
    }
    const queueInfo = document.getElementById('quiz-queue-info');
    queueInfo.textContent = `Due: ${counts.due} | New: ${counts.new} | Learning: ${counts.learning}`;

    setTimeout(() => {
      input.focus();
    }, 50);
  }

  chooseLocalNextQuiz(level, mode, previousId) {
    const kanjiList = this.getKanjiForLevel(level);
    const cards = this.getLocalCards();
    const newCards = [];
    const dueCards = [];
    const futureCards = [];

    for (const k of kanjiList) {
      const card = cards[k.id];
      if (!card || !card.last_review) {
        newCards.append ? newCards.append(k) : newCards.push(k);
      } else if (this.isLocalCardDue(card)) {
        dueCards.push(k);
      } else {
        futureCards.push(k);
      }
    }

    const counts = {
      due: dueCards.length,
      new: newCards.length,
      learning: futureCards.length,
      total: kanjiList.length,
    };

    let candidates = [];
    if (mode === 'due_only') {
      candidates = dueCards;
    } else {
      if (dueCards.length > 0) {
        candidates = dueCards.concat(newCards.slice(0, 5));
      } else if (newCards.length > 0) {
        candidates = newCards;
      } else {
        candidates = futureCards;
      }
    }

    if (candidates.length === 0) {
      return { kanji: null, counts };
    }

    if (candidates.length > 1 && previousId) {
      const filtered = candidates.filter((k) => k.id !== previousId);
      if (filtered.length > 0) candidates = filtered;
    }

    const chosen = candidates[Math.floor(Math.random() * candidates.length)];
    return { kanji: chosen, counts };
  }

  handleQuizSubmit(event) {
    if (event) event.preventDefault();
    const input = document.getElementById('quiz-input');
    const answer = input.value.trim();
    if (!answer || !this.currentQuiz) return;

    const check = this.checkLocalAnswer(answer, this.currentQuiz.meaning);
    this.showQuizResult({
      correct: check.correct,
      user_answer: answer,
      accepted_meanings: check.accepted,
      kanji: this.currentQuiz,
    });
  }

  checkLocalAnswer(userAnswer, meaningStr) {
    const normalize = (t) => t.toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').trim();
    const normUser = normalize(userAnswer);
    const meanings = (meaningStr || '').split('/').map((m) => m.trim()).filter(Boolean);

    for (const m of meanings) {
      if (normUser === normalize(m)) {
        return { correct: true, accepted: meanings };
      }
      const cleanM = m.replace(/\(.*?\)/g, '').trim();
      if (cleanM && normUser === normalize(cleanM)) {
        return { correct: true, accepted: meanings };
      }
    }
    return { correct: false, accepted: meanings };
  }

  showQuizResult(result) {
    this.quizPhase = 'result';
    this.updateFooterShortcuts();

    const qBox = document.getElementById('quiz-question-box');
    const rBox = document.getElementById('quiz-result-box');

    qBox.classList.add('hidden');
    rBox.classList.remove('hidden');

    const banner = document.getElementById('result-banner');
    const icon = document.getElementById('result-icon');
    const text = document.getElementById('result-text');

    if (result.correct) {
      banner.className = 'result-banner correct';
      icon.textContent = '✓';
      text.textContent = 'Correct!';
    } else {
      banner.className = 'result-banner incorrect';
      icon.textContent = '✗';
      text.textContent = 'Incorrect';
    }

    document.getElementById('result-glyph').textContent = result.kanji.character;
    document.getElementById('result-readings').textContent =
      `On: ${result.kanji.onyomi || '-'}  |  Kun: ${result.kanji.kunyomi || '-'}`;
    document.getElementById('result-user-answer').textContent = result.user_answer;
    document.getElementById('result-expected-meanings').textContent = result.accepted_meanings.join(' / ');
  }

  submitRating(rating) {
    if (!this.currentQuiz) return;
    this.reviewLocalCard(this.currentQuiz.id, rating);
    this.nextQuizQuestion();
  }

  reviewLocalCard(kanjiId, rating) {
    const cards = this.getLocalCards();
    const existing = cards[kanjiId] || { reps: 0, state: 0 };
    const now = new Date();

    let nextDueMinutes = 1;
    let nextState = 1;
    let newReps = (existing.reps || 0) + 1;

    // fsrs
    switch (rating) {
      case 1: // again
        nextDueMinutes = 1;
        nextState = 1;
        newReps = 0;
        break;
      case 2: // hard
        nextDueMinutes = 5;
        nextState = 1;
        break;
      case 3: // good
        nextDueMinutes = existing.reps >= 1 ? 1440 : 10; // 10 mins or 1 day
        nextState = existing.reps >= 1 ? 2 : 1;
        break;
      case 4: // easy
        nextDueMinutes = 5760; // 4 days
        nextState = 2;
        break;
    }

    const dueDate = new Date(now.getTime() + nextDueMinutes * 60 * 1000);
    cards[kanjiId] = {
      id: kanjiId,
      state: nextState,
      reps: newReps,
      last_review: now.toISOString(),
      due: dueDate.toISOString(),
    };

    this.saveLocalCards(cards);
  }

  // stats

  loadReviewStats() {
    const stats = this.getLocalStats(this.currentLevel);

    document.getElementById('stat-due').textContent = stats.due;
    document.getElementById('stat-new').textContent = stats.new;
    document.getElementById('stat-learning').textContent = stats.learning;
    document.getElementById('stat-total').textContent = stats.total;

    const reviewLevel = document.getElementById('review-level-name');
    if (reviewLevel) {
      reviewLevel.textContent = this.currentLevel;
    }

    const dueBtn = document.getElementById('btn-start-due-review');
    const dueCountSpan = document.getElementById('btn-due-count');
    dueCountSpan.textContent = stats.due;
    if (stats.due === 0) {
      dueBtn.classList.add('btn-outline');
      dueBtn.classList.remove('btn-primary');
    } else {
      dueBtn.classList.add('btn-primary');
      dueBtn.classList.remove('btn-outline');
    }

    const total = stats.total || 1;
    const duePct = (stats.due / total) * 100;
    const learningPct = (stats.learning / total) * 100;
    const newPct = (stats.new / total) * 100;

    const barDue = document.getElementById('bar-due');
    const barLearning = document.getElementById('bar-learning');
    const barNew = document.getElementById('bar-new');
    const masteryEl = document.getElementById('mastery-percent');

    // Reset bar segments to 0% width without transition to prime left-to-right fill
    if (barDue && barLearning && barNew) {
      barDue.style.transition = 'none';
      barLearning.style.transition = 'none';
      barNew.style.transition = 'none';
      barDue.style.width = '0%';
      barLearning.style.width = '0%';
      barNew.style.width = '0%';

      // Force layout reflow to commit initial 0% state
      void barDue.offsetWidth;

      // Restore CSS transitions with staggered fill delays
      barDue.style.transition = '';
      barLearning.style.transition = '';
      barNew.style.transition = '';

      // Trigger smooth expansion across the bar track
      requestAnimationFrame(() => {
        barDue.style.width = `${duePct}%`;
        barLearning.style.width = `${learningPct}%`;
        barNew.style.width = `${newPct}%`;
      });
    }

    // Animate mastery percentage count-up smoothly in sync with the bar fill
    const learnedCount = stats.due + stats.learning;
    const learnedPct = Math.round((learnedCount / total) * 100);

    if (masteryEl) {
      if (this.masteryAnimFrame) {
        cancelAnimationFrame(this.masteryAnimFrame);
      }
      const duration = 850;
      const startTime = performance.now();
      const animateMastery = (now) => {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const currentPct = Math.round(ease * learnedPct);
        const currentCount = Math.round(ease * learnedCount);
        masteryEl.textContent = `${currentPct}% learned (${currentCount}/${total})`;
        if (progress < 1) {
          this.masteryAnimFrame = requestAnimationFrame(animateMastery);
        } else {
          this.masteryAnimFrame = null;
        }
      };
      this.masteryAnimFrame = requestAnimationFrame(animateMastery);
    }
  }

  // settings

  confirmResetSRS() {
    const ok = window.confirm(
      'Are you sure you want to reset all SRS progress? This will delete all review records and reset all cards to New.'
    );
    if (!ok) return;

    localStorage.removeItem('kansu_srs_cards');
    window.alert('SRS review history reset.');
    this.loadReviewStats();
    this.updateMenuStats();
  }

  escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.app = new KansuApp();
});
