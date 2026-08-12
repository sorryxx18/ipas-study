import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import vm from "node:vm";
import { join } from "node:path";

const ROOT = join(import.meta.dir, "..");

function loadGuideReader() {
  const source = readFileSync(join(ROOT, "webapp", "guide-reader.js"), "utf8");
  const sandbox: any = { window: {} };
  vm.runInNewContext(source, sandbox);
  return sandbox.window.GuideReader;
}

const SAMPLE = `# 範例主題

這是一段**正式說法**。

## 1. 核心概念
- 第一個重點
- 第二個重點

## 2. 考試重點
| 方法 | 特性 |
|---|---|
| CBOW | 速度快 |

## 3. 名詞解釋
<script>alert('xss')</script>`;

describe("GuideReader", () => {
  test("將教材依二級標題拆成可導覽章節", () => {
    const reader = loadGuideReader();
    const sections = reader.parseSections(SAMPLE);
    expect(sections.map((section: any) => section.title)).toEqual([
      "導讀",
      "1. 核心概念",
      "2. 考試重點",
      "3. 名詞解釋",
    ]);
  });

  test("將標題、粗體、清單與表格渲染成語意化 HTML", () => {
    const reader = loadGuideReader();
    const html = reader.render(SAMPLE);
    expect(html).toContain("guide-section-nav");
    expect(html).toContain("guide-section-card");
    expect(html).toContain("<strong>正式說法</strong>");
    expect(html).toContain("<ul>");
    expect(html).toContain("<table>");
    expect(html).not.toContain("## 1. 核心概念");
  });

  test("先跳脫教材中的 HTML，再套用安全 Markdown 標記", () => {
    const reader = loadGuideReader();
    const html = reader.render(SAMPLE);
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
  });

  test("科目一與科目三共 167 段教材皆可渲染", () => {
    const reader = loadGuideReader();
    const files = ["guide_s1.json", "guide_s3.json"];
    const segments = files.flatMap((file) => JSON.parse(readFileSync(join(ROOT, file), "utf8")).segments);
    expect(segments).toHaveLength(167);
    for (const segment of segments) {
      const html = reader.render(segment.content);
      expect(html).toContain("guide-section-card");
      expect(html).not.toContain("<script>");
    }
  });
});

describe("guide reader integration", () => {
  for (const relative of ["webapp/index.html", "docs/index.html"]) {
    test(`${relative} 使用共同的 GuideReader`, () => {
      const html = readFileSync(join(ROOT, relative), "utf8");
      expect(html).toContain('src="guide-reader.js?v=20260812"');
      expect(html).toContain("GuideReader.render");
      expect(html).toContain("initGuideReadingProgress");
    });
  }
});
