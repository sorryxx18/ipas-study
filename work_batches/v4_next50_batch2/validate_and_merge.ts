import { readFileSync, writeFileSync } from "fs";
import { createHash } from "crypto";

const ROOT = process.cwd();
const STYLE = "teacher_walkthrough_v4_plain_fullpoints";
const HEADINGS = [
  "【先抓題目關鍵字】",
  "【這題在考什麼】",
  "【正解怎麼想】",
  "【錯項陷阱】",
  "【下次怎麼秒判斷】",
  "【必要名詞】",
];
const BATCH_DIR = `${ROOT}/work_batches/v4_next50_batch2`;
const CANDIDATES = [1, 2, 3, 4, 5, 6].map(n => `${BATCH_DIR}/candidate_part${n}.json`);
const SOURCE_PATH = `${BATCH_DIR}/source_all.json`;
const TARGET_IDS_PATH = `${ROOT}/backups/explanation_v4_next50_batch2_20260901_215157/target_ids.json`;
const OUT_PATH = `${BATCH_DIR}/candidate_all.json`;
const FORBIDDEN = [
  "只是相關名詞",
  "最直接符合題目",
  "最符合題意",
  "不是最佳答案",
  "沒有精準對上題意",
  "正解之所以成立",
  "此選項雖可能是相關名詞",
  "先把題幹縮成",
  "不能只因名詞相關",
  "只有作用層次與題幹一致",
];

type SourceQuestion = {
  id: string;
  topic?: string;
  question?: string;
  options: Record<string, string>;
  answer: string;
  explanation?: string;
  explanation_style?: string;
  [key: string]: unknown;
};

type Candidate = {
  id: string;
  topic: string;
  explanation: string;
  explanation_style: string;
};

function load<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8"));
}

