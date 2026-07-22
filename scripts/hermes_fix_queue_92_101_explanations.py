#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
# repair obvious option contamination in subject3_45 D
byid['official_115_1_subject3_45']['options']['D']='程式碼 C、程式碼 D'
explanations={
'official_115_1_subject1_33':'''【考點】
合成資料（Synthetic Data）在 AI 訓練中的角色。題目場景是真實惡劣天氣資料不足，重點是合成資料可在可控制條件下補足稀有、多樣或危險場景，但不能無條件完全取代真實資料。

【正解】
D。合成資料可在控制條件下產生多樣化場景，用於擴充訓練資料並提升模型的泛化能力。

【為什麼】
自駕車需要面對大雨、濃霧、逆光、夜間等長尾場景，但真實收集成本高且風險高。透過模擬器或生成式方法產生合成資料，可控制天氣、光線、道路與物件配置，補充訓練集，讓模型更常見到罕見情境。仍需用真實資料驗證與校準，避免 synthetic-to-real gap。

【錯誤選項解析】
A：錯。合成資料不只用於文字，也常用於影像、自駕、醫療、機器人等任務。
B：錯。合成資料通常不能完全取代真實資料，仍需真實資料驗證分布與泛化。
C：錯。合成資料主要在訓練資料擴充與場景覆蓋，不是降低推論計算成本。
D：對。可控制、多樣化、補充稀有場景，是合成資料的核心價值。

【名詞解釋】
- Synthetic Data：人工生成或模擬產生的資料。
- Data Augmentation：資料擴增，增加訓練樣本多樣性。
- Long-tail Scenario：罕見但重要的場景。
- Synthetic-to-real Gap：合成資料與真實世界分布差距。
- Generalization：模型對未見情境的泛化能力。

【記憶】
合成資料口訣：**「真實難收，合成補場景；不能全取代，還要真實驗證」**。''',
'official_115_1_subject1_32':'''【考點】
CNN 卷積輸出接全連接層前的維度轉換。卷積層輸出通常是 N×C×H×W 的特徵圖，而 Linear/全連接層需要一維向量輸入，因此要先 Flatten。

【正解】
B。使用 Flatten 將特徵圖展平成一維向量。

【為什麼】
PyTorch 中 Conv2d 輸出仍保留 channel、高度、寬度等空間維度。若要接 nn.Linear，必須把每張圖片的特徵圖展平成 shape 為 batch_size × features 的二維張量。常見做法是在 forward 中使用 torch.flatten(x, 1) 或 nn.Flatten()。若維度未轉換，Linear 層通常會因形狀不符而報錯。

【錯誤選項解析】
A：錯。Global Average Pooling 也可作為架構選擇，但題目問卷積輸出接全連結層中間需要插入的基本操作，標準答案是 Flatten。
B：對。Flatten 是卷積特徵圖接全連接分類器的常見必要步驟。
C：錯。系統不會自動把卷積輸出轉成 Linear 所需一維向量。
D：錯。Softmax 通常放在分類輸出後，不是在進入全連接層前。

【名詞解釋】
- Flatten：把多維張量展平成一維特徵向量。
- Feature Map：卷積層輸出的特徵圖。
- Fully Connected Layer：全連接層，通常接收向量輸入。
- torch.flatten(x, 1)：保留 batch 維度，展平其餘維度。
- Linear Layer：PyTorch 的 nn.Linear。

【記憶】
CNN 接 FC 口訣：**「卷積出圖，Linear 要向量，中間先 Flatten」**。''',
'official_114_2_subject1_36':'''【考點】
Grid Search 與超參數搜尋。題目說針對多種模型設定進行系統化測試，想找出驗證資料上表現最穩定的組合，最符合 Grid Search。

【正解】
B。透過網格搜尋（Grid Search）在多組超參數設定中進行系統化搜尋與評估。

【為什麼】
Grid Search 會先定義每個超參數的候選值，例如 learning rate、tree depth、regularization，再窮舉所有組合並用驗證資料或交叉驗證評估表現。題目關鍵字是「多種模型設定」、「系統化測試」、「找出組合」，因此不是泛泛的交叉驗證，而是超參數組合搜尋。

【錯誤選項解析】
A：錯。交叉驗證是評估方法，可搭配調參，但本題問系統化測試多組超參數組合。
B：對。Grid Search 正是針對多組超參數候選值逐一搜尋評估。
C：錯。Random Search 也是調參方法，但題目強調系統化測試，較像 Grid Search。
D：錯。Bayesian Optimization 會根據歷次結果動態選下一組，不是單純網格系統化搜尋。

【名詞解釋】
- Hyperparameter：訓練前設定的參數，如學習率、樹深度。
- Grid Search：窮舉超參數候選組合。
- Validation Set：用於比較模型設定表現的資料。
- Random Search：隨機抽樣部分參數組合。
- Bayesian Optimization：利用代理模型動態選擇下一組參數。

【記憶】
調參口訣：**「列好候選值、一格一格試，就是 Grid Search」**。''',
'S3_24':'''【考點】
AUC-ROC 的意義。AUC 越接近 1，代表模型越能把正類排在負類前面，區分正負類的能力越強。

【正解】
B。模型區分正負類的能力越強。

【為什麼】
ROC 曲線描述不同分類閾值下 TPR 與 FPR 的關係，AUC 是 ROC 曲線下面積。AUC=0.5 接近隨機猜測，AUC=1 代表排序能力完美。它衡量的是模型對正負樣本的排序/區分能力，不直接代表資料量、訓練是否過擬合或模型一定在業務上有效。

【錯誤選項解析】
A：錯。AUC 越接近 1 通常越好，不是越差。
B：對。AUC 高代表正負類排序區分能力強。
C：錯。AUC 高不必然表示過擬合；需比較訓練/驗證/測試表現。
D：錯。訓練資料量多不會由 AUC 直接判斷。

【名詞解釋】
- ROC：以 FPR 為 x 軸、TPR 為 y 軸的曲線。
- AUC：ROC 曲線下面積。
- TPR/Recall：真正類被找出的比例。
- FPR：負類被錯判成正類的比例。
- Ranking Ability：模型把正類排在負類前面的能力。

【記憶】
AUC 口訣：**「0.5 像亂猜，越接近 1 越會分」**。''',
'official_115_1_subject1_19':'''【考點】
AI 導入成效不能只看離線模型指標。推薦系統上線後，需要同時看離線指標與線上業務指標，例如 CTR、CVR、營收、留存與使用者體驗。

【正解】
A。僅依賴離線指標 AUC 判斷模型成效，忽略線上業務指標變化，可能導致錯誤結論。

【為什麼】
AUC 衡量模型排序能力，但推薦系統真正成效取決於使用者是否點擊、購買、停留或提升營收。離線 AUC 高不代表線上 CTR 或營收一定變好，因為線上環境有曝光位置、推薦多樣性、使用者互動與商業目標等因素。導入成效應用 A/B test 或線上監控綜合評估。

【錯誤選項解析】
A：對。只看 AUC 是根本問題，忽略業務指標可能得出錯誤結論。
B：錯。CTR 下降不能被 AUC 高直接抵消，推薦品質需看線上效果。
C：錯。CTR 略降不一定立即 rollback，需看統計顯著性與多指標。
D：錯。平均訂單金額提升也不能單獨代表成功，仍需看整體指標。

【名詞解釋】
- AUC：模型排序能力指標。
- CTR：點擊率。
- CVR：轉換率。
- Offline Metric：離線評估指標。
- Online Business Metric：線上業務指標，如營收與留存。

【記憶】
導入成效口訣：**「AUC 高只是模型會排，業務好不好要看線上指標」**。''',
'official_115_1_subject3_4':'''【考點】
資料擴增的語意一致性（Semantic Consistency）。水平翻轉不是所有影像任務都安全，若翻轉會改變標籤語意，就會造成錯誤訓練訊號。

【正解】
C。手寫數字辨識。

【為什麼】
貓狗分類、車型分類、行人偵測通常水平翻轉後類別語意仍相同。但手寫數字可能因翻轉造成語意改變，例如 6/9、2/5 或某些手寫形狀變得不合理，模型會學到錯誤標籤。資料增強必須符合任務語意，不能只因為常見就套用到所有影像任務。

【錯誤選項解析】
A：錯。貓狗水平翻轉後仍是貓或狗，通常語意不變。
B：錯。多數車型水平翻轉後仍是同車型，較不會改變標籤。
C：對。手寫數字方向與形狀具有語意，翻轉可能改變或破壞標籤。
D：錯。行人偵測水平翻轉通常仍是行人，常用於資料增強。

【名詞解釋】
- Data Augmentation：透過轉換增加資料多樣性。
- Semantic Consistency：增強後樣本仍保持原標籤語意。
- Horizontal Flip：水平翻轉影像。
- Label Noise：標籤錯誤或被破壞。
- Image Classification：影像分類任務。

【記憶】
資料增強口訣：**「翻轉前先問：標籤會不會變？」**。會改變語意就不能亂翻。''',
'official_114_2_subject3_39':'''【考點】
Dropout 正則化。題目雖提到附圖，但選項中若程式碼是在訓練時隨機關閉部分神經元或使用 dropout layer，對應的正則化技術就是 Dropout。

【正解】
C。Dropout。

【為什麼】
Dropout 會在訓練過程中以一定機率將部分神經元輸出設為 0，迫使模型不要過度依賴特定神經元組合，降低 co-adaptation 與過擬合。推論時通常不隨機關閉，而是使用完整網路並依框架處理縮放。

【錯誤選項解析】
A：錯。L1 正則化是在 loss 中加入權重絕對值懲罰，會促進稀疏。
B：錯。L2 正則化是在 loss 中加入權重平方懲罰，常稱 weight decay。
C：對。隨機丟棄神經元輸出就是 Dropout。
D：錯。Batch Normalization 是正規化 mini-batch 的分布，不是隨機關閉神經元。

【名詞解釋】
- Dropout：訓練時隨機將部分神經元輸出設為 0 的正則化方法。
- Regularization：降低過擬合的技術。
- Overfitting：模型過度記住訓練資料。
- Co-adaptation：神經元彼此過度依賴。
- Batch Normalization：對 batch 統計量做正規化的層。

【記憶】
Dropout 口訣：**「訓練時隨機關掉一些神經元，避免模型太依賴」**。''',
'S1_10':'''【考點】
GDPR 對個人資料使用的核心要求。GDPR 強調合法性、透明性、目的限制、資料最小化與資料主體權利，使用個資前需有合法依據並清楚告知目的；同意必須明確且可撤回。

【正解】
B。個資使用前需取得明確同意並告知目的。

【為什麼】
GDPR 要求組織處理個人資料時必須有合法依據，例如明確同意、契約必要、合法利益等，且要告知資料使用目的、保存方式與權利。題目選項中最符合核心精神的是「明確同意並告知目的」。加密只是安全措施，不能取代合法依據與透明告知。

【錯誤選項解析】
A：錯。個資不能自由使用，需合法依據與告知。
B：對。明確同意與目的告知符合 GDPR 核心要求。
C：錯。加密不代表可任意使用個資。
D：錯。個資不只政府可用，企業也可在合法依據下處理。

【名詞解釋】
- GDPR：歐盟一般資料保護規則。
- Consent：資料主體明確同意。
- Purpose Limitation：資料只能用於告知的特定目的。
- Data Minimization：只收集必要資料。
- Data Subject Rights：資料主體權利，如查詢、刪除、撤回同意。

【記憶】
GDPR 口訣：**「先告知、要依據、只為特定目的用個資」**。''',
'official_115_1_subject3_45':'''【考點】
Stratified Cross-Validation 與類別比例維持。題目要求每次交叉驗證分割時，訓練集與測試集類別比例和原始資料一致，核心是 stratify / StratifiedKFold。

【正解】
A。程式碼 B、程式碼 C、程式碼 D。

【為什麼】
分類任務若類別不平衡，普通 KFold 可能讓某些 fold 的類別比例偏差，影響準確率估計。StratifiedKFold 或在 train_test_split 中使用 stratify，可確保每個分割大致維持原始類別比例。此題 JSON 的 D 選項原本混入下一段 CIFAR-10 題幹，已修正為「程式碼 C、程式碼 D」。

【錯誤選項解析】
A：對。依官方答案，B/C/D 皆屬於能維持類別比例的合適程式碼組合。
B：錯。少了部分可行的 stratified 設定，且包含不完整組合。
C：錯。包含不合適或缺漏組合，不能保證正確。
D：錯。只含 C/D 少了 B，不符合官方答案組合。

【名詞解釋】
- StratifiedKFold：分層 K 折交叉驗證，維持類別比例。
- cross_val_score：scikit-learn 執行交叉驗證評分的函式。
- cv：交叉驗證分割策略參數。
- Class Imbalance：類別比例不均。
- Stratify：依類別比例分層抽樣。

【記憶】
分層驗證口訣：**「分類要顧比例，cv 用 Stratified」**。看到每折類別比例一致，就選 stratified 方法。''',
'official_115_1_subject3_39':'''【考點】
公平性去偏策略：pre-processing、in-processing、post-processing。題目限制推論階段不能使用性別欄位調整輸出，因此不能使用依性別分組調整門檻的後處理；仍可在訓練中加入公平性懲罰。

【正解】
A。訓練中在損失函數加入公平性懲罰項，降低不同群體的錯誤拒絕比例差異。

【為什麼】
女性中「實際有還款能力卻被拒絕」比例較高，表示 false negative / 錯誤拒絕存在群體差異。若法務不允許推論階段使用性別欄位，就不能在後處理按性別調門檻；但可以在訓練階段使用公平性約束或懲罰項，讓模型學到較公平的決策邊界，部署時不需直接用性別欄位調整輸出。

【錯誤選項解析】
A：對。In-processing 可在訓練中加入公平性目標，符合限制。
B：錯。前處理重採樣可做，但選項說「無法直接修正既有模型」且不是最符合題意的策略。
C：錯。Post-processing 依性別調整門檻，推論階段需要使用性別欄位，違反限制。
D：錯。改用 Demographic Parity 指標不會讓錯誤拒絕比例自動消失，也未直接處理 equal opportunity 類問題。

【名詞解釋】
- In-processing：訓練過程中加入公平性約束或懲罰。
- Post-processing：模型訓練後調整輸出或門檻。
- False Negative：實際正例卻被判為負例。
- Equal Opportunity：不同群體真陽性率/錯誤拒絕差異相關公平指標。
- Fairness Penalty：加入 loss 的公平性懲罰項。

【記憶】
公平去偏口訣：**「不能推論時按群體調，就把公平性放進訓練目標」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
