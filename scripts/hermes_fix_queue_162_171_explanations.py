#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
# 修正明顯選項污染
byid['official_115_1_subject3_41']['options']['D']='ToTensor() 應放在所有幾何變換之前才能保持座標對應正確'
explanations={
'official_114_2_subject3_26':'''【考點】
防止監督式學習過擬合的方法，以及哪些方法是降低模型複雜度或限制學習能力。正則化、Dropout、Early Stopping 都會限制模型過度記住訓練資料；擴增輸入特徵則可能提高模型表達能力，不屬於降低複雜度。

【正解】
D。擴增輸入特徵變數以提升模型表達能力。

【為什麼】
題目問「不屬於」降低複雜度或限制學習能力的作法。L1/L2 會懲罰權重，Dropout 會隨機關閉神經元，Early Stopping 會提早停止訓練，這些都能限制模型。相反地，增加輸入特徵可能提供更多訊號，但也可能讓模型更複雜、自由度更高，若特徵品質不佳反而增加過擬合風險。

【錯誤選項解析】
A：錯。L1/L2 正則化屬於限制模型權重與複雜度的作法。
B：錯。Dropout 是典型防止過擬合的正則化方法。
C：錯。Early Stopping 限制訓練時間，避免模型繼續貼合訓練資料。
D：對。增加特徵提升表達能力，不是降低複雜度或限制學習能力。

【名詞解釋】
- Overfitting：過擬合。
- L1/L2 Regularization：權重懲罰正則化。
- Dropout：訓練時隨機關閉神經元。
- Early Stopping：驗證表現不再改善時停止訓練。
- Model Complexity：模型複雜度。

【記憶】
過擬合題口訣：**「正則、Dropout、早停都在限制；增加特徵是在擴張能力」**。''',
'official_115_1_subject1_18':'''【考點】
多模態學習中的跨模態對齊（Cross-Modal Alignment）。CT 影像、電子病歷文字、基因序列屬於不同模態，資料表示方式差異很大，需要對齊到可共同理解的語意空間。

【正解】
D。將不同模態的資料表示對齊至共同語意空間，使模型能建立跨模態之間的語意關聯。

【為什麼】
跨模態對齊的目標，是讓不同來源但語意相關的資訊能被模型連起來。例如某 CT 影像病灶、病歷中的症狀描述、基因突變訊號，可能都指向同一疾病風險。若表示空間未對齊，模型難以理解這些資訊之間的關聯。對齊後可做融合、檢索、預測與互補推論。

【錯誤選項解析】
A：錯。跨模態對齊不是只聚焦 CT，也不是排除其他模態。
B：錯。它不等於自動生成配對標註；標註生成是另一個問題。
C：錯。降低儲存與計算成本不是 alignment 的主要目的。
D：對。共同語意空間與跨模態關聯是核心。

【名詞解釋】
- Cross-Modal Alignment：跨模態對齊。
- Multimodal Learning：多模態學習。
- Semantic Space：語意空間。
- Representation：資料表示。
- Fusion：融合多模態資訊。

【記憶】
跨模態對齊口訣：**「不同資料說同一件事，要先對齊到同一語意空間」**。''',
'official_114_2_subject3_8':'''【考點】
資訊增益（Information Gain）的主要應用。資訊增益常用於決策樹，在每次節點分裂時衡量某特徵能降低多少分類不確定性，進而選擇最佳分裂特徵。

【正解】
D。透過遞迴分裂方式建立分類規則的決策樹模型。

【為什麼】
決策樹會從根節點開始，反覆選擇能最好區分類別的特徵。資訊增益以熵（Entropy）為基礎，衡量分裂前後不確定性下降多少。下降越多，代表該特徵對分類越有幫助，因此適合作為分裂依據。ID3 等決策樹演算法就是典型例子。

【錯誤選項解析】
A：錯。L1 正則化線性模型也可做特徵選擇，但不是資訊增益的主要模型架構。
B：錯。深度神經網路通常透過梯度學習特徵，不以資訊增益遞迴分裂。
C：錯。核方法如 SVM 使用 kernel 映射，不是資訊增益核心應用。
D：對。資訊增益最常見於決策樹分裂。

【名詞解釋】
- Information Gain：資訊增益。
- Entropy：熵，不確定性的量度。
- Decision Tree：決策樹。
- Recursive Splitting：遞迴分裂。
- Feature Selection：特徵選擇。

【記憶】
資訊增益口訣：**「算分裂後不確定性少多少，決策樹選特徵用它」**。''',
'official_114_2_subject1_29':'''【考點】
持續整合（CI）的核心實踐。CI 強調開發者頻繁提交程式碼後，由系統自動建置、測試與檢查，越早發現整合問題，越能降低合併風險。

【正解】
B。每次程式碼提交後自動觸發建置、單元測試及靜態程式碼分析。

【為什麼】
CI 的重點是「自動化」與「頻繁整合」。每次 commit 或 pull request 都觸發 build、unit tests、lint/static analysis，可快速發現語法錯誤、測試失敗、相依性問題或品質問題。手動、定期、訓練完成後才合併都太晚，容易累積整合風險。

【錯誤選項解析】
A：錯。每日手動合併不符合 CI 的自動化與即時回饋精神。
B：對。提交後自動建置、測試、靜態分析，是 CI 核心。
C：錯。模型訓練完成後才回顧合併太晚，不是持續整合。
D：錯。自動部署偏 CD/部署流程，不是 CI 核心實踐。

【名詞解釋】
- CI：Continuous Integration，持續整合。
- Build：建置。
- Unit Test：單元測試。
- Static Analysis：靜態程式碼分析。
- Main Branch：主分支。

【記憶】
CI 口訣：**「每次提交，自動建置測試檢查」**。''',
'official_114_2_subject3_42':'''【考點】
VGG16 中參數量分布。VGG16 的全連接層（Linear/FC）參數量最多，尤其是 Flatten 後接大型 dense layer，會產生大量權重。

【正解】
B。全連接層（Linear）。

【為什麼】
前面曾遇到 VGG16 的 FLOPs 題，答案是卷積層；但本題問的是 parameter count。VGG16 的 FC 層如 25088×4096、4096×4096、4096×1000，參數量極大。卷積層雖然計算量高，但因權重共享，參數量通常少於大型全連接層總和。ReLU 與池化幾乎沒有可訓練參數。

【錯誤選項解析】
A：錯。卷積層 FLOPs 多，但 VGG16 參數量最多的是全連接層。
B：對。Linear/FC 層參數量最大。
C：錯。ReLU 沒有可訓練參數。
D：錯。池化層通常沒有可訓練參數。

【名詞解釋】
- Parameter Count：參數量。
- FLOPs：運算量。
- Linear/Fully Connected Layer：全連接層。
- Weight Sharing：權重共享。
- VGG16：經典 CNN 架構。

【記憶】
VGG16 雙題口訣：**「問 FLOPs 選 Conv；問參數量選 Linear」**。''',
'official_115_1_subject1_42':'''【考點】
MLOps 監控中的整體指標與分群監控。整體 RMSE 沒變，但高額理賠樣本僅 5% 且誤差上升，代表整體指標掩蓋了長尾/少數群體的問題，應做分群監控。

【正解】
D。僅監控整體 RMSE，未針對不同理賠金額區間進行分群監控。

【為什麼】
高額理賠案件比例小，整體 RMSE 可能被大量一般案件主導，因此少數高額區間惡化不一定使整體指標明顯變化。監控設計應依理賠金額區間、產品類別、地區、客群等重要 segment 做切片分析，才能及時發現局部表現退化。

【錯誤選項解析】
A：錯。即時串流不一定能解決分群被整體平均掩蓋的問題。
B：錯。長尾不是無法監控，而是需要針對長尾族群設計監控。
C：錯。MAE 也可能被整體樣本主導；核心問題是未分群監控。
D：對。只看整體 RMSE 會漏掉少數高額理賠區間惡化。

【名詞解釋】
- RMSE：均方根誤差。
- Segment Monitoring：分群/切片監控。
- Long-tail Distribution：長尾分布。
- Model Monitoring：模型監控。
- Slice Analysis：切片分析。

【記憶】
監控口訣：**「整體沒變，不代表每群都好；長尾問題要分群看」**。''',
'official_114_2_subject3_3':'''【考點】
非凸最佳化與局部最優解。非線性模型的目標函數若是 non-convex，可能有多個局部極小值、鞍點或平坦區，使最佳化結果受初始化與訓練路徑影響。

【正解】
C。局部最優解。

【為什麼】
凸函數理想情況下局部最小就是全域最小；但非凸函數可能有許多山谷。演算法如梯度下降可能停在某個局部最小點，而不是全域最佳點，導致不同初始化得到不同結果。這是深度學習與非線性模型最佳化常見議題。

【錯誤選項解析】
A：錯。梯度消失是深層網路反向傳播梯度變小，不是非凸多極值最直接描述。
B：錯。資料過少是資料量問題，不是非凸函數本身造成。
C：對。非凸目標函數最典型問題是局部最優或鞍點。
D：錯。過擬合是泛化問題，不是多個極值點的直接答案。

【名詞解釋】
- Non-convex Function：非凸函數。
- Local Optimum：局部最優。
- Global Optimum：全域最優。
- Gradient Descent：梯度下降。
- Saddle Point：鞍點。

【記憶】
非凸口訣：**「山谷很多，容易卡在局部最優」**。''',
'official_115_1_subject1_49':'''【考點】
線上持續監控與離線實驗追蹤的差異。線上監控關注部署後服務健康、資料漂移、預測分布與回饋品質；訓練過程中每個 epoch 的學習率與超參數軌跡屬於離線實驗管理。

【正解】
A。訓練實驗中每個 Epoch 的學習率變化曲線與超參數設定軌跡。

【為什麼】
Continuous Monitoring 是模型上線後持續觀察推論 API 延遲、RPS、錯誤率、輸入特徵分布、預測分布、資料漂移與回收標籤表現。學習率曲線與 hyperparameter 設定則是在訓練/實驗階段產生，應由 MLflow、W&B 或實驗追蹤系統管理，不適合放在線上即時監控儀表板當核心指標。

【錯誤選項解析】
A：對本題而言最不適合線上監控，應由離線實驗追蹤管理。
B：錯。API P50/P95/P99 延遲與 RPS 是典型線上服務監控。
C：錯。PSI 可用於偵測線上資料漂移，屬於持續監控。
D：錯。預測分布與回收標籤對比可監控模型表現與漂移。

【名詞解釋】
- Continuous Monitoring：線上持續監控。
- Experiment Tracking：實驗追蹤。
- PSI：Population Stability Index。
- RPS：每秒請求數。
- Hyperparameter：超參數。

【記憶】
監控分類口訣：**「上線後看延遲漂移預測；訓練時看 LR 和超參數」**。''',
'official_115_1_subject3_41':'''【考點】
OCR 資料增強與語意保持。手寫字母 b/d/p/q 對左右或上下方向非常敏感，RandomHorizontalFlip 會改變字母語意，造成標籤錯誤或資料污染。

【正解】
B。RandomHorizontalFlip 破壞字母方向語義，使模型以 50% 機率學到鏡像錯誤標籤。

【為什麼】
資料增強必須保持標籤語意不變。對一般自然影像，水平翻轉常合理；但 OCR 字母辨識中，b 翻轉可能像 d，p/q 也可能混淆。若套用 RandomHorizontalFlip 且標籤不變，模型會看見與標籤不一致的樣本，導致部署時 b/d/p/q 錯誤率高。題目原 D 選項混入下一題題幹，已修回乾淨選項。

【錯誤選項解析】
A：錯。15 度旋轉可能影響字形，但本題 b/d/p/q 異常更直接指向水平翻轉。
B：對。水平翻轉會破壞方向性字母的語意。
C：錯。灰階變化通常不會把 b 變 d，不是最可能根因。
D：錯。ToTensor 放置順序不是造成鏡像錯誤標籤的核心。

【名詞解釋】
- Data Augmentation：資料增強。
- RandomHorizontalFlip：隨機水平翻轉。
- OCR：光學字元辨識。
- Label-preserving Transform：不改變標籤語意的轉換。
- Semantic Invariance：語意不變性。

【記憶】
OCR 增強口訣：**「增強不能改標籤；b/d/p/q 不可亂翻轉」**。''',
'official_114_2_subject1_44':'''【考點】
同時滿足預測與資料生成的模型選擇。若要預測顧客流失，又要模擬促銷策略下行為變化、生成多樣化虛擬樣本，可考慮生成模型如 VAE 或 GAN。

【正解】
C。使用變分自編碼器（VAE）或生成對抗網路（GAN）。

【為什麼】
Random Forest 與 Logistic Regression 可做預測，但不擅長生成多樣化樣本。VAE 可學習潛在空間並生成類似訓練分布的新樣本；GAN 可透過生成器與判別器學習資料分布，產生逼真的合成樣本。若電商想模擬不同策略下的顧客行為資料，用生成模型更符合「預測 + 資料生成」需求。

【錯誤選項解析】
A：錯。隨機森林適合分類/迴歸，不是主要生成模型。
B：錯。邏輯迴歸可預測流失機率，但無法生成多樣化虛擬樣本。
C：對。VAE/GAN 是典型生成模型，能產生合成樣本。
D：錯。強化學習適合策略互動與序列決策，但題目重點是資料生成與預測兼顧。

【名詞解釋】
- VAE：Variational Autoencoder，變分自編碼器。
- GAN：Generative Adversarial Network，生成對抗網路。
- Synthetic Data：合成資料。
- Churn Prediction：流失預測。
- Latent Space：潛在空間。

【記憶】
生成需求口訣：**「只預測可用分類器；要生虛擬樣本，想到 VAE/GAN」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
