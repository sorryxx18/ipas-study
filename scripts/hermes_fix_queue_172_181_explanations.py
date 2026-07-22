#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_114_2_subject1_46':'''【考點】
MLOps 線上監控中的資料漂移（Data Drift）與概念漂移（Concept Drift）。模型服務本身沒有錯誤，但準確率逐漸下降，且輸入資料分布與訓練資料相比出現顯著偏移，最應建立漂移監測與預警。

【正解】
A。建立即時的資料漂移與概念漂移監測機制。

【為什麼】
資料漂移指輸入特徵分布改變，例如顧客行為、產品組合、季節或市場環境不同；概念漂移指特徵與標籤的關係改變。這兩者都可能讓模型在系統正常運作下準確率下降。MLOps 應監控輸入分布、預測分布、標籤回收後表現、PSI/KL divergence 等指標，並觸發告警或再訓練流程。

【錯誤選項解析】
A：對。漂移監測正是主動偵測這類問題的做法。
B：錯。量化降低延遲，不能偵測資料分布變化。
C：錯。增加超參數調整次數屬於訓練階段，不是線上漂移預警。
D：錯。固定 random seed 只能提升訓練重現性，不能處理部署後資料漂移。

【名詞解釋】
- Data Drift：輸入資料分布改變。
- Concept Drift：特徵與目標關係改變。
- MLOps：機器學習維運流程。
- PSI：Population Stability Index，常用漂移指標。
- Continuous Monitoring：持續監控。

【記憶】
線上準確率下降但系統沒壞：**先想資料漂移/概念漂移監控**。''',
'official_115_1_subject3_24':'''【考點】
高基數類別特徵與 One-Hot 編碼的維度爆炸。商品類別有約 3,000 個不同項目時，One-Hot 會為每個類別建立一個維度，最容易造成稀疏高維特徵。

【正解】
D。One-Hot 編碼。

【為什麼】
One-Hot Encoding 對每一個類別建立一個欄位，若商品項目有 3,000 種，就會產生 3,000 維稀疏向量。類別數越多，維度越高，記憶體、計算成本與模型訓練難度都會上升。高基數類別常改用 target encoding、hashing trick、embedding 或其他壓縮表示。

【錯誤選項解析】
A：錯。目標編碼通常把類別轉為統計值，不會產生 3,000 個欄位，但需防資料洩漏。
B：錯。Label Encoding 只給每個類別一個整數，不會直接造成維度爆炸，但可能引入假順序。
C：錯。Embedding 將類別映射到低維稠密向量，常用於高基數特徵。
D：對。One-Hot 對高基數類別最容易維度爆炸。

【名詞解釋】
- High Cardinality：高基數，類別種類很多。
- One-Hot Encoding：每類別一個二元欄位。
- Target Encoding：用目標統計量表示類別。
- Embedding：低維稠密向量表示。
- Sparse Vector：稀疏向量。

【記憶】
高基數口訣：**「類別幾千種，One-Hot 就爆維度」**。''',
'official_114_2_subject1_16':'''【考點】
Seq2Seq 模型適用情境。序列到序列模型適合把一段輸入序列轉成另一段輸出序列，例如機器翻譯、摘要、對話生成、語音轉文字等。

【正解】
D。將輸入文字轉換成語意等價的另一段文字，如自動翻譯或摘要生成。

【為什麼】
Seq2Seq 的典型結構是 encoder 讀入一段序列，decoder 產生另一段序列。翻譯是把來源語言句子轉成目標語言句子；摘要是把長文本轉成短文本。兩者輸入與輸出長度都可不同，且輸出本身仍是序列，因此最符合 Seq2Seq。

【錯誤選項解析】
A：錯。預測未來數值序列可用時間序列模型，但題目典型 Seq2Seq 場景是文字轉文字。
B：錯。NER 是序列標註，不是把整段序列生成成另一段文字。
C：錯。關鍵字頻率統計與可視化不是 Seq2Seq 生成任務。
D：對。翻譯與摘要是 Seq2Seq 經典應用。

【名詞解釋】
- Seq2Seq：Sequence-to-Sequence，序列到序列。
- Encoder：編碼器，讀取輸入序列。
- Decoder：解碼器，生成輸出序列。
- Machine Translation：機器翻譯。
- Text Summarization：文本摘要。

【記憶】
Seq2Seq 口訣：**「一段序列進去，另一段序列出來」**；翻譯、摘要最典型。''',
'official_115_1_subject3_10':'''【考點】
任務類型與損失函數選擇。使用時長是連續數值預測，屬於迴歸，常用 MSE；是否流失是二元分類，常用 Binary Cross-Entropy。

