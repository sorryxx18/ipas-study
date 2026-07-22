#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_115_1_subject1_50':'''【考點】
多模態晚期融合（Late Fusion）的特性。晚期融合是各模態先各自建模或各自產生預測，再在決策層整合結果；它不是在輸入階段就把多模態特徵合在一起。

【正解】
D。晚期融合會在輸入階段整合多模態特徵，因此能避免低品質資料影響。

【為什麼】
題目問「最不可能」原因。晚期融合的優點是影像模型與文字模型相對獨立，若問診文字品質不佳，融合層可降低文字模態權重，影像模態仍可提供主要判斷，因此整體效能只小幅下降。D 把晚期融合說成「輸入階段整合多模態特徵」，這其實比較像早期融合（Early Fusion），與 late fusion 定義相反，所以最不可能。

【錯誤選項解析】
A：錯。這是晚期融合的合理優點，各模態獨立預測可降低單一模態劣化影響。
B：錯。融合階段調整權重是合理原因。
C：錯。獨立模型可避免低品質特徵在早期特徵層直接污染其他模態。
D：對本題而言不可能。晚期融合不是輸入階段整合，而是決策/輸出階段整合。

【名詞解釋】
- Late Fusion：晚期融合，各模態先獨立預測再整合。
- Early Fusion：早期融合，在輸入或特徵層先合併模態。
- Modality：模態，如影像、文字、語音。
- Robustness：魯棒性，面對低品質資料仍維持表現。
- Fusion Weight：融合權重。

【記憶】
融合口訣：**「Early 先合特徵，Late 後合結果」**。題目說輸入階段整合，就不是 late fusion。''',
'S3_11':'''【考點】
PCA 主成分分析的核心數學原理。PCA 會尋找一組彼此正交的方向，使資料投影到這些方向後保留最大的變異量，第一主成分保留最大變異，第二主成分在與第一正交條件下保留次大變異。

【正解】
B。找到能最大化資料變異量的正交向量方向。

【為什麼】
PCA 是非監督式降維方法，目標不是分類，也不是隨機刪特徵，而是找出資料最有變化的方向。從線性代數角度看，PCA 可透過協方差矩陣的特徵分解或 SVD 找到主成分；選擇前幾個主成分即可用較少維度保留大部分資料變異。這也是它常用於資料視覺化、去冗餘與降維的原因。

【錯誤選項解析】
A：錯。最小化資料點間距離不是 PCA 的核心，容易混淆成某些分群/嵌入方法。
B：對。PCA 找最大變異方向，且主成分彼此正交。
C：錯。平均值只用於資料中心化，不是 PCA 的核心目標。
D：錯。PCA 是有數學依據的投影，不是隨機刪除特徵。

【名詞解釋】
- PCA：Principal Component Analysis，主成分分析。
- Principal Component：主成分，最大化變異量的方向。
- Orthogonal：正交，方向彼此垂直、互不重複。
- Variance：變異量。
- Dimensionality Reduction：降維。

【記憶】
PCA 口訣：**「找正交方向，保留最大變異」**。看到 PCA 核心原理就選最大化變異量。''',
'official_114_2_subject1_14':'''【考點】
超參數調整與避免過度調參造成的過擬合。使用交叉驗證在多個資料切分上評估參數組合，可避免只對單一驗證集調到太剛好，提升泛化能力。

【正解】
A。採用交叉驗證於多組參數組合間反覆評估，選擇在驗證資料上表現最穩定的設定。

【為什麼】
超參數搜尋若只盯著單一 validation set，可能把參數調到剛好適合那份驗證資料，導致真正部署時泛化變差。Cross-Validation 透過不同 fold 重複訓練與驗證，能估計參數設定在不同資料切分上的穩定性。選擇平均表現好且變異小的設定，比單次驗證更可靠。

【錯誤選項解析】
A：對。交叉驗證能更穩健評估超參數，降低對單一驗證集過擬合。
B：錯。Early Stopping 應監控驗證誤差，不是訓練誤差；且它主要控制訓練輪數，不是超參數搜尋穩健性的最佳答案。
C：錯。標準化有助於訓練穩定，但不能直接避免過度調參。
D：錯。提高複雜度與擴大搜尋範圍反而可能加劇過擬合與搜尋成本。

【名詞解釋】
- Hyperparameter：超參數，訓練前設定的參數。
- Cross-Validation：交叉驗證。
- Overfitting：過擬合。
- Generalization：泛化能力。
- Validation Set：驗證集。

