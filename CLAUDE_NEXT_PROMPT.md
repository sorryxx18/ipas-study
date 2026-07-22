# 下一步請直接照做

請讀：

`/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/RECOVERY_CONTEXT.md`

然後繼續解析官方 PDF 並匯入題庫。

## 重要：不要用 Read 一次讀整份 PDF

Claude Code 的 Read 工具讀 PDF 會遇到頁數限制，例如：

- `This PDF has 14 pages, which is too many to read at once`
- `This PDF has 19 pages, which is too many to read at once`

請改用下列方式：

1. 用 `/opt/homebrew/bin/pdftotext` 把 PDF 轉成文字檔；或
2. 用 `python3` + `pypdf` 逐頁解析 PDF。

## 題庫檔案

- 題庫：`/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/questions.json`
- 進度：`/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/progress.json`

## 官方 PDF 位置

`/Users/leifhuang/AIAP_middle_subject_1_3_past_exams`

## 需求

- 解析官方 114-2、115-1 的中級科目一與科目三 PDF。
- 抽出題目、選項、答案、解析。
- 匯入 `questions.json`。
- 官方考古題要排在自建 60 題前面。
- 每題加 `source` 欄位，例如：
  - `official_114_2_subject1`
  - `official_115_1_subject1`
  - `official_114_2_subject3`
  - `official_115_1_subject3`
  - `generated`
- 更新 `progress.json`，刷題順序以官方考古題優先。
- 完成後請回覆：新增幾題、各來源幾題、目前題庫總題數。
