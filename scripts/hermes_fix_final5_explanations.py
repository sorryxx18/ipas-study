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
'official_114_2_subject3_44': '''【考點】
VGG16 架構與參數量判讀。題目要求根據 VGG16 的層級摘要判斷正確敘述，重點是 VGG16 的經典結構：13 層卷積層與 3 層全連接層，總參數約 138M。

【正解】
D。VGG16 包含 13 層卷積層（conv）與 3 層全連接層（FC），總參數數目約為 138,357,544（約 138.36M）。

【為什麼】
VGG16 的「16」指有權重的 16 層，包含 13 個 convolution layers 與 3 個 fully connected layers。題目附表列出的 Total params 為 138,357,544，與經典 VGG16 參數量一致。VGG16 參數量主要集中在後段全連接層，尤其第一個 Linear 層。

【錯誤選項解析】
A：錯。雖然前一個 MaxPool 輸出可能是 512×4×4，但後面有 AdaptiveAvgPool2d 輸出 512×7×7，再攤平給 Linear-33，因此輸入維度不是 512×4×4=8192，而是 512×7×7=25088。
B：錯。Linear 層參數量通常包含權重與 bias。Linear-33 的參數 102,764,544 = 25088×4096 + 4096，已包含 bias。
C：錯。Estimated Total Size 通常只是模型摘要中的估算，不完整代表訓練所需全部 GPU 記憶體；訓練還需要梯度、optimizer state、batch activation 等，一張 1GB GPU 不足以訓練 VGG16。
D：對。VGG16 經典架構就是 13 conv + 3 FC，總參數約 138.36M。

【名詞解釋】
- VGG16：Visual Geometry Group 提出的經典 CNN，共 16 個有權重層。
- Conv Layer：卷積層，用於擷取局部影像特徵。
- Fully Connected Layer：全連接層，通常位於分類器後段。
- AdaptiveAvgPool2d：將特徵圖調整到固定空間尺寸的池化層。
- Parameters：模型需要學習的權重與偏差。

【記憶】
VGG16 口訣：**「13 卷積 + 3 全連接 = 16 層有權重」**。看到 138M 參數與 VGG16 結構，選 13 conv / 3 FC。''',

'official_114_2_subject3_23': '''【考點】
蒙地卡羅方法（Monte Carlo Method）的應用情境。題目關鍵字是「高度隨機性」、「隨機抽樣」、「模擬多種可能情境」、「估算機率分佈與風險區間」。

【正解】
A。蒙地卡羅方法（Monte Carlo Method）。

【為什麼】
Monte Carlo 方法透過大量隨機抽樣與模擬，估計不確定系統的可能結果分布。太陽能發電量受到日照、雲量、溫度等隨機因素影響，若要預測未來三個月的波動範圍與風險區間，可以反覆抽樣不同氣候條件並模擬發電結果，得到機率分布、信賴區間或風險範圍。

【錯誤選項解析】
A：對。Monte Carlo 正是用隨機抽樣模擬多種情境，以估計分布與風險。
B：錯。K-means 是非監督式分群方法，用於把資料分成 K 群，不是用來隨機模擬機率分布。
C：錯。SVR 是監督式回歸模型，可做預測，但題目強調隨機抽樣與估算機率分布，較符合 Monte Carlo。
D：錯。特徵選取是挑選重要變數的前處理方法，不是模擬未來情境與風險區間的方法。

【名詞解釋】
- Monte Carlo Method：用大量隨機抽樣估計複雜系統結果的方法。
- Probability Distribution：描述不同結果發生機率的分布。
- Risk Interval：可能結果的風險區間或不確定範圍。
- K-means：指定 K 個群集的分群演算法。
- SVR：Support Vector Regression，支援向量迴歸。

【記憶】
Monte Carlo 口訣：**「不確定很多，就抽樣模擬很多次」**。看到隨機抽樣、多情境、機率分布、風險區間，選 Monte Carlo。''',

