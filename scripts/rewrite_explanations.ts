#!/usr/bin/env bun
/**
 * rewrite_explanations.ts
 *
 * Batch rewrites explanation fields in questions.json with meaningful content.
 * Checkpoint/resume: explanation_rewrite_state.json in BASE directory.
 *
 * Usage:
 *   bun scripts/rewrite_explanations.ts --limit 10          # first 10 questions
 *   bun scripts/rewrite_explanations.ts --subject 1         # subject 1 only
 *   bun scripts/rewrite_explanations.ts --subject 3         # subject 3 only
 *   bun scripts/rewrite_explanations.ts --reset             # clear checkpoint and restart
 *   bun scripts/rewrite_explanations.ts --retry-failed      # retry previously-failed questions
 */

import { spawn } from "child_process";
import { readFileSync, writeFileSync, existsSync, copyFileSync } from "fs";
import { join } from "path";

const BASE = "/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study";
const QUESTIONS_FILE = join(BASE, "questions.json");
const STATE_FILE = join(BASE, "explanation_rewrite_state.json");
const MODEL = "sonnet";
const DELAY_MS = 1500;
const TIMEOUT_MS = 120000;

const args = process.argv.slice(2);
const subjectFlag = args.includes("--subject") ? parseInt(args[args.indexOf("--subject") + 1]) : null;
const resetFlag = args.includes("--reset");
const retryFailedFlag = args.includes("--retry-failed");
const limitFlag = args.includes("--limit") ? parseInt(args[args.indexOf("--limit") + 1]) : null;

// ── Types ────────────────────────────────────────────────────────────────────

interface Question {
  id: string;
  source?: string;
  question: string;
  options: Record<string, string>;
  answer: string;
  explanation: string;
  topic?: string;
}

interface QuestionsFile {
  questions: Question[];
  [key: string]: unknown;
}

interface RewriteState {
  completed: string[];
  failed: string[];
  failedIds: Record<string, string>;
  startedAt: string;
  lastUpdated: string;
}

// ── State management ──────────────────────────────────────────────────────────

function loadState(): RewriteState {
  if (!resetFlag && existsSync(STATE_FILE)) {
    const state: RewriteState = JSON.parse(readFileSync(STATE_FILE, "utf-8"));
    if (retryFailedFlag) {
      state.failed = [];
      state.failedIds = {};
      console.log("--retry-failed: cleared all failed IDs (completed IDs preserved)");
    }
    return state;
  }
  return {
    completed: [],
    failed: [],
    failedIds: {},
    startedAt: new Date().toISOString(),
    lastUpdated: new Date().toISOString(),
  };
}

