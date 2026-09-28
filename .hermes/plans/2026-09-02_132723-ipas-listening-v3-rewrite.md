# iPAS 科目一與科目三 v3 聆聽逐字稿重寫計畫

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 依 `guide_s1.json` 與 `guide_s3.json` 的正式 v3 內容，重寫科目一第 11–71 段與科目三第 1–96 段，共 157 段、16 份可直接交給後續 TTS 管線的臺灣繁體中文老師講課逐字稿；不處理 TTS、合輯、字幕、YouTube、播放清單或追蹤 JSON。

**Architecture:** 正式 guide 是唯一內容來源；科目一第 1–10 段完成稿與單段樣稿只作語氣、密度及 TTS 斷句基準。先按「單段候選稿」產生與驗收，再組裝成 16 份正式合輯；每份合輯先在隔離工作區通過結構、來源涵蓋與聽感審查，最後才原子式覆寫正式 TXT。

**Tech Stack:** UTF-8 純文字、Python 3、JSON guide、既有 `validate_listening_scripts.py`、Hermes 平行子代理與人工語意審查。

---

## 一、已確認現況

1. 正式來源：
   - `/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/guide_s1.json`
   - `/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study/guide_s3.json`
2. 規格：`/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/WRITING_SPEC.md`
3. 驗證器：`/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/validate_listening_scripts.py`
4. 語氣基準：
   - `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S1_01_10_listening_script.txt`
   - `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2_samples/IPAS_S1_01_listening_sample.txt`
5. 科目一第 1–10 段已完成 TTS、影片、字幕與追蹤，不納入重寫範圍。
6. 8 月 12 日舊影片保留，不刪除、不修改。
7. 交接文件寫「其餘 163 段」是算術筆誤；正式範圍為 61＋96＝157 段。
8. 16 份舊逐字稿目前均只有 `source_ratio < 0.75` 這項自動驗證失敗，但本次仍須依新版 source 全面重寫，不能把舊稿補字數後冒充新版。
9. 16 份目標合輯依現行驗證器的最低總字元要求合計約 1,256,993 字元；實作時應保留 1–2% 安全餘量，不貼著門檻寫。
10. 已完成的科目一第 1–10 段，目前也因 `source_ratio=0.37` 未通過現行驗證器。這是既有完成品的已知例外；本工作不得為追求全套 exit 0 而重寫或覆蓋它。

## 二、不可變更範圍

- 不修改 `IPAS_S1_01_10_listening_script.txt`。
- 不修改 `progress.json`、`daily_log.json`、`guide_progress.json` 或任何影片追蹤 JSON。
- 不執行 TTS、BGM、SRT、封面、MP4、合輯或上傳腳本。
- 不啟動 CDP 瀏覽器。
- 不刪除或改動任何舊 YouTube 影片。
- 不修改正式 guide。
- 不把舊逐字稿當內容來源。
- 未經使用者另外要求，不做 Git commit 或 push。

## 三、正式交付檔案

### 科目一（61 段、6 份）

- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S1_11_20_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S1_21_30_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S1_31_40_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S1_41_50_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S1_51_60_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S1_61_71_listening_script.txt`

### 科目三（96 段、10 份）

- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_01_10_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_11_20_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_21_30_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_31_40_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_41_50_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_51_60_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_61_70_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_71_80_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_81_90_listening_script.txt`
- `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/IPAS_S3_91_96_listening_script.txt`

## 四、執行階段

### Task 1：建立不可變基準與工作清單

**Objective:** 在任何正式檔案變更前，建立可驗證回復點與 157 段完整 manifest。

**Files:**
- Create: `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/backups/v3_rewrite_<timestamp>/`
- Create: `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v3_work/manifest.json`
- Create: `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v3_work/source_hashes.txt`

**Steps:**
1. 將 16 份目標舊稿完整複製到時間戳備份目錄；不含已完成的 S1 01–10，因它不會被改動。
2. 記錄兩份 guide、16 份目標稿及三個進度檔的 SHA-256。
3. 從 guide 建立 157 段 manifest，欄位至少包含 subject、id、title、source_chars、target_compilation、status。
4. 驗證科目一 ID 11–71 連續且唯一，科目三 ID 1–96 連續且唯一。
5. 驗證 16 份 target filename 與 `WRITING_SPEC.md` 一致。

**Gate:** manifest 應顯示 157 個唯一段落、16 份唯一合輯；任何缺段或重複立即停止。

### Task 2：建立隔離候選區與精準驗證報告

**Objective:** 所有撰稿先落在候選區，不直接覆寫正式稿。

