import { readFileSync, writeFileSync, copyFileSync, mkdirSync } from "fs";

const mode = process.argv[2] || "validate";
const dir = "work_batches/v4_final50";
const src = JSON.parse(readFileSync(`${dir}/source_all.json`, "utf8"));
let candidates = [];
for (const n of [1, 2, 3]) candidates.push(...JSON.parse(readFileSync(`${dir}/candidate_part${n}.json`, "utf8")));
const cm = new Map(candidates.map(x => [x.id, x]));
const H = ["【先抓題目關鍵字】", "【這題在考什麼】", "【正解怎麼想】", "【錯項陷阱】", "【下次怎麼秒判斷】", "【必要名詞】"];
const bad = ["只是相關名詞", "最直接符合題目", "最符合題意", "不是最佳答案", "沒有精準對上題意", "正解之所以成立", "此選項雖可能是相關名詞", "先把題幹縮成", "不能只因名詞相關", "只有作用層次與題幹一致"];
const han = s => (s.match(/[\u3400-\u9fff\uf900-\ufaff]/g) || []).length;
const errors = [], lengths = [];
if (src.length !== 50) errors.push(`source count ${src.length}`);
if (candidates.length !== 50) errors.push(`candidate count ${candidates.length}`);
if (cm.size !== 50) errors.push(`unique count ${cm.size}`);
for (let i = 0; i < src.length; i++) {
  const q = src[i], x = cm.get(q.id);
  if (!x) { errors.push(`${q.id} missing`); continue; }
  if (candidates[i]?.id !== q.id) errors.push(`${q.id} order ${i}: ${candidates[i]?.id}`);
  if (JSON.stringify(Object.keys(x).sort()) !== JSON.stringify(["explanation", "explanation_style", "id", "topic"])) errors.push(`${q.id} keys`);
  if (x.explanation_style !== "teacher_walkthrough_v4_plain_fullpoints") errors.push(`${q.id} style`);
  const n = han(x.explanation); lengths.push({ id: q.id, n }); if (n < 900) errors.push(`${q.id} han ${n}`);
  let prev = -1;
  for (const h of H) { const count = x.explanation.split(h).length - 1, pos = x.explanation.indexOf(h); if (count !== 1 || pos <= prev) errors.push(`${q.id} heading ${h} count=${count}`); prev = pos; }
  const correct = x.explanation.slice(x.explanation.indexOf(H[2]), x.explanation.indexOf(H[3]));
  const answerText = String(q.options[q.answer]).trim();
  if (!new RegExp(`正確答案是\\s*${q.answer}`).test(correct)) errors.push(`${q.id} answer label`);
  if (!correct.includes(answerText)) errors.push(`${q.id} answer text`);
  const traps = x.explanation.slice(x.explanation.indexOf(H[3]), x.explanation.indexOf(H[4]));
  for (const label of Object.keys(q.options)) if (!new RegExp(`(?:^|\\n)\\s*${label}[：:]`).test(traps)) errors.push(`${q.id} option ${label}`);
  for (const b of bad) if (x.explanation.includes(b)) errors.push(`${q.id} forbidden ${b}`);
}
const seen = new Map();
for (const x of candidates) for (const raw of x.explanation.split(/\n+/)) {
  const s = raw.replace(/\s+/g, " ").trim(); if (han(s) < 45) continue;
  const prior = seen.get(s); if (prior && prior !== x.id) errors.push(`duplicate ${prior}/${x.id}: ${s.slice(0, 60)}`); else seen.set(s, x.id);
}
lengths.sort((a, b) => a.n - b.n);
console.log(JSON.stringify({ count: candidates.length, unique: cm.size, min: lengths[0], median: lengths[Math.floor(lengths.length / 2)], max: lengths.at(-1), errors_count: errors.length, errors }, null, 2));
if (errors.length) process.exit(1);
if (mode === "merge") {
  const canonical = JSON.parse(readFileSync("questions.json", "utf8"));
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const backup = `backups/before_final50_merge_${stamp}`;
  mkdirSync(backup, { recursive: true });
  copyFileSync("questions.json", `${backup}/questions.json`);
  copyFileSync("docs/questions.json", `${backup}/docs_questions.json`);
  canonical.questions = canonical.questions.map(q => {
    const c = cm.get(q.id); return c ? { ...q, topic: c.topic, explanation: c.explanation, explanation_style: c.explanation_style } : q;
  });
  const out = JSON.stringify(canonical, null, 2) + "\n";
  writeFileSync("questions.json", out); writeFileSync("docs/questions.json", out);
  console.log(JSON.stringify({ merged: 50, backup }, null, 2));
}
