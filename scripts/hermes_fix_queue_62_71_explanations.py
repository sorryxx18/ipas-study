#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_115_1_subject1_20':'''【考點】
即時推薦系統的低延遲架構規劃。題目要求 100 毫秒內回應、依最新使用者行為調整、尖峰 3000 QPS，因此核心是批次模型可保留，但即時特徵不能繞進高延遲資料倉儲，應用 Kafka 串流與 Redis/Feature Store 快取降低延遲。

【正解】
A。保留(1)(2)(3)，移除(4)，並加入(5)以降低延遲。

【為什麼】
歷史資料可用批次訓練建立協同過濾或候選召回模型；線上服務可用 REST API 做即時推論；Kafka 可接收即時點擊流並更新特徵。若每次都先把即時資料寫入 Data Warehouse 再算特徵，通常延遲太高，不適合 100ms 推薦。Redis 或 Feature Store 可保存最新特徵，讓線上推論快速讀取。

【錯誤選項解析】
A：對。保留批次訓練、API 推論、串流處理，移除高延遲資料倉儲路徑，加入快取/Feature Store。
B：錯。移除 Kafka 會失去即時行為更新能力，只靠資料倉儲難以滿足低延遲。
C：錯。直接移除批次訓練、改全線上學習，對小團隊與穩定性風險較高，且不一定必要。
D：錯。全部保留會讓資料倉儲路徑成為延遲瓶頸，無法兼顧即時性。

【名詞解釋】
- Batch Training：定期用歷史資料離線訓練模型。
- REST API：線上模型推論服務常見介面。
- Kafka：高吞吐串流資料平台。
- Feature Store：管理離線/線上特徵的一致性與快速讀取。
- Redis：低延遲鍵值快取，常用於即時特徵讀取。

【記憶】
即時推薦口訣：**「模型可批次，特徵要即時；資料倉儲別卡在線上路徑」**。看到 100ms，優先排除高延遲流程。''',
'official_115_1_subject3_50':'''【考點】
PyTorch 訓練迴圈中的梯度裁剪位置與目的。Gradient Clipping 應在 loss.backward() 之後、optimizer.step() 之前執行，因為此時梯度已計算完成，但權重尚未更新。

【正解】
B。插入於位置 4 與位置 5 之間；用以限制梯度範數過大，避免更新步幅失控導致數值不穩。

【為什麼】
典型 PyTorch 流程是：清梯度 optimizer.zero_grad() → forward → loss → backward → clip_grad_norm_ → optimizer.step()。梯度裁剪不是限制 loss，而是限制參數梯度的 norm，避免 exploding gradients 造成權重更新過大、loss 變 NaN 或訓練不穩定。

【錯誤選項解析】
A：錯。梯度裁剪不是限制 Loss 數值，也不是主要處理梯度消失；它處理梯度爆炸。
B：對。backward 後、step 前裁剪梯度範數，是正確插入位置。
C：錯。optimizer.step() 後才裁剪已經太晚，權重已依過大梯度更新。
D：錯。輸入影像批次標準化是資料/模型層處理，和梯度裁剪無關。

【名詞解釋】
- Gradient Clipping：限制梯度大小，避免梯度爆炸。
- clip_grad_norm_：PyTorch 中依梯度 norm 裁剪的函式。
- loss.backward()：反向傳播，計算梯度。
- optimizer.step()：依梯度更新模型參數。
- Exploding Gradient：梯度過大導致訓練不穩或 NaN。

【記憶】
梯度裁剪口訣：**「先 backward 算梯度，再 clip，最後 step」**。看到 NaN、梯度爆炸、更新失控，就想到 step 前裁剪。''',
'official_114_2_subject3_16':'''【考點】
F1-score 計算。F1 是 Precision 與 Recall 的調和平均，用於同時考量精確率與召回率，公式為 F1 = 2PR / (P + R)。

【正解】
A。0.686。

