#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_114_2_subject1_45':'''【考點】
PCA 降維後接 SVM 的合理性。PCA 可把高維特徵投影到少數主成分，降低計算成本與噪音，可能減少過擬合風險，但不保證分類準確率一定提升。

【正解】
D。降維後可降低訓練時間並減少過擬合風險。

【為什麼】
影像特徵從 1024 維降到 100 維，可減少 SVM 訓練時的特徵數量，降低運算成本。若原始特徵中有大量冗餘或噪音，PCA 保留主要變異方向也可能改善泛化。不過 PCA 是無監督降維，只看變異量，不直接看分類標籤，因此不保證準確率一定提高。

【錯誤選項解析】
A：錯。PCA 保留高變異主成分，但高變異不一定最有分類力，不能說必然提升準確率。
B：錯。原始高維資料保留資訊較多，但高維也可能帶來計算成本與過擬合，PCA 有實際意義。
C：錯。PCA 不會讓 SVM 自動處理非線性；非線性通常靠 kernel SVM。
D：對。降維能降低訓練時間，並可能減少過擬合風險。

【名詞解釋】
- PCA：主成分分析，保留最大變異方向的降維方法。
- SVM：支持向量機，可做分類或迴歸。
- Dimensionality Reduction：降維，減少特徵數。
- Overfitting：過度貼合訓練資料，泛化差。
- Kernel SVM：使用核函數處理非線性資料的 SVM。

【記憶】
PCA + SVM 口訣：**「降維省時間、降噪防過擬合；不保證一定變準」**。''',
'S1_21':'''【考點】
模型部署時 API 的用途。API 讓模型以標準介面提供服務，使不同平台、不同語言或不同系統能呼叫模型推論功能。

【正解】
B。實現跨平台、跨語言的系統整合。

【為什麼】
模型部署成 API 後，前端網站、手機 App、後端系統或其他服務都能透過 HTTP/REST/gRPC 等方式送資料並取得預測結果。呼叫端不需要知道模型內部用 Python、PyTorch 或其他框架實作，只要遵守輸入輸出格式即可整合。

【錯誤選項解析】
A：錯。API 主要提供服務呼叫，不會自動訓練模型。
B：對。跨平台、跨語言整合是 API 部署的主要優點。
C：錯。API 通常仍需要伺服器、容器、雲端或邊緣設備承載。
D：錯。自動生成訓練資料不是 API 的功能。

【名詞解釋】
- API：應用程式介面，讓不同系統互相呼叫。
- REST API：常見 HTTP 介面風格。
- Inference：模型推論。
- Deployment：模型部署到可被使用的環境。
- JSON：API 常見資料交換格式。

【記憶】
API 口訣：**「模型包成服務，別的系統都能叫」**。''',
'official_115_1_subject1_29':'''【考點】
CNN 醫療影像可解釋方法選擇。題目要求近即時、不可大量採樣、以影像像素區域視覺化原因呈現，最適合 Grad-CAM。

【正解】
C。使用 Grad-CAM，透過梯度反向傳播生成類別關注區域。

【為什麼】
Grad-CAM 利用目標類別對卷積層特徵圖的梯度，產生熱力圖，顯示模型判斷時關注的影像區域。它適合 CNN 影像模型，通常比 LIME 或 Kernel SHAP 的大量擾動/採樣更快，能滿足近即時解釋需求。醫師可透過熱區判斷模型是否關注合理病灶區。

【錯誤選項解析】
A：錯。LIME 需要大量超像素擾動取樣，較難滿足 200ms 近即時限制。
B：錯。SHAP KernelExplainer 通常計算成本高，像素級 Shapley 值更不適合即時。
C：對。Grad-CAM 是 CNN 影像分類常用快速視覺化解釋方法。
D：錯。TreeExplainer 適用樹模型，不是 CNN 影像模型。

【名詞解釋】
- Grad-CAM：以梯度產生類別激活熱圖的 CNN 解釋方法。
- LIME：以局部擾動樣本近似模型行為的解釋方法。
- SHAP：基於 Shapley value 的特徵貢獻方法。
- Heatmap：熱力圖，顯示重要區域。
- CNN：卷積神經網路，常用於影像任務。

【記憶】
影像 CNN 解釋口訣：**「要快、要熱圖、要看病灶，選 Grad-CAM」**。''',
'S3_16':'''【考點】
AI 偏見（Bias）的常見來源。偏見最常來自訓練資料本身，例如歷史歧視、樣本不均衡、標籤偏差或收集方式不具代表性。

【正解】
B。訓練資料本身存在歷史偏差或樣本不均衡。

