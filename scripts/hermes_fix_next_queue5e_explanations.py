#!/usr/bin/env python3
import json
import pathlib
import datetime

base = pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path = base / 'questions.json'
data = json.loads(path.read_text())
questions = data['questions'] if isinstance(data, dict) and 'questions' in data else data
byid = {q['id']: q for q in questions}

byid['official_115_1_subject3_43']['options']['D'] = '為了避免更新步伐過大，破壞預訓練模型原本已學好的良好特徵表示'

explanations = {
'official_114_2_subject1_32': '''【考點】
模型監控中的資料漂移預警指標。題目問「提前偵測模型效能可能衰退」且選項包含 PSI，因此重點是監控輸入特徵分布相對訓練資料是否穩定，而不是只看系統資源或 API 延遲。

【正解】
D。輸入特徵與訓練資料分布差異的 PSI（Population Stability Index）指數。

【為什麼】
PSI 用來衡量目前輸入特徵分布和基準分布（通常是訓練資料或穩定期間資料）之間的差異。若 PSI 明顯升高，代表上線資料分布已偏離訓練資料，模型可能面臨 Data Drift，進而造成效能下降。這類指標通常能在真實標籤回來前提供早期預警。

【錯誤選項解析】
A：錯。CPU 與記憶體使用率是系統健康指標，可偵測服務資源問題，但不能直接預測模型準確率或資料分布衰退。
B：錯。置信度分布變化可作為輔助訊號，但它是模型輸出端變化，未必能直接指出輸入特徵與訓練資料分布差異。
C：錯。API 回應時間與延遲屬於服務效能監控，不是模型效能衰退或資料漂移的主要預警指標。
D：對。PSI 直接比較輸入特徵分布與訓練資料分布，是偵測資料漂移與模型衰退風險的常用監控指標。

【名詞解釋】
- PSI：Population Stability Index，用於衡量兩個資料分布的穩定性差異。
- Data Drift：上線輸入資料分布與訓練資料不同。
- Model Monitoring：模型上線後監控資料、效能、漂移與服務狀態的流程。
- Confidence：模型對預測結果的信心分數。
- Service Monitoring：監控 API 延遲、錯誤率、CPU、記憶體等系統指標。

【記憶】
模型預警口訣：**「系統慢看延遲，模型漂看 PSI」**。題目問資料分布與效能衰退風險，優先選 PSI。''',

'official_115_1_subject3_43': '''【考點】
遷移學習微調時學習率設定較小的原因。題目問 Fine-Tuning 為什麼常用很小 learning rate，核心是避免大幅破壞預訓練模型已學到的通用特徵表示。

【正解】
D。為了避免更新步伐過大，破壞預訓練模型原本已學好的良好特徵表示。

【為什麼】
Fine-tuning 是在預訓練模型的基礎上，用特定任務資料繼續訓練。預訓練模型通常已學到可泛化的特徵，例如語意、語法、影像邊緣或紋理。若微調時學習率太大，參數更新幅度過大，可能造成 catastrophic forgetting 或破壞原有特徵，使模型表現變差。因此微調常用較小學習率，讓模型以較溫和方式適應新任務。

【錯誤選項解析】
A：錯。學習率大小主要影響參數更新步伐，不是解決 OOM 記憶體不足；OOM 通常要調整 batch size、模型大小或梯度累積。
B：錯。較小學習率通常不一定加速收斂，而是讓微調更穩定。
C：錯。學習率不能強制損失函數歸零，損失能否下降取決於資料、模型、任務與訓練設定。
D：對。小學習率可避免破壞預訓練模型已學到的良好表示，是微調常見設定。

【名詞解釋】
- Fine-tuning：在預訓練模型上用新任務資料繼續訓練。
- Learning Rate：每次參數更新的步伐大小。
- Pretrained Model：先在大型資料集或通用任務上訓練好的模型。
- Catastrophic Forgetting：模型在學新任務時遺忘原本已學到能力的現象。
- Feature Representation：模型內部對資料特徵的表示。

【記憶】
微調口訣：**「預訓練已經會，小步調才不毀」**。Fine-tuning 用小 learning rate，是為了保留原本學好的特徵。''',

'S3_22': '''【考點】
集成學習方法分類：XGBoost 屬於 Boosting。題目要區分 Bagging、Boosting、Stacking、Voting 的差異。

【正解】
C。Boosting。

【為什麼】
XGBoost 是 eXtreme Gradient Boosting，是梯度提升決策樹（GBDT）的高效實作與強化版本。Boosting 的核心是序列式訓練多個弱學習器，後面的模型嘗試修正前面模型的錯誤或殘差，最後組合成強模型。XGBoost 也加入正則化、缺失值處理與高效計算等工程改進。

【錯誤選項解析】
A：錯。Bagging 是平行訓練多個模型再平均或投票，例如 Random Forest，不是 XGBoost 的主要類型。
B：錯。Stacking 是用第二層 meta-model 學習如何整合多個基模型輸出，和 XGBoost 不同。
C：對。XGBoost 屬於 Boosting，特別是 Gradient Boosting 的高效實作。
D：錯。Voting 是簡單投票集成，通常不強調序列修正錯誤；XGBoost 不是單純 voting。

【名詞解釋】
- XGBoost：高效的梯度提升樹模型，常用於表格資料競賽與實務分類/回歸。
- Boosting：序列式集成學習，逐步修正前一輪模型錯誤。
- Bagging：透過重抽樣平行訓練多模型，例如 Random Forest。
- Stacking：用 meta-model 整合多個模型輸出。
- Weak Learner：單獨表現有限、但可透過集成提升效果的模型。

【記憶】
集成口訣：**「Random Forest 是 Bagging，XGBoost 是 Boosting」**。看到 XGBoost，直接想到 Boosting。''',

'official_115_1_subject3_46': '''【考點】
資料處理流程判讀題。此題原始題幹依賴附圖中的描述 A–F，但目前題庫 JSON 只保留選項組合，未保留附圖/描述內容；因此解析先依官方答案 B 補成判讀策略，並提醒實際作答需回看附圖。

【正解】
B。描述 B、描述 D、描述 E、描述 F。

【為什麼】
這類題通常要求根據資料處理圖，判斷哪些描述符合流程，例如資料切分、標準化、訓練集/測試集使用、模型評估或交叉驗證等。官方答案為 B，代表圖中的 B、D、E、F 為正確描述；A、C 至少各有一處與圖示流程不符。由於目前題庫缺少附圖與描述 A–F 的原文，無法精確說明每個描述錯在哪裡，後續若能補回附圖文字，應再做完整解析校準。

【錯誤選項解析】
A：錯。此組合包含描述 A、C，而官方答案未包含 A、C，表示至少其中一項與圖中資料處理流程不符。
B：對。官方答案組合為 B、D、E、F，代表這四項符合附圖資料處理流程。
C：錯。此組合包含 C，且缺少 D；和官方答案不一致。
D：錯。此組合包含 A，且比官方答案多出不正確描述；不可因選項較完整就選。

【名詞解釋】
- 資料處理流程：從原始資料到模型訓練/評估前的清理、轉換、切分與標準化步驟。
- Train/Test Split：將資料分成訓練集與測試集，以評估泛化能力。
- Standardization：將特徵轉換為平均值 0、標準差 1 的尺度。
- Data Leakage：測試資料資訊不當流入訓練過程，造成評估過度樂觀。
- Cross Validation：用多次資料切分評估模型穩定性。

【記憶】
圖表組合題口訣：**「先看流程箭頭，再比描述是否偷換資料集」**。此題目前 JSON 缺附圖，已先保留官方答案 B；若之後補回 A–F 原文，要再精修。''',

'official_114_2_subject1_17': '''【考點】
RAG 檢索階段的核心挑戰：檢索結果要和查詢意圖真正相關，而不是只在向量空間語意相近。題目問「檢索階段最關鍵挑戰」，重點是 retrieval quality。

【正解】
D。避免向量檢索結果僅具語意相似但與查詢意圖無實質關聯的情況。

【為什麼】
RAG 的效果高度依賴檢索品質。若檢索階段抓到的文件只是表面語意相似，但沒有回答使用者真正意圖，後續語言模型即使生成能力再強，也可能產生不正確或不相關回答。高品質 RAG 需要處理查詢改寫、chunk 設計、embedding 模型、reranking、metadata filter 等問題，確保取回內容對任務有實質幫助。

【錯誤選項解析】
A：錯。Context Window 是否能完整放入文件是生成階段與上下文管理問題，不是檢索階段最核心挑戰；而且 RAG 通常不需要完整塞入所有文件。
B：錯。Faiss、ScaNN 是向量搜尋工具，選工具重要，但工具選擇本身不等於檢索品質的核心挑戰。
C：錯。降低 embedding 計算成本與記憶體占用是效率問題，不是確保檢索結果符合查詢意圖的主要品質問題。
D：對。檢索結果若只語意相似但不符合查詢意圖，會直接導致 RAG 回答錯誤，是檢索階段核心挑戰。

【名詞解釋】
- RAG：Retrieval-Augmented Generation，先檢索外部知識，再交給語言模型生成回答。
- Embedding：將文字轉為向量表示，以便計算語意相似度。
- Vector Search：在向量空間中搜尋相似內容的方法。
- Reranking：對初步檢索結果重新排序，以提升相關性。
- Context Window：語言模型一次可讀取的上下文長度。

【記憶】
RAG 口訣：**「檢索錯，生成再強也會錯」**。看到檢索階段挑戰，優先選檢索相關性與查詢意圖匹配。'''
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
print('repaired option D for official_115_1_subject3_43')
