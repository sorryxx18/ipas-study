#!/usr/bin/env bun
/**
 * rewrite_guides.ts
 *
 * Batch rewrites stub segments in guide_s1.json and guide_s3.json.
 * A segment is considered a stub if content length < 2000 chars.
 *
 * Checkpoint/resume: rewrite_state.json in BASE directory.
 * Run from any terminal (no CLAUDECODE needed — the script strips it for subprocesses).
 *
 * Usage:
 *   bun scripts/rewrite_guides.ts
 *   bun scripts/rewrite_guides.ts --subject 1      # only S1 (uses sonnet)
 *   bun scripts/rewrite_guides.ts --subject 3      # only S3 (uses haiku)
 *   bun scripts/rewrite_guides.ts --reset          # clear checkpoint and restart
 *   bun scripts/rewrite_guides.ts --retry-failed   # retry previously-failed segments
 *   bun scripts/rewrite_guides.ts --limit 3        # process only N segments this run
 *
 * Model selection:
 *   S1 → claude-sonnet (better quality, more nuanced planning content)
 *   S3 → claude-haiku  (fast + cheap, sufficient for ML technical content)
 */

import { spawn } from "child_process";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";

const BASE = "/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study";
const STATE_FILE = join(BASE, "rewrite_state.json");
const STUB_THRESHOLD = 2000;
const DELAY_MS = 1500;
const TIMEOUT_MS = 90000;

const args = process.argv.slice(2);
const subjectFlag = args.includes("--subject") ? parseInt(args[args.indexOf("--subject") + 1]) : null;
const resetFlag = args.includes("--reset");
const retryFailedFlag = args.includes("--retry-failed");
const limitFlag = args.includes("--limit") ? parseInt(args[args.indexOf("--limit") + 1]) : null;

// Model per subject: S1 uses sonnet (planning/application content needs more nuance),
// S3 uses haiku (ML technical content is well-structured and cheaper to generate).
const MODEL_S1 = "sonnet";
const MODEL_S3 = "haiku";

// ── Types ────────────────────────────────────────────────────────────────────

interface Segment {
  id: number;
  title: string;
  content: string;
  [key: string]: unknown;
}

interface GuideFile {
  subject: number;
  title: string;
  total: number;
  segments: Segment[];
}

interface SubjectState {
  completed: number[];
  failed: number[];
  failedTitles: Record<number, string>;
}

interface RewriteState {
  s1: SubjectState;
  s3: SubjectState;
  startedAt: string;
  lastUpdated: string;
}

// ── State management ──────────────────────────────────────────────────────────

function emptySubject(): SubjectState {
  return { completed: [], failed: [], failedTitles: {} };
}

function loadState(): RewriteState {
  if (!resetFlag && existsSync(STATE_FILE)) {
    const state: RewriteState = JSON.parse(readFileSync(STATE_FILE, "utf-8"));
    if (retryFailedFlag) {
      state.s1.failed = [];
      state.s1.failedTitles = {};
      state.s3.failed = [];
      state.s3.failedTitles = {};
      console.log("--retry-failed: cleared all failed IDs (completed IDs preserved)");
    }
    return state;
  }
  return {
    s1: emptySubject(),
    s3: emptySubject(),
    startedAt: new Date().toISOString(),
    lastUpdated: new Date().toISOString(),
  };
}

