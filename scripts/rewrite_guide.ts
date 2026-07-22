#!/usr/bin/env bun
/**
 * rewrite_guide.ts
 * 逐段重寫 IPAS 教材內容（S1 + S3），支援斷點續傳。
 * 使用方式: bun run rewrite_guide.ts [--subject 1|3] [--start-id N] [--dry-run]
 *
 * 進度追蹤: scripts/rewrite_state.json
 * 執行後每段立即寫回 guide_s{N}.json
 */

import { join, dirname } from "path";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { spawn } from "bun";

const BASE = dirname(dirname(import.meta.path)); // project root

const PATHS = {
  guideS1: join(BASE, "guide_s1.json"),
  guideS3: join(BASE, "guide_s3.json"),
  state: join(BASE, "scripts", "rewrite_state.json"),
};

const INFERENCE = "/Users/leifhuang/.claude/PAI/TOOLS/Inference.ts";
const BUN = "/Users/leifhuang/.bun/bin/bun";

function readJSON(p: string) {
  try { return JSON.parse(readFileSync(p, "utf-8")); } catch { return null; }
}
function writeJSON(p: string, d: unknown) {
  writeFileSync(p, JSON.stringify(d, null, 2), "utf-8");
}

function loadState(): Record<string, boolean> {
  return readJSON(PATHS.state) ?? {};
}
function markDone(key: string) {
  const s = loadState();
  s[key] = true;
  writeJSON(PATHS.state, s);
}

const SYSTEM_PROMPT = `你是 IPAS AI 應用規劃師中級考試的頂尖家教，精通科目一（AI應用規劃）和科目三（機器學習技術）。
請用繁體中文，針對給定的考試段落，重新撰寫完整的學習指引內容。
格式必須嚴格遵守以下結構（共6個區塊，每區塊後跟一個空行）：

## 1. 核心概念
[200-350字 說明此主題的本質定義、運作原理、核心用途。從「是什麼、為什麼需要、怎麼運作」三個角度切入。]

## 2. 考試重點
[以bullet point列出4-6個最高頻考點，每點15-30字，精準到可直接背誦]

## 3. 名詞解釋
[列出本段3-6個關鍵術語，格式：**術語**：一句話定義（含英文原文）]

## 4. 常見陷阱
[列出3-5個考生最容易混淆或答錯的地方，每個陷阱後給出正確觀念]

## 5. 考題怎麼問
[列出3-4種此主題出現在考題的常見問法，附上「看到XXX關鍵字→答XXX」的判斷規則]

## 6. 記憶口訣
[1-2句易記的中文口訣或記憶法，幫助快速記住最重要的判斷規則或公式]

重要規定：
- 只輸出上述6個區塊，不要輸出其他內容
- 每個區塊都必須有實質內容，不可以空白或敷衍
- 內容必須針對此段落的具體主題，不可以使用通用模板
- 考試重點和考題怎麼問必須反映 IPAS 中級考試的實際出題風格
- 保留所有 ## 標題格式`;

async function callInference(userMsg: string): Promise<string> {
  const proc = spawn(
    [BUN, INFERENCE, "--level", "standard", "--timeout", "60000", SYSTEM_PROMPT, userMsg],
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

  const timeout = new Promise<"timeout">((r) => setTimeout(() => r("timeout"), 70000));
  const done = proc.exited.then(() => "done" as const);
  const result = await Promise.race([done, timeout]);

  if (result === "timeout") {
    proc.kill();
    throw new Error("inference timeout");
  }

  const out = (await new Response(proc.stdout).text()).trim();
  const err = (await new Response(proc.stderr).text()).trim();
  if (proc.exitCode !== 0 || !out) throw new Error(`inference failed: ${err}`);
  return out;
}

function buildPrompt(seg: any, subject: number): string {
  const subjectDesc = subject === 1
    ? "科目一 AI 應用規劃師（著重 AI 導入規劃、專案管理、治理、應用情境判斷）"
    : "科目三 機器學習技術應用（著重機器學習原理、演算法、評估指標、模型選擇與部署）";

  return `科目：${subjectDesc}
段落ID：${seg.id}
段落標題：${seg.title}

請針對「${seg.title}」這個主題，為 IPAS 中級考試考生撰寫完整的6個學習區塊。
內容必須精準、正確、以考試角度切入，適合考前衝刺使用。`;
}

function injectNewContent(existingContent: string, newSections: string): string {
  // Replace sections 1-6, keep section 7 intact
  const s7Match = existingContent.match(/(\n## 7\. 官方指引對應線索\n[\s\S]*?)$/);
  const s7 = s7Match ? s7Match[1] : "";

  // Get title line (# Title)
  const titleMatch = existingContent.match(/^(# [^\n]+\n)/);
  const title = titleMatch ? titleMatch[1] : `# ${""}\n`;

  return title + "\n" + newSections.trim() + (s7 ? "\n" + s7.trim() : "");
}

async function processSegment(seg: any, guide: any, guidePath: string, subject: number): Promise<boolean> {
  const key = `s${subject}_${seg.id}`;
  const state = loadState();
  if (state[key]) {
    console.log(`  [SKIP] s${subject}/${seg.id} already done`);
    return false;
  }

  console.log(`  [REWRITE] s${subject}/${seg.id}: ${seg.title}`);

  try {
    const prompt = buildPrompt(seg, subject);
    const newContent = await callInference(prompt);

    // Validate output has expected sections
    const hasSections = [1,2,3,4,5,6].every(n => newContent.includes(`## ${n}.`));
    if (!hasSections) {
      console.warn(`    ⚠️  Missing sections in output, skipping`);
      return false;
    }

    // Inject new content while preserving section 7
    seg.content = injectNewContent(seg.content ?? `# ${seg.title}\n`, newContent);

    // Write back immediately
    writeJSON(guidePath, guide);
    markDone(key);
    console.log(`    ✅ Done`);
    return true;
  } catch (e: any) {
    console.error(`    ❌ Failed: ${e.message}`);
    return false;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const subjectArg = args.includes("--subject") ? parseInt(args[args.indexOf("--subject") + 1]) : 0;
  const startId = args.includes("--start-id") ? parseInt(args[args.indexOf("--start-id") + 1]) : 1;
  const dryRun = args.includes("--dry-run");

  const subjects = subjectArg ? [subjectArg] : [1, 3];

  for (const subject of subjects) {
    const guidePath = subject === 1 ? PATHS.guideS1 : PATHS.guideS3;
    const guide = readJSON(guidePath);
    if (!guide) { console.error(`Cannot read guide_s${subject}.json`); continue; }

    const segments = guide.segments.filter((s: any) => s.id >= startId);
    console.log(`\n=== Subject ${subject}: processing ${segments.length} segments from id ${startId} ===`);

    let done = 0;
    for (const seg of segments) {
      if (dryRun) {
        const key = `s${subject}_${seg.id}`;
        const state = loadState();
        const status = state[key] ? "DONE" : "PENDING";
        console.log(`  [${status}] s${subject}/${seg.id}: ${seg.title}`);
        continue;
      }

      const rewritten = await processSegment(seg, guide, guidePath, subject);
      if (rewritten) done++;

      // Small pause between calls to be respectful
      await new Promise(r => setTimeout(r, 500));
    }

    if (!dryRun) console.log(`\nSubject ${subject}: rewrote ${done} segments`);
  }

  console.log("\n✅ All done.");
}

main().catch(console.error);