【為什麼】
題目給 Precision = 0.8、Recall = 0.6。代入公式：F1 = 2 × 0.8 × 0.6 / (0.8 + 0.6) = 0.96 / 1.4 = 0.6857，四捨五入約為 0.686。因此答案選 A。

【錯誤選項解析】
A：對。0.686 是依 F1 公式計算後的近似值。
B：錯。0.700 不是正確代入公式的結果，可能是粗略平均或誤算。
C：錯。0.720 偏高，沒有符合調和平均公式。
D：錯。0.750 更接近 Precision 與 Recall 的錯誤加權結果，非 F1。

【名詞解釋】
- Precision：預測為正的樣本中，真正為正的比例。
- Recall：所有真正為正的樣本中，被模型找出的比例。
- F1-score：Precision 與 Recall 的調和平均。
- Harmonic Mean：調和平均，會被較低的數值拉低。
- 二元分類：輸出正類/負類的分類問題。

【記憶】
F1 口訣：**「F1 = 2PR / (P+R)」**。不要用普通平均；P=0.8、R=0.6 時，F1 約 0.686。''',
'official_115_1_subject3_18':'''【考點】
CNN 池化層（Pooling Layer）的作用。題目說卷積層後直接接全連接層造成參數量過高，因此池化最主要解決的是降低特徵圖空間維度，進而減少後續參數量與計算成本。

【正解】
A。降低特徵圖空間維度，減少參數與計算量。

【為什麼】
卷積輸出的特徵圖若尺寸很大，攤平後接全連接層會產生大量參數。Pooling 例如 Max Pooling 或 Average Pooling 可把特徵圖寬高縮小，保留重要摘要資訊，減少後續 layer 的輸入維度，因此降低參數量、記憶體使用與計算成本。

【錯誤選項解析】
A：對。池化降低空間解析度，是降低參數與計算量的主要方式。
B：錯。非線性表達主要由 ReLU 等 activation function 提供，不是 pooling 的主要任務。
C：錯。梯度消失主要靠合適激活函數、初始化、正規化或殘差設計改善，不是 pooling 的核心目的。
D：錯。Pooling 可能有助於泛化與平移不變性，但它確實會影響特徵圖空間維度。

【名詞解釋】
- Pooling Layer：降低特徵圖尺寸的層。
- Max Pooling：取局部區域最大值。
- Average Pooling：取局部區域平均值。
- Feature Map：卷積層輸出的特徵圖。
- Fully Connected Layer：全連接層，輸入維度大時參數量會暴增。

【記憶】
Pooling 口訣：**「縮寬高、降參數、留重點」**。看到卷積後全連接參數太多，就想到 pooling 降維。''',
'S1_26':'''【考點】
TF-IDF 中 IDF（Inverse Document Frequency）的作用。題目問 IDF，核心是降低在大量文件中都出現的常見詞權重，凸顯較能代表特定文件的詞。

【正解】
B。降低在大量文件中都出現的常見詞的權重。

【為什麼】
TF-IDF = TF × IDF。TF 衡量詞在當前文件中出現多頻繁；IDF 衡量詞在整個文件集合中有多稀有。像「的」、「是」、「and」這類詞出現在許多文件中，區辨力低，因此 IDF 會給較低權重；較少出現但能代表主題的詞，IDF 權重較高。

【錯誤選項解析】
A：錯。計算詞在當前文件中的出現頻率是 TF，不是 IDF。
B：對。IDF 會降低常見詞權重，提升稀有且具代表性詞的影響。
C：錯。將詞轉換為向量是詞向量/embedding 的概念，不是 IDF 本身。
D：錯。移除停用詞是前處理方法，IDF 則是權重計算。

【名詞解釋】
- TF：Term Frequency，詞在某文件中的出現頻率。
- IDF：Inverse Document Frequency，逆文件頻率。
- TF-IDF：結合詞頻與逆文件頻率的文字特徵權重。
- Stop Words：常見但資訊量低的停用詞。
- Document Corpus：文件集合，用來計算 IDF。