【記憶】
超參數調整口訣：**「不要只信一份驗證集，多 fold 穩定才可靠」**。''',
'official_115_1_subject3_37':'''【考點】
局部可解釋性（Local Explainability）。銀行貸款單筆拒絕原因需要解釋「這一位申請人」的決策理由，因此要用能計算單筆預測特徵貢獻的方法，如 SHAP。

【正解】
A。SHAP 值：計算每個特徵對單筆預測的貢獻。

【為什麼】
Local explainability 強調個別案例的解釋。例如某申請被拒，可說明負債比、收入、信用紀錄、延遲繳款等特徵各自如何推高或降低核准機率。SHAP 基於 Shapley value，可為單筆預測分配特徵貢獻，適合產生拒絕理由與合規稽核。全域重要性只說整體趨勢，不足以解釋單一個案。

【錯誤選項解析】
A：對。SHAP 可提供單筆預測的局部特徵貢獻。
B：錯。全域特徵重要性解釋整體模型，不是單筆個案。
C：錯。Grad-CAM 主要用於影像模型熱力圖，不適合一般貸款表格資料拒絕理由。
D：錯。混淆矩陣是整體評估指標，不能解釋某筆決策。

【名詞解釋】
- SHAP：以 Shapley value 估計特徵貢獻的解釋方法。
- Local Explainability：局部可解釋性，解釋單筆預測。
- Global Feature Importance：全域特徵重要性。
- Grad-CAM：影像模型熱力圖解釋。
- Confusion Matrix：混淆矩陣。

【記憶】
局部解釋口訣：**「要解釋這一筆，選 SHAP；要看整體趨勢，才看全域重要性」**。''',
'official_114_2_subject3_22':'''【考點】
貝氏定理與條件機率分類。題目描述「在觀察到這些行為特徵的情況下，顧客會購買的機率」，正是計算後驗機率 P(會購買 | 行為特徵)。

【正解】
B。以條件機率方式計算顧客屬於「會購買」或「不會購買」的分類機率。

【為什麼】
Bayes’ Theorem 的核心是用先驗機率與觀察到的證據更新成後驗機率。電商可根據瀏覽紀錄、停留時間、商品偏好、購買歷史等特徵，估計顧客在這些條件下購買的機率，並比較「會購買」與「不會購買」兩類後驗機率。這是典型的貝氏分類思路。

【錯誤選項解析】
A：錯。自動分群較像 clustering，不是貝氏定理核心。
B：對。貝氏推論使用條件機率計算分類後驗機率。
C：錯。最小平方誤差預測購買金額是迴歸，不是本題分類機率。
D：錯。回饋信號動態調整策略屬於強化學習。

【名詞解釋】
- Bayes’ Theorem：貝氏定理。
- Conditional Probability：條件機率。
- Posterior Probability：後驗機率。
- Prior Probability：先驗機率。
- Classification：分類。

【記憶】
貝氏題口訣：**「看到在某些特徵條件下的機率，就是 P(類別 | 特徵)」**。''',
'official_114_2_subject3_11':'''【考點】
Random Search 相對 Grid Search 的優勢。當超參數維度高、真正重要的參數只有少數時，Random Search 通常比固定網格更有效率探索高維空間。

【正解】
D。能更有效率搜尋高維參數空間。

【為什麼】
Grid Search 會窮舉預先設定的格點，維度一多組合數會爆炸，而且可能把大量試驗浪費在不重要的超參數上。Random Search 隨機抽樣參數組合，在相同試驗次數下常能覆蓋更廣範圍，較有機會找到重要參數的好區間。這也是高維超參數調整時常先用 random search 的原因。

【錯誤選項解析】
A：錯。自動產生模型架構不是 Random Search 的主要特性。
B：錯。是否使用更大訓練集與搜尋方法無直接關係。
C：錯。Random Search 不保證避免過擬合，仍需驗證集或交叉驗證。
D：對。高維參數空間中，Random Search 通常比 Grid Search 更有效率。

【名詞解釋】
- Grid Search：網格搜尋，窮舉固定格點。
- Random Search：隨機搜尋。
- Hyperparameter：超參數。
- High-dimensional Space：高維空間。
- Search Budget：搜尋預算/試驗次數。

【記憶】
搜尋口訣：**「低維可 Grid，高維先 Random」**。問主要優勢就選高維效率。''',
'official_115_1_subject3_9':'''【考點】
Adam 優化器的核心。Adam 結合 Momentum 的一階動量估計與 RMSProp 類似的二階矩自適應學習率，能針對每個參數調整更新步長，使訓練更穩定。

【正解】
A。同時結合一階動量與自適應學習率，為每個參數調整更新步長。

【為什麼】
Momentum 會累積過去梯度方向，降低震盪並加速一致方向的移動；自適應學習率會根據不同參數梯度尺度調整步長。Adam 同時使用一階矩 m 與二階矩 v 的估計，對稀疏梯度或尺度差異大的參數較穩定，因此常比單純 SGD 收斂更快、更平滑。

