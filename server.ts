import { serve } from "bun";
import { join, dirname } from "path";
import { readFileSync, writeFileSync, existsSync } from "fs";

const BASE = dirname(import.meta.path);

const PATHS = {
  progress: join(BASE, "progress.json"),
  guideProgress: join(BASE, "guide_progress.json"),
  questions: join(BASE, "questions.json"),
  guideS3: join(BASE, "guide_s3.json"),
  guideS1: join(BASE, "guide_s1.json"),
  dailyLog: join(BASE, "daily_log.json"),
  webapp: join(BASE, "webapp", "index.html"),
};

const DAILY_TARGETS = { guide: 20, quiz: 10 };

function todayStr() {
  return new Date().toLocaleDateString("en-CA", { timeZone: "Asia/Taipei" });
}

function getDailyLog() {
  return readJSON(PATHS.dailyLog) ?? {};
}

function getTodayEntry() {
  const log = getDailyLog();
  const today = todayStr();
  return log[today] ?? { guide_completed: 0, quiz_answered: 0, rested_early: false, bonus_rounds: 0 };
}

function getDailyStatus() {
  const today = todayStr();
  const guideS1 = readJSON(PATHS.guideS1);
  const guideS3 = readJSON(PATHS.guideS3);

  const guideToday = [
    ...(guideS1?.segments ?? []),
    ...(guideS3?.segments ?? []),
  ].filter((s: any) => s.completed && s.completed_date === today).length;

  const entry = getTodayEntry();
  const quizToday = entry.quiz_answered;

  const guideDone = guideToday >= DAILY_TARGETS.guide;
  const quizDone = quizToday >= DAILY_TARGETS.quiz;
  const allDone = guideDone && quizDone;

  return {
    date: today,
    guide: { today: guideToday, target: DAILY_TARGETS.guide, done: guideDone },
    quiz: { today: quizToday, target: DAILY_TARGETS.quiz, done: quizDone },
    allDone,
    restedEarly: entry.rested_early,
    bonusRounds: entry.bonus_rounds,
  };
}

function recordDailyQuiz() {
  const log = getDailyLog();
  const today = todayStr();
  if (!log[today]) log[today] = { guide_completed: 0, quiz_answered: 0, rested_early: false, bonus_rounds: 0 };
  log[today].quiz_answered = (log[today].quiz_answered ?? 0) + 1;
  writeJSON(PATHS.dailyLog, log);
}

function recordEarlyRest(note = "") {
  const log = getDailyLog();
  const today = todayStr();
  if (!log[today]) log[today] = { guide_completed: 0, quiz_answered: 0, rested_early: false, bonus_rounds: 0 };
  log[today].rested_early = true;
  log[today].rest_note = note;
  log[today].rest_time = new Date().toISOString();
  writeJSON(PATHS.dailyLog, log);
  return { ok: true, date: today };
}

function recordBonusRound() {
  const log = getDailyLog();
  const today = todayStr();
  if (!log[today]) log[today] = { guide_completed: 0, quiz_answered: 0, rested_early: false, bonus_rounds: 0 };
  log[today].bonus_rounds = (log[today].bonus_rounds ?? 0) + 1;
  writeJSON(PATHS.dailyLog, log);
  return { ok: true, bonusRounds: log[today].bonus_rounds };
}

function readJSON(path: string) {
  try { return JSON.parse(readFileSync(path, "utf-8")); } catch { return null; }
}

function writeJSON(path: string, data: unknown) {
  writeFileSync(path, JSON.stringify(data, null, 2));
}

function calcStreak(): number {
  const log = readJSON(PATHS.dailyLog) ?? {};
  const today = new Date().toISOString().slice(0, 10);
  const todayEntry = log[today];
  const isActive = (e: any) => e && (e.guide_completed > 0 || e.quiz_answered > 0 || e.rested_early);
  const todayActive = isActive(todayEntry);
  let streak = 0;
  for (let i = todayActive ? 0 : 1; i < 365; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const key = d.toISOString().slice(0, 10);
    if (isActive(log[key])) {
      streak++;
    } else {
      break;
    }
  }
  return streak;
}

function examDaysLeft() {
  const exam = new Date("2026-11-14");
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return Math.ceil((exam.getTime() - today.getTime()) / 86400000);
}

