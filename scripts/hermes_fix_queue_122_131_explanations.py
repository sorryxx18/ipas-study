#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_114_2_subject1_31':'''【考點】
高流量 AI 推論服務架構。每次請求約 1 秒、流量高達 10,000 RPS，代表需要大量並行處理能力、高可用性與峰值流量彈性，最適合容器化、水平擴展與 Auto Scaling。

【正解】
B。採用容器化部署並水平擴展服務實例，結合自動彈性伸縮機制。

【為什麼】
若單次推論需 1 秒，10,000 RPS 代表同時可能有大量請求在處理。單台機器垂直擴展有上限，也有單點故障風險。容器化部署可把推論服務拆成多個 replica，搭配負載平衡、Kubernetes HPA 或雲端 Auto Scaling，依流量增加或減少服務實例，才能穩定面對尖峰並維持高可用性。

【錯誤選項解析】
A：錯。單台高效能伺服器有垂直擴展上限，也缺乏高可用性。
B：對。水平擴展加自動伸縮最符合高 RPS 與高可用需求。
C：錯。限制併發可保護系統，但會犧牲服務能力，不能支撐 10,000 RPS。
D：錯。增大批次可能提高吞吐，但不一定符合即時請求延遲與高可用架構需求。

【名詞解釋】
- RPS：每秒請求數。
- Horizontal Scaling：增加服務實例數量來擴展容量。
- Auto Scaling：根據負載自動調整資源。
- Containerization：容器化部署，如 Docker/Kubernetes。
- High Availability：高可用性，避免單點故障。

【記憶】
高流量推論口訣：**「單機撐不住，高可用靠水平擴展與自動伸縮」**。''',
'official_115_1_subject1_8':'''【考點】
ROC 曲線的座標與醫療意義。ROC 的 X 軸是假陽率 FPR，Y 軸是真陽率 TPR；醫療情境中分別代表誤診健康者的風險，以及正確找出病患的能力。

【正解】
B。X 軸為 FPR，Y 軸為 TPR，反映誤診健康個體的風險與正確識別病患的能力。

【為什麼】
TPR 又稱 Recall/Sensitivity，表示真正惡性病變中有多少被模型抓出；FPR 表示實際良性卻被判成惡性的比例，也就是誤報或過度警示風險。ROC 曲線透過調整分類閾值觀察 TPR 與 FPR 的取捨，醫療場景常重視高 TPR 以避免漏診，但也需控制 FPR 避免不必要檢查。

【錯誤選項解析】
A：錯。ROC X 軸不是 Accuracy。
B：對。ROC 標準座標就是 FPR 對 TPR。
C：錯。Precision-Recall 曲線才是 Precision 與 Recall。
D：錯。IoU 與 mAP 屬於物件偵測評估，不是二元分類 ROC。

【名詞解釋】
- ROC：Receiver Operating Characteristic 曲線。
- FPR：False Positive Rate，假陽率。
- TPR：True Positive Rate，真陽率，也稱 Recall/Sensitivity。
- Threshold：分類閾值。
- Sensitivity：敏感度，醫療中常指找出病患能力。

【記憶】
ROC 口訣：**「X 是假陽 FPR，Y 是真陽 TPR」**；醫療中 Y 高代表少漏診，X 高代表誤報多。''',
'official_114_2_subject1_49':'''【考點】
情感分析中的跨語言/跨族群偏誤與資料治理。題目問「不正確」描述，需找出較不直接、概念不符合主要問題的說法。

【正解】
A。模型未啟用詞嵌入正規化可能造成語意距離不穩定，導致預測誤差。

【為什麼】
題目描述的核心是不同語言、族群書寫風格、語氣與文化語用差異造成情感判斷不一致。這通常來自訓練語料分布偏差、文化/語氣特徵不足、標註不一致或模型雖有上下文能力但仍學到偏誤。Embedding normalization 不是解決這類文化語意偏誤的主要必要條件，把問題歸因於未啟用它過度簡化且不精確。

【錯誤選項解析】
A：對本題而言不正確。語意距離正規化不是此情境偏誤的主要技術/治理分析。
B：錯。訓練語料偏向特定文化或語氣，確實會造成內隱偏誤。
C：錯。資料來源不平衡會導致不同語言或族群風格判斷不準。
D：錯。Transformer 能捕捉上下文，但資料偏差仍會被模型學到。

【名詞解釋】
- Implicit Bias：模型從資料中學到的隱性偏誤。
- Distribution Shift：訓練與部署資料分布差異。
- Sentiment Analysis：情感分析。
- Transformer：擅長上下文建模的架構。
- Data Governance：資料治理，包含資料代表性與品質管理。

【記憶】
跨文化情感分析口訣：**「語氣與文化不同，問題多半在資料代表性，不是單靠 embedding normalization」**。''',
'official_115_1_subject3_3':'''【考點】
矩陣乘法維度。若矩陣 A 形狀為 (m, n)，矩陣 B 形狀為 (n, p)，則 A×B 輸出形狀為 (m, p)。

【正解】
A。(1, 64)。

