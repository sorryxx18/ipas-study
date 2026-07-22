(function () {
  const DAILY_TARGETS = { guide: 20, quiz: 10 };
  const state = {
    questions: null,
    guideS1: null,
    guideS3: null,
    progress: {
      completed_correct: [],
      wrong_history: {},
      current_queue: [],
      current_question: null,
      stats: { total_answered: 0, total_correct: 0, total_wrong: 0 },
      round: 1,
    },
    guideProgress: { round: 1 },
    dailyLog: {},
  };

  function todayStr() {
    return new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Taipei' });
  }

  function getTodayEntry() {
    const today = todayStr();
    if (!state.dailyLog[today]) {
      state.dailyLog[today] = { guide_completed: 0, quiz_answered: 0, rested_early: false, bonus_rounds: 0 };
    }
    return state.dailyLog[today];
  }

  function getDailyStatus() {
    const today = todayStr();
    const guideToday = [...(state.guideS1.segments || []), ...(state.guideS3.segments || [])]
      .filter((s) => s.completed && s.completed_date === today).length;
    const entry = getTodayEntry();
    const quizToday = entry.quiz_answered;
    const guideDone = guideToday >= DAILY_TARGETS.guide;
    const quizDone = quizToday >= DAILY_TARGETS.quiz;
    return {
      date: today,
      guide: { today: guideToday, target: DAILY_TARGETS.guide, done: guideDone },
      quiz: { today: quizToday, target: DAILY_TARGETS.quiz, done: quizDone },
      allDone: guideDone && quizDone,
      restedEarly: entry.rested_early,
      bonusRounds: entry.bonus_rounds,
    };
  }

  function examDaysLeft() {
    const exam = new Date('2026-11-14');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return Math.ceil((exam.getTime() - today.getTime()) / 86400000);
  }

  function getStatus() {
    const s3Done = state.guideS3.segments.filter((s) => s.completed).length;
    const s1Done = state.guideS1.segments.filter((s) => s.completed).length;
    const wrongHistory = state.progress.wrong_history;
    const completedCorrect = new Set(state.progress.completed_correct);
    const wrongPending = Object.keys(wrongHistory).filter((id) => !completedCorrect.has(id)).length;
    const totalQuestions = state.questions.questions.length;
    const mastered = completedCorrect.size;
    return {
      daysLeft: examDaysLeft(),
      streak: 0,
      guide: {
        s3: { done: s3Done, total: state.guideS3.total ?? 95 },
        s1: { done: s1Done, total: state.guideS1.total ?? 70 },
        round: state.guideProgress.round,
      },
      quiz: {
        answered: state.progress.stats.total_answered,
        correct: mastered,
        mastered,
        total: totalQuestions,
        wrongPending,
        round: state.progress.round,
      },
    };
  }

  function getCurrentQuestion() {
    const wrongHistory = state.progress.wrong_history;
    const priorityWrong = Object.entries(wrongHistory)
      .filter(([id, h]) => h.count >= 2 && !state.progress.completed_correct.includes(id))
      .sort((a, b) => b[1].count - a[1].count);
    let qid = state.progress.current_question;
    if (priorityWrong.length > 0 && Math.random() < 0.3) qid = priorityWrong[0][0];
    const q = state.questions.questions.find((q) => q.id === qid);
    if (!q) return null;
    return {
      id: q.id,
      source: q.source,
      question: q.question,
      options: q.options,
      image: q.image ?? null,
      wrongCount: wrongHistory[qid]?.count ?? 0,
      totalInQueue: state.progress.current_queue.length,
      totalAnswered: state.progress.stats.total_answered,
    };
  }

  function recordAnswer(id, answer) {
    const q = state.questions.questions.find((q) => q.id === id);
    if (!q) return { error: 'question not found' };
    const correct = q.answer === answer;
    const wrongHistory = state.progress.wrong_history;

    if (correct) {
      state.progress.completed_correct.push(id);
      state.progress.current_queue = state.progress.current_queue.filter((qid) => qid !== id);
    } else {
      if (!wrongHistory[id]) wrongHistory[id] = { count: 0, last_wrong: null, history: [] };
      wrongHistory[id].count += 1;
      wrongHistory[id].last_wrong = answer;
      wrongHistory[id].history.push(answer);
      state.progress.current_queue = state.progress.current_queue.filter((qid) => qid !== id);
      state.progress.current_queue.push(id);
    }

    state.progress.stats.total_answered += 1;
    if (correct) state.progress.stats.total_correct += 1;
    else state.progress.stats.total_wrong += 1;

    const nextId = state.progress.current_queue[0] ?? null;
    state.progress.current_question = nextId;

    const entry = getTodayEntry();
    entry.quiz_answered += 1;

    const daily = getDailyStatus();
    const masteredCount = state.progress.completed_correct.length;
    const totalQ = state.questions.questions.length;

    scheduleSave();
    return {
      correct,
      correctAnswer: q.answer,
      explanation: q.explanation ?? '',
      nextQuestion: nextId,
      daily,
      allQuizMastered: masteredCount >= totalQ,
    };
  }

  function getGuideSegment(subject) {
    const guide = subject === 1 ? state.guideS1 : state.guideS3;
    const next = guide.segments.find((s) => !s.completed);
    if (!next) return { done: true, subject, total: guide.total };
    return {
      id: next.id,
      title: next.title,
      content: next.content,
      subject,
      round: next.round,
      completedCount: guide.segments.filter((s) => s.completed).length,
      total: guide.total,
      hasContent: !!next.content,
    };
  }

  function completeSegment(subject, id) {
    const guide = subject === 1 ? state.guideS1 : state.guideS3;
    const seg = guide.segments.find((s) => s.id === id);
    if (!seg) return { error: 'segment not found' };
    seg.completed = true;
    seg.completed_date = todayStr();

    const entry = getTodayEntry();
    entry.guide_completed += 1;

    const s1Done = state.guideS1.segments.filter((s) => s.completed).length;
    const s3Done = state.guideS3.segments.filter((s) => s.completed).length;
    const allGuideComplete = s1Done >= state.guideS1.total && s3Done >= state.guideS3.total;

    scheduleSave();
    return { ok: true, completedId: id, allGuideComplete, daily: getDailyStatus() };
  }

  function startGuideNewRound() {
    for (const seg of state.guideS1.segments) { seg.completed = false; delete seg.completed_date; }
    for (const seg of state.guideS3.segments) { seg.completed = false; delete seg.completed_date; }
    state.guideProgress.round = (state.guideProgress.round ?? 1) + 1;
    scheduleSave();
    return { ok: true, round: state.guideProgress.round };
  }

  function startQuizNewRound() {
    const allIds = state.questions.questions.map((q) => q.id);
    state.progress.round = (state.progress.round ?? 1) + 1;
    state.progress.completed_correct = [];
    state.progress.wrong_history = {};
    state.progress.current_queue = [...allIds];
    state.progress.current_question = allIds[0] ?? null;
    state.progress.stats.total_answered = 0;
    scheduleSave();
    return { ok: true, round: state.progress.round };
  }

  function recordEarlyRest(note) {
    const entry = getTodayEntry();
    entry.rested_early = true;
    entry.rest_note = note;
    scheduleSave();
    return { ok: true, date: todayStr() };
  }

  function recordBonusRound() {
    const entry = getTodayEntry();
    entry.bonus_rounds = (entry.bonus_rounds ?? 0) + 1;
    scheduleSave();
    return { ok: true, bonusRounds: entry.bonus_rounds };
  }

  function getGuideSegmentById(subject, id) {
    const guide = subject === 1 ? state.guideS1 : state.guideS3;
    const seg = guide.segments.find((s) => s.id === id);
    if (!seg) return { error: 'not found' };
    return { id: seg.id, title: seg.title, content: seg.content, subject, completed: seg.completed, total: guide.total };
  }

  function getQuestionByIndex(n) {
    const q = state.questions.questions[n - 1];
    if (!q) return { error: 'not found' };
    const wrongHistory = state.progress.wrong_history;
    const completedCorrect = new Set(state.progress.completed_correct);
    return {
      id: q.id,
      source: q.source,
      question: q.question,
      options: q.options,
      image: q.image ?? null,
      wrongCount: wrongHistory[q.id]?.count ?? 0,
      totalInQueue: state.progress.current_queue.length,
      totalAnswered: state.progress.stats.total_answered,
      mastered: completedCorrect.has(q.id),
      index: n,
    };
  }

  async function init() {
    const [questions, guideS1, guideS3] = await Promise.all([
      fetch('questions.json').then((r) => r.json()),
      fetch('guide_s1.json').then((r) => r.json()),
      fetch('guide_s3.json').then((r) => r.json()),
    ]);
    state.questions = questions;
    state.guideS1 = JSON.parse(JSON.stringify(guideS1));
    state.guideS3 = JSON.parse(JSON.stringify(guideS3));
    for (const seg of state.guideS1.segments) { seg.completed = false; delete seg.completed_date; }
    for (const seg of state.guideS3.segments) { seg.completed = false; delete seg.completed_date; }
    const allIds = questions.questions.map((q) => q.id);
    state.progress.current_queue = allIds;
    state.progress.current_question = allIds[0] ?? null;

    if (getToken()) {
      const loaded = await ghLoad();
      if (loaded.ok && loaded.reason === 'loaded') {
        const stillQueued = new Set(state.progress.current_queue);
        state.progress.current_queue = state.progress.current_queue.filter((id) => stillQueued.has(id));
        if (!state.progress.current_question) state.progress.current_question = state.progress.current_queue[0] ?? null;
      }
    }
  }


  // ── GitHub-token based progress sync (option B) ───────────
  const GH_OWNER = 'sorryxx18';
  const GH_REPO = 'ipas-study';
  const GH_PATH = 'docs/demo_progress.json';
  const GH_API = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/contents/${GH_PATH}`;
  const TOKEN_KEY = 'ipas_demo_gh_token';
  let ghFileSha = null;
  let saveTimer = null;

  function getToken() {
    return localStorage.getItem(TOKEN_KEY) || '';
  }

  function setToken(token) {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  }

  function snapshotDynamicState() {
    return {
      progress: state.progress,
      guideProgress: state.guideProgress,
      dailyLog: state.dailyLog,
      s1Completed: state.guideS1.segments.filter((s) => s.completed).map((s) => ({ id: s.id, completed_date: s.completed_date })),
      s3Completed: state.guideS3.segments.filter((s) => s.completed).map((s) => ({ id: s.id, completed_date: s.completed_date })),
      savedAt: new Date().toISOString(),
    };
  }

  function applyDynamicState(snap) {
    if (!snap) return;
    state.progress = snap.progress ?? state.progress;
    state.guideProgress = snap.guideProgress ?? state.guideProgress;
    state.dailyLog = snap.dailyLog ?? state.dailyLog;
    for (const seg of state.guideS1.segments) seg.completed = false;
    for (const seg of state.guideS3.segments) seg.completed = false;
    for (const c of snap.s1Completed ?? []) {
      const seg = state.guideS1.segments.find((s) => s.id === c.id);
      if (seg) { seg.completed = true; seg.completed_date = c.completed_date; }
    }
    for (const c of snap.s3Completed ?? []) {
      const seg = state.guideS3.segments.find((s) => s.id === c.id);
      if (seg) { seg.completed = true; seg.completed_date = c.completed_date; }
    }
  }

  async function ghLoad() {
    const token = getToken();
    if (!token) return { ok: false, reason: 'no-token' };
    try {
      const res = await fetch(GH_API, { headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json' } });
      if (res.status === 404) return { ok: true, reason: 'not-found' };
      if (!res.ok) return { ok: false, reason: `http ${res.status}` };
      const data = await res.json();
      ghFileSha = data.sha;
      const decoded = decodeURIComponent(escape(atob(data.content.replace(/\n/g, ''))));
      applyDynamicState(JSON.parse(decoded));
      return { ok: true, reason: 'loaded' };
    } catch (e) {
      return { ok: false, reason: String(e) };
    }
  }

  async function ghSave() {
    const token = getToken();
    if (!token) return { ok: false, reason: 'no-token' };
    try {
      const snap = snapshotDynamicState();
      const content = btoa(unescape(encodeURIComponent(JSON.stringify(snap, null, 2))));
      const res = await fetch(GH_API, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json' },
        body: JSON.stringify({
          message: `demo progress sync: ${snap.savedAt}`,
          content,
          sha: ghFileSha || undefined,
        }),
      });
      if (!res.ok) return { ok: false, reason: `http ${res.status}` };
      const data = await res.json();
      ghFileSha = data.content?.sha ?? ghFileSha;
      return { ok: true };
    } catch (e) {
      return { ok: false, reason: String(e) };
    }
  }

  function scheduleSave() {
    if (!getToken()) return;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => { ghSave(); }, 3000);
  }

  const readyPromise = init();


  window.__localApi = async function (path, opts) {
    await readyPromise;
    const method = (opts && opts.method) || 'GET';
    const body = opts && opts.body ? JSON.parse(opts.body) : {};
    const url = new URL(path, 'https://static-demo.invalid');
    const p = url.pathname;
    const qs = url.searchParams;

    if (p === '/api/status') return getStatus();
    if (p === '/api/daily/status') return getDailyStatus();
    if (p === '/api/guide/current') return getGuideSegment(parseInt(qs.get('subject') || '3', 10));
    if (p === '/api/guide/complete' && method === 'POST') return completeSegment(body.subject, body.id);
    if (p === '/api/quiz/current') return getCurrentQuestion() ?? { error: 'no question' };
    if (p === '/api/quiz/answer' && method === 'POST') return recordAnswer(body.id, body.answer);
    if (p === '/api/daily/rest' && method === 'POST') return recordEarlyRest(body.note ?? '');
    if (p === '/api/daily/bonus' && method === 'POST') return recordBonusRound();
    if (p === '/api/guide/segment') return getGuideSegmentById(parseInt(qs.get('subject') || '1', 10), parseInt(qs.get('id') || '0', 10));
    if (p === '/api/quiz/question') return getQuestionByIndex(parseInt(qs.get('n') || '1', 10));
    if (p === '/api/guide/newround' && method === 'POST') return startGuideNewRound();
    if (p === '/api/quiz/newround' && method === 'POST') return startQuizNewRound();

    if (p === '/api/demo/sync-status') return { hasToken: !!getToken() };
    if (p === '/api/demo/set-token' && method === 'POST') {
      setToken(body.token || '');
      if (body.token) {
        const result = await ghLoad();
        return { hasToken: true, loadResult: result };
      }
      return { hasToken: false };
    }
    if (p === '/api/demo/sync-now' && method === 'POST') {
      clearTimeout(saveTimer);
      const result = await ghSave();
      return result;
    }

    return { error: 'not found (static demo)' };
  };
})();