【錯誤選項解析】
A：對。Adam 的重點就是 momentum + adaptive learning rate。
B：錯。Adam 不是強制所有參數使用相同學習率，而是自適應調整。
C：錯。Batch Normalization 是網路層/正規化技術，不是 Adam 的作用。
D：錯。梯度裁剪是另一種技術，Adam 本身不等於固定範圍裁剪。

【名詞解釋】
- Adam：Adaptive Moment Estimation。
- Momentum：一階動量，累積梯度方向。
- Adaptive Learning Rate：自適應學習率。
- Gradient：梯度。
- Optimizer：優化器。

【記憶】
Adam 口訣：**「動量穩方向，自適應調步長」**。''',
'S1_01':'''【考點】
BERT 與 GPT 的主要差異。BERT 是雙向編碼器式預訓練，擅長理解任務；GPT 是單向/因果式解碼器生成模型，擅長根據前文生成後續文字。

【正解】
B。BERT 是雙向預訓練，GPT 是單向生成。

【為什麼】
BERT 使用 masked language modeling，可同時利用左右上下文理解被遮住的詞，因此常用於分類、抽取、語意理解等任務。GPT 使用 causal language modeling，只能看左側前文預測下一 token，因此天然適合文字生成、對話與續寫。兩者都處理文字，也都基於 Transformer，但注意力方向與訓練目標不同。

【錯誤選項解析】
A：錯。說反了；BERT 偏理解，GPT 偏生成。
B：對。BERT 雙向，GPT 單向生成，是主要差異。
C：錯。兩者都可處理文字，不是圖像/文字這種差別。
D：錯。兩者雖都源自 Transformer，但架構用途與預訓練方式不同。

【名詞解釋】
- BERT：Bidirectional Encoder Representations from Transformers。
- GPT：Generative Pre-trained Transformer。
- Bidirectional：雙向上下文。
- Causal Language Modeling：因果語言模型，只看前文預測後文。
- Masked Language Modeling：遮罩語言模型。

【記憶】
BERT/GPT 口訣：**「BERT 看左右做理解，GPT 看前文做生成」**。''',
'S3_21':'''【考點】
假設檢定中的 p 值與顯著水準 α。若 p 值 < α，代表在虛無假設 H0 為真時，觀察到目前或更極端結果的機率很小，因此拒絕 H0。

【正解】
B。拒絕虛無假設 H0。

【為什麼】
p 值是衡量資料與虛無假設相容程度的指標。顯著水準 α 是事先設定的拒絕門檻，例如 0.05。若 p < α，表示結果達統計顯著，資料提供足夠證據反對 H0，因此做出「拒絕 H0」的決策。注意統計上通常說「拒絕」或「未能拒絕」H0，而不是證明 H0 為真或接受 H0。

【錯誤選項解析】
A：錯。p < α 時不是接受 H0，而是拒絕 H0。
B：對。p 值小於顯著水準，拒絕虛無假設。
C：錯。是否重收資料不是標準假設檢定決策。
D：錯。可以做出拒絕 H0 的統計決策。

【名詞解釋】
- p-value：p 值。
- α：顯著水準。
- H0：虛無假設。
- Statistical Significance：統計顯著。
- Hypothesis Testing：假設檢定。

【記憶】
假設檢定口訣：**「p 小於 α，拒絕 H0」**。''',
'S3_23':'''【考點】
Dropout 的原理。Dropout 在訓練時隨機關閉部分神經元，使模型不能過度依賴特定神經元或特徵組合，藉此降低過擬合。

【正解】
B。訓練時隨機關閉部分神經元，防止過擬合。

【為什麼】
Dropout 每個訓練 step 會以一定機率把部分神經元輸出設為 0，相當於訓練許多不同子網路的集成效果。這會迫使模型學到更分散、更穩健的表示，降低 co-adaptation。推論時通常不隨機關閉，而是使用完整網路並按框架規則縮放輸出。

【錯誤選項解析】
A：錯。Dropout 不是刪除訓練資料雜訊。
B：對。隨機關閉神經元以防止過擬合。
C：錯。它不會自動選最佳架構。
D：錯。Dropout 主要是正則化，不是加速反向傳播。

【名詞解釋】
- Dropout：隨機失活神經元的正則化方法。
- Overfitting：過擬合。
- Regularization：正則化。
- Co-adaptation：神經元過度共同適應。
- Inference：推論階段。

【記憶】
Dropout 口訣：**「訓練時隨機關一些神經元，逼模型不要死背」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