【正解】
A。使用時長預測：均方誤差（MSE）；流失預測：二元交叉熵（Binary Cross-Entropy）。

【為什麼】
隔日 App 使用時長以分鐘為單位，是連續值，因此模型預測數值與真實數值之間可用 MSE 衡量平方誤差。隔日是否流失是 yes/no 的二元標籤，模型通常輸出流失機率，使用 binary cross-entropy 衡量機率預測與真實標籤的差距。

【錯誤選項解析】
A：對。迴歸用 MSE，二元分類用 BCE。
B：錯。把兩個任務的 loss 顛倒了。
C：錯。Hinge 常見於 SVM 類分類；MAE 可做迴歸但不適合此二元流失分類搭配。
D：錯。不是所有有不確定性的輸出都用交叉熵；連續數值預測常用迴歸損失。

【名詞解釋】
- MSE：Mean Squared Error，均方誤差。
- Binary Cross-Entropy：二元交叉熵。
- Regression：迴歸，預測連續數值。
- Binary Classification：二元分類。
- Loss Function：損失函數。

【記憶】
損失函數口訣：**「連續數值 MSE，是/否分類 BCE」**。''',
'official_114_2_subject3_6':'''【考點】
CNN 相對 FCNN 處理影像更有效率的原因。CNN 透過局部感受野與參數共享，大幅降低參數量與運算複雜度，同時保留影像空間結構。

【正解】
C。CNN 透過區域感知與參數共享機制，降低模型參數量與運算複雜度。

【為什麼】
若用全連接網路處理影像，每個像素都與下一層大量神經元連接，參數量會非常大，也忽略局部空間結構。CNN 的卷積核只看局部區域，且同一組卷積核在整張影像共享權重，因此能用少量參數學習邊緣、紋理與物件特徵。這讓 CNN 在影像任務中比 FCNN 更有效率。

【錯誤選項解析】
A：錯。CNN 可學到一定程度平移等特性，但旋轉/比例不變性不是此題效率主因。
B：錯。CNN 可自動學特徵，但題目問訓練與推論效率，C 更精準。
C：對。局部感受野與參數共享降低參數與計算成本。
D：錯。CNN 並未捨棄激活函數，常用 ReLU 等。

【名詞解釋】
- CNN：卷積神經網路。
- FCNN：全連接神經網路。
- Local Receptive Field：局部感受野。
- Parameter Sharing：參數共享。
- Convolution Kernel：卷積核。

【記憶】
CNN 效率口訣：**「局部看、權重共享，所以參數少」**。''',
'official_115_1_subject3_29':'''【考點】
只有正常資料、缺乏故障標註時的異常偵測。大量正常振動時序資料、沒有確認故障樣本，最符合非監督或半監督異常偵測。

【正解】
B。非監督或半監督異常偵測。

【為什麼】
監督式二元分類需要正常與故障兩類標註資料，但題目明確說沒有故障標註樣本。此時常用 one-class SVM、autoencoder reconstruction error、Isolation Forest、統計閾值等方式，先學正常模式，再把偏離正常分布的振動視為異常。若只用正常資料訓練，也常稱半監督異常偵測。

【錯誤選項解析】
A：錯。監督式二元分類需要故障樣本標註。
B：對。只有正常資料時，適合非監督/半監督異常偵測。
C：錯。強化學習用於互動式決策，不是此情境核心。
D：錯。自監督學習可作為表示學習方法，但題目問任務範疇，異常偵測更直接。

【名詞解釋】
- Anomaly Detection：異常偵測。
- Semi-supervised Anomaly Detection：用正常資料學正常模式。
- One-class Classification：單類分類。
- Reconstruction Error：重建誤差。
- Time Series：時序資料。

【記憶】
異常偵測口訣：**「只有正常、沒有故障標籤，就用非監督/半監督異常偵測」**。''',
'official_114_2_subject3_36':'''【考點】
同態加密（Homomorphic Encryption）的關鍵特性。資料保持加密狀態時仍可進行特定數值運算，解密後得到等同於在明文上運算的結果。

【正解】
D。資料在加密狀態下仍可進行數值運算，模型訓練可於未解密資料上完成。

【為什麼】
多家銀行或合作機構共同訓練信用風險模型時，最擔心原始交易資料外洩。同態加密讓運算方可對密文執行加法、乘法或更一般的運算，而不直接看到明文資料。這可支援隱私保護的聯合分析或模型訓練，但通常會帶來較高計算成本。

