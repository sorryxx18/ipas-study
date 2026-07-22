#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'S1_04':'''【考點】
GAN（Generative Adversarial Network，生成對抗網路）的基本組成。GAN 由生成器與判別器兩個模型互相對抗訓練，生成器負責製造假資料，判別器負責分辨真假。

【正解】
B。生成器 + 判別器。

【為什麼】
GAN 的核心是 adversarial training。Generator 嘗試產生越來越像真實資料的樣本；Discriminator 則學習分辨輸入是真實資料還是生成資料。兩者在對抗中共同進步，最後生成器能產生逼真的影像、文字或其他資料樣本。

【錯誤選項解析】
A：錯。編碼器 + 解碼器較常見於 Autoencoder 或 Seq2Seq，不是 GAN 的核心兩部分。
B：對。GAN 由 Generator 與 Discriminator 組成。
C：錯。訓練器 + 測試器不是模型架構組成。
D：錯。分類器 + 迴歸器是監督式任務模型類型，不是 GAN 架構。

【名詞解釋】
- Generator：生成器，從隨機噪音或條件輸入產生假資料。
- Discriminator：判別器，判斷資料是真實或生成。
- Adversarial Training：生成器與判別器互相競爭的訓練方式。
- Latent Vector：生成器常用的隱含空間輸入。
- Generative Model：能產生新資料的模型。

【記憶】
GAN 口訣：**「一個造假，一個抓假」**。造假的是 Generator，抓假的是 Discriminator。''',
'S1_07':'''【考點】
CNN 池化層（Pooling Layer）的功能。池化層主要用來降低特徵圖空間尺寸、減少計算量，並保留局部區域的重要特徵摘要。

【正解】
B。降低特徵圖維度、減少計算量並提取主要特徵。

【為什麼】
Pooling 常見形式有 Max Pooling 與 Average Pooling。它會在局部區域取最大值或平均值，使特徵圖寬高縮小，降低後續層的輸入量與運算成本。Max Pooling 也能保留最強反應特徵，讓模型對小幅位置偏移更具魯棒性。

【錯誤選項解析】
A：錯。Pooling 通常降低解析度，不是增加解析度。
B：對。這正是池化層最主要功能。
C：錯。將圖像轉換為文字屬於影像字幕或 OCR 之類任務，不是 pooling。
D：錯。計算損失函數是訓練目標的一部分，不是 CNN pooling 層工作。

【名詞解釋】
- Pooling Layer：縮小特徵圖尺寸的層。
- Max Pooling：取局部區域最大值。
- Average Pooling：取局部區域平均值。
- Feature Map：卷積層輸出的特徵圖。
- Robustness：模型對小變化仍能維持穩定判斷的能力。

【記憶】
Pooling 口訣：**「縮圖、降算量、留重點」**。看到降低特徵圖維度與計算量，就選 pooling。''',
'official_114_2_subject3_7':'''【考點】
LSTM 適用於序列資料與時間序列預測。題目問最適合採用 LSTM 的應用，重點是資料是否有時間順序與長期依賴。

【正解】
A。預測未來七天的電力需求變化趨勢。

【為什麼】
LSTM 是 RNN 的改良模型，擅長處理序列資料，例如時間序列、語音、文字與感測器序列。電力需求會受時間、週期、天氣與歷史用電行為影響，屬於典型時間序列預測任務。LSTM 可利用過去多個時間點資訊預測未來趨勢。

【錯誤選項解析】
A：對。未來七天電力需求預測是時間序列問題，適合 LSTM。
B：錯。影像物件辨識通常使用 CNN、YOLO、Faster R-CNN 等電腦視覺模型。
C：錯。顧客分群屬於非監督式學習，常用 K-means、DBSCAN 等。
D：錯。高維資料壓縮常用 PCA、Autoencoder 等降維方法。

【名詞解釋】
- LSTM：長短期記憶網路，適合序列資料。
- Time Series Forecasting：利用歷史時間資料預測未來。
- RNN：循環神經網路，按序列順序處理資料。
- Long-term Dependency：長距離依賴，早期資訊影響後續預測。
- Demand Forecasting：需求預測，例如用電量或銷售量預測。

【記憶】
LSTM 口訣：**「有時間順序、有過去影響未來，就想 LSTM」**。影像找 CNN，分群找 K-means/DBSCAN。''',
'S1_02':'''【考點】
即時物件偵測模型選擇。題目問最適合即時物件偵測的技術，YOLO 是經典 one-stage detector，速度快，適合即時場景。

【正解】
C。YOLO。

【為什麼】
YOLO 是 You Only Look Once，能在一次前向傳播中同時預測物件位置與類別，因此常用於即時影像偵測，例如監控、車載視覺、產線瑕疵偵測。相較兩階段偵測器，YOLO 更重視速度與即時性。