【記憶】
TF-IDF 口訣：**「TF 看本篇多常出現，IDF 看全庫多不常見」**。題目問常見詞降權，選 IDF。''',
'official_114_2_subject1_9':'''【考點】
資料增強造成分布偏移與語意不一致。資料增強的前提是增強樣本仍保持原標籤與真實資料分布；若增強後特徵分布偏離原始資料，反而會傷害泛化。

【正解】
B。增強後資料的特徵分佈與原始資料不一致，影響模型的泛化能力，應檢查並調整增強策略以維持語意一致性。

【為什麼】
資料增強用來擴充訓練樣本，但不是越多越好。若影像增強過度改變物件外觀、文字增強改變語意、生成樣本品質低或和真實資料分布不一致，模型會學到錯誤模式。改善方式是檢查增強策略、限制增強強度、確保標籤不變，並比較增強前後資料分布。

【錯誤選項解析】
A：錯。隨機初始化不是資料增強效能下降的主要原因，且重新設計啟動流程不對題。
B：對。增強資料分布與語意偏移，是效能下降最常見且合理原因。
C：錯。若增強比例過高造成偏好，應降低或調整比例，不是提高增強比例。
D：錯。標註可信度可能是問題，但選項提出半監督校正過於跳躍；題目更直接指向增強分布不一致。

【名詞解釋】
- Data Augmentation：透過轉換或生成方式擴充訓練資料。
- Distribution Shift：訓練資料與真實資料分布不一致。
- Semantic Consistency：增強後樣本仍保持原本語意與標籤。
- Generalization：模型對未見資料的泛化能力。
- Train-Inference Gap：訓練資料與推論場景差異。

【記憶】
資料增強口訣：**「增強要像真資料，不能改掉語意」**。模型變差時先檢查增強是否造成分布偏移。''',
'official_114_2_subject3_4':'''【考點】
DBSCAN 中核心點、邊界點與雜訊點的判斷。題目說該點鄰域樣本數不足，不是核心點；又未被任何核心點鄰域包含，也無密度可達關係，因此會被標為 Noise Point。

【正解】
B。雜訊點（Noise Point）。

【為什麼】
DBSCAN 以 ε 半徑與 MinPts 判斷資料點類型。核心點是在 ε 鄰域內有足夠多點；邊界點本身鄰域點數不足，但落在某核心點鄰域內，可歸屬某群集。若一個點既不是核心點，也不屬於任何核心點鄰域，且無法由密度可達關係連到群集，就會被視為雜訊點或離群點。

【錯誤選項解析】
A：錯。Neighbor Point 不是 DBSCAN 標準輸出類型。
B：對。題幹完整描述了 Noise Point 的條件。
C：錯。邊界點雖然不是核心點，但必須落在核心點鄰域內；本題明確說沒有。
D：錯。Potential Point 不是 DBSCAN 的標準分類。

【名詞解釋】
- DBSCAN：基於密度的分群方法，可辨識雜訊點。
- Core Point：ε 鄰域內點數達 MinPts 的核心點。
- Border Point：非核心點，但位於核心點鄰域內。
- Noise Point：不屬於任何群集的雜訊/離群點。
- Density Reachability：密度可達關係，用於連接同一群集內的點。

【記憶】
DBSCAN 點類型口訣：**「夠密是核心，被核心包是邊界，兩者都不是就是雜訊」**。''',
'official_115_1_subject3_13':'''【考點】
過擬合與 L2 權重衰減（Weight Decay）。題目說訓練 F1=0.96、驗證 F1=0.71，典型過擬合；且問從降低模型複雜度角度緩解，因此選 L2 正則化。

【正解】
C。對 Embedding 層與全連結層加入 L2 權重衰減，懲罰參數值。

【為什麼】
L2 正則化會在損失函數中加入權重平方懲罰，讓模型傾向使用較小權重，降低模型複雜度與對訓練資料細節的過度依賴。文本分類模型若訓練集表現遠高於驗證集，加入 weight decay、dropout、early stopping 或資料增強都可能有助，但題目強調「降低模型複雜度」，L2 最直接。