function getStatus() {
  const progress = readJSON(PATHS.progress);
  const guideProgress = readJSON(PATHS.guideProgress);
  const guideS3 = readJSON(PATHS.guideS3);
  const guideS1 = readJSON(PATHS.guideS1);
  const questions = readJSON(PATHS.questions);

  const s3Done = guideS3?.segments?.filter((s: any) => s.completed).length ?? 0;
  const s1Done = guideS1?.segments?.filter((s: any) => s.completed).length ?? 0;
  const wrongHistory = progress?.wrong_history ?? {};
  const completedCorrect = new Set(progress?.completed_correct ?? []);
  const wrongPending = Object.keys(wrongHistory).filter((id) => !completedCorrect.has(id)).length;
  const totalQuestions = questions?.questions?.length ?? 260;
  const mastered = completedCorrect.size;
  const answeredEvents = progress?.stats?.total_answered ?? (mastered + Object.values(wrongHistory).reduce((sum: number, h: any) => sum + (h?.count ?? 0), 0));

  return {
    daysLeft: examDaysLeft(),
    streak: calcStreak(),
    guide: {
      s3: { done: s3Done, total: guideS3?.total ?? 95 },
      s1: { done: s1Done, total: guideS1?.total ?? 70 },
      round: guideProgress?.round ?? 1,
    },
    quiz: {
      answered: answeredEvents,
      correct: mastered,
      mastered,
      total: totalQuestions,
      wrongPending,
      round: progress?.round ?? 1,
    },
  };
}

function getCurrentQuestion() {
  const progress = readJSON(PATHS.progress);
  const questions = readJSON(PATHS.questions);
  if (!progress || !questions) return null;

  // Prioritize wrong questions that have been wrong 2+ times
  const wrongHistory = progress.wrong_history ?? {};
  const priorityWrong = Object.entries(wrongHistory)
    .filter(([id, h]: [string, any]) => h.count >= 2 && !progress.completed_correct?.includes(id))
    .sort(([, a]: [string, any], [, b]: [string, any]) => b.count - a.count);

  let qid = progress.current_question;
  if (priorityWrong.length > 0 && Math.random() < 0.3) {
    qid = priorityWrong[0][0];
  }

  const q = questions.questions?.find((q: any) => q.id === qid);
  if (!q) return null;

  return {
    id: q.id,
    source: q.source,
    question: q.question,
    options: q.options,
    image: q.image ?? null,
    wrongCount: wrongHistory[qid]?.count ?? 0,
    totalInQueue: progress.current_queue?.length ?? 0,
    totalAnswered: progress.stats?.total_answered ?? 0,
  };
}

function recordAnswer(id: string, answer: string) {
  const progress = readJSON(PATHS.progress);
  const questions = readJSON(PATHS.questions);
  if (!progress || !questions) return { error: "data not found" };

  const q = questions.questions?.find((q: any) => q.id === id);
  if (!q) return { error: "question not found" };

  const correct = q.answer === answer;
  const wrongHistory = progress.wrong_history ?? {};

  if (correct) {
    // Move from queue to completed
    progress.completed_correct = [...(progress.completed_correct ?? []), id];
    progress.current_queue = progress.current_queue?.filter((qid: string) => qid !== id) ?? [];
    // Keep in wrong_history but mark as fixed if it was wrong before
  } else {
    // Record wrong answer
    if (!wrongHistory[id]) {
      wrongHistory[id] = { count: 0, last_wrong: null, history: [] };
    }
    wrongHistory[id].count = (wrongHistory[id].count ?? 0) + 1;
    wrongHistory[id].last_wrong = answer;
    wrongHistory[id].history = [...(wrongHistory[id].history ?? []), answer];
    // Move to back of queue (will come back soon)
    progress.current_queue = progress.current_queue?.filter((qid: string) => qid !== id) ?? [];
    progress.current_queue.push(id);
  }

  // Update stats
  progress.stats = progress.stats ?? { total_answered: 0, total_correct: 0, total_wrong: 0 };
  progress.stats.total_answered = (progress.stats.total_answered ?? 0) + 1;
  if (correct) progress.stats.total_correct = (progress.stats.total_correct ?? 0) + 1;
  else progress.stats.total_wrong = (progress.stats.total_wrong ?? 0) + 1;

  progress.wrong_history = wrongHistory;

  // Advance to next question
  const nextId = progress.current_queue?.[0] ?? null;
  progress.current_question = nextId;

  writeJSON(PATHS.progress, progress);

  // Track daily quiz count
  recordDailyQuiz();

  const daily = getDailyStatus();
  const masteredCount = (progress.completed_correct ?? []).length;
  const totalQ = questions.questions?.length ?? 260;
  const allQuizMastered = masteredCount >= totalQ;

  return {
    correct,
    correctAnswer: q.answer,
    explanation: q.explanation ?? "",
    nextQuestion: nextId,
    daily,
    allQuizMastered,
  };
}