【為什麼】
模型會學習資料中的模式。如果過去資料中某些族群被低估、標籤標註不公平，或某些族群樣本太少，模型就可能延續甚至放大偏差。模型架構、學習率也會影響性能，但 AI 倫理中的偏見問題最常指資料與標籤中的社會/歷史偏差。

【錯誤選項解析】
A：錯。模型架構錯誤可能造成效能差，但不是 bias 最常見來源。
B：對。歷史偏差與樣本不均衡是常見偏見來源。
C：錯。資料多不必然造成偏見；偏見資料很多反而會放大問題。
D：錯。學習率過高會影響訓練穩定，不是偏見主要來源。

【名詞解釋】
- Bias：資料或模型造成的系統性偏差。
- Historical Bias：歷史決策或社會結構留下的偏差。
- Sampling Bias：樣本收集不具代表性。
- Label Bias：標籤本身帶有偏見。
- Fairness：模型對不同群體是否公平。

【記憶】
Bias 口訣：**「資料怎麼偏，模型就怎麼偏」**。''',
'S3_30':'''【考點】
機器學習模型選擇原則。選模型應依資料型態、任務性質、資料量、可解釋性、延遲與部署限制，而不是追逐名稱或新穎度。

【正解】
B。資料類型、任務性質（分類/迴歸/聚類）及資料量。

【為什麼】
分類、迴歸、分群、時間序列、影像、文字等任務適合的模型不同。資料量少時可能偏好簡單模型或遷移學習；資料量大且非線性複雜時可考慮樹模型或深度學習。模型選擇要服務問題，而不是只看名稱是否高科技、是否最新或工具是否免費。

【錯誤選項解析】
A：錯。模型名稱聽起來高科技不代表適合問題。
B：對。資料型態、任務性質與資料量是最基本考量。
C：錯。最新模型不一定最穩定、最可解釋或最適合資料。
D：錯。工具成本是工程考量，但不是模型選擇的核心因素。

【名詞解釋】
- Classification：分類，預測離散類別。
- Regression：迴歸，預測連續數值。
- Clustering：分群，無監督找群組。
- Data Type：資料型態，如表格、影像、文字、時序。
- Model Selection：根據需求選擇模型。

【記憶】
選模型口訣：**「先看資料，再看任務，最後看限制」**。''',
'official_115_1_subject1_40':'''【考點】
邊緣推論延遲優化。題目限制不更換硬體，且要降低推論延遲並維持合理準確率，最適合模型量化與推論加速。

【正解】
D。將模型由 FP32 量化為 INT8，並進行推論加速優化。

【為什麼】
INT8 量化可把模型權重與運算從 32-bit 浮點降低到 8-bit 整數，減少記憶體頻寬與計算成本，常能顯著降低邊緣裝置推論延遲。配合 TensorRT、OpenVINO、ONNX Runtime 等加速工具，可在準確率小幅犧牲下達成即時需求。

【錯誤選項解析】
A：錯。減少訓練資料不一定讓推論更快，且可能降低準確率。
B：錯。批次推論提高吞吐量，但即時單張延遲可能變差，不適合低於 200ms 要求。
C：錯。模型集成通常增加計算成本與延遲。
D：對。量化與推論加速是邊緣即時推論常用手段。

【名詞解釋】
- Quantization：量化，降低數值精度以加速推論。
- FP32：32 位元浮點數。
- INT8：8 位元整數。
- Edge Device：靠近資料來源的邊緣設備。
- Inference Latency：單次推論延遲。

【記憶】
邊緣加速口訣：**「不換硬體要變快，先想量化 INT8」**。''',
'official_115_1_subject1_41':'''【考點】
GPU 推論服務效能瓶頸分析。GPU 使用率只有 60%、kernel 間有閒置、小批次推論且尖峰延遲波動，最可能是排程與批次大小不當導致 GPU 未被充分利用。

【正解】
A。GPU 排程策略與批次大小設定不當，導致 GPU 運算單元未被有效利用。

【為什麼】
GPU 擅長大量平行運算。若多租戶服務多以小批次零散送入，kernel 啟動間隔與排程等待會造成 GPU 空轉；尖峰時又可能因批次聚合不足、請求排隊策略不佳，導致延遲抖動。題目已排除 CPU、記憶體、硬體、網路與併發控制異常，因此 A 最符合觀察。

【錯誤選項解析】
A：對。小批次與 kernel 閒置顯示 GPU 利用不佳，需改善 batching/scheduling。
B：錯。題目已排除請求併發控制異常。
C：錯。GPU 使用率僅 60%，不支持硬體效能已滿載不足。
D：錯。未量化可能影響成本，但題目特徵更指向排程與批次設定問題。