【錯誤選項解析】
A：錯。BERT 是自然語言處理模型，不是物件偵測模型。
B：錯。LSTM 適合序列/時間資料，不是影像中物件定位。
C：對。YOLO 專為快速物件偵測設計。
D：錯。PCA 是降維方法，不會直接做物件偵測。

【名詞解釋】
- YOLO：單階段即時物件偵測模型。
- Object Detection：找出影像中物件位置與類別。
- Bounding Box：包住物件位置的矩形框。
- BERT：NLP 語意理解模型。
- PCA：主成分分析，用於降維。

【記憶】
模型選擇口訣：**「即時物件偵測找 YOLO」**。文字理解看 BERT，時間序列看 LSTM，降維看 PCA。''',
'official_115_1_subject3_26':'''【考點】
時間序列特徵工程中的滑動窗口（Sliding Window）與滯後特徵（Lag Features）。題目說把過去多個時間點觀測值組成模型輸入，目的就是讓模型使用歷史資訊預測當前或未來。

【正解】
D。建立滯後特徵。

【為什麼】
時間序列資料中，過去值常對未來有預測力。Sliding Window 會把 t-1、t-2、t-3 等過去時間點的觀測值整理成特徵欄位，讓一般機器學習模型也能學到時間依賴。例如用過去 7 天銷售量預測明天銷售量，就是典型滑動窗口。

【錯誤選項解析】
A：錯。滑動窗口可增加訓練樣本形式，但主要目的不是資料增強，而是建立歷史依賴特徵。
B：錯。去除雜訊通常用平滑、濾波等方法，不是 sliding window 的主要定義。
C：錯。滑動窗口通常會增加輸入特徵數，不是降低維度。
D：對。把過去時間點變成 lag features，是 sliding window 核心目的。

【名詞解釋】
- Sliding Window：用固定長度窗口在時間序列上移動，建立樣本。
- Lag Feature：過去時間點的觀測值作為特徵。
- Time Series：依時間順序排列的資料。
- Forecasting：預測未來值。
- Window Size：窗口包含多少個過去時間點。

【記憶】
時間序列口訣：**「過去幾步當特徵，就是 lag；窗口往前滑，就是 sliding window」**。''',
'S1_29':'''【考點】
A/B 測試在 AI 系統上線驗證中的用途。A/B 測試用真實流量比較兩個版本，常用來量化新舊模型對業務指標的差異。

【正解】
B。比較新舊模型版本的實際效益差異。

【為什麼】
A/B 測試會將使用者隨機分成 A 組與 B 組，例如 A 組用舊模型、B 組用新模型，再比較 CTR、CVR、留存率、滿意度等真實指標。它能避免只依離線測試指標判斷，因為線上使用者行為可能與離線資料不同。

【錯誤選項解析】
A：錯。伺服器硬體效能通常用壓力測試或負載測試，不是 A/B 測試主要用途。
B：對。A/B 測試就是比較不同版本在真實環境的效果。
C：錯。語法錯誤靠編譯、測試或 lint 工具檢查。
D：錯。生成訓練資料是資料增強或生成模型任務，不是 A/B 測試。

【名詞解釋】
- A/B Test：將流量分成不同組別比較版本效果。
- Control Group：控制組，通常使用舊版本。
- Treatment Group：實驗組，使用新版本。
- CTR：點擊率，常見線上指標。
- Statistical Significance：統計顯著性，用於判斷差異是否可靠。

【記憶】
A/B 測試口訣：**「新舊版本分流量，看真實指標誰比較好」**。不是測硬體，也不是測語法。''',
'official_114_2_subject3_13':'''【考點】
標籤偏差（Label Bias）的來源。題目問 Label Bias 通常因何造成，核心是標註資料本身含有主觀偏見、歷史偏見或標註規則偏差。

【正解】
B。標記資料本身帶有主觀偏見。

【為什麼】
模型是從標註資料學習，如果標註者本身帶有偏見、標註準則不一致、歷史決策不公平，模型就會學到這些偏差。例如招募資料中過去對某群體評分較低，模型可能延續這種偏見。Label Bias 不是資料量大或特徵多本身造成，而是標籤品質與標註過程的偏差。

【錯誤選項解析】
A：錯。資料量大不必然造成標籤偏差；大量偏差標籤反而會放大問題。
B：對。標記資料本身帶有主觀偏見，是 Label Bias 的典型原因。
C：錯。模型結構不當可能影響效能，但不是標籤偏差的主要定義。
D：錯。特徵數量過多可能造成過擬合或噪音，不等同標籤偏差。

【名詞解釋】
- Label Bias：標籤本身或標註過程造成的偏差。
- Annotation：人工或系統給資料加標籤的過程。
- Historical Bias：歷史資料中已存在的不公平或偏見。
- Fairness：AI 對不同群體是否產生公平結果。
- Data Quality：資料正確性、一致性與代表性。

