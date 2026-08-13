# iPAS 近期修改與 Claude Code 交接

更新時間：2026-08-13（Asia/Taipei）

> 這份文件是目前最新交接依據。舊的 `RECOVERY_CONTEXT.md`、`CLAUDE_NEXT_PROMPT.md` 與 `TELEGRAM_RECOVERY_CONTEXT.md` 記錄的是 7 月早期狀態，其中「尚未匯入官方題」「下一步解析 PDF」等內容已過期，不可再照做。

---

## 1. 專案、網站與部署位置

### 專案目錄

```text
/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study
```

### 正式站

```text
https://study.tfd-train.com
```

- 服務：Bun `server.ts`
- 本機連接埠：`127.0.0.1:8080`
- LaunchAgent：`com.leif.ipas-study-server`
- Cloudflare Tunnel LaunchAgent：`com.leif.study-tfd-cloudflared`
- 正式站直接使用本機 repo 的 `webapp/` 與 root JSON，所以檔案寫入後通常立即生效；不要為了靜態內容修改而任意重啟服務。

### GitHub 與 GitHub Pages

```text
Repo: https://github.com/sorryxx18/ipas-study
Pages: https://sorryxx18.github.io/ipas-study/
Pages source: main /docs
```

最新人工同步提交：

```text
c6a6c2a7384a8b20388995db8ce92c617d7f5465
補齊題目對應指引覆蓋狀態
```

GitHub Pages workflow `31710162607` 已成功 build＋deploy。

---

## 2. Source of truth 與同步副本

### 題庫（唯一內容來源）

```text
questions.json               # root：正式題庫 source of truth，260 題
docs/questions.json          # GitHub Pages 靜態鏡像
```

- 題庫共 260 題：科目一 130、科目三 130。
- 來源組成：官方 200 題＋自建 60 題。
- `questions.json` 是唯一題庫 source；`docs/questions.json` 只能從 root 同步，不能反向覆蓋。
- 題目解析已於 2026-08-12 全面改為老師講題風格，詳見第 4 節。

### 指引（正式內容來源）

```text
guide_s1.json                # root：科目一正式指引，71 段
guide_s3.json                # root：科目三正式指引，96 段
docs/guide_s1.json           # GitHub Pages 鏡像
docs/guide_s3.json           # GitHub Pages 鏡像
```

- root 是正式站 runtime source。
- `docs/guide_s1.json` 必須與 root `guide_s1.json` 完全相同。
- `docs/guide_s3.json` 必須與 root `guide_s3.json` 完全相同。
- 2026-08-13 的修正只在受影響段落 `content` 末尾附加：

```markdown
## 8. 題庫補充考點
```

- 原本第 1～7 章沒有被刪除或重寫。
- 有補強的 segment 另含：

```json
{
  "coverage_patch_question_ids": ["..."],
  "coverage_patch_version": "question_guide_coverage_v1"
}
```

### 題目→指引映射與覆蓋狀態

```text
webapp/exam_emphasis_s1.json # 正式站科目一映射
webapp/exam_emphasis_s3.json # 正式站科目三映射
docs/exam_emphasis_s1.json   # Pages 鏡像
docs/exam_emphasis_s3.json   # Pages 鏡像
```

每個 `hitQuestions[]` 現在包含：

```json
{
  "id": "題目 ID",
  "note": "映射理由",
  "coverageStatus": "full | partial | none | disputed",
  "coverageNote": "使用者看得到的覆蓋說明"
}
```

**重要：** `exam_emphasis_s1.md`、`exam_emphasis_s3.md` 是 8/11 初版分析文件；2026-08-13 的四級覆蓋狀態是直接寫入 JSON。不要用舊 Markdown 無條件重新生成 JSON，否則會把 `coverageStatus`／`coverageNote` 洗掉。

### 前端與 Pages 鏡像

```text
webapp/index.html             # 正式站主頁
webapp/study-navigation.js    # 正式站題目↔指引導覽
webapp/exam-emphasis.html     # 正式站出題熱區

docs/index.html               # Pages 主頁鏡像
docs/study-navigation.js      # Pages 導覽鏡像
docs/exam-emphasis.html       # Pages 出題熱區（含 EMBEDDED_DATA）
```

