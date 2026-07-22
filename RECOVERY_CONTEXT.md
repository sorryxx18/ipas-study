# Claude Code iPAS 恢復上下文

產生時間：2026-07-04

## 使用者要求

使用者正在準備 iPAS AI應用規劃師中級，選考：

- 科目一：人工智慧技術應用與規劃
- 科目三：機器學習技術與應用
- 考試日期：2026-11-14

使用者要求：

- 課程與刷題並行
- 刷題一題一題出
- 必須記錄答錯題、分析錯因
- 錯題要重複考，直到每一題都答對
- 考古題優先，自建題作補充
- 清除 / 重啟 / compact 前必須先記住目前上下文

## 現有 Claude Code 題庫狀態

Claude Code 已建立：

- `/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/questions.json`
- `/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/progress.json`
- `/Users/leifhuang/.claude/projects/-Users-leifhuang/memory/project_ipas_exam.md`

目前 `questions.json` 是自建 60 題：

- 科目一 30 題
- 科目三 30 題

`progress.json` 顯示尚未開始作答，`completed_correct` 為空，`wrong_history` 為空。

## 官方考古題 PDF 位置

官方中級科目一、科目三歷屆公告試題已由 Hermes 下載並解壓縮完成：

優先使用：

`/Users/leifhuang/AIAP_middle_subject_1_3_past_exams`

說明檔：

`/Users/leifhuang/AIAP_EXAM_LOCATION.md`

原始下載資料夾：

`/Users/leifhuang/Downloads/AIAP_中級_科目1_3_歷屆考題`

內含 4 份 PDF：

- 114年第二梯次_中級_科目1_人工智慧技術應用與規劃_公告試題.pdf
- 115年第一次_中級_科目1_人工智慧技術應用與規劃_公告試題.pdf
- 114年第二梯次_中級_科目3_機器學習技術與應用_公告試題.pdf
- 115年第一次_中級_科目3_機器學習技術與應用_公告試題.pdf

## 下一步

請解析官方 PDF，抽出題目、選項、答案與解析，匯入 `questions.json`，並更新 `progress.json`：

1. 官方考古題排在刷題最前面。
2. CCChen 題與自建題排在官方考古題後面。
3. 題目需標記來源：official_114_2、official_115_1、ccchen、generated。
4. 刷題時每次只出一題。
5. 使用者答錯要記錄錯因與重考次數。