【記憶】
Label Bias 口訣：**「標籤怎麼偏，模型就怎麼學」**。看到標註者主觀、歷史偏見，就選標籤偏差。''',
'S3_03':'''【考點】
ReLU 激活函數的優點。ReLU 的數學式是 f(x)=max(0,x)，計算簡單，且正數區梯度為 1，有助於緩解深層網路中的梯度消失。

【正解】
B。計算簡單且有效緩解梯度消失問題。

【為什麼】
Sigmoid 或 tanh 在輸入很大或很小時容易飽和，梯度接近 0，深層網路訓練會變慢。ReLU 在 x>0 時梯度固定為 1，計算也只需取 max，因此訓練速度快、效果穩定，是 CNN 與 DNN 隱藏層常用激活函數。

【錯誤選項解析】
A：錯。輸出 0 到 1 是 sigmoid 的特性，不是 ReLU；ReLU 正值可大於 1。
B：對。ReLU 計算簡單，並能緩解梯度消失。
C：錯。輸出機率分布通常用 softmax，不是 ReLU。
D：錯。ReLU 對負值輸入輸出 0，並非特別「處理負值」的優勢。

【名詞解釋】
- ReLU：Rectified Linear Unit，f(x)=max(0,x)。
- Activation Function：提供非線性能力的函數。
- Vanishing Gradient：梯度太小導致深層模型難以學習。
- Sigmoid：輸出 0 到 1，常用於二元分類輸出。
- Softmax：多類別分類常用輸出函數。

【記憶】
ReLU 口訣：**「正的照過，負的歸零」**。問隱藏層常用、計算快、緩解梯度消失，選 ReLU。''',
'official_114_2_subject3_14':'''【考點】
AI 可解釋性（Explainability）在高風險場景的重要性。題目問哪種應用最需要可解釋性，醫療診斷因牽涉生命安全、臨床責任與醫師信任，最關鍵。

【正解】
C。醫院導入 AI 模型分析病患影像並給出腫瘤惡性可能性，作為臨床醫師診斷依據。

【為什麼】
醫療 AI 的結果會影響診斷、治療與病患安全。臨床醫師需要理解模型依據，例如影像哪些區域支持判斷、模型信心與限制，才能負責任地採納建議。可解釋性也有助於稽核、法規合規與錯誤追蹤。

【錯誤選項解析】
A：錯。電商推播也可受益於解釋，但通常風險低於醫療診斷。
B：錯。廣告出價可解釋性有商業價值，但不是生命安全等高風險決策。
C：對。醫療影像輔助診斷是高風險、高責任場景，可解釋性最關鍵。
D：錯。銀行客戶流失預測涉及商業決策，可解釋性重要，但題目選項中醫療診斷更關鍵。

【名詞解釋】
- Explainability：讓人理解模型判斷依據的能力。
- High-stakes Decision：高風險決策，例如醫療、司法、金融授信。
- Clinical Decision Support：臨床決策輔助系統。
- Saliency Map：顯示影像中哪些區域影響模型判斷。
- Accountability：系統決策可被追責與審查。

【記憶】
可解釋性口訣：**「風險越高，越要能說明為什麼」**。醫療診斷、金融授信、司法決策都要特別重視。''',
'official_115_1_subject1_37':'''【考點】
類別不平衡（Class Imbalance）的資料前處理解法。題目限制不改模型架構與演算法，只透過資料前處理改善少數類別辨識，因此最適合使用 SMOTE 等少數類別過採樣。

【正解】
A。使用 SMOTE 等過採樣方法進行少數類別擴增。

【為什麼】
良品 99%、瑕疵品 1% 時，模型若追求整體 accuracy，可能幾乎都預測良品，卻抓不到真正重要的瑕疵品。SMOTE 會根據少數類別樣本在特徵空間中合成新樣本，增加少數類別比例，使模型有更多機會學到瑕疵特徵。這屬於資料層面的處理，符合題目限制。

【錯誤選項解析】
A：對。SMOTE/過採樣能增加少數類別樣本，是資料前處理解法。
B：錯。L1/L2 是模型正則化，不是僅透過資料前處理，也不是直接解決類別不平衡。
C：錯。增加網路層數是改模型架構，且可能加劇過擬合。
D：錯。複製更多良品會讓不平衡更嚴重，accuracy 可能更高但瑕疵辨識更差。

【名詞解釋】
- Class Imbalance：不同類別樣本數差距很大。
- SMOTE：Synthetic Minority Over-sampling Technique，合成少數類別樣本。
- Oversampling：增加少數類別樣本比例。
- Accuracy：整體正確率，在不平衡資料中可能誤導。
- Recall：少數類別偵測常重視的召回率。

【記憶】
不平衡口訣：**「少數太少，就補少數；不要再補多數」**。題目說只做資料前處理，選 SMOTE/過採樣。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