- `study-navigation.js` 會把映射的 `coverageStatus`、`coverageNote` 傳給刷題頁。
- 刷題頁目前顯示：
  - ✅ 指引完整涵蓋
  - 🟡 指引部分涵蓋
  - 🔴 指引尚未涵蓋
  - ⚠️ 題目／官方答案有技術爭議
- `exam-emphasis.html` 內含 `EMBEDDED_DATA`，更新映射 JSON 時也要同步更新內嵌資料，否則某些靜態環境會顯示舊資料。

### 個人進度（不可混入內容修改）

```text
progress.json
question_progress.json（若存在，先確認實際用途）
guide_progress.json
daily_log.json
bonus_progress.json
```

這些是使用者個人作答／閱讀／每日任務狀態，不是教材內容。除非使用者明確要求修進度，否則不得重建、清空、回退或用 Git 遠端版本覆蓋。

---

## 3. 8/11：出題熱區與跨頁導覽

主要 Git 歷史：

```text
1208f3b Add exam emphasis analysis page (questions mapped to guide segments)
84cd19c Fix exam-emphasis page: use relative fetch path for JSON data
3ac4972 Embed exam emphasis data directly in the page instead of fetching
3afe574 Add deep link from exam-emphasis hotspots into the guide reader
1c5074b Make TOP hotspot cards scroll to the matching segment, not navigate away
```

做了什麼：

1. 新增「出題熱區分析」頁。
2. 將 260 題映射到科目一／三指引段落。
3. 可由熱區頁跳到指引段落。
4. 可由刷題結果跳到對應指引，再返回題目。
5. 靜態 Pages 因 fetch 路徑／環境問題，加入內嵌資料 fallback。

主要檔案：

```text
webapp/exam-emphasis.html
docs/exam-emphasis.html
webapp/exam_emphasis_s1.json
webapp/exam_emphasis_s3.json
docs/exam_emphasis_s1.json
docs/exam_emphasis_s3.json
webapp/index.html
docs/index.html
server.ts
```

---

## 4. 8/12：題解與閱讀指引全面重寫

主要 Git 歷史：

```text
39aafe2 docs:全面重寫題庫老師講題解析
8a09e0c feat: 改善指引閱讀與題目跳轉
236b439 docs: 全面完善科目一與科目三學習指引
```

### 題目解析

修改：

```text
questions.json
docs/questions.json
```

目標：

- 每題都是繁體中文老師講題，不是短摘要。
- 保留術語、公式、例子、錯項陷阱。
- 解釋正解為何成立，也逐一說明主要錯項為何錯。
- 圖片／程式碼素材缺失時要誠實揭露，不能虛構圖或程式。
- 技術上有爭議者不能硬說其他合理選項必錯。

品質稽核：

```text
audit_reports/explanation_quality_audit_20260811_231617.md
audit_reports/explanation_quality_audit_20260811_231617.csv
```

### 指引閱讀器

新增／修改：

```text
webapp/guide-reader.js
docs/guide-reader.js
webapp/study-navigation.js
docs/study-navigation.js
webapp/index.html
docs/index.html
scripts/guide_reader_ui.test.ts
scripts/study_navigation.test.ts
```

目標：

- 指引變成可閱讀的段落式教材。
- 段內有快速導覽與折疊章節。
- 題目／熱區／指引間可深連結。
- 「閱讀、聽課、刷題」是不同使用模式，不可把逐題解答直接塞入閱讀指引。

### 科目一／三指引

修改：

```text
guide_s1.json
guide_s3.json
docs/guide_s1.json
docs/guide_s3.json
```

每段的閱讀正文採 `web_reading_calibrated_v2`，通常含：

1. 核心概念
2. 考試重點
3. 名詞解釋
4. 常見陷阱
5. 考題怎麼問
6. 記憶口訣
7. 官方指引對應線索

2026-08-13 後，必要段落另有第 8 章題庫補充考點。

---

## 5. 8/13：260 題「題目→指引」語意覆蓋稽核與補強

### 為什麼做

原本「有映射連結」不代表「讀完該指引真的能解題」。因此逐題檢查：

> 只讀映射到的指引內容，是否足以推出正解並排除主要錯項？

這是語意稽核，不是只找關鍵字。

### 初始稽核結果

| 狀態 | 題數 |
|---|---:|
| `full` | 163 |
| `partial` | 54 |
| `none` | 30 |
| `disputed` | 13 |
| 總計 | 260 |