function normalize(s: string): string {
  return s.normalize("NFKC")
    .replace(/[\s「」『』“”"'：:／/（）()，,。．、；;！？!?·・—–-]/g, "")
    .toLowerCase();
}

function hanCount(s: string): number {
  return (s.match(/[\p{Script=Han}]/gu) ?? []).length;
}

function sha(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function sentences(text: string): string[] {
  return text
    .split(/[。！？\n]/)
    .map(s => s.trim().replace(/^[-*\s]+/, ""))
    .filter(s => hanCount(s) >= 28);
}

function validate(): { source: SourceQuestion[]; candidates: Candidate[]; report: unknown } {
  const source = load<SourceQuestion[]>(SOURCE_PATH);
  const expectedIds = load<string[]>(TARGET_IDS_PATH);
  const candidates = CANDIDATES.flatMap(path => load<Candidate[]>(path));
  const errors: string[] = [];
  const warnings: string[] = [];
  const allowedKeys = ["explanation", "explanation_style", "id", "topic"];

  if (source.length !== 50) errors.push(`source count ${source.length} != 50`);
  if (candidates.length !== 50) errors.push(`candidate count ${candidates.length} != 50`);
  const ids = candidates.map(x => x.id);
  if (new Set(ids).size !== ids.length) errors.push("candidate IDs are not unique");
  if (JSON.stringify(ids) !== JSON.stringify(expectedIds)) errors.push("candidate ID order/scope differs from locked target IDs");

  const sourceById = new Map(source.map(q => [q.id, q]));
  const sentenceOwners = new Map<string, Set<string>>();
  const lengths: Record<string, number> = {};

  for (const c of candidates) {
    const q = sourceById.get(c.id);
    if (!q) { errors.push(`${c.id}: missing source`); continue; }
    const keys = Object.keys(c).sort();
    if (JSON.stringify(keys) !== JSON.stringify(allowedKeys)) errors.push(`${c.id}: keys ${keys.join(",")}`);
    if (c.explanation_style !== STYLE) errors.push(`${c.id}: wrong style ${c.explanation_style}`);
    if (!c.topic?.trim()) errors.push(`${c.id}: empty topic`);
    if (!c.explanation?.trim()) { errors.push(`${c.id}: empty explanation`); continue; }

    const h = hanCount(c.explanation);
    lengths[c.id] = h;
    if (h < 900) errors.push(`${c.id}: only ${h} Han chars (<900)`);

    let prev = -1;
    for (const heading of HEADINGS) {
      const count = c.explanation.split(heading).length - 1;
      const pos = c.explanation.indexOf(heading);
      if (count !== 1) errors.push(`${c.id}: heading ${heading} count=${count}`);
      if (pos <= prev) errors.push(`${c.id}: heading order failure at ${heading}`);
      prev = pos;
    }

    const answer = String(q.answer).trim();
    const answerText = String(q.options?.[answer] ?? "").trim();
    const correctStart = c.explanation.indexOf("【正解怎麼想】");
    const correctEnd = c.explanation.indexOf("【錯項陷阱】");
    const correct = c.explanation.slice(correctStart, correctEnd);
    if (!new RegExp(`正確答案是\\s*${answer}(?:[。．、：:，,]|\\s)`).test(correct)) {
      errors.push(`${c.id}: correct section does not explicitly say 正確答案是 ${answer}`);
    }
    if (!normalize(correct).includes(normalize(answerText))) {
      errors.push(`${c.id}: correct section lacks full official option text: ${answerText}`);
    }

    for (const label of Object.keys(q.options ?? {})) {
      const trapStart = c.explanation.indexOf("【錯項陷阱】");
      const trapEnd = c.explanation.indexOf("【下次怎麼秒判斷】");
      const trap = c.explanation.slice(trapStart, trapEnd);
      if (!new RegExp(`(?:^|\\n)\\s*${label}[：:]`).test(trap)) errors.push(`${c.id}: missing ${label}： in 錯項陷阱`);
    }

    for (const phrase of FORBIDDEN) {
      if (c.explanation.includes(phrase)) errors.push(`${c.id}: forbidden phrase「${phrase}」`);
    }

    for (const s of sentences(c.explanation)) {
      const n = normalize(s);
      if (n.length < 28) continue;
      if (!sentenceOwners.has(n)) sentenceOwners.set(n, new Set());
      sentenceOwners.get(n)!.add(c.id);
    }
  }

  for (const [sentence, owners] of sentenceOwners) {
    if (owners.size > 1) errors.push(`duplicate long sentence across ${[...owners].join(",")}: ${sentence.slice(0, 80)}`);
  }

  const sortedLengths = Object.values(lengths).sort((a,b) => a-b);
  const report = {
    valid: errors.length === 0,
    count: candidates.length,
    unique_ids: new Set(ids).size,
    min_han: sortedLengths[0] ?? 0,
    median_han: sortedLengths[Math.floor(sortedLengths.length / 2)] ?? 0,
    max_han: sortedLengths.at(-1) ?? 0,
    errors,
    warnings,
  };
  writeFileSync(OUT_PATH, JSON.stringify(candidates, null, 2) + "\n");
  writeFileSync(`${BATCH_DIR}/validation.json`, JSON.stringify(report, null, 2) + "\n");
  console.log(JSON.stringify(report, null, 2));
  if (errors.length) process.exit(1);
  return { source, candidates, report };
}

function merge(): void {
  const { candidates } = validate();
  const candidateById = new Map(candidates.map(c => [c.id, c]));
  const rootRaw = load<any>(`${ROOT}/questions.json`);
  const rootItems: SourceQuestion[] = Array.isArray(rootRaw) ? rootRaw : rootRaw.questions;
  const beforeProtected = load<string[]>(TARGET_IDS_PATH);
  let changed = 0;
  for (const q of rootItems) {
    const c = candidateById.get(q.id);
    if (!c) continue;
    q.topic = c.topic;
    q.explanation = c.explanation;
    q.explanation_style = c.explanation_style;
    changed++;
  }
  if (changed !== 50) throw new Error(`merge changed ${changed}, expected 50`);
  const out = JSON.stringify(rootRaw, null, 2) + "\n";
  writeFileSync(`${ROOT}/questions.json`, out);
  writeFileSync(`${ROOT}/docs/questions.json`, out);
  console.log(JSON.stringify({ merged: changed, ids: beforeProtected, root_sha256: sha(`${ROOT}/questions.json`), docs_sha256: sha(`${ROOT}/docs/questions.json`) }, null, 2));
}

const mode = process.argv[2] ?? "validate";
if (mode === "validate") validate();
else if (mode === "merge") merge();
else throw new Error(`unknown mode: ${mode}`);