【為什麼】
題目中 Q 的形狀是 (1, 10)，WQ 的形狀是 (10, 64)。前者第二維 10 與後者第一維 10 相同，因此矩陣相乘相容。輸出保留左矩陣的列數 1 與右矩陣的欄數 64，所以結果為 (1, 64)。這也符合 Transformer 中把輸入投影到 d_model 或 attention 維度的概念。

【錯誤選項解析】
A：對。(1,10)×(10,64)=(1,64)。
B：錯。(10,10) 不是矩陣乘法輸出規則。
C：錯。(64,1) 是維度順序顛倒。
D：錯。內部維度 10 與 10 相同，所以可以相乘。

【名詞解釋】
- Matrix Multiplication：矩陣乘法。
- Query Projection：Attention 中將輸入投影成 Query 的線性變換。
- Shape：張量維度形狀。
- Inner Dimension：矩陣乘法需相等的中間維度。
- Transformer：使用 Q/K/V attention 的模型架構。

【記憶】
矩陣乘法口訣：**「外面留下來，中間要一樣」**。本題外面是 1 和 64。''',
'official_115_1_subject3_42':'''【考點】
特徵萃取（Feature Extraction）與微調方式辨識。題目文字目前缺少完整程式碼，但官方答案為 C，表示該程式行應是在凍結或使用預訓練模型抽取特徵，而非更新整個模型。

【正解】
C。特徵萃取（Feature Extraction）。

【為什麼】
特徵萃取通常使用已訓練好的模型作為固定特徵產生器，只取其輸出 embedding 或中間層表示，再接下游分類器或簡單模型。若程式碼中出現凍結參數、model.eval()、no_grad()、只取 features、不更新 backbone 等線索，就屬於 feature extraction。它和 full fine-tuning 不同，後者會更新整個預訓練模型權重。

【錯誤選項解析】
A：錯。全面微調會更新整個模型或大部分權重，和固定特徵抽取不同。
B：錯。零樣本學習是不用任務標訓練直接泛化，非此題官方答案。
C：對。用預訓練模型抽取表示供後續任務使用，就是特徵萃取。
D：錯。知識蒸餾是學生模型學習教師模型輸出，不是單純取特徵。

【名詞解釋】
- Feature Extraction：使用模型抽取特徵表示。
- Backbone：預訓練主幹模型。
- Full Fine-Tuning：更新整個模型權重。
- Zero-shot Learning：未見任務或類別上的直接泛化。
- Knowledge Distillation：教師模型指導學生模型訓練。

【記憶】
特徵萃取口訣：**「大模型當特徵機，後面再接小模型」**。''',
'official_115_1_subject3_40':'''【考點】
多類別單標籤分類的輸出層 activation 與 loss。10 個類別且標籤是 One-Hot 編碼，典型搭配是 softmax + categorical_crossentropy。

【正解】
B。softmax，categorical_crossentropy。

【為什麼】
手寫數字 0–9 是 10 類單標籤分類，每張圖只屬於一個類別。輸出層應有 10 個神經元並用 softmax 轉成總和為 1 的類別機率分布。標籤已是 one-hot，因此 loss 使用 categorical_crossentropy。若標籤是整數 0–9，才常用 sparse_categorical_crossentropy。

【錯誤選項解析】
A：錯。sigmoid + MSE 不適合一般多類別單標籤分類。
B：對。one-hot 多類別分類標準組合是 softmax + categorical_crossentropy。
C：錯。relu 不適合輸出機率，binary_crossentropy 用於二元或多標籤情境。
D：錯。tanh 不適合作為多類別機率輸出；sparse loss 搭配整數標籤，不是 one-hot。

【名詞解釋】
- Softmax：將 logits 轉成多類別機率分布。
- Categorical Crossentropy：one-hot 多類別分類常用損失。
- One-Hot Encoding：正確類別為 1，其餘為 0 的標籤表示。
- MLP：多層感知機。
- Single-label Classification：每筆樣本只屬於一個類別。

【記憶】
分類輸出口訣：**「one-hot 多類別：softmax + categorical_crossentropy」**。''',
'official_115_1_subject1_45':'''【考點】
微服務連鎖故障（Cascading Failure）與斷路器模式。外部服務逾時導致鏈路壅塞時，應用 Circuit Breaker 快速失敗、暫停呼叫並提供降級回應。

【正解】
B。為外部服務導入斷路器模式，在異常時暫停呼叫並提供替代回應。

【為什麼】
當外部 API 偶發延遲或 timeout，若平台持續等待與重試，會耗盡連線、執行緒或請求佇列，導致整體服務中斷。Circuit Breaker 會在錯誤率或逾時達門檻時打開，暫停呼叫問題服務，直接回傳 fallback、快取或降級結果，避免故障擴散。

【錯誤選項解析】
A：錯。同步串行且取消逾時會讓阻塞更嚴重。
B：對。斷路器正是防止外部依賴拖垮整體系統的模式。
C：錯。盲目擴大 thread pool 可能延後爆炸，不能根治連鎖故障。
D：錯。停用健康檢查會降低可觀測性與自動復原能力。

