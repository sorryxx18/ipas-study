(function (root) {
  "use strict";

  let cache = null;

  async function loadMaps() {
    if (cache) return cache;
    const files = [
      { subject: 1, url: "exam_emphasis_s1.json" },
      { subject: 3, url: "exam_emphasis_s3.json" },
    ];
    const datasets = await Promise.all(files.map(async (item) => {
      const response = await fetch(item.url);
      if (!response.ok) throw new Error(`考點映射載入失敗：${response.status}`);
      return { subject: item.subject, data: await response.json() };
    }));
    cache = datasets;
    return cache;
  }

  async function findGuides(questionId) {
    if (!questionId) return [];
    try {
      const datasets = await loadMaps();
      const matches = [];
      for (const { subject, data } of datasets) {
        for (const segment of data.segments || []) {
          for (const question of segment.hitQuestions || []) {
            if (question.id === questionId) {
              matches.push({
                subject,
                segmentId: segment.id,
                segmentTitle: segment.title,
                note: question.note || "",
              });
            }
          }
        }
      }
      return matches;
    } catch (error) {
      console.warn(error);
      return [];
    }
  }

  function guideUrl(ref, questionId, from) {
    const params = new URLSearchParams({
      jump: "guide",
      subject: String(ref.subject),
      seg: String(ref.segmentId),
      from: from || "quiz",
    });
    if (questionId) params.set("qid", questionId);
    return `?${params.toString()}`;
  }

  function quizUrl(questionId, from) {
    const params = new URLSearchParams({ jump: "quiz", from: from || "hotspot" });
    if (questionId) params.set("qid", questionId);
    return `?${params.toString()}`;
  }

  function sourceLabel(questionId) {
    const official = String(questionId || "").match(/^official_(\d{3})_(\d)_subject(\d)_(\d+)$/);
    if (official) return `${official[1]}-${official[2]} 科目${official[3]}第 ${official[4]} 題`;
    return String(questionId || "自編題").startsWith("official_") ? "官方題" : "題庫題目";
  }

  root.StudyNavigation = { loadMaps, findGuides, guideUrl, quizUrl, sourceLabel };
})(typeof window !== "undefined" ? window : globalThis);