function getGuideSegment(subject: number) {
  const path = subject === 1 ? PATHS.guideS1 : PATHS.guideS3;
  const guide = readJSON(path);
  if (!guide) return null;

  const next = guide.segments?.find((s: any) => !s.completed);
  if (!next) return { done: true, subject, total: guide.total };

  return {
    id: next.id,
    title: next.title,
    content: next.content,
    subject,
    round: next.round,
    completedCount: guide.segments?.filter((s: any) => s.completed).length ?? 0,
    total: guide.total,
    hasContent: !!next.content,
  };
}

function completeSegment(subject: number, id: number) {
  const path = subject === 1 ? PATHS.guideS1 : PATHS.guideS3;
  const guide = readJSON(path);
  if (!guide) return { error: "guide not found" };

  const seg = guide.segments?.find((s: any) => s.id === id);
  if (!seg) return { error: "segment not found" };

  seg.completed = true;
  seg.completed_date = todayStr();

  // Also update guide_progress.json
  const guideProgress = readJSON(PATHS.guideProgress);
  if (guideProgress) {
    const key = `subject${subject}` as "subject1" | "subject3";
    if (guideProgress[key]) {
      guideProgress[key].completed_segments = guide.segments?.filter((s: any) => s.completed).length;
    }
    writeJSON(PATHS.guideProgress, guideProgress);
  }

  writeJSON(path, guide);

  // Track in daily_log so streak and history are accurate
  const log = getDailyLog();
  const today = todayStr();
  if (!log[today]) log[today] = { guide_completed: 0, quiz_answered: 0, rested_early: false, bonus_rounds: 0 };
  log[today].guide_completed = (log[today].guide_completed ?? 0) + 1;
  writeJSON(PATHS.dailyLog, log);

  // Check if ALL guide content across both subjects is now complete
  const s1 = readJSON(PATHS.guideS1);
  const s3 = readJSON(PATHS.guideS3);
  const s1Total = s1?.total ?? 70;
  const s3Total = s3?.total ?? 95;
  const s1Done = s1?.segments?.filter((s: any) => s.completed).length ?? 0;
  const s3Done = s3?.segments?.filter((s: any) => s.completed).length ?? 0;
  const allGuideComplete = s1Done >= s1Total && s3Done >= s3Total;

  return { ok: true, completedId: id, allGuideComplete };
}

function startGuideNewRound() {
  const guideProgress = readJSON(PATHS.guideProgress);
  const s1 = readJSON(PATHS.guideS1);
  const s3 = readJSON(PATHS.guideS3);
  if (!s1 || !s3) return { error: "guide data not found" };

  for (const seg of s1.segments ?? []) { seg.completed = false; delete seg.completed_date; }
  for (const seg of s3.segments ?? []) { seg.completed = false; delete seg.completed_date; }

  const newRound = (guideProgress?.round ?? 1) + 1;
  if (guideProgress) {
    guideProgress.round = newRound;
    guideProgress.subject1 = { ...guideProgress.subject1, completed_segments: 0 };
    guideProgress.subject3 = { ...guideProgress.subject3, completed_segments: 0 };
    writeJSON(PATHS.guideProgress, guideProgress);
  }

  writeJSON(PATHS.guideS1, s1);
  writeJSON(PATHS.guideS3, s3);
  return { ok: true, round: newRound };
}

function startQuizNewRound() {
  const progress = readJSON(PATHS.progress);
  const questions = readJSON(PATHS.questions);
  if (!progress || !questions) return { error: "data not found" };

  const allIds = questions.questions?.map((q: any) => q.id) ?? [];
  const newRound = (progress.round ?? 1) + 1;

  progress.round = newRound;
  progress.completed_correct = [];
  progress.wrong_history = {};
  progress.current_queue = [...allIds];
  progress.current_question = allIds[0] ?? null;
  progress.stats = { ...progress.stats, total_answered: 0 };
  writeJSON(PATHS.progress, progress);
  return { ok: true, round: newRound };
}