【名詞解釋】
- GPU Kernel：GPU 上執行的運算任務。
- Dynamic Batching：動態批次，把請求合併提高利用率。
- Scheduling：排程，決定工作何時送到 GPU。
- Latency Jitter：延遲波動。
- Throughput：單位時間處理量。

【記憶】
GPU 推論口訣：**「利用率低又有空檔，先查 batch 與排程」**。''',
'official_114_2_subject1_20':'''【考點】
GAN 模式崩潰（Mode Collapse）與 WGAN。模式崩潰是生成器只產生少數類型樣本，缺乏多樣性；WGAN 使用 Wasserstein 距離改善訓練穩定性，是常見解法。

【正解】
B。採用 Wasserstein 距離（WGAN 損失）替代原始 GAN 損失函數。

【為什麼】
原始 GAN 訓練可能不穩定，生成器容易找到欺騙鑑別器的少數模式，導致 mode collapse。WGAN 以 Wasserstein distance 衡量真實分布與生成分布距離，提供較平滑且有意義的梯度，使訓練更穩定、生成樣本多樣性較好。WGAN-GP 也常結合梯度懲罰進一步穩定。

【錯誤選項解析】
A：錯。梯度懲罰常用於 WGAN-GP，可穩定訓練，但本題最常見核心解法是 WGAN 損失。
B：對。Wasserstein 距離是處理 GAN 不穩定與模式崩潰的經典方法。
C：錯。單純加入隨機擾動不一定解決生成器忽略多樣性的問題。
D：錯。多尺度鑑別器可能幫助影像品質，但不是 mode collapse 最典型解法。

【名詞解釋】
- Mode Collapse：GAN 只生成少數模式。
- WGAN：使用 Wasserstein 距離的 GAN。
- Wasserstein Distance：衡量兩分布差異的距離。
- Generator：生成器。
- Discriminator/Critic：鑑別器或 WGAN 中的 critic。

【記憶】
GAN 崩潰口訣：**「模式崩潰找 WGAN，Wasserstein 讓訓練更穩」**。''',
'S3_08':'''【考點】
One-Hot Encoding 適用於無序類別特徵。當類別之間沒有大小順序，例如顏色、城市、品類，one-hot 可避免模型誤以為類別有數值大小關係。

【正解】
C。無序類別特徵（如顏色：紅/藍/綠）。

【為什麼】
One-hot encoding 會為每個類別建立一個二元欄位，例如顏色紅、藍、綠各自一欄。這樣模型只知道類別是否存在，不會把紅=1、藍=2、綠=3 誤解成大小順序。它適合低到中等基數的 nominal categorical feature。

【錯誤選項解析】
A：錯。連續數值特徵通常做標準化、正規化或分桶，不是 one-hot 的主要對象。
B：錯。時間序列特徵需考慮時間順序與滯後特徵。
C：對。無序類別特徵最適合 one-hot。
D：錯。圖像像素是數值矩陣，不會用 one-hot 表示每個像素。

【名詞解釋】
- One-Hot Encoding：每個類別一個 0/1 欄位。
- Categorical Feature：類別型特徵。
- Nominal Feature：無序類別特徵。
- Ordinal Feature：有順序類別特徵。
- High Cardinality：類別數很多。

【記憶】
One-hot 口訣：**「沒有大小順序的類別，用一格一格 0/1 表示」**。''',
'official_114_2_subject3_10':'''【考點】
AutoML 的適用情境。AutoML 適合在時間、人力或專業工程資源不足時，快速比較多種模型、特徵處理與超參數設定，提高模型開發效率。

【正解】
C。行銷部門希望短時間比較多種顧客流失預測模型，缺乏專職工程師與時間進行手動建模。

【為什麼】
AutoML 可自動化資料前處理、模型選擇、超參數搜尋與評估，適合非專職資料科學團隊快速建立 baseline 或比較候選模型。顧客流失預測通常是表格分類問題，很適合 AutoML 快速探索。若已有成熟 MLOps 或高度客製化需求，AutoML 的優勢就比較低。

【錯誤選項解析】
A：錯。已有完整平台與資深團隊時，AutoML 不是最迫切提升效率的情境。
B：錯。模型已長期穩定，只需定期調參，不一定需要導入 AutoML。
C：對。缺乏人力與時間、需快速比較模型，是 AutoML 適合情境。
D：錯。高度客製化且需精細控制時，AutoML 可能限制太多。

【名詞解釋】
- AutoML：自動化機器學習流程。
- Model Selection：模型選擇。
- Hyperparameter Tuning：超參數調整。
- Baseline Model：基準模型。
- Churn Prediction：顧客流失預測。

【記憶】
AutoML 口訣：**「人少、時間短、要快試很多模型，就用 AutoML」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
