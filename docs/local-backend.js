(function () {
  const DAILY_TARGETS = { guide: 20, quiz: 10 };
  const BONUS_BOOKS = { llms: "bonus_llms.json", agent: "bonus_agent.json" };
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
    bonusProgress: { round: 1, completed: { llms: [], agent: [] }, current: { llms: 1, agent: 1 }, updated: null },
    bonusData: { llms: null, agent: null },
  };

  // ── Local persistence (localStorage) ───────────────────────────────
  // Keeps progress on-device across app restarts even with no network at
  // all (e.g. an e-ink reader offline for days). GitHub sync below is a
  // separate, best-effort layer on top of this — the device never depends
  // on connectivity just to remember what's already been read/answered.
  const LOCAL_KEY = 'ipas_local_state_v1';

  function saveLocalState() {
    try {
      const snapshot = {
        progress: state.progress,
        guideProgress: state.guideProgress,
        guideS1: state.guideS1,
        guideS3: state.guideS3,
        dailyLog: state.dailyLog,
        bonusProgress: state.bonusProgress,
        savedAt: new Date().toISOString(),
      };
      localStorage.setItem(LOCAL_KEY, JSON.stringify(snapshot));
    } catch (e) {
      console.warn('local save failed:', e);
    }
  }

  function loadLocalState() {
    try {
      const raw = localStorage.getItem(LOCAL_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

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

  function calcStreak() {
    const today = new Date();
    const todayKey = today.toISOString().slice(0, 10);
    const isActive = (e) => e && ((e.guide_completed ?? 0) > 0 || (e.quiz_answered ?? 0) > 0 || (e.bonus_chapters_completed ?? 0) > 0 || e.rested_early);
    const todayActive = isActive(state.dailyLog[todayKey]);
    let streak = 0;
    for (let i = todayActive ? 0 : 1; i < 365; i++) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      if (isActive(state.dailyLog[key])) streak += 1;
      else break;
    }
    return streak;
  }

  function getStatus() {
    const s3Done = state.guideS3.segments.filter((s) => s.completed).length;
    const s1Done = state.guideS1.segments.filter((s) => s.completed).length;
    const wrongHistory = state.progress.wrong_history;
    const completedCorrect = new Set(state.progress.completed_correct);
    const wrongPending = Object.keys(wrongHistory).filter((id) => !completedCorrect.has(id)).length;
    const totalQuestions = state.questions.questions.length;
    const mastered = completedCorrect.size;
    const bonus = getBonusStatus();
    return {
      daysLeft: examDaysLeft(),
      streak: calcStreak(),
      guide: {
        s3: { done: s3Done, total: state.guideS3.total ?? 95 },
        s1: { done: s1Done, total: state.guideS1.total ?? 70 },
        round: state.guideProgress.round ?? 1,
      },
      quiz: {
        answered: state.progress.stats.total_answered,
        correct: mastered,
        mastered,
        total: totalQuestions,
        wrongPending,
        round: state.progress.round ?? 1,
      },
      bonus,
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

  function getBonusStatus() {
    const books = Object.keys(BONUS_BOOKS).map((book) => {
      const data = state.bonusData[book];
      const total = data?.segments?.length ?? 0;
      const completed = Array.from(new Set(state.bonusProgress.completed?.[book] ?? []));
      const next = data?.segments?.find((seg) => !completed.includes(seg.id)) ?? null;
      return { book, title: data?.title ?? book, total, done: completed.length, completed, next: next ? { id: next.id, title: next.title } : null };
    });
    const total = books.reduce((sum, b) => sum + b.total, 0);
    const done = books.reduce((sum, b) => sum + b.done, 0);
    return { round: state.bonusProgress.round ?? 1, total, done, pct: total ? Math.round(done / total * 100) : 0, books };
  }

  function completeBonusChapter(book, id) {
    const data = state.bonusData[book];
    const seg = data?.segments?.find((s) => s.id === id);
    if (!seg) return { error: 'bonus chapter not found' };
    const list = new Set(state.bonusProgress.completed?.[book] ?? []);
    list.add(id);
    state.bonusProgress.completed[book] = Array.from(list).sort((a, b) => a - b);
    const next = data.segments.find((s) => !state.bonusProgress.completed[book].includes(s.id));
    state.bonusProgress.current[book] = next?.id ?? id;
    state.bonusProgress.updated = new Date().toISOString();
    const entry = getTodayEntry();
    entry.bonus_chapters_completed = (entry.bonus_chapters_completed ?? 0) + 1;
    entry.last_bonus = { book, id, title: seg.title, time: new Date().toISOString() };
    scheduleSave();
    return { ok: true, book, completedId: id, next: next ? { id: next.id, title: next.title } : null, status: getBonusStatus(), daily: getDailyStatus() };
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

  function getQuestionById(id) {
    const index = state.questions.questions.findIndex((q) => q.id === id);
    return index >= 0 ? getQuestionByIndex(index + 1) : { error: 'not found' };
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
    bonusProgress: 'bonus_progress.json',
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
      if (data.content) {
        // Contents API inlines base64 content for files up to 1MB.
        return { ok: true, found: true, json: JSON.parse(b64ToUtf8(data.content)) };
      }
      // Past 1MB (guide_s1.json / guide_s3.json already are, and only grow),
      // Contents API omits inline content — fetch the blob directly by sha
      // instead; the Git Data API supports blobs up to 100MB.
      const blobRes = await fetch(`https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/git/blobs/${data.sha}`, {
        headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json' },
      });
      if (!blobRes.ok) {
        const body = await blobRes.text().catch(() => '');
        return { ok: false, reason: `blob http ${blobRes.status}: ${body.slice(0, 300)}` };
      }
      const blob = await blobRes.json();
      return { ok: true, found: true, json: JSON.parse(b64ToUtf8(blob.content)) };
    } catch (e) {
      return { ok: false, reason: `network error: ${e && e.message ? e.message : e}` };
    }
  }

  async function ghPutFileOnce(key, json) {
    // The Contents API's single-call PUT only accepts content up to 1MB
    // decoded; guide_s1.json/guide_s3.json are already past that and only
    // grow. Do it the way git itself commits: create a blob, graft it into
    // a new tree off the current commit, create the commit, fast-forward
    // the branch ref — this has no file-size ceiling below 100MB/blob.
    const token = getToken();
    const path = SYNC_FILES[key];
    const content = JSON.stringify(json, null, 2);
    const authHeaders = {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'Content-Type': 'application/json',
    };
    const gitApi = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/git`;

    const refRes = await fetch(`${gitApi}/refs/heads/main`, { headers: authHeaders });
    if (!refRes.ok) return { ok: false, status: refRes.status, reason: `ref read http ${refRes.status}` };
    const ref = await refRes.json();
    const baseCommitSha = ref.object.sha;

    const commitRes = await fetch(`${gitApi}/commits/${baseCommitSha}`, { headers: authHeaders });
    if (!commitRes.ok) return { ok: false, status: commitRes.status, reason: `commit read http ${commitRes.status}` };
    const baseCommit = await commitRes.json();

    const blobRes = await fetch(`${gitApi}/blobs`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ content: utf8ToB64(content), encoding: 'base64' }),
    });
    if (!blobRes.ok) return { ok: false, status: blobRes.status, reason: `blob create http ${blobRes.status}` };
    const blob = await blobRes.json();

    const treeRes = await fetch(`${gitApi}/trees`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ base_tree: baseCommit.tree.sha, tree: [{ path, mode: '100644', type: 'blob', sha: blob.sha }] }),
    });
    if (!treeRes.ok) return { ok: false, status: treeRes.status, reason: `tree create http ${treeRes.status}` };
    const tree = await treeRes.json();

    const newCommitRes = await fetch(`${gitApi}/commits`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ message: `sync ${key}: ${new Date().toISOString()}`, tree: tree.sha, parents: [baseCommitSha] }),
    });
    if (!newCommitRes.ok) return { ok: false, status: newCommitRes.status, reason: `commit create http ${newCommitRes.status}` };
    const newCommit = await newCommitRes.json();

    const updateRefRes = await fetch(`${gitApi}/refs/heads/main`, {
      method: 'PATCH',
      headers: authHeaders,
      body: JSON.stringify({ sha: newCommit.sha }),
    });
    if (!updateRefRes.ok) {
      const body = await updateRefRes.text().catch(() => '');
      // Non-fast-forward (something else moved main since baseCommitSha was
      // read) surfaces as 422 here — the same conflict class ghPutFile
      // already retries on below.
      return { ok: false, status: updateRefRes.status, reason: `ref update http ${updateRefRes.status}: ${body.slice(0, 200)}` };
    }
    ghShas[key] = blob.sha;
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
      ghPutFile('bonusProgress', state.bonusProgress),
    ]);
    const failed = results.filter((r) => !r.ok);
    if (failed.length) return { ok: false, reason: failed.map((f) => f.reason).join('; ') };
    return { ok: true };
  }

  let lastSyncFailed = false;
  let lastSyncReason = '';

  function scheduleSave() {
    // Always persist locally first and immediately — this must not depend
    // on having a GitHub token or being online.
    saveLocalState();
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

  // ── Merge helpers for cross-device sync ────────────────────────────
  // Progress in this app is monotonic (a segment read stays read, a question
  // mastered stays mastered), so merging two copies is a safe union rather
  // than a risky "pick one side" — a device that's been offline for weeks
  // never loses progress made on another device, and vice versa.

  function mergeGuideContent(bundled, local) {
    // Content (title/body) always comes from the freshest bundled build;
    // only completed/completed_date carries over from what's on-device.
    if (!bundled) return local;
    if (!local) return JSON.parse(JSON.stringify(bundled));
    const localById = new Map((local.segments ?? []).map((s) => [s.id, s]));
    const merged = JSON.parse(JSON.stringify(bundled));
    for (const seg of merged.segments ?? []) {
      const ls = localById.get(seg.id);
      if (ls?.completed) {
        seg.completed = true;
        seg.completed_date = ls.completed_date ?? seg.completed_date ?? todayStr();
      }
    }
    return merged;
  }

  function mergeGuideCompleted(current, remote) {
    if (!remote || !current) return current;
    const remoteById = new Map((remote.segments ?? []).map((s) => [s.id, s]));
    for (const seg of current.segments ?? []) {
      const rs = remoteById.get(seg.id);
      if (rs?.completed && !seg.completed) {
        seg.completed = true;
        seg.completed_date = rs.completed_date ?? seg.completed_date ?? todayStr();
      }
    }
    return current;
  }

  function mergeProgress(local, remote) {
    if (!remote) return local;
    const merged = { ...local };
    merged.completed_correct = Array.from(new Set([...(local.completed_correct ?? []), ...(remote.completed_correct ?? [])]));
    const wh = { ...(remote.wrong_history ?? {}) };
    for (const [id, lh] of Object.entries(local.wrong_history ?? {})) {
      const rh = wh[id];
      if (!rh) { wh[id] = lh; continue; }
      const lLen = lh.history?.length ?? 0;
      const rLen = rh.history?.length ?? 0;
      wh[id] = {
        count: Math.max(lh.count ?? 0, rh.count ?? 0),
        last_wrong: lLen >= rLen ? lh.last_wrong : rh.last_wrong,
        history: lLen >= rLen ? lh.history : rh.history,
      };
    }
    merged.wrong_history = wh;
    merged.stats = {
      total_answered: Math.max(local.stats?.total_answered ?? 0, remote.stats?.total_answered ?? 0),
      total_correct: Math.max(local.stats?.total_correct ?? 0, remote.stats?.total_correct ?? 0),
      total_wrong: Math.max(local.stats?.total_wrong ?? 0, remote.stats?.total_wrong ?? 0),
    };
    merged.round = Math.max(local.round ?? 1, remote.round ?? 1);
    return merged;
  }

  function mergeDailyLog(local, remote) {
    const merged = { ...local };
    for (const [date, rEntry] of Object.entries(remote ?? {})) {
      const lEntry = merged[date];
      if (!lEntry) { merged[date] = rEntry; continue; }
      merged[date] = {
        guide_completed: Math.max(lEntry.guide_completed ?? 0, rEntry.guide_completed ?? 0),
        quiz_answered: Math.max(lEntry.quiz_answered ?? 0, rEntry.quiz_answered ?? 0),
        rested_early: !!(lEntry.rested_early || rEntry.rested_early),
        rest_note: lEntry.rest_note || rEntry.rest_note,
        bonus_rounds: Math.max(lEntry.bonus_rounds ?? 0, rEntry.bonus_rounds ?? 0),
        bonus_chapters_completed: Math.max(lEntry.bonus_chapters_completed ?? 0, rEntry.bonus_chapters_completed ?? 0),
        last_bonus: lEntry.last_bonus || rEntry.last_bonus,
      };
    }
    return merged;
  }

  function mergeBonusProgress(local, remote) {
    if (!remote) return local;
    const merged = { ...local, completed: { ...local.completed }, current: { ...local.current } };
    merged.round = Math.max(local.round ?? 1, remote.round ?? 1);
    for (const book of Object.keys(BONUS_BOOKS)) {
      merged.completed[book] = Array.from(new Set([...(local.completed?.[book] ?? []), ...(remote.completed?.[book] ?? [])])).sort((a, b) => a - b);
    }
    merged.current = { ...local.current, ...remote.current };
    return merged;
  }

  function mergeGuideProgress(local, remote) {
    if (!remote) return local;
    return {
      round: Math.max(local.round ?? 1, remote.round ?? 1),
      subject1: { completed_segments: Math.max(local.subject1?.completed_segments ?? 0, remote.subject1?.completed_segments ?? 0) },
      subject3: { completed_segments: Math.max(local.subject3?.completed_segments ?? 0, remote.subject3?.completed_segments ?? 0) },
    };
  }

  function reconcileQuizQueue() {
    const allIds = state.questions.questions.map((q) => q.id);
    const stillQueued = new Set(allIds);
    const mastered = new Set(state.progress.completed_correct ?? []);
    state.progress.current_queue = (state.progress.current_queue ?? []).filter((id) => stillQueued.has(id) && !mastered.has(id));
    for (const id of allIds) {
      if (!mastered.has(id) && !state.progress.current_queue.includes(id)) state.progress.current_queue.push(id);
    }
    if (!state.progress.current_question || !stillQueued.has(state.progress.current_question) || mastered.has(state.progress.current_question)) {
      state.progress.current_question = state.progress.current_queue[0] ?? null;
    }
  }

  async function pullAndMerge() {
    const token = getToken();
    if (!token) return { ok: false, reason: 'no-token' };
    const [pRes, gpRes, s1Res, s3Res, dlRes, bpRes] = await Promise.all([
      ghGetFile('progress'),
      ghGetFile('guideProgress'),
      ghGetFile('guideS1'),
      ghGetFile('guideS3'),
      ghGetFile('dailyLog'),
      ghGetFile('bonusProgress'),
    ]);
    const failures = [pRes, gpRes, s1Res, s3Res, dlRes, bpRes].filter((r) => !r.ok);
    if (failures.length) return { ok: false, reason: failures.map((f) => f.reason).join('; ') };

    if (pRes.found) state.progress = mergeProgress(state.progress, pRes.json);
    if (gpRes.found) state.guideProgress = mergeGuideProgress(state.guideProgress, gpRes.json);
    if (dlRes.found) state.dailyLog = mergeDailyLog(state.dailyLog, dlRes.json);
    if (bpRes.found) state.bonusProgress = mergeBonusProgress(state.bonusProgress, bpRes.json);
    if (s1Res.found) state.guideS1 = mergeGuideCompleted(state.guideS1, s1Res.json);
    if (s3Res.found) state.guideS3 = mergeGuideCompleted(state.guideS3, s3Res.json);

    reconcileQuizQueue();
    saveLocalState();
    // Push the merged (union) result back so every device converges on the
    // same state instead of the pull silently staying ahead of GitHub.
    const pushResult = await ghSave();
    return pushResult.ok ? { ok: true } : { ok: false, reason: pushResult.reason };
  }

  async function fetchJSONOrNull(path) {
    try {
      const res = await fetch(path);
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  }

  async function init() {
    const questions = await fetch('questions.json').then((r) => r.json());
    state.questions = questions;
    const allIds = questions.questions.map((q) => q.id);

    const [bundledS1, bundledS3, bundledBonusLlms, bundledBonusAgent] = await Promise.all([
      fetchJSONOrNull('guide_s1.json'),
      fetchJSONOrNull('guide_s3.json'),
      fetchJSONOrNull('bonus_llms.json'),
      fetchJSONOrNull('bonus_agent.json'),
    ]);
    state.bonusData.llms = bundledBonusLlms;
    state.bonusData.agent = bundledBonusAgent;

    const local = loadLocalState();
    const token = getToken();

    if (local) {
      // Offline-first: this device already has progress — trust it
      // immediately, with zero dependency on network. Content itself still
      // tracks the freshest bundled build; only completed/completed_date
      // carries over from what's on-device.
      state.progress = local.progress ?? state.progress;
      state.guideProgress = local.guideProgress ?? state.guideProgress;
      state.dailyLog = local.dailyLog ?? state.dailyLog;
      state.bonusProgress = local.bonusProgress ?? state.bonusProgress;
      state.guideS1 = mergeGuideContent(bundledS1, local.guideS1);
      state.guideS3 = mergeGuideContent(bundledS3, local.guideS3);
    } else if (!token) {
      // True first run, no saved progress, no token: this is the public
      // GitHub Pages demo — show content but not any owner-only progress.
      state.guideS1 = bundledS1 ? JSON.parse(JSON.stringify(bundledS1)) : null;
      state.guideS3 = bundledS3 ? JSON.parse(JSON.stringify(bundledS3)) : null;
      for (const seg of state.guideS1?.segments ?? []) { seg.completed = false; delete seg.completed_date; }
      for (const seg of state.guideS3?.segments ?? []) { seg.completed = false; delete seg.completed_date; }
    } else {
      // First run on this device but a token is already configured (e.g.
      // app reinstalled) — start from bundled content, real sync happens
      // in the background pull below.
      state.guideS1 = bundledS1 ? JSON.parse(JSON.stringify(bundledS1)) : null;
      state.guideS3 = bundledS3 ? JSON.parse(JSON.stringify(bundledS3)) : null;
    }

    reconcileQuizQueue();

    if (token) {
      // Don't block first render on network — pull, merge (union, never
      // destructive) and persist in the background once it resolves.
      pullAndMerge().then((result) => {
        lastSyncFailed = !result.ok;
        lastSyncReason = result.reason || '';
        if (window.__onSyncResult) window.__onSyncResult({ ...result, pulled: true });
      });
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
    if (p === '/api/bonus/status') return getBonusStatus();
    if (p === '/api/bonus/complete' && method === 'POST') return completeBonusChapter(body.book, body.id);
    if (p === '/api/guide/current') return getGuideSegment(parseInt(qs.get('subject') || '3', 10));
    if (p === '/api/guide/complete' && method === 'POST') return completeSegment(body.subject, body.id);
    if (p === '/api/quiz/current') return getCurrentQuestion() ?? { error: 'no question' };
    if (p === '/api/quiz/answer' && method === 'POST') return recordAnswer(body.id, body.answer);
    if (p === '/api/daily/rest' && method === 'POST') return recordEarlyRest(body.note ?? '');
    if (p === '/api/daily/bonus' && method === 'POST') return recordBonusRound();
    if (p === '/api/guide/segment') return getGuideSegmentById(parseInt(qs.get('subject') || '1', 10), parseInt(qs.get('id') || '0', 10));
    if (p === '/api/quiz/question') return qs.get('id') ? getQuestionById(qs.get('id')) : getQuestionByIndex(parseInt(qs.get('n') || '1', 10));
    if (p === '/api/guide/newround' && method === 'POST') return startGuideNewRound();
    if (p === '/api/quiz/newround' && method === 'POST') return startQuizNewRound();

    if (p === '/api/demo/sync-status') return { hasToken: !!getToken(), lastSyncFailed, lastSyncReason };
    if (p === '/api/demo/set-token' && method === 'POST') {
      setToken(body.token || '');
      return { hasToken: !!body.token };
    }
    if (p === '/api/demo/sync-now' && method === 'POST') {
      clearTimeout(saveTimer);
      const result = await pullAndMerge();
      lastSyncFailed = !result.ok;
      lastSyncReason = result.reason || '';
      return result;
    }

    return { error: 'not found (static demo)' };
  };
})();
