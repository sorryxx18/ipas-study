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

    const key = subject === 1 ? 'subject1' : 'subject3';
    if (state.guideProgress[key]) {
      state.guideProgress[key].completed_segments = guide.segments.filter((s) => s.completed).length;
    }

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

  // ── GitHub-token based progress sync (option B, shared with production) ──
  const GH_OWNER = 'sorryxx18';
  const GH_REPO = 'ipas-study';
  const GH_API_BASE = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/contents/`;
  const TOKEN_KEY = 'ipas_demo_gh_token';

  // These are the SAME root-level files the production server.ts reads/writes,
  // so progress made here and progress made via study.tfd-train.com converge
  // through the same GitHub repo (each side syncs when triggered, not live).
  const SYNC_FILES = {
    progress: 'progress.json',
    guideProgress: 'guide_progress.json',
    guideS1: 'guide_s1.json',
    guideS3: 'guide_s3.json',
    dailyLog: 'daily_log.json',
  };

  const ghShas = {};
  let saveTimer = null;

  function getToken() {
    return localStorage.getItem(TOKEN_KEY) || '';
  }

  function setToken(token) {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  }

  function b64ToUtf8(b64) {
    return decodeURIComponent(escape(atob(b64.replace(/\n/g, ''))));
  }

  function utf8ToB64(str) {
    return btoa(unescape(encodeURIComponent(str)));
  }

  async function ghGetFile(key) {
    const token = getToken();
    const path = SYNC_FILES[key];
    try {
      const res = await fetch(GH_API_BASE + path, {
        headers: token
          ? { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json' }
          : { Accept: 'application/vnd.github+json' },
      });
      if (res.status === 404) return { ok: true, found: false };
      if (!res.ok) {
        const body = await res.text().catch(() => '');
        return { ok: false, reason: `http ${res.status}: ${body.slice(0, 300)}` };
      }
      const data = await res.json();
      ghShas[key] = data.sha;
      return { ok: true, found: true, json: JSON.parse(b64ToUtf8(data.content)) };
    } catch (e) {
      return { ok: false, reason: `network error: ${e && e.message ? e.message : e}` };
    }
  }

  async function ghPutFileOnce(key, json) {
    const token = getToken();
    const path = SYNC_FILES[key];
    const res = await fetch(GH_API_BASE + path, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'application/vnd.github+json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: `sync ${key}: ${new Date().toISOString()}`,
        content: utf8ToB64(JSON.stringify(json, null, 2)),
        sha: ghShas[key] || undefined,
      }),
    });
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      return { ok: false, status: res.status, reason: `http ${res.status}: ${body.slice(0, 300)}` };
    }
    const data = await res.json();
    ghShas[key] = data.content?.sha ?? ghShas[key];
    return { ok: true };
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function ghPutFile(key, json) {
    const token = getToken();
    if (!token) return { ok: false, reason: 'no-token' };
    const MAX_ATTEMPTS = 4;
    try {
      let last = await ghPutFileOnce(key, json);
      let attempt = 1;
      // 409 (sha conflict) or 422 (missing/invalid sha) means someone else — production
      // syncing at the same time, or another device — moved the file forward between
      // our last read and this write. Both production and this demo can be in active
      // use simultaneously, so refetch-and-retry a few times with a short backoff
      // instead of giving up after one attempt.
      while (!last.ok && (last.status === 409 || last.status === 422) && attempt < MAX_ATTEMPTS) {
        await sleep(300 * attempt + Math.floor(Math.random() * 250));
        const refetch = await ghGetFile(key);
        if (!refetch.ok) break;
        last = await ghPutFileOnce(key, json);
        attempt += 1;
      }
      return last;
    } catch (e) {
      return { ok: false, reason: `network error: ${e && e.message ? e.message : e}` };
    }
  }

  async function ghSave() {
    if (!getToken()) return { ok: false, reason: 'no-token' };
    const results = await Promise.all([
      ghPutFile('progress', state.progress),
      ghPutFile('guideProgress', state.guideProgress),
      ghPutFile('guideS1', state.guideS1),
      ghPutFile('guideS3', state.guideS3),
      ghPutFile('dailyLog', state.dailyLog),
    ]);
    const failed = results.filter((r) => !r.ok);
    if (failed.length) return { ok: false, reason: failed.map((f) => f.reason).join('; ') };
    return { ok: true };
  }

  let lastSyncFailed = false;
  let lastSyncReason = '';

  function scheduleSave() {
    if (!getToken()) return;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      ghSave().then((result) => {
        lastSyncFailed = !result.ok;
        lastSyncReason = result.reason || '';
        if (!result.ok) console.error('background sync failed:', result.reason);
        if (window.__onSyncResult) window.__onSyncResult(result);
      });
    }, 3000);
  }

  async function init() {
    const questions = await fetch('questions.json').then((r) => r.json());
    state.questions = questions;
    const allIds = questions.questions.map((q) => q.id);

    const token = getToken();
    let guideS1 = null;
    let guideS3 = null;
    let loadedFromGh = false;

    if (token) {
      const [pRes, gpRes, s1Res, s3Res, dlRes] = await Promise.all([
        ghGetFile('progress'),
        ghGetFile('guideProgress'),
        ghGetFile('guideS1'),
        ghGetFile('guideS3'),
        ghGetFile('dailyLog'),
      ]);
      if (pRes.ok && pRes.found) state.progress = pRes.json;
      if (gpRes.ok && gpRes.found) state.guideProgress = gpRes.json;
      if (dlRes.ok && dlRes.found) state.dailyLog = dlRes.json;
      if (s1Res.ok && s1Res.found) { guideS1 = s1Res.json; loadedFromGh = true; }
      if (s3Res.ok && s3Res.found) { guideS3 = s3Res.json; loadedFromGh = true; }
    }

    if (!guideS1 || !guideS3) {
      const [bundledS1, bundledS3] = await Promise.all([
        fetch('guide_s1.json').then((r) => r.json()),
        fetch('guide_s3.json').then((r) => r.json()),
      ]);
      if (!guideS1) guideS1 = JSON.parse(JSON.stringify(bundledS1));
      if (!guideS3) guideS3 = JSON.parse(JSON.stringify(bundledS3));
    }
    state.guideS1 = guideS1;
    state.guideS3 = guideS3;

    if (!token || !loadedFromGh) {
      // No shared progress found (or no token) — demo starts from a clean slate,
      // matching the previous no-persistence behavior.
      for (const seg of state.guideS1.segments) { if (!token) { seg.completed = false; delete seg.completed_date; } }
      for (const seg of state.guideS3.segments) { if (!token) { seg.completed = false; delete seg.completed_date; } }
    }

    if (!token) {
      state.progress.current_queue = allIds;
      state.progress.current_question = allIds[0] ?? null;
    } else {
      const stillQueued = new Set(allIds);
      state.progress.current_queue = (state.progress.current_queue ?? allIds).filter((id) => stillQueued.has(id));
      if (!state.progress.current_question) state.progress.current_question = state.progress.current_queue[0] ?? allIds[0] ?? null;
    }
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

    if (p === '/api/demo/sync-status') return { hasToken: !!getToken(), lastSyncFailed, lastSyncReason };
    if (p === '/api/demo/set-token' && method === 'POST') {
      setToken(body.token || '');
      return { hasToken: !!body.token };
    }
    if (p === '/api/demo/sync-now' && method === 'POST') {
      clearTimeout(saveTimer);
      const result = await ghSave();
      lastSyncFailed = !result.ok;
      lastSyncReason = result.reason || '';
      return result;
    }

    return { error: 'not found (static demo)' };
  };
})();
