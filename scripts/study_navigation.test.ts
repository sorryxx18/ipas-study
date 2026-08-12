import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import vm from "node:vm";
import { join } from "node:path";

const ROOT = join(import.meta.dir, "..");

function loadNavigation() {
  const source = readFileSync(join(ROOT, "webapp", "study-navigation.js"), "utf8");
  const datasets: Record<string, any> = {
    "exam_emphasis_s1.json": JSON.parse(readFileSync(join(ROOT, "webapp", "exam_emphasis_s1.json"), "utf8")),
    "exam_emphasis_s3.json": JSON.parse(readFileSync(join(ROOT, "webapp", "exam_emphasis_s3.json"), "utf8")),
  };
  const sandbox: any = {
    window: {},
    URLSearchParams,
    console,
    fetch: async (url: string) => ({ ok: true, json: async () => datasets[url] }),
  };
  vm.runInNewContext(source, sandbox);
  return sandbox.window.StudyNavigation;
}

describe("StudyNavigation", () => {
  test("可由題目 ID 找到對應指引", async () => {
    const nav = loadNavigation();
    const refs = await nav.findGuides("official_115_1_subject1_3");
    expect(refs.length).toBeGreaterThan(0);
    expect(refs.some((ref: any) => ref.subject === 1 && ref.segmentId === 4)).toBe(true);
  });

  test("產生保留來源的雙向網址", () => {
    const nav = loadNavigation();
    const guide = nav.guideUrl({ subject: 1, segmentId: 4 }, "official_115_1_subject1_3", "quiz");
    const quiz = nav.quizUrl("official_115_1_subject1_3", "hotspot");
    expect(guide).toContain("jump=guide");
    expect(guide).toContain("qid=official_115_1_subject1_3");
    expect(quiz).toContain("jump=quiz");
    expect(quiz).toContain("from=hotspot");
  });
});

describe("navigation integration", () => {
  for (const relative of ["webapp/index.html", "docs/index.html"]) {
    test(`${relative} 支援 qid 跳題與題目回指引`, () => {
      const html = readFileSync(join(ROOT, relative), "utf8");
      expect(html).toContain("study-navigation.js?v=20260812");
      expect(html).toContain("buildQuestionGuideLinks");
      expect(html).toContain("/api/quiz/question?id=");
      expect(html).toContain("返回正常刷題進度");
    });
  }

  for (const relative of ["webapp/exam-emphasis.html", "docs/exam-emphasis.html"]) {
    test(`${relative} 將閱讀與正式作答入口分開`, () => {
      const html = readFileSync(join(ROOT, relative), "utf8");
      expect(html).toContain("閱讀這篇指引");
      expect(html).toContain("正式作答代表題");
      expect(html).toContain("前往這一題");
    });
  }
});