**Files:**
- Create: `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v3_work/segments/`
- Create: `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v3_work/compilations/`
- Create: `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v3_work/reports/`

**Steps:**
1. 每個段落一個工作檔，例如 `S1_011.txt`、`S3_001.txt`，避免單一代理一次輸出 6–10 萬字而逾時或後段縮水。
2. 為每份合輯計算精確門檻：`ceil(source_chars × 0.75)` 與 `segment_count × 2400` 取較大值。
3. 實際目標設為精確門檻以上 1–2%，同時每段正文至少 1,800 字元。
4. 不改既有 validator；另產生 target-only 報告，以免已完成 S1 01–10 的已知 ratio 例外讓整套命令永遠非零。

**Gate:** 工作區中不得出現正式目標檔的直接寫入；報告需能區分「16 份本次目標」與「S1 01–10 已知非目標例外」。

### Task 3：先完成校準批 S1 11–20

**Objective:** 用第一個新批次校準後續 15 份合輯的資訊密度、語氣與組裝方式。

**Source:** `guide_s1.json` 第 11–20 段。

**Steps:**
1. 逐段建立來源涵蓋表：定義、英文／縮寫、公式、變數、案例、方法比較、限制、陷阱、勘誤、考試判斷。
2. 將 10 段拆成小組平行撰稿，每個子代理只讀指定 guide 段與規格；不得讀舊 S1 11–20 內容。
3. 每段候選稿必須是完整老師講課稿，不是摘要或 Markdown 去標記版。
4. 組裝成一份合輯，補上合輯開場、自然轉場與總結；主段標題保持獨立一行且只出現一次。
5. 執行 target validator，輸出 chars、精確未四捨五入 ratio、primary headers、每段長度、title hits、forbidden syntax。
6. 做人工聽感審查：開頭、全部段界、公式段、結尾逐段朗讀；修正視覺語言、重複句、難以朗讀的符號與縮寫。
7. 做獨立來源忠實度審查，確認沒有漏掉 guide 的核心知識，也沒有加入無來源支撐的斷言。

**Gate:** S1 11–20 的結構、來源涵蓋、TTS 聽感、精確 ratio 與人工語意審查全部通過，才把相同作法擴展至其他合輯；不需等待使用者逐批確認。

### Task 4：分波重寫其餘科目一

**Objective:** 完成 S1 21–71 共 51 段、5 份合輯。

**Wave:**
- Wave S1-A：21–30、31–40
- Wave S1-B：41–50、51–60
- Wave S1-C：61–71

**Steps per compilation:**
1. 來源涵蓋 map。
2. 每段獨立候選稿。
3. reviewer 對 guide 做逐項查漏。
4. 組裝開場、主段與結尾。
5. validator 精準驗收。
6. TTS 聽感與高風險內容審查。
7. 修正後重跑驗證。

**Gate:** 每份各自 PASS；科目一 61 個目標 ID 完整、順序正確、無重複。

### Task 5：分波重寫科目三

**Objective:** 完成 S3 1–96 共 96 段、10 份合輯。

**Wave:**
- Wave S3-A：01–10、11–20、21–30
- Wave S3-B：31–40、41–50、51–60
- Wave S3-C：61–70、71–80
- Wave S3-D：81–90、91–96

**策略:** 最多三個獨立撰稿工作並行；每份仍按單段工作檔撰寫，不讓代理一次承擔完整 10 段的超長輸出。完成每一波後立刻驗證，不等全部 96 段才發現系統性錯誤。

**Gate:** 每份各自 PASS；科目三 96 個 ID 完整、順序正確、無重複。

### Task 6：高風險知識專項複核

**Objective:** 補足自動 validator 無法證明的正確性。

**Review categories:**
1. 公式與計算：先講變數、分母、單位與解讀，算式口述無誤。
2. 機器學習方法方向：例如 CBOW／Skip-gram、TF-IDF、分類／偵測／分割、指標與類別不平衡。
3. 程式與流程：順序、前置條件與例外不能顛倒。
4. 法規、倫理與治理：不得把條件性規範說成絕對規則。
5. 官方勘誤與臺灣用語：全部使用修正版。
6. TTS：縮寫、英文、數字、公式、符號需能自然朗讀。

**Gate:** 每個高風險段至少有一筆來源對照紀錄；發現問題時修候選稿並重跑該合輯驗證。

### Task 7：16 份合輯整體一致性審查

**Objective:** 確保各批次連續收聽時像同一套課程，而非 16 個獨立模板。

