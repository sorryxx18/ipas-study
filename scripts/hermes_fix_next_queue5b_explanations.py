#!/usr/bin/env python3
import json
import pathlib
import datetime

base = pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path = base / 'questions.json'
data = json.loads(path.read_text())
questions = data['questions'] if isinstance(data, dict) and 'questions' in data else data
byid = {q['id']: q for q in questions}

explanations = {
'official_115_1_subject3_32': '''【考點】
分類模型評估指標中的 Precision、Recall 與 F1-score。題目情境是詐欺偵測，需要同時避免誤凍結正常帳號，也不能漏抓詐欺，因此考的是 Precision-Recall tradeoff 與 F1-score 的調和平均特性。

【正解】
D。F1-score = 2 × (Precision × Recall) / (Precision + Recall)，為調和平均，對較小值敏感。

【為什麼】
F1-score 是 Precision 與 Recall 的調和平均，不是算術平均。調和平均的特性是對較小的數值更敏感，因此只要 Precision 或 Recall 其中一個很低，F1-score 就會被明顯拉低。這適合用在希望同時兼顧精確率與召回率的場景，例如詐欺偵測、疾病篩檢、異常偵測等。

【錯誤選項解析】
A：錯。這是算術平均，不是 F1-score。F1-score 使用調和平均，會更懲罰其中一個指標偏低的情況。
B：錯。F1-score 不是 Precision 的加權平均，而是 Precision 與 Recall 的調和平均。若要加權，可用 F-beta score。
C：錯。F1-score 常用於類別不平衡資料，尤其正類較少且需兼顧 Precision / Recall 時；不是僅適用於類別平衡資料。
D：對。這是 F1-score 的正確公式與核心特性，能反映 Precision 和 Recall 的平衡程度。

【名詞解釋】
- Precision：被模型判為正類的樣本中，實際為正類的比例；重點是「抓到的有多準」。
- Recall：所有實際正類中，被模型成功抓到的比例；重點是「有沒有漏抓」。
- F1-score：Precision 與 Recall 的調和平均，用來兼顧兩者。
- 調和平均：比算術平均更受小值影響，適合衡量兩個指標是否均衡。
- Precision-Recall Tradeoff：調整分類閾值時，Precision 和 Recall 常會互相拉扯。

【記憶】
F1 口訣：**「F1 看平衡，小的會拖累」**。看到 Precision 和 Recall 都重要，就想到 F1-score；看到要偏重 Recall 或 Precision，再想到 F-beta。''',

'official_114_2_subject1_25': '''【考點】
生成式 AI 的著作權風險治理。題目問「最能有效預防侵權問題產生」，重點在源頭治理：訓練資料的授權、來源、篩選與紀錄，而不是只在輸出端補救。

【正解】
B。建立訓練資料篩選與授權驗證機制，排除未授權或高風險資料來源。

【為什麼】
生成式 AI 的著作權風險常來自訓練資料或微調資料包含未授權內容，導致模型可能產生高度相似或侵權輸出。最有效的預防策略是從資料來源做治理：確認資料授權、保留來源紀錄、排除未授權或高風險資料、建立資料使用政策。這是比事後偵測更根本的風險降低方式。

【錯誤選項解析】
A：錯。語意相似度比對可在輸出端偵測疑似侵權內容，屬於事後風險控管，不如訓練資料授權治理能從源頭預防。
B：對。建立資料篩選與授權驗證機制，能從資料來源降低侵權風險，是最直接的預防措施。
C：錯。差分隱私可降低模型記憶個別樣本與個資推斷風險，但不能保證資料具有著作權授權，也不是主要的著作權合規機制。
D：錯。浮水印或數位指紋有助於追蹤生成內容來源，但不能防止模型使用未授權資料，也不能直接避免侵權內容生成。

【名詞解釋】
- 生成式 AI：能產生文字、影像、音訊、程式等內容的 AI 系統。
- 著作權風險：AI 訓練或輸出內容可能侵犯他人著作權的法律風險。
- 授權驗證：確認資料來源是否允許用於訓練、微調或商業用途。
- 差分隱私：透過加入噪聲降低個體資料被推斷的風險，主要處理隱私而非著作權授權。
- Watermarking：在生成內容中加入可追蹤標記，協助辨識來源或產製系統。

【記憶】
著作權風險口訣：**「侵權要預防，先管資料源」**。輸出比對與浮水印是輔助，授權驗證才是源頭治理。''',

'S3_26': '''【考點】
邏輯迴歸（Logistic Regression）的輸出函數。二元分類的 Logistic Regression 使用 Sigmoid 函數，將線性模型輸出轉換成 0 到 1 之間的機率。

【正解】
C。Sigmoid。

【為什麼】
Logistic Regression 雖然名稱有 Regression，但常用於二元分類。它先計算線性組合 z = w x + b，再透過 Sigmoid 函數 1 / (1 + e^-z) 把輸出壓縮到 0 到 1 之間，表示樣本屬於正類的機率。若機率大於某個閾值，例如 0.5，就判為正類。

【錯誤選項解析】
A：錯。ReLU 常用於神經網路隱藏層，輸出為 max(0, x)，不是 Logistic Regression 的機率輸出函數。
B：錯。線性函數可用於線性迴歸；Logistic Regression 需要 Sigmoid 將輸出轉成機率。
C：對。二元 Logistic Regression 的輸出層使用 Sigmoid。
D：錯。Softmax 常用於多類別分類，將多個類別分數轉成機率分布；二元邏輯迴歸通常用 Sigmoid。

【名詞解釋】
- Logistic Regression：常用於二元分類的線性分類模型。
- Sigmoid：將任意實數轉換為 0 到 1 之間數值的函數，可解釋為機率。
- ReLU：常見神經網路激活函數，輸出非負值。
- Softmax：多類別分類常用函數，將多個分數轉為各類別機率。
- Decision Threshold：分類閾值，例如機率大於 0.5 判為正類。

【記憶】
二元分類口訣：**「Logistic 用 Sigmoid，多類別用 Softmax」**。看到 Logistic Regression 的輸出層，先選 Sigmoid。''',

'S1_30': '''【考點】
遷移學習（Transfer Learning）與微調（Fine-tuning）的關係。題目要分辨：Fine-tuning 不是從零訓練，而是遷移學習中的一種常見實作方式。

【正解】
B。Fine-tuning 是遷移學習的一種實作方式，用少量資料在預訓練模型上繼續訓練。

【為什麼】
遷移學習是把模型在原任務或大型資料集學到的知識，轉移到新任務使用。Fine-tuning 則是在預訓練模型基礎上，用新任務資料繼續訓練部分或全部參數，使模型適應特定領域或任務。因此 Fine-tuning 是遷移學習的一種實作方式，常用於影像模型、語言模型與各種小資料情境。

【錯誤選項解析】
A：錯。Fine-tuning 和遷移學習密切相關，並非完全無關。
B：對。Fine-tuning 是在預訓練模型上用少量或特定領域資料繼續訓練，是遷移學習的常見方法。
C：錯。從零訓練是 training from scratch，不是 Fine-tuning。Fine-tuning 的前提是已有預訓練模型。
D：錯。遷移學習不只用於電腦視覺，也常用於 NLP、語音、推薦系統與大型語言模型。

【名詞解釋】
- Transfer Learning：將已學到的模型知識轉移到新任務的技術。
- Fine-tuning：在預訓練模型上用目標任務資料繼續訓練。
- Pretrained Model：已在大型資料集或通用任務上訓練完成的模型。
- Training from Scratch：不使用預訓練權重，從隨機初始化開始訓練。
- Domain Adaptation：讓模型適應新領域資料分布的技術。

【記憶】
關係口訣：**「遷移學習是大概念，Fine-tuning 是常見做法」**。看到「預訓練模型 + 少量資料繼續訓練」，答案就是 Fine-tuning。''',

'official_114_2_subject1_27': '''【考點】
半結構化 JSON 日誌的特徵工程。題目關鍵字是「巢狀欄位」、「時序特徵」、「故障預測」，因此最實務的策略是遞迴展開巢狀欄位，再依時間窗口做聚合與特徵萃取。

【正解】
C。設計遞迴函式展開巢狀欄位，並基於時間窗口（Time Window）進行聚合與特徵萃取。

【為什麼】
系統日誌常是 JSON 格式，可能包含巢狀欄位、事件類型、錯誤碼、設備狀態與時間戳記。要用於故障預測，必須先把巢狀欄位結構化展開，再按時間窗口計算特徵，例如某錯誤碼出現次數、平均延遲、最大溫度、異常事件頻率等。這樣才能保留結構資訊與時序變化，並轉成模型可使用的特徵。

【錯誤選項解析】
A：錯。扁平化轉 CSV 加統計量可能是部分流程，但若只做簡單扁平化，容易忽略巢狀結構與時間窗口；題目要求最有效且實務可行，C 更完整。
B：錯。直接把原始 JSON 字串丟進 RNN 不利於結構化特徵抽取，且資料量、格式變化與可解釋性都會有問題。
C：對。遞迴展開巢狀欄位並依 Time Window 聚合，能同時處理 JSON 結構與時序特徵。
D：錯。只保留時間戳記會丟失錯誤碼、狀態值、事件內容等關鍵資訊，無法有效做故障預測。

【名詞解釋】
- 半結構化資料：有一定格式但欄位可能彈性變化的資料，例如 JSON、XML、日誌。
- Nested Fields：巢狀欄位，欄位內還包含物件或陣列。
- Feature Engineering：將原始資料轉換成模型可用特徵的過程。
- Time Window：將事件依時間區間分組，例如每 5 分鐘、每 1 小時統計特徵。
- 故障預測：利用歷史事件與感測資料預測設備或系統是否將發生故障。

【記憶】
JSON 日誌特徵工程口訣：**「先展開巢狀，再按時間聚合」**。看到 nested fields + time series，就選遞迴展開與時間窗口特徵。'''
}

for qid, exp in explanations.items():
    byid[qid]['explanation'] = exp

if isinstance(data, dict) and 'questions' in data:
    data['questions'] = questions
    data.setdefault('meta', {})['last_explanation_fix'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else:
    data = questions

path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print('updated explanations:', ', '.join(explanations))