【錯誤選項解析】
A：錯。加入隨機雜訊保護統計結果較像差分隱私。
B：錯。交換私鑰會破壞安全性，不是同態加密重點。
C：錯。壓縮並加密不是同態加密的核心特性。
D：對。密文狀態下可運算是同態加密關鍵。

【名詞解釋】
- Homomorphic Encryption：同態加密。
- Ciphertext：密文。
- Plaintext：明文。
- Privacy-preserving Computation：隱私保護運算。
- Differential Privacy：差分隱私，以噪音降低個資洩漏風險。

【記憶】
同態加密口訣：**「資料不解密，也能算」**。''',
'official_114_2_subject1_23':'''【考點】
醫療 AI 的漸進式部署（Phased Rollout）。高風險臨床場景應從範圍小、流程可控、回饋可收斂的單位開始，逐步擴展到全院。

【正解】
A。從單一專科或特定病房開始啟用，逐步擴展至全院。

【為什麼】
醫療 AI 直接全院部署風險高，若影響臨床工作流程或出現錯誤，難以定位與修正。先從放射科、單一病房或特定病種啟用，可在受控範圍內觀察使用者回饋、模型表現、責任流程與例外處理，再逐步擴大。這符合風險可控與回饋收斂的 phased rollout 精神。

【錯誤選項解析】
A：對。單一專科/病房起步，逐步擴展，是最合適漸進式部署。
B：錯。急診病例量高且風險高，不適合作為第一階段降低衝擊。
C：錯。只在夜班或離峰啟用不一定能代表主要流程，也可能缺少支援。
D：錯。全院同步體驗範圍太大，不利於風險控制與回饋收斂。

【名詞解釋】
- Phased Rollout：分階段/漸進式部署。
- Clinical Workflow：臨床流程。
- Risk Control：風險控管。
- Feedback Loop：回饋迴路。
- Pilot Deployment：試點部署。

【記憶】
醫療 AI 部署口訣：**「先小範圍試點，再逐步擴全院」**。''',
'official_115_1_subject1_22':'''【考點】
MLOps 的核心角色。MLOps 不是單純標註、AutoML 或部署後不再維運，而是建立訓練、測試、部署、監控、再訓練的自動化流程與版本管理。

【正解】
C。建立機器學習流程的自動化與版本管理機制，支援模型部署、監控與持續更新。

【為什麼】
題目明確提到「模型訓練→測試→部署→監控→再訓練」的流程串接，以及線上模型版本可追溯。這正是 MLOps 的範圍：pipeline automation、model registry、data/model versioning、CI/CD/CT、monitoring、rollback 與治理。它把 ML 開發和維運變成可重複、可追蹤、可監控的工程流程。

【錯誤選項解析】
A：錯。資料標註與品質重要，但只是整體流程的一部分。
B：錯。AutoML/超參數搜尋不是 MLOps 的完整核心角色。
C：對。自動化流程、版本管理、部署監控與持續更新是 MLOps 核心。
D：錯。MLOps 不是減少後續更新需求，而是支援持續維運與更新。

【名詞解釋】
- MLOps：機器學習維運。
- Model Registry：模型註冊與版本管理。
- Pipeline Automation：流程自動化。
- CI/CD/CT：持續整合、部署、訓練。
- Model Monitoring：模型監控。

【記憶】
MLOps 口訣：**「訓練到部署監控再訓練，都要自動化、版本化、可追蹤」**。''',
'official_115_1_subject1_27':'''【考點】
高風險醫療 AI 的安全設計與 Human-in-the-Loop。人命攸關且最終臨床責任需由人類承擔時，系統應設計為醫師最終審核決策，而不是 AI 全自動決定。

【正解】
A。採用人機協作（Human-in-the-Loop, HITL）架構，由醫師最終審核決策。

【為什麼】
醫療影像診斷輔助系統應定位為輔助工具，提供建議、風險提示或標記可疑區域，但最終診斷與治療決策需由合格醫師負責。HITL 能保留專業判斷、處理模型不確定與例外案例，也符合責任歸屬、病人安全與監管要求。

【錯誤選項解析】
A：對。HITL 讓醫師保有最終審核與責任，是高風險醫療場景關鍵。
B：錯。低信心自動關機不等於安全臨床流程，應升級給人審核。
C：錯。隨機切換模型與多數決不能解決責任與安全問題。
D：錯。對影像加入隨機擾動可能降低品質，非安全機制。

【名詞解釋】
- HITL：Human-in-the-Loop，人機協作/人在迴路中。
- Clinical Decision Support：臨床決策支援。
- Accountability：責任歸屬。
- Threshold：閾值。
- Patient Safety：病人安全。

【記憶】
醫療 AI 安全口訣：**「AI 輔助，醫師最後決策」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