function saveState(state: RewriteState) {
  state.lastUpdated = new Date().toISOString();
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// ── Content generation ────────────────────────────────────────────────────────

function buildPrompt(segment: Segment, subject: number): string {
  const subjectCtx =
    subject === 1
      ? "科目一（AI 應用規劃師，重視應用規劃、導入判斷、風險治理、商業情境，不考數學推導）"
      : "科目三（機器學習技術，重視原理理解、演算法選擇、評估指標、訓練限制、模型部署，需要能說出數學/演算法直覺）";

  return `你是 IPAS 中級機器學習工程師考試的專業教材撰寫者，擅長把技術概念講得清楚、有條理，且直接對應考試需求。

主題：${segment.title}
考試科目：${subjectCtx}

請輸出完整的學習段落，嚴格按照以下7節格式：

# ${segment.title}

## 1. 核心概念
（400-600字）清楚說明：
- 是什麼（What）：給出精確定義，帶英文術語
- 為什麼需要（Why）：這個技術解決了什麼問題、什麼場景用
- 怎麼運作（How）：具體機制、步驟或公式，讓讀者理解原理
用「**粗體**」標出關鍵術語，分層說明。

## 2. 考試重點
列出 6-8 個具體考點，每點格式：「- **考點名稱**：一句話說清楚考試答案」
不要只說「理解X」，要直接說出知識點的正確答案。

## 3. 名詞解釋
列出 4-6 個此主題核心術語，每個格式：
**中文名稱**：清楚定義（英文原文）

## 4. 常見陷阱
列出 4-5 個考生容易混淆或答錯的陷阱，每個格式：
**陷阱N：[誤解描述]**
> ❌ 誤解：具體說明錯誤想法
> ✅ 正確：給出正確觀念，包含細節

## 5. 考題怎麼問
列出 3-4 種常見出題角度，每種格式：
**問法N：[題型描述]**
→ 看到「[關鍵詞]」→ 答 [具體答案]

## 6. 記憶口訣
2-3 個幫助記憶的口訣、縮寫或比喻，每個要能真正幫助記住考試重點。

## 7. 官方指引對應線索
說明此主題在 IPAS 官方學習指引中屬於哪個章節範圍，考試最常從哪個角度命題（50-100字）。

❗ 重要規範：
- 所有資訊必須正確，技術細節不可捏造
- 使用繁體中文，術語需附英文
- 針對 IPAS 中級考試程度（不是研究所，不是入門）
- 每節都要有實質內容，禁止使用「理解X的目的」「掌握X的重要性」這類空話
- 直接輸出教材內容，不要加「好的，以下是...」開頭`;
}

async function callClaude(prompt: string, model: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const childEnv: Record<string, string> = {};
    for (const [k, v] of Object.entries(process.env)) {
      if (k !== "CLAUDECODE" && v !== undefined) childEnv[k] = v;
    }

    let stdout = "";
    let stderr = "";

    const child = spawn(
      "claude",
      ["--model", model, "--print", prompt],
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
      if (code === 0 && stdout.length > 800) {
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

// ── Main processing ───────────────────────────────────────────────────────────

async function processSubject(subject: number, state: RewriteState) {
  const key = `s${subject}` as "s1" | "s3";
  const model = subject === 1 ? MODEL_S1 : MODEL_S3;
  const filepath = join(BASE, `guide_s${subject}.json`);
  const guide: GuideFile = JSON.parse(readFileSync(filepath, "utf-8"));

  const completed = new Set(state[key].completed);
  const failed = new Set(state[key].failed);

  let toProcess = guide.segments.filter(
    (s) => !completed.has(s.id) && !failed.has(s.id) && (s.content || "").length < STUB_THRESHOLD
  );
  if (limitFlag && limitFlag > 0) toProcess = toProcess.slice(0, limitFlag);

  const total = toProcess.length;
  const limitNote = limitFlag ? ` | limit: ${limitFlag}` : "";
  console.log(`\n[S${subject}] model=${model} | ${total} stubs to rewrite | already done: ${completed.size} | skipping failed: ${failed.size}${limitNote}`);

  if (total === 0) {
    console.log(`[S${subject}] Nothing to do.`);
    return;
  }

  let done = 0;
  for (const segment of toProcess) {
    console.log(`[S${subject}] [${done + 1}/${total}] id=${segment.id} — ${segment.title}`);

    try {
      const prompt = buildPrompt(segment, subject);
      const content = await callClaude(prompt, model);

      const idx = guide.segments.findIndex((s) => s.id === segment.id);
      if (idx >= 0) guide.segments[idx].content = content;

      writeFileSync(filepath, JSON.stringify(guide, null, 2));

      state[key].completed.push(segment.id);
      saveState(state);

      done++;
      console.log(`[S${subject}] ✓ id=${segment.id} — ${content.length} chars written`);

      await new Promise((r) => setTimeout(r, DELAY_MS));
    } catch (err) {
      console.error(`[S${subject}] ✗ id=${segment.id} FAILED: ${err}`);
      state[key].failed.push(segment.id);
      if (!state[key].failedTitles) state[key].failedTitles = {};
      state[key].failedTitles[segment.id] = segment.title;
      saveState(state);
    }
  }

  console.log(`[S${subject}] Batch complete — ${done}/${total} succeeded`);
}

async function main() {
  console.log("=== IPAS Guide Rewriter ===");
  console.log(`Stub threshold: ${STUB_THRESHOLD} chars | Reset: ${resetFlag} | RetryFailed: ${retryFailedFlag}`);
  console.log(`Models: S1 → ${MODEL_S1} | S3 → ${MODEL_S3}`);
  if (subjectFlag) console.log(`Running subject ${subjectFlag} only`);

  const state = loadState();

  if (!subjectFlag || subjectFlag === 1) await processSubject(1, state);
  if (!subjectFlag || subjectFlag === 3) await processSubject(3, state);

  console.log("\n=== Final Summary ===");
  console.log(`S1 — completed: ${state.s1.completed.length}, failed: ${state.s1.failed.length}`);
  console.log(`S3 — completed: ${state.s3.completed.length}, failed: ${state.s3.failed.length}`);
  if (state.s1.failed.length || state.s3.failed.length) {
    console.log("Failed segments can be retried by running the script again (failed IDs are skipped until --reset).");
    console.log("To retry failed only, edit rewrite_state.json and move IDs from 'failed' to nowhere.");
  }
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