【錯誤選項解析】
A：錯。增加 epoch 會讓模型更記住訓練資料，通常加重過擬合。
B：錯。加入 URL、HTML 等原始噪音特徵可能增加複雜度與過擬合。
C：對。L2 權重衰減懲罰大權重，降低模型複雜度。
D：錯。移除驗證集會失去泛化評估依據，也可能掩蓋過擬合。

【名詞解釋】
- Overfitting：訓練集表現好、驗證/測試集表現差。
- L2 Regularization：對權重平方和加懲罰。
- Weight Decay：深度學習中常見的 L2 正則化實作。
- Embedding Layer：把 token 轉成向量表示的層。
- Validation Set：用來監控泛化能力的資料集。

【記憶】
過擬合口訣：**「訓練高、驗證低，要降複雜度」**。看到懲罰參數值，就選 L2/Weight Decay。''',
'official_114_2_subject1_47':'''【考點】
多任務學習（Multi-task Learning）中的任務競爭與 loss 權重平衡。題目說 NER 準確率提升時文檔分類下降，架構正確、資料品質良好，最可能是不同任務的 loss 權重未平衡，導致共享表示偏向某一任務。

【正解】
C。損失函數未進行權重平衡，導致任務間競爭。

【為什麼】
多任務模型通常共享 Transformer encoder，再接不同任務輸出頭。若 NER loss 權重過高或梯度主導共享層，模型會更偏向序列標註任務，犧牲文檔分類表現。解法是調整 loss weight、採用動態權重、梯度平衡或分階段訓練，讓任務共同受益。

【錯誤選項解析】
A：錯。Transformer 可同時支援分類與序列標註，只要設計不同輸出頭即可。
B：錯。文檔分類同樣需要 contextualized representation。
C：對。任務間 loss/梯度未平衡，是多任務此類此消彼長的常見原因。
D：錯。BERT 可加多個任務輸出頭，不是不支援 multi-head outputs。

【名詞解釋】
- Multi-task Learning：單一模型同時學多個任務。
- Loss Weight：不同任務損失在總損失中的權重。
- NER：命名實體辨識，屬於序列標註任務。
- Document Classification：文檔分類，通常輸出整篇文件類別。
- Shared Encoder：多任務模型中共用的表示學習層。

【記憶】
多任務口訣：**「共享表示會互相拉扯，loss 權重要平衡」**。某任務變好另一任務變差，先看任務競爭。''',
'official_115_1_subject1_43':'''【考點】
推薦系統上線前的線上驗證策略：Canary Release。題目要在可控制風險下量化真實業務指標，重點是把少量真實流量導向新模型，觀察 CTR、CVR 等線上指標後逐步擴量。

【正解】
C。金絲雀發布：將 1–5% 使用者流量導向新模型，量測 CTR、CVR 等指標並逐步擴量。

【為什麼】
離線 AUC、NDCG@10 無法完全代表真實互動效果。Canary Release 讓新模型先服務少量用戶，能在真實環境量測點擊率、轉換率、停留時間、錯誤率等指標，同時把風險限制在小流量範圍。若指標良好再逐步擴大，若出問題可快速回滾。

【錯誤選項解析】
A：錯。Shadow Mode 可比較輸出差異與系統穩定，但使用者仍看舊模型，無法量化真實業務互動指標。
B：錯。Backtesting 仍是歷史資料模擬，不是真實線上互動。
C：對。少量真實流量 + 業務指標 + 可回滾，是控制風險的線上驗證。
D：錯。Load Testing 只測壓力與效能，不能驗證推薦業務效果，直接全面上線風險太高。

【名詞解釋】
- Canary Release：先將少量流量導向新版本，觀察穩定後擴量。
- CTR：Click-through Rate，點擊率。
- CVR：Conversion Rate，轉換率。
- Shadow Mode：新模型後台運行但不影響使用者結果。
- Backtesting：用歷史資料回測模型表現。

【記憶】
上線驗證口訣：**「要真實業務指標，就給少量真流量」**。離線好不代表線上好，正式前用 Canary 控風險。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