分科：

| 科目 | full | partial | none | disputed | 合計 |
|---|---:|---:|---:|---:|---:|
| 科目一 | 73 | 34 | 17 | 6 | 130 |
| 科目三 | 90 | 20 | 13 | 7 | 130 |

### 實際修正

- `partial` 54 題＋`none` 30 題：共 84 題內容缺口已補齊。
- `disputed` 13 題：不硬改成 full；指引明列「官方作答」與「技術事實／爭議」。
- 共補強 51 個指引段落：
  - 科目一 31 段
  - 科目三 20 段
- 同一段多題的共同知識已合併成一次完整教材，沒有逐題重複貼解析。
- 補強內容禁止答案字母與 A/B/C/D 逐項解析，維持「閱讀歸閱讀、刷題歸刷題」。

### 完整稽核資料

```text
audit_reports/question_guide_coverage_audit_20260813.json  # 260 題完整逐題資料
audit_reports/question_guide_coverage_audit_20260813.md    # 人類可讀摘要與 13 題爭議表
```

JSON 每題含：

```text
id
status
primary_subject
primary_segment_id
required_knowledge
covered_knowledge
missing_knowledge
rationale
patch_sections
verification_terms
```

### 備份

```text
backups/guide_coverage_fix_20260813_212450/
```

內含修改前的指引、映射、前端導覽與 protected SHA 清單。此備份只在本機，沒有提交 GitHub。

### 驗證結果

- 51 段精確涵蓋 97 題（84 題內容缺口＋13 題爭議），無漏題。
- 跨段無 80 字以上完全相同長文。
- 補充教材沒有答案字母或逐選項刷題解析格式。
- root／docs 指引一致。
- webapp／docs 映射一致。
- JavaScript 語法通過。
- 正式站與 GitHub Pages 均實際載入 `full`／`disputed`。
- S3-75 的第 8 章已實際渲染，含 LoRA 公式、參數預算、跨層覆蓋與官方／技術事實。
- 瀏覽器 console 0 error。

---

## 6. 13 題技術爭議

完整理由看：

```text
audit_reports/question_guide_coverage_audit_20260813.md
audit_reports/question_guide_coverage_audit_20260813.json
```

題目 ID：

```text
official_114_2_subject1_5
official_114_2_subject1_44
official_114_2_subject1_50
official_114_2_subject3_17
official_114_2_subject3_34
official_114_2_subject3_37
official_115_1_subject1_46
official_115_1_subject3_30
official_115_1_subject3_35
official_115_1_subject3_45
official_115_1_subject3_46
S1_10
S1_23
```

處理原則：

1. 題庫官方答案可保留，不能擅自改 key。
2. 指引需區分命題意圖、官方作答與嚴格技術／法律事實。
3. 前端保持 `disputed`，不可為了數字漂亮改成 `full`。
4. 若未來查到官方勘誤或完整原圖／程式碼，才重新稽核並留下來源。

---

## 7. 現在最重要的 Git 風險

### 遠端已完成

遠端 `origin/main` 最新人工同步提交是：

```text
c6a6c2a7384a8b20388995db8ce92c617d7f5465
```

該提交只包含本次 16 個成果檔，沒有題庫與個人進度。

### 本機工作樹目前不是乾淨狀態

交接時實際 `git status --short`：

```text
UU daily_log.json
MM docs/questions.json
MM questions.json
UU progress.json
M  guide／映射／前端等本次成果檔
?? audit_reports/question_guide_coverage_audit_20260813.json
?? audit_reports/question_guide_coverage_audit_20260813.md
```

原因：本機正式站有自動 Git 同步／背景 pull，且題庫與進度先前已有未合併／未提交狀態；這次為避免捲入使用者資料，使用乾淨 `/tmp` clone 從最新 `origin/main` 複製 16 個成果檔並獨立 push。因此：

- **遠端與 Pages 已經有本次成果。**
- 本機 `M/??` 不代表成果尚未同步；只是本機 HEAD／index 未對齊遠端。
- `progress.json`、`daily_log.json` 的遠端版本在 `c6a6c2a` 前後 SHA 完全相同，這次沒有修改。

### 禁止直接做的事

在沒有先備份與確認 index 三階段內容前，不可：

```bash
git add -A
git commit -am ...
git reset --hard
git checkout -- progress.json daily_log.json questions.json
git pull --rebase --autostash
```

