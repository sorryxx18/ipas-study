(function (root) {
  "use strict";

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function renderInline(value) {
    let text = escapeHtml(value);
    text = text.replace(/`([^`]+)`/g, "<code>$1</code>");
    text = text.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    text = text.replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>");
    return text;
  }

  function slugify(title, index) {
    const slug = String(title)
      .toLowerCase()
      .replace(/<[^>]+>/g, "")
      .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 36);
    return `guide-section-${index + 1}-${slug || "content"}`;
  }

  function parseSections(markdown) {
    const lines = String(markdown ?? "").replace(/\r\n?/g, "\n").split("\n");
    const sections = [];
    let current = { title: "導讀", lines: [] };

    for (const line of lines) {
      const match = line.match(/^##\s+(.+)\s*$/);
      if (match) {
        const meaningful = current.lines.some((item) => item.trim() && !/^#\s+/.test(item));
        if (meaningful) sections.push(current);
        current = { title: match[1].trim(), lines: [] };
      } else if (!/^#\s+/.test(line)) {
        current.lines.push(line);
      }
    }

    const meaningful = current.lines.some((item) => item.trim());
    if (meaningful || sections.length === 0) sections.push(current);

    return sections.map((section, index) => ({
      id: slugify(section.title, index),
      title: section.title,
      body: section.lines.join("\n").trim(),
    }));
  }

  function splitTableRow(line) {
    return line.trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim());
  }

  function isTableDivider(line) {
    const cells = splitTableRow(line);
    return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell));
  }

  function renderBlocks(markdown) {
    const lines = String(markdown ?? "").split("\n");
    const html = [];
    let index = 0;

    while (index < lines.length) {
      const line = lines[index].trim();
      if (!line) {
        index += 1;
        continue;
      }

      if (line.includes("|") && index + 1 < lines.length && isTableDivider(lines[index + 1])) {
        const headers = splitTableRow(lines[index]);
        const rows = [];
        index += 2;
        while (index < lines.length && lines[index].trim().includes("|") && lines[index].trim()) {
          rows.push(splitTableRow(lines[index]));
          index += 1;
        }
        html.push(`<div class="guide-table-wrap"><table><thead><tr>${headers.map((cell) => `<th>${renderInline(cell)}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${renderInline(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
        continue;
      }

      if (/^###\s+/.test(line)) {
        html.push(`<h3>${renderInline(line.replace(/^###\s+/, ""))}</h3>`);
        index += 1;
        continue;
      }

      if (/^>\s?/.test(line)) {
        const quote = [];
        while (index < lines.length && /^>\s?/.test(lines[index].trim())) {
          quote.push(lines[index].trim().replace(/^>\s?/, ""));
          index += 1;
        }
        html.push(`<blockquote>${quote.map(renderInline).join("<br>")}</blockquote>`);
        continue;
      }

      if (/^[-*]\s+/.test(line)) {
        const items = [];
        while (index < lines.length && /^[-*]\s+/.test(lines[index].trim())) {
          items.push(lines[index].trim().replace(/^[-*]\s+/, ""));
          index += 1;
        }
        html.push(`<ul>${items.map((item) => `<li>${renderInline(item)}</li>`).join("")}</ul>`);
        continue;
      }

      if (/^\d+[.)]\s+/.test(line)) {
        const items = [];
        while (index < lines.length && /^\d+[.)]\s+/.test(lines[index].trim())) {
          items.push(lines[index].trim().replace(/^\d+[.)]\s+/, ""));
          index += 1;
        }
        html.push(`<ol>${items.map((item) => `<li>${renderInline(item)}</li>`).join("")}</ol>`);
        continue;
      }

      const paragraph = [line];
      index += 1;
      while (index < lines.length) {
        const next = lines[index].trim();
        if (!next || /^###\s+/.test(next) || /^>\s?/.test(next) || /^[-*]\s+/.test(next) || /^\d+[.)]\s+/.test(next)) break;
        if (next.includes("|") && index + 1 < lines.length && isTableDivider(lines[index + 1])) break;
        paragraph.push(next);
        index += 1;
      }
      html.push(`<p>${paragraph.map(renderInline).join("<br>")}</p>`);
    }

    return html.join("");
  }

  function isInitiallyOpen(section, index) {
    return index < 3 || /^1[.、\s]/.test(section.title) || /^2[.、\s]/.test(section.title);
  }

  function render(markdown) {
    const sections = parseSections(markdown);
    const chars = String(markdown ?? "").replace(/\s/g, "").length;
    const minutes = Math.max(1, Math.ceil(chars / 500));
    const nav = sections.map((section) => `<button type="button" class="guide-nav-chip" data-target="${section.id}" onclick="GuideReader.openAndScroll('${section.id}')">${escapeHtml(section.title.replace(/^\d+[.、]\s*/, ""))}</button>`).join("");
    const cards = sections.map((section, index) => {
      const open = isInitiallyOpen(section, index);
      return `<section class="guide-section-card${open ? " open" : ""}" id="${section.id}">
        <button type="button" class="guide-section-toggle" aria-expanded="${open}" onclick="GuideReader.toggleSection('${section.id}')">
          <span>${escapeHtml(section.title)}</span><span class="guide-section-arrow">⌄</span>
        </button>
        <div class="guide-section-body"${open ? "" : " hidden"}>${renderBlocks(section.body)}</div>
      </section>`;
    }).join("");

    return `<div class="guide-reader" data-guide-reader>
      <div class="guide-reading-meta"><span>約 ${minutes} 分鐘</span><span>${sections.length} 個章節</span></div>
      <div class="guide-reading-progress" aria-label="本段閱讀進度"><div class="guide-reading-progress-fill" data-guide-progress></div></div>
      <nav class="guide-section-nav" aria-label="段內快速導覽">${nav}</nav>
      <div class="guide-sections">${cards}</div>
      <button type="button" class="guide-back-top" onclick="GuideReader.scrollToTop()">↑ 回到本段頂部</button>
    </div>`;
  }

  function toggleSection(id, forceOpen) {
    if (typeof document === "undefined") return;
    const card = document.getElementById(id);
    if (!card) return;
    const body = card.querySelector(".guide-section-body");
    const button = card.querySelector(".guide-section-toggle");
    const shouldOpen = forceOpen === undefined ? !card.classList.contains("open") : forceOpen;
    card.classList.toggle("open", shouldOpen);
    if (body) body.hidden = !shouldOpen;
    if (button) button.setAttribute("aria-expanded", String(shouldOpen));
  }

  function openAndScroll(id) {
    if (typeof document === "undefined") return;
    toggleSection(id, true);
    const target = document.getElementById(id);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function scrollToTop() {
    if (typeof document === "undefined") return;
    const reader = document.querySelector("[data-guide-reader]");
    if (reader) reader.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  let progressHandler = null;
  function initProgress() {
    if (typeof window === "undefined" || typeof document === "undefined") return;
    if (progressHandler) window.removeEventListener("scroll", progressHandler);
    progressHandler = function () {
      const reader = document.querySelector("[data-guide-reader]");
      const bar = document.querySelector("[data-guide-progress]");
      if (!reader || !bar) return;
      const rect = reader.getBoundingClientRect();
      const viewport = window.innerHeight || 1;
      const travelled = Math.max(0, viewport * 0.3 - rect.top);
      const distance = Math.max(1, rect.height - viewport * 0.6);
      const progress = Math.min(100, Math.round((travelled / distance) * 100));
      bar.style.width = `${progress}%`;
    };
    window.addEventListener("scroll", progressHandler, { passive: true });
    progressHandler();
  }

  root.GuideReader = {
    escapeHtml,
    parseSections,
    renderBlocks,
    render,
    toggleSection,
    openAndScroll,
    scrollToTop,
    initProgress,
  };
})(typeof window !== "undefined" ? window : globalThis);