function saveSegmentContent(subject: number, id: number, content: string) {
  const path = subject === 1 ? PATHS.guideS1 : PATHS.guideS3;
  const guide = readJSON(path);
  if (!guide) return { error: "guide not found" };

  const seg = guide.segments?.find((s: any) => s.id === id);
  if (!seg) return { error: "segment not found" };

  seg.content = content;
  writeJSON(path, guide);
  return { ok: true };
}

function getQuestionById(id?: string) {
  if (!id) return null;
  const questions = readJSON(PATHS.questions);
  return questions?.questions?.find((q: any) => q.id === id) ?? null;
}

function buildStudyFallback(question: string, context: string, currentQuestionId?: string): string {
  const q = getQuestionById(currentQuestionId);
  if (q) {
    const options = Object.entries(q.options ?? {})
      .map(([key, text]) => `${key}. ${text}`)
      .join("\n");
    return `目前 Claude 額度或 AI 服務暫時不可用，我先用題庫內建解析回答。\n\n【你的問題】\n${question || "請解釋目前這題"}\n\n【目前題目】\n${q.question}\n\n【選項】\n${options}\n\n${q.explanation ?? "此題尚無解析。"}`;
  }

  if (context) {
    return `目前 Claude 額度或 AI 服務暫時不可用，我先根據目前段落內容整理。\n\n【你的問題】\n${question}\n\n【目前段落重點】\n${context.slice(0, 1800)}\n\n【建議】先把本段名詞、適用情境、限制與常見混淆點整理成筆記；若是題目，請切到刷題頁再問「解釋目前題目」。`;
  }

  return "目前 Claude 額度或 AI 服務暫時不可用；請先切到題目或指引段落後再問，我會用當前內容提供解析。";
}

async function askAI(question: string, context: string, currentQuestionId?: string): Promise<string> {
  const fallback = buildStudyFallback(question, context, currentQuestionId);
  const q = getQuestionById(currentQuestionId);
  const currentQuestionContext = q ? `\n目前刷題題目：\n${q.question}\n選項：${JSON.stringify(q.options, null, 2)}\n標準解析：\n${q.explanation ?? ""}` : "";
  const systemPrompt = `你是 IPAS AI 應用規劃師中級考試的專業助教。
請用繁體中文回答，口吻像考前家教：清楚、直接、以考試判斷為主。
回答必須包含：1. 簡短結論 2. 考點 3. 容易混淆處 4. 記憶方式。
${context ? `\n目前學習段落內容：\n${context}` : ""}${currentQuestionContext}`;

  const proc = Bun.spawn(
    ["/Users/leifhuang/.bun/bin/bun", "/Users/leifhuang/.claude/PAI/TOOLS/Inference.ts", "--level", "fast", "--timeout", "20000", systemPrompt, question || "請解釋目前內容"],
    {
      stdout: "pipe",
      stderr: "pipe",
      env: {
        ...process.env,
        HOME: "/Users/leifhuang",
        PATH: "/Users/leifhuang/.local/bin:/opt/homebrew/bin:/Users/leifhuang/.bun/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
      },
    }
  );

  const timeout = new Promise<"timeout">((resolve) => setTimeout(() => resolve("timeout"), 25000));
  const exited = proc.exited.then(() => "exited" as const);
  const status = await Promise.race([exited, timeout]);
  if (status === "timeout") {
    proc.kill();
    return fallback;
  }

  const output = (await new Response(proc.stdout).text()).trim();
  const stderr = (await new Response(proc.stderr).text()).trim();
  if (proc.exitCode !== 0 || !output) {
    console.warn("AI chat fallback:", stderr || `exit ${proc.exitCode}`);
    return fallback;
  }
  return output;
}