**Steps:**
1. 比對 16 份開場，避免完全相同模板。
2. 比對相鄰合輯的結尾與下一份開頭，避免內容重複或斷裂。
3. 掃描大量重複長句與空泛口號。
4. 掃描 Markdown、網址、路徑、JSON／UI 語言、「如下表」「請看圖」及 replacement characters。
5. 驗證首次出現英文與縮寫的介紹方式一致。
6. 驗證每份合輯都有範圍、主題路線、總結與下一段銜接。

**Gate:** 16 份 target-only 驗證均 PASS，157 段順序完整；語意審查無未解決問題。

### Task 8：原子式交付正式 TXT

**Objective:** 只有通過全部驗收的候選稿才能取代舊稿。

**Steps:**
1. 再確認正式 16 份舊稿備份存在且雜湊可讀。
2. 將通過驗收的 16 份候選稿一次性複製到正式檔名。
3. 對正式檔重新執行 target-only 驗證，不能只信候選區結果。
4. 核對 16 份正式稿與候選稿 SHA-256 相同。
5. 核對 S1 01–10、兩份 guide、三個進度檔與任何追蹤 JSON 均未改變。

**Gate:** 16 份正式稿全部驗證通過，受保護檔案雜湊一致；若任何一份複製或驗證失敗，從備份回復全部 16 份，避免半套新稿半套舊稿。

### Task 9：交付報告，不啟動媒體管線

**Objective:** 讓 Claude Code 可直接接手 TTS／合輯／上傳，且不必猜稿件狀態。

**Create:** `/Users/leifhuang/Movies/ipas_videos/listening_scripts_v2/HERMES_DELIVERY_V3_<timestamp>.md`

**Report contents:**
- 實際完成範圍：S1 11–71、S3 1–96，共 157 段／16 份。
- 每份 chars、精確 source ratio、最短段長、title hits、validator 結果。
- 高風險段落與人工複核摘要。
- 16 份正式稿 SHA-256。
- 明確聲明 S1 01–10、舊影片、追蹤 JSON、TTS 與 YouTube 均未處理。
- 明確列出現行 validator 對已完成 S1 01–10 的既有 ratio 例外，避免後續誤判為本次交付失敗。

## 五、最終驗收標準

- [ ] 16 份目標合輯全部重新撰寫，非補寫舊內容。
- [ ] S1 61 段＋S3 96 段＝157 段，ID 完整、唯一且順序正確。
- [ ] 每份達到精確 `source_ratio >= 0.75`，並保留 1–2% 餘量。
- [ ] 每段正文至少 1,800 字元；每份總字元亦達 validator floor。
- [ ] 來源標題 100% 命中。
- [ ] 沒有 Markdown、網址、路徑、表格、編碼損壞或編輯殘留。
- [ ] 每段有直覺、正式概念、案例／比較、限制、陷阱、考試判斷及整理。
- [ ] 公式與縮寫適合純聽覺 TTS。
- [ ] 高風險技術內容完成獨立語意複核。
- [ ] 正式 TXT 與驗收候選 SHA-256 相同。
- [ ] S1 01–10 與所有進度／追蹤資料保持不變。
- [ ] 沒有執行 TTS、合輯、字幕、上傳或影片刪除。

## 六、風險與處理

1. **輸出規模極大：** 16 份最低合計約 125.7 萬字元。以單段候選稿拆分，避免代理逾時與後段資訊縮水。
2. **現行 validator 與既有完成品矛盾：** S1 01–10 已上線但 source ratio 只有 0.37。此次只驗本次 16 份，完整 suite 的非零結果需標記為既有例外，不得偷偷重寫 S1 01–10。
3. **來源過長導致機械改寫：** 先做來源涵蓋 map，再按教學功能重組；不得逐句壓縮 guide，也不得拿舊稿補字。
4. **批次風格漂移：** S1 11–20 先校準，後續共用相同品質契約，最後做跨合輯一致性審查。
5. **半成品污染正式稿：** 所有撰稿在隔離目錄，16 份全數通過後才原子式交付。
6. **後續誤啟動媒體流程：** 交付停在 TXT 與報告，不呼叫任何 TTS／上傳腳本。

## 七、建議執行順序

`建立基準與 manifest → S1 11–20 校準 → 其餘 S1 → S3 四波 → 高風險複核 → 16 份一致性審查 → 原子式覆寫 → 交付報告`

此順序不要求使用者逐批確認；開始後可自主連續執行至全部 157 段逐字稿交付，但不得越界進入 TTS 或 YouTube 階段。
