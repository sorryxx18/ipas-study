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
'official_114_2_subject1_42': '''【考點】
模型上線後的資料分佈偏移偵測，以及 VAE 在潛在空間監控中的用途。題目已明確說「新樣本錯誤率上升」、「輸入資料分佈與原訓練集不同」，因此重點是偵測資料偏移，而不是盲目換模型或增加模型容量。

【正解】
D。使用變分自編碼器（VAE）監控潛在空間分佈，偵測輸入資料偏移。

【為什麼】
VAE 可將輸入資料編碼到潛在空間，學習訓練資料的分佈結構。當上線資料進來後，若其潛在空間分佈和訓練時明顯不同，就可作為資料偏移或異常輸入的訊號。金融風控模型上線後錯誤率升高，且已發現輸入資料分佈不同，最合理的第一步是建立監控與偏移偵測機制，確認新資料是否偏離訓練分佈。

【錯誤選項解析】
A：錯。GAN 生成新樣本可能用於資料增強，但題目問的是上線後資料分佈偏移的應對與監控；直接混入生成樣本不一定能解決真實分佈改變。
B：錯。改用 Logistic Regression 不一定提升穩定性，也沒有針對資料分佈偏移做偵測或治理。
C：錯。增加模型容量可能讓模型更複雜，甚至更容易過擬合；資料分佈已改變時，單純加大模型不是最合適策略。
D：對。用 VAE 監控潛在空間分佈，可偵測輸入資料是否偏離原訓練集，是針對資料偏移的合理方法。

【名詞解釋】
- VAE：變分自編碼器，可學習資料的潛在表示與分佈。
- 潛在空間：模型將原始資料壓縮後的低維表示空間。
- Data Drift：上線後輸入資料分佈和訓練資料不同。
- Discriminative Model：鑑別式模型，直接學習輸入到標籤的判別邊界。
- Model Capacity：模型可表達複雜函數的能力。

【記憶】
看到「輸入分佈變了」→ 先做 drift 監控；看到「潛在空間分佈」→ 想到 VAE / autoencoder 類方法。不要一看到錯誤率升高就選加大模型。''',

'official_115_1_subject3_30': '''【考點】
Bias-Variance 診斷與交叉驗證結果判讀。題目給出「訓練 AUC 很高、驗證 AUC 明顯低、K-fold 結果差異大、少數樣本預測波動大」，這是高變異的典型特徵。

【正解】
B。高變異。

【為什麼】
高變異代表模型對訓練資料或資料切分非常敏感。訓練 AUC=0.97 很高，但驗證 AUC=0.72 明顯下降，表示模型在訓練集表現好、泛化到驗證資料表現差。不同 K-fold 切分結果差異明顯，也代表模型對資料抽樣變動很敏感。這些現象最符合高變異。過擬合通常是高變異的一種表現，但題目問「最可能的問題」且答案給高變異，是更精準的診斷。

【錯誤選項解析】
A：錯。高偏差通常表現為訓練集與驗證集都不好，例如訓練 AUC 也低；本題訓練 AUC 很高，不像高偏差。
B：對。訓練表現高、驗證表現低、K-fold 波動大，都是高變異特徵。
C：錯。過擬合和高變異有關，但本題選項中「高變異」更直接描述 K-fold 差異與少數樣本波動。
D：錯。資料漂移是上線資料分佈與訓練資料不同；題目描述的是訓練/驗證與交叉驗證表現，不是部署後資料分佈改變。

【名詞解釋】
- 高變異：模型對訓練資料變動很敏感，容易在不同資料切分下表現差異大。
- 高偏差：模型過於簡單，訓練集與驗證集表現都差。
- AUC：衡量分類模型排序能力的指標。
- K-fold Cross Validation：把資料分成 K 份輪流驗證，用來估計模型穩定性。
- 過擬合：模型過度記住訓練資料，導致泛化能力差。

【記憶】
診斷口訣：**「訓練好、驗證差、切分波動大＝高變異」**；「訓練也差、驗證也差＝高偏差」。''',