const server = serve({
  port: 8080,
  fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname;

    // CORS
    const headers = new Headers({
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    });

    // Serve webapp
    if (path === "/" || path === "/index.html") {
      const html = readFileSync(PATHS.webapp, "utf-8");
      return new Response(html, { headers: new Headers({ "Content-Type": "text/html" }) });
    }

    // Serve AI Agent book notes subpage
    if (path === "/ai-agent-book" || path === "/ai-agent-book.html") {
      const html = readFileSync(join(BASE, "webapp", "ai-agent-book.html"), "utf-8");
      return new Response(html, { headers: new Headers({ "Content-Type": "text/html; charset=utf-8" }) });
    }

    // Serve static webapp assets (images, etc.)
    if (path.startsWith("/images/")) {
      const filePath = join(BASE, "webapp", path);
      if (existsSync(filePath)) {
        const file = Bun.file(filePath);
        return new Response(file);
      }
      return new Response("Not found", { status: 404 });
    }

    // API routes
    if (path === "/api/status") {
      return Response.json(getStatus());
    }

    if (path === "/api/quiz/current") {
      return Response.json(getCurrentQuestion() ?? { error: "no question" });
    }

    if (path === "/api/quiz/answer" && req.method === "POST") {
      return req.json().then((body: any) => {
        const result = recordAnswer(body.id, body.answer);
        return Response.json(result);
      });
    }

    if (path.match(/^\/api\/guide\/s(1|3)\/current$/)) {
      const subject = path.includes("/s1/") ? 1 : 3;
      return Response.json(getGuideSegment(subject) ?? { error: "not found" });
    }

    if (path.match(/^\/api\/guide\/(1|3)\/current$/)) {
      const subject = parseInt(path.split("/")[3]);
      return Response.json(getGuideSegment(subject) ?? { error: "not found" });
    }

    if (path.match(/^\/api\/guide\/current\/(\d+)$/)) {
      const subject = parseInt(url.searchParams.get("subject") ?? "3");
      return Response.json(getGuideSegment(subject) ?? { error: "not found" });
    }

    if (path === "/api/guide/current") {
      const subject = parseInt(url.searchParams.get("subject") ?? "3");
      return Response.json(getGuideSegment(subject) ?? { error: "not found" });
    }

    if (path === "/api/guide/save-content" && req.method === "POST") {
      return req.json().then((body: any) => {
        return Response.json(saveSegmentContent(body.subject, body.id, body.content));
      });
    }

    if (path === "/api/daily/status") {
      return Response.json(getDailyStatus());
    }

    if (path === "/api/daily/rest" && req.method === "POST") {
      return req.json().then((body: any) => {
        return Response.json(recordEarlyRest(body.note ?? ""));
      });
    }

    if (path === "/api/daily/bonus" && req.method === "POST") {
      return Response.json(recordBonusRound());
    }

    if (path === "/api/guide/complete" && req.method === "POST") {
      return req.json().then((body: any) => {
        const result = completeSegment(body.subject, body.id);
        return Response.json({ ...result, daily: getDailyStatus() });
      });
    }

    if (path === "/api/chat" && req.method === "POST") {
      return req.json().then(async (body: any) => {
        const answer = await askAI(body.question ?? "", body.context ?? "", body.currentQuestionId);
        return Response.json({ answer });
      });
    }

    if (path === "/api/guide/newround" && req.method === "POST") {
      return Response.json(startGuideNewRound());
    }

    if (path === "/api/quiz/newround" && req.method === "POST") {
      return Response.json(startQuizNewRound());
    }

    if (path === "/api/guide/segment") {
      const subject = parseInt(url.searchParams.get("subject") ?? "1");
      const id = parseInt(url.searchParams.get("id") ?? "0");
      const guidePath = subject === 1 ? PATHS.guideS1 : PATHS.guideS3;
      const guide = readJSON(guidePath);
      const seg = guide?.segments?.find((s: any) => s.id === id);
      if (!seg) return Response.json({ error: "not found" }, { status: 404 });
      return Response.json({ id: seg.id, title: seg.title, content: seg.content, subject, completed: seg.completed, total: guide.total });
    }

    if (path === "/api/quiz/question") {
      const n = parseInt(url.searchParams.get("n") ?? "1");
      const questions = readJSON(PATHS.questions);
      const q = questions?.questions?.[n - 1];
      if (!q) return Response.json({ error: "not found" }, { status: 404 });
      const progress = readJSON(PATHS.progress);
      const wrongHistory = progress?.wrong_history ?? {};
      const completedCorrect = new Set(progress?.completed_correct ?? []);
      return Response.json({
        id: q.id, source: q.source, question: q.question, options: q.options, image: q.image ?? null,
        wrongCount: wrongHistory[q.id]?.count ?? 0,
        totalInQueue: progress?.current_queue?.length ?? 0,
        totalAnswered: progress?.stats?.total_answered ?? 0,
        mastered: completedCorrect.has(q.id),
        index: n,
      });
    }

    return new Response("Not found", { status: 404 });
  },
});

console.log(`IPAS 備考系統 running at http://localhost:8080`);