function saveState(state: RewriteState) {
  state.lastUpdated = new Date().toISOString();
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// ── Subject detection ─────────────────────────────────────────────────────────

function getSubject(id: string): 1 | 3 | null {
  if (id.includes("subject1") || id.startsWith("S1_")) return 1;
  if (id.includes("subject3") || id.startsWith("S3_")) return 3;
  return null;
}

// ── Prompt ────────────────────────────────────────────────────────────────────

function buildPrompt(q: Question): string {
  const subject = getSubject(q.id);
  const subjectCtx =
    subject === 3
      ? "科目三（機器學習技術，重視原理理解、演算法選擇、評估指標、訓練限制、模型部署）"
      : "科目一（AI 應用規劃師，重視應用規劃、導入判斷、風險治理、商業情境，不考數學推導）";

  const optLines = Object.entries(q.options)
    .map(([k, v]) => `${k}：${v}`)
    .join("\n");

  const correctText = q.options[q.answer] ?? "";

  return `你是 IPAS 中級機器學習工程師考試的解析撰寫者，任務是針對以下選擇題寫出有真正教學價值的解析。

考試科目：${subjectCtx}
題目：${q.question}

選項：
${optLines}

正確答案：${q.answer}。${correctText}

請嚴格按照以下格式輸出，不要加「好的，以下是...」等任何前言：

【考點】[2-5字的核心考點，例如「Transformer架構」「資料可行性評估」]
【正解】${q.answer}。${correctText}
【為什麼】（2-4句）從技術原理說明 ${q.answer} 為何正確：這個技術/概念的核心機制是什麼、它解決什麼問題、為何符合題目的情境需求。禁止使用「最直接符合題幹」「多半是相近概念」等套話。
【選項分析】
${Object.keys(q.options).map(k =>
  `${k}：[說明這個選項描述的具體技術/概念是什麼，以及為何${k === q.answer ? "正確——點出其核心特性" : "錯誤——指出它實際上描述的是什麼、和正確答案的本質差異"}，一句話]`
).join("\n")}
【名詞解釋】
列出題目中最重要的 2-3 個術語，格式：**中文術語**：定義（English term）
【記憶】[一句針對這題知識點的具體記憶鉤，不是通用考試技巧]

❗ 重要規範：
- 【為什麼】必須解釋技術原理，不能只重複選項文字
- 【選項分析】每個選項都要說出它描述的具體概念，讓考生知道「這個選項其實是在說什麼」
- 使用繁體中文，關鍵術語附英文
- 所有技術說明必須正確，不可捏造`;
}

// ── Claude call ───────────────────────────────────────────────────────────────

async function callClaude(prompt: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const childEnv: Record<string, string> = {};
    for (const [k, v] of Object.entries(process.env)) {
      if (k !== "CLAUDECODE" && v !== undefined) childEnv[k] = v;
    }

    let stdout = "";
    let stderr = "";

    const child = spawn(
      "claude",
      ["--model", MODEL, "--print", prompt],
      { env: childEnv, stdio: ["pipe", "pipe", "pipe"] }
    );

    child.stdout.on("data", (d) => { stdout += d.toString(); });
    child.stderr.on("data", (d) => { stderr += d.toString(); });

    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      reject(new Error(`Timeout after ${TIMEOUT_MS / 1000}s`));
    }, TIMEOUT_MS);

    child.on("close", (code) => {
      clearTimeout(timer);
      if (code === 0 && stdout.length > 200) {
        resolve(stdout.trim());
      } else {
        reject(new Error(`Exit ${code}; stderr: ${stderr.slice(0, 300)}; stdout_len: ${stdout.length}`));
      }
    });

    child.on("error", (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  console.log("=== IPAS Explanation Rewriter ===");
  console.log(`Model: ${MODEL} | Reset: ${resetFlag} | RetryFailed: ${retryFailedFlag}`);
  if (subjectFlag) console.log(`Subject filter: ${subjectFlag}`);

  const data: QuestionsFile = JSON.parse(readFileSync(QUESTIONS_FILE, "utf-8"));
  const state = loadState();

  // Backup on first run
  if (state.completed.length === 0 && state.failed.length === 0) {
    const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    const backupPath = join(BASE, `backups/${ts}-before-explanation-rewrite.json`);
    try {
      copyFileSync(QUESTIONS_FILE, backupPath);
      console.log(`Backup saved: ${backupPath}`);
    } catch {
      console.warn("Could not create backup (backups/ dir may not exist) — continuing anyway");
    }
  }

  const completed = new Set(state.completed);
  const failed = new Set(state.failed);

  let toProcess = data.questions.filter((q) => {
    if (completed.has(q.id) || failed.has(q.id)) return false;
    if (subjectFlag) return getSubject(q.id) === subjectFlag;
    return true;
  });

  if (limitFlag && limitFlag > 0) toProcess = toProcess.slice(0, limitFlag);

  const total = toProcess.length;
  console.log(`\nTo process: ${total} | Already done: ${completed.size} | Skipping failed: ${failed.size}`);

  if (total === 0) {
    console.log("Nothing to do.");
    return;
  }

  let done = 0;
  for (const q of toProcess) {
    const subj = getSubject(q.id);
    const subjLabel = subj ? `S${subj}` : "??";
    console.log(`\n[${done + 1}/${total}] [${subjLabel}] ${q.id}`);
    console.log(`  Topic: ${q.topic ?? "(none)"} | Answer: ${q.answer}`);

    try {
      const prompt = buildPrompt(q);
      const explanation = await callClaude(prompt);

      const idx = data.questions.findIndex((x) => x.id === q.id);
      if (idx >= 0) data.questions[idx].explanation = explanation;
      writeFileSync(QUESTIONS_FILE, JSON.stringify(data, null, 2));

      state.completed.push(q.id);
      saveState(state);

      done++;
      console.log(`  ✓ ${explanation.length} chars written`);

      await new Promise((r) => setTimeout(r, DELAY_MS));
    } catch (err) {
      console.error(`  ✗ FAILED: ${err}`);
      state.failed.push(q.id);
      state.failedIds[q.id] = String(err).slice(0, 200);
      saveState(state);
    }
  }

  console.log(`\n=== Done: ${done}/${total} succeeded | ${state.failed.length} total failed ===`);
  if (state.failed.length > 0) {
    console.log("Retry failed: bun scripts/rewrite_explanations.ts --retry-failed");
  }
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