'official_115_1_subject1_25': '''【考點】
NIST AI RMF 中可驗證性（Verifiability）與可重現評估。題目問如何讓第三方稽核人員能獨立重現模型評估結果，重點是測試資料、評估流程、模型版本與設定要可追溯。

【正解】
B。建立可追溯的測試資料與評估流程，並記錄模型訓練與評估過程中的關鍵設定，以確保結果可被重現。

【為什麼】
可驗證性不是單純追求高準確率，而是讓外部人員能檢查、重現與確認模型評估結果。實務上需保存測試資料版本、資料切分方式、模型版本、超參數、隨機種子、評估指標、程式碼版本與執行環境。這些紀錄能讓第三方稽核人員獨立重跑或檢查評估流程。

【錯誤選項解析】
A：錯。99% 準確率不代表可驗證；若資料、流程與設定不可追溯，外部仍無法重現結果。
B：對。可追溯資料與評估流程、記錄關鍵設定，最直接符合可驗證性。
C：錯。加快迭代速度可能提升開發效率，但不代表評估結果可被第三方重現。
D：錯。增加訓練資料量可能改善泛化，但不是可驗證性的核心；沒有紀錄流程仍無法稽核。

【名詞解釋】
- NIST AI RMF：美國 NIST 提出的 AI 風險管理框架。
- Verifiability：可驗證性，指系統結果與流程可被檢查、確認或重現。
- Reproducibility：可重現性，在相同資料、程式與設定下能得到一致結果。
- Audit Trail：稽核軌跡，記錄資料、模型、流程與決策歷程。
- Evaluation Pipeline：模型評估流程，包含測試資料、指標、程式與設定。

【記憶】
可驗證性口訣：**「不是分數高，是別人能重跑」**。看到第三方稽核、重現評估，選可追溯資料與流程紀錄。''',

'official_115_1_subject1_10': '''【考點】
物件偵測架構比較：YOLO 是單階段偵測，Faster R-CNN 是兩階段偵測。題目場景是即時影像瑕疵偵測，因此常考速度與流程差異。

【正解】
A。YOLO 採用單階段偵測，直接從整張影像預測物件位置與類別；Faster R-CNN 則先產生候選區域再進行分類。

【為什麼】
YOLO（You Only Look Once）屬於 one-stage detector，直接在一次前向傳播中預測 bounding box 與類別，因此速度快，適合即時影像流。Faster R-CNN 屬於 two-stage detector，先透過 Region Proposal Network 產生候選區域，再對候選區域分類與修正位置，通常較精準但速度較慢。

【錯誤選項解析】
A：對。完整描述 YOLO 單階段與 Faster R-CNN 兩階段的核心差異。
B：錯。YOLO 不是兩階段流程；它是單階段偵測器。
C：錯。YOLO 的特色不是增加候選區域數量，而是直接從整張影像預測位置與類別。
D：錯。Faster R-CNN 不是單階段偵測，它先產生候選區域再分類。

【名詞解釋】
- Object Detection：物件偵測，同時找出物件位置與類別。
- YOLO：單階段物件偵測模型，速度快，常用於即時偵測。
- Faster R-CNN：兩階段物件偵測模型，先產生候選區域再分類。
- Bounding Box：框出物件位置的矩形框。
- Region Proposal Network：Faster R-CNN 中產生候選區域的網路。

【記憶】
偵測模型口訣：**「YOLO 一眼看完，R-CNN 先框再判」**。即時速度常選 YOLO；兩階段精細偵測常想到 Faster R-CNN。''',

'official_115_1_subject3_16': '''【考點】
XGBoost 目標函數中的正則化設計。題目問 XGBoost 相較傳統 GBDT，哪個核心設計讓它更能防過擬合，答案是加入樹複雜度懲罰與葉節點權重正則化。

【正解】
A。加入樹的複雜度懲罰項（包含深度、葉節點數量與葉節點權重的 L2 正則化）。

【為什麼】
XGBoost 的目標函數不只包含訓練損失，也加入正則化項來控制模型複雜度。正則化項會懲罰樹的葉節點數量與葉節點權重大小，避免模型長出過於複雜的樹或對訓練資料擬合過度。這是 XGBoost 相較傳統 GBDT 更重視泛化與防過擬合的重要特色。

【錯誤選項解析】
A：對。樹複雜度懲罰與葉節點權重正則化是 XGBoost 目標函數的重要設計。
B：錯。學習率衰減可作為訓練策略，但不是題目所問 XGBoost 目標函數中的核心正則化設計。
C：錯。卷積運算屬於 CNN 影像模型，與 XGBoost 樹模型無關。
D：錯。強制所有樹深度為 1 是 decision stump 的限制，不是 XGBoost 的一般核心設計；XGBoost 可設定樹深，但不是全部固定為 1。

【名詞解釋】
- XGBoost：高效梯度提升樹模型，加入正則化、缺失值處理與高效計算。
- Objective Function：訓練時要最小化的目標函數，通常包含損失與正則化。
- Regularization：限制模型複雜度以降低過擬合。
- Leaf Weight：樹模型葉節點的輸出權重。
- GBDT：Gradient Boosting Decision Tree，逐步建立樹修正前一輪錯誤。

【記憶】
XGBoost 防過擬合口訣：**「損失之外，加樹的複雜度懲罰」**。看到目標函數與防過擬合，選正則化項。'''
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