【名詞解釋】
- Circuit Breaker：斷路器模式，異常時停止呼叫依賴服務。
- Cascading Failure：連鎖故障。
- Timeout：逾時。
- Fallback：替代回應或降級策略。
- Microservice：微服務架構。

【記憶】
斷路器口訣：**「外部服務壞掉時，不要一起等死；先斷開、快失敗、給降級」**。''',
'official_115_1_subject3_31':'''【考點】
強化學習中的獎勵設計與 Reward Hacking。機器手臂反覆抓放同一物品來刷分，是獎勵函數鼓勵了錯誤行為，需要重新做 reward shaping。

【正解】
A。獎勵塑形：將獎勵改為「成功完成一次揀貨任務」而非單次抓取行為。

【為什麼】
原獎勵「每成功抓取一個貨品 +1」沒有區分是否完成真正任務，因此 agent 找到漏洞：反覆抓放同一物品即可累積分數。這是 reward hacking / specification gaming。修正方式是把獎勵綁定到真正目標，例如物品被成功放到指定位置、訂單完成、重複抓取不給分，並可加入時間成本或重複行為懲罰。

【錯誤選項解析】
A：對。獎勵應對齊任務完成，而不是可被刷分的中間動作。
B：錯。降低學習率不能修正獎勵目標錯誤。
C：錯。Credit assignment 是如何分配延遲回饋，非本題核心。
D：錯。災難性遺忘與反覆刷分行為無關。

【名詞解釋】
- Reward Shaping：設計更合適的獎勵訊號。
- Reward Hacking：代理人鑽獎勵漏洞。
- Reinforcement Learning：強化學習。
- Policy：策略，決定 agent 行為。
- Specification Gaming：符合字面獎勵但違背真實目標。

【記憶】
RL 獎勵口訣：**「獎勵什麼，模型就鑽什麼；要獎任務完成，不獎刷分動作」**。''',
'official_115_1_subject3_44':'''【考點】
資料洩漏與交叉驗證流程。若先用整體資料做 LDA，再交叉驗證 KNN，測試 fold 的標籤資訊已影響降維，會造成資料洩漏。

【正解】
B。此寫法存在資料洩漏，應將 LDA 納入交叉驗證流程中一併進行。

【為什麼】
LDA 是監督式降維，會使用類別標籤尋找能分開類別的投影方向。若在切分 cross-validation 前先對全資料 fit LDA，測試資料的標籤資訊已被用來學投影方向，評估結果會過度樂觀。正確做法是建立 Pipeline，讓每個 fold 只用訓練 fold fit LDA，再 transform 該 fold 的驗證資料並訓練/評估 KNN。

【錯誤選項解析】
A：錯。先用整體資料 fit LDA 不是標準嚴謹流程，會洩漏。
B：對。LDA 應放進交叉驗證流程或 Pipeline 中。
C：錯。資料洩漏會讓結果不能代表真實泛化能力。
D：錯。可否跳過 LDA 不是本題重點，重點是預處理也要在 CV 內完成。

【名詞解釋】
- Data Leakage：測試資料資訊進入訓練流程。
- LDA：Linear Discriminant Analysis，監督式降維/分類方法。
- KNN：K 近鄰分類器。
- Cross-Validation：交叉驗證。
- Pipeline：把預處理與模型串成一致訓練流程。

【記憶】
CV 防洩漏口訣：**「會 fit 的步驟都要放進 fold 裡」**。''',
'official_115_1_subject3_49':'''【考點】
ResNet 與深層網路梯度消失。超過 50 層的深層 CNN 若擔心梯度消失，最經典解法是 ResNet 的 residual/skip connection。

【正解】
C。ResNet 透過殘差連接，使梯度能跨層傳遞並降低深層訓練困難。

【為什麼】
傳統深層網路層數增加時，梯度在反向傳播中容易變小，導致前面層難以更新。ResNet 引入 shortcut/skip connection，讓模型學習殘差 F(x)，並把輸入 x 直接加到後續輸出，使梯度可沿捷徑傳遞。這讓 50、101、152 層等非常深的網路更容易訓練，適合細微瑕疵特徵抽取。

【錯誤選項解析】
A：錯。VGG 只是重複堆疊 3×3 卷積，並非主要靠殘差解決梯度消失。
B：錯。GoogLeNet 的 Inception 強調多尺度卷積與效率，不是最典型的梯度消失解法。
C：對。ResNet 的殘差/跳接是深層網路訓練困難的經典解法。
D：錯。ViT 不會「完全沒有」深層訓練問題，且題目問經典架構應優先考慮 ResNet。

【名詞解釋】
- ResNet：Residual Network，殘差網路。
- Residual Connection：殘差連接。
- Skip Connection：跳接，讓訊息跨層傳遞。
- Vanishing Gradient：梯度消失。
- Deep CNN：深層卷積神經網路。

【記憶】
深層 CNN 口訣：**「層很深怕梯度消失，先想 ResNet 跳接」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