'official_115_1_subject1_48': '''【考點】
Data Drift、Concept Drift、Training-Serving Skew 與 Threshold Shift 的差異。題目特別說「特徵分布未明顯變化」，但「原本高風險的交易型態逐漸轉為一般消費」，代表特徵與標籤之間的關係變了，屬於概念漂移。

【正解】
C。概念漂移（Concept Drift），因特徵與目標標籤之間的關聯性改變。

【為什麼】
Concept Drift 指輸入特徵和目標標籤之間的關係改變。這題中，交易金額、地區、裝置等特徵分布沒有明顯變化，所以不是 Data Drift；也沒有說線上線下特徵處理不一致，所以不是 Training-Serving Skew。關鍵是疫情後使用者行為改變，深夜電商交易從高風險型態逐漸變成一般消費，表示同樣特徵對「是否盜刷」的意義改變，因此是概念漂移。

【錯誤選項解析】
A：錯。Data Drift 是輸入特徵分布改變；題目明說交易金額、地區、裝置等特徵分布未明顯變化。
B：錯。Training-Serving Skew 是訓練與線上服務時特徵處理不一致；題目未提到資料管線或特徵工程不一致。
C：對。特徵與標籤關係改變，原本高風險行為變成一般消費，正是 Concept Drift。
D：錯。Threshold Shift 是分類門檻設定問題；題目重點不是門檻調錯，而是行為型態與風險關係改變。

【名詞解釋】
- Data Drift：輸入特徵分布改變。
- Concept Drift：輸入特徵與目標標籤的關係改變。
- Training-Serving Skew：訓練時與線上服務時資料處理邏輯不一致。
- Threshold Shift：分類決策門檻設定改變或不適合。
- AUC：衡量模型排序能力的指標，AUC 穩定不代表所有營運指標都不變。

【記憶】
漂移判斷口訣：**「特徵分布變＝Data Drift；特徵意義變＝Concept Drift」**。題目說分布沒變但行為意義變，就選概念漂移。''',

'official_115_1_subject1_34': '''【考點】
增量學習（Incremental Learning）在動態特徵空間與即時更新場景的應用。題目關鍵字是「每天新增數百個特徵」、「特徵空間動態擴展」、「批次重訓導致模型過期」，因此要選能隨新資料與新特徵持續更新的模型方向。

【正解】
B。採用支援增量學習的模型，使模型能隨新資料即時更新並適應新增特徵，而不需重新訓練整個模型。

【為什麼】
CTR 預測系統常面對用戶行為、廣告位、設備類型等特徵快速變化。如果只用靜態模型定期批次重訓，模型會跟不上最新資料分佈與新特徵。Incremental Learning 或 Online Learning 允許模型在新資料到來時逐步更新參數，降低全量重訓成本，也能更快適應變化。

【錯誤選項解析】
A：錯。把每週重訓改成每日重訓只能降低延遲，仍是批次靜態流程，且不一定能有效處理特徵空間頻繁擴展。
B：對。增量學習可隨新資料即時更新，適合 CTR 這類動態、高頻變化場景。
C：錯。固定架構 DNN 每次新增特徵就重定義輸入層並全量重訓，成本高且不即時，正是題目要避免的問題。
D：錯。GNN 可建模圖結構關係，但題目核心不是圖資料，而是新特徵與資料持續到來；預訓練 GNN 不能自動解決動態特徵空間問題。

【名詞解釋】
- Incremental Learning：模型隨新資料逐步更新，而不是每次從頭重訓。
- Online Learning：模型在資料流到來時即時或近即時更新。
- CTR：Click-Through Rate，點擊率，常用於廣告預測。
- Dynamic Feature Space：特徵集合會隨時間新增或變動。
- Batch Retraining：定期使用累積資料重新訓練整個模型。

【記憶】
動態特徵口訣：**「特徵一直長，模型要能增量學」**。看到每天新增特徵、批次模型過期，就選 Incremental Learning。''',

'official_114_2_subject1_11': '''【考點】
DBSCAN 分群演算法的兩個主要超參數：Epsilon ε 與 MinPts。題目關鍵字是「密度式分群」、「主要群集與雜訊資料」，DBSCAN 正是透過鄰域半徑與最小點數判斷核心點、邊界點與雜訊點。

【正解】
C。鄰域半徑（Epsilon ε）與最小點數（MinPts）。

【為什麼】
DBSCAN 是 Density-Based Spatial Clustering of Applications with Noise，會以每個點周圍的密度形成群集。ε 決定一個點的鄰域半徑；MinPts 決定在該半徑內至少要有多少點才可成為核心點。若某點不屬於任何足夠密度的區域，就可能被標為雜訊。因此 DBSCAN 能自動找出主要群集並辨識離群/雜訊資料。

【錯誤選項解析】
A：錯。特徵數不是 DBSCAN 的主要超參數，學習率則常見於梯度式模型訓練，DBSCAN 不用學習率。
B：錯。K 值是 K-means 或 KNN 類方法常見參數；DBSCAN 不需要事先指定群集數 K。
C：對。ε 與 MinPts 是 DBSCAN 的兩個核心超參數。
D：錯。交叉熵與權重初始化是神經網路訓練相關概念，和 DBSCAN 分群無關。

【名詞解釋】
- DBSCAN：密度式分群方法，可找到任意形狀群集並辨識雜訊點。
- Epsilon ε：判斷鄰近點的半徑範圍。
- MinPts：在 ε 半徑內形成核心點所需的最小點數。
- Core Point：鄰域內點數達到 MinPts 的核心點。
- Noise Point：不屬於任何群集的雜訊或離群點。
- K-means：需事先指定 K 個群集的分群方法，和 DBSCAN 不同。

【記憶】
DBSCAN 口訣：**「半徑 ε 看多近，MinPts 看夠不夠密」**。看到 DBSCAN 主要參數，就選 ε + MinPts。'''
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