`server.ts` 的 `gitSync()` 目前會：

```text
git pull --rebase --autostash
git add -A
git commit
git push
```

在工作樹有 `UU/MM` 時這很危險，也可能持續 sync failed。若 Claude Code 要整理 Git：

1. 先停止或暫停自動 Git sync（可透過 `NO_GIT_SYNC=1` 的受控方式；不要隨意停正式站）。
2. 先備份上述 protected 檔、index stage 1/2/3 與工作樹版本。
3. `git fetch origin`，確認 `origin/main` 至少為 `c6a6c2a`。
4. 分別判讀 `questions/progress/daily_log` 的 ours、theirs、工作樹與遠端，保留使用者最新真實資料。
5. 不得用「遠端較新」或「本機較新」單一時間判斷進度真相。
6. 整理 Git 應是獨立任務，不要跟教材內容修改混在同一 commit。

---

## 8. Claude Code 後續修改規則

### 題解

- 只改使用者指定的題庫範圍；不要順手重寫其他題。
- 老師講題要白話但不精簡，保留公式、術語、例子與陷阱。
- 疑義先查官方或第一手技術文件。
- 缺圖／缺程式碼要明說，不能虛構素材。
- 不可改錯題 key 只為讓解析好寫。

### 題目→指引

- 不能只因有關鍵字就標 `full`。
- `full` 的標準是：讀完指引能推出正解並排除主要錯項。
- 同一題若多映射，只有真正完整教學的主段落可標 full；延伸段落可標 partial 並指向主段落。
- `disputed` 必須保留官方作答／技術事實分層。

### 指引

- 閱讀／聽課／刷題分離。
- 指引補充教概念、機制、例子與常見誤解；不要出現「正確答案是 A」或 A/B/C/D 逐項解析。
- 優先補入既有最合理段落，不要為單題濫建新段落。
- 修改 root guide 後，同步 `docs/guide_*.json`。

### 前端與部署

- 修改 `webapp/` 後，評估是否要同步 `docs/`。
- 修改映射 JSON 後，同步 `exam-emphasis.html` 的 `EMBEDDED_DATA`。
- 驗證正式站重要 URL 未被改壞：
  - `https://study.tfd-train.com`
  - `https://study.tfd-train.com/exam-emphasis.html`
  - `https://sorryxx18.github.io/ipas-study/`
- 不要把 GitHub Pages 靜態展示進度當成正式站個人進度。

---

## 9. 快速驗證清單

內容修改完成後至少執行：

```bash
# JSON 能解析
python3 -m json.tool guide_s1.json >/dev/null
python3 -m json.tool guide_s3.json >/dev/null
python3 -m json.tool webapp/exam_emphasis_s1.json >/dev/null
python3 -m json.tool webapp/exam_emphasis_s3.json >/dev/null

# JS 語法
node --check webapp/study-navigation.js
node --check docs/study-navigation.js

# root/docs 同步
cmp guide_s1.json docs/guide_s1.json
cmp guide_s3.json docs/guide_s3.json
cmp webapp/exam_emphasis_s1.json docs/exam_emphasis_s1.json
cmp webapp/exam_emphasis_s3.json docs/exam_emphasis_s3.json

# whitespace／patch 錯誤
git diff --check
```

另需用瀏覽器實際檢查：

1. 一題 `full`：`official_115_1_subject3_24`。
2. 一題 `disputed`：`official_115_1_subject3_35`。
3. S3 第 75 段能顯示第 8 章。
4. console 0 error。

---

## 10. 建議 Claude Code 開場指令

```text
請先閱讀：
/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/CLAUDE_CODE_HANDOFF_20260813.md

把它視為目前 iPAS 最新交接依據。不要照舊的 RECOVERY_CONTEXT.md 或 CLAUDE_NEXT_PROMPT.md 去重新解析官方 PDF；260 題題庫、題解、指引補強與覆蓋稽核都已完成。

開始任何修改前先執行 git status、git fetch origin，確認 origin/main 至少是 c6a6c2a。注意本機 questions.json/docs/questions.json/progress.json/daily_log.json 有 MM/UU 狀態，禁止直接 git add -A、reset --hard、checkout 或 pull --rebase。先說明你看到的狀態與準備保留哪些資料，再依使用者指定任務做最小修改。
```
