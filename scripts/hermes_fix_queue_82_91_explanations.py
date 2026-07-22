#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_114_2_subject1_8':'''【考點】
Softmax 與 Max-Pooling 的功能差異。Softmax 用於把一組分數轉成機率分布，保留所有輸入項目的相對比例；Max-Pooling 則在局部區域只保留最大值，用於特徵下採樣。

【正解】
C。Softmax 會保留所有輸入資訊，但以比例表示；Max-Pooling 只保留區域最大值。

【為什麼】
Softmax 會對每個輸入分數取指數並除以總和，使輸出總和為 1，常用於多類別分類輸出。它不只取最大值，而是讓每個類別都有一個機率比例。Max-Pooling 則是在特徵圖的局部窗口中取最大值，降低空間維度並保留最強反應，因此會丟棄非最大值資訊。

【錯誤選項解析】
A：錯。Softmax 不會壓縮成單一最大值；它輸出一組機率分布。
B：錯。Max-Pooling 不做機率分布轉換，只取局部最大值。
C：對。Softmax 保留各輸入相對比例，Max-Pooling 只保留區域最大反應。
D：錯。Softmax 主要用於分類輸出，Max-Pooling 主要用於特徵降維。

【名詞解釋】
- Softmax：將 logits 轉為機率分布的函數。
- Max-Pooling：在局部區域取最大值的下採樣操作。
- Logits：模型輸出、尚未轉成機率的分數。
- Feature Map：CNN 卷積後產生的特徵圖。
- Downsampling：降低特徵圖空間尺寸。

【記憶】
口訣：**「Softmax 分機率，Max-Pooling 取最大」**。分類輸出看 Softmax，特徵降維看 Pooling。''',
'official_114_2_subject3_35':'''【考點】
PCA 特徵值與解釋變異量計算。總變異量等於所有特徵值總和，單一主成分解釋比例為該特徵值除以總和。

【正解】
A。前兩個主成分合計解釋 90% 的總變異量，因此可安全降維至二維，且仍保留大部分資訊。

【為什麼】
三個特徵值為 6.0、3.0、1.0，總和是 10。第一主成分解釋 6/10=60%，第二主成分解釋 3/10=30%，前兩個合計 90%。題目要求至少保留 80% 總變異量，所以保留前兩個主成分即可達標，並可把資料從三維降到二維。

【錯誤選項解析】
A：對。前兩個主成分合計 90%，超過 80% 門檻。
B：錯。第一主成分只有 60%，未達至少 80%，不能只保留一維。
C：錯。第二主成分貢獻 30% 應保留，但第三主成分只有 10%，在 80% 門檻下可捨棄。
D：錯。特徵值 6、3、1 差異明顯，不是均衡分布。

【名詞解釋】
- PCA：主成分分析，用正交方向保留最大變異量。
- Eigenvalue：特徵值，代表該主成分解釋的變異量。
- Explained Variance Ratio：解釋變異比例。
- Dimensionality Reduction：降維，減少特徵數但保留主要資訊。
- Principal Component：主成分，PCA 找出的新軸向。

【記憶】
PCA 口訣：**「特徵值相加當總量，前幾個累積看門檻」**。本題 6+3=9，9/10=90%。''',
'official_114_2_subject1_40':'''【考點】
VAE、GAN、Diffusion Model 的生成策略差異，以及在多模態潛在空間對齊中的典型特性。

【正解】
A。VAE 透過顯式潛在變數建模；GAN 透過對抗損失學習分佈映射；擴散模型以條件化去噪反推實現高保真生成。

【為什麼】
VAE 有明確 latent variable 與變分推論，適合學習整體語意結構與連續潛在空間，但生成結果常較平滑。GAN 透過生成器與判別器對抗訓練，可生成銳利高品質樣本，但訓練可能不穩定、出現 mode collapse。Diffusion Model 透過逐步加噪與去噪學習資料分布，條件化後可做文字到影像等高保真跨模態生成，穩定性與多樣性通常較好。

【錯誤選項解析】
A：對。這正確區分三者的建模與生成策略。
B：錯。VAE 不是依賴對抗式訓練，GAN 也不是顯式後驗估計。
C：錯。GAN/VAE 不都使用馬爾可夫鏈進行跨模態轉換；Diffusion 才常與逐步馬爾可夫去噪過程相關。
D：錯。三者不只是解碼器不同，訓練目標與生成機制根本不同。

【名詞解釋】
- VAE：變分自編碼器，以顯式潛在變數建模。
- GAN：生成對抗網路，以對抗損失訓練生成器。
- Diffusion Model：擴散模型，學習從噪聲逐步去噪生成資料。
- Latent Alignment：不同模態在潛在空間中的語意對齊。
- Mode Collapse：GAN 只生成少數模式的失敗現象。

【記憶】
口訣：**「VAE 有 latent，GAN 會對抗，Diffusion 逐步去噪」**。問三者差異就抓訓練目標與生成流程。''',
'S1_11':'''【考點】
差分隱私（Differential Privacy）的目的。差分隱私透過加入控制過的隨機雜訊，降低從模型輸出或統計結果反推出個人資料的風險。

【正解】
B。在資料中加入適量雜訊，防止個人資料被還原。

【為什麼】
差分隱私的核心是讓單一個體是否存在於資料集中，不會對輸出結果造成過大影響。實務上可在資料、統計查詢或梯度更新中加入雜訊，使攻擊者難以根據輸出推回某個人的敏感資訊。它常用於醫療、金融、使用者行為分析等隱私敏感場景。

【錯誤選項解析】
A：錯。加入雜訊通常不會加快訓練，甚至可能增加成本。
B：對。差分隱私主要是保護個資，降低被還原或推斷風險。
C：錯。差分隱私可能犧牲部分準確率，目的不是提高準確率。
D：錯。自動標註資料與差分隱私無關。

【名詞解釋】
- Differential Privacy：限制單一個體對輸出影響的隱私保護技術。
- Noise Injection：加入隨機雜訊。
- Privacy Budget ε：衡量隱私保護強度的參數。
- Re-identification：重新識別個人身份的攻擊。
- DP-SGD：在梯度中加入雜訊的差分隱私訓練方法。

【記憶】
差分隱私口訣：**「加一點雜訊，保一個人的秘密」**。看到防止個資被反推，就選差分隱私。''',
'S3_14':'''【考點】
SVM 核函數（Kernel）的作用。Kernel trick 可在不明確計算高維座標的情況下，等效把資料映射到高維特徵空間，使原本線性不可分的資料變得可分。

【正解】
B。將資料映射到高維空間，讓線性不可分資料變為可分。

【為什麼】
SVM 會尋找能最大化間隔的分類超平面。若原始空間中資料不是線性可分，可使用 kernel function 計算高維空間中的內積，例如 RBF kernel、多項式 kernel，使模型能建立非線性決策邊界。重點是 kernel 幫助 SVM 處理非線性分類。

【錯誤選項解析】
A：錯。模型準確率是評估指標，不是 kernel 的作用。
B：對。核函數用於高維映射與非線性可分。
C：錯。學習率是梯度式最佳化超參數，SVM kernel 不負責選學習率。
D：錯。缺失值處理是資料前處理，不是 kernel 功能。

【名詞解釋】
- SVM：支持向量機，尋找最大間隔分類邊界。
- Kernel Trick：用核函數等效計算高維內積。
- RBF Kernel：常見非線性核函數。
- Hyperplane：分類超平面。
- Linear Separability：資料能否被直線/平面分開。

【記憶】
SVM kernel 口訣：**「低維分不開，核函數拉到高維分」**。看到線性不可分，就想到 kernel。''',
'official_115_1_subject1_28':'''【考點】
SHAP 值的方向與大小解讀。SHAP 表示某特徵相對於 base value 對單一預測輸出的貢獻方向與幅度，不等同百分比，也不代表全域重要性。

【正解】
B。「月收入」SHAP=-2.3 表示相對於基準值，此特徵將模型輸出值往負方向推移 2.3 個單位，表示月收入對該申請人有降低違約風險的貢獻。

【為什麼】
SHAP 是局部解釋方法，對單一樣本說明各特徵如何把模型輸出從 base value 推到最終預測。負值代表往負方向推動，若模型輸出越高代表違約風險越高，則月收入 SHAP=-2.3 表示降低風險輸出。它通常是在模型輸出尺度上解讀，不一定是機率百分點。

【錯誤選項解析】
A：錯。-2.3 不一定代表機率降低 2.3%，要看模型輸出尺度。
B：對。這正確描述 SHAP 相對 base value 的方向與單位推移。
C：錯。負 SHAP 不代表特徵不重要，只代表對該樣本往負方向影響。
D：錯。單一樣本 +1.8 不代表全訓練集中最重要，只是該樣本局部貢獻。

【名詞解釋】
- SHAP：基於 Shapley value 的模型解釋方法。
- Base Value：模型平均輸出或基準輸出。
- Local Explanation：針對單一樣本的解釋。
- Feature Contribution：特徵對預測的貢獻。
- Summary Plot：展示特徵影響分布的圖。

【記憶】
SHAP 口訣：**「正負看方向，大小看推力；不是百分比，也不是全域排名」**。''',
'S3_02':'''【考點】
Adam 優化器的自適應學習率。Adam 會為每個參數維護一階動量與二階動量估計，據此自動調整每個參數的更新步幅。

【正解】
C。Adam。

【為什麼】
SGD 與普通梯度下降通常使用同一全域學習率。Adam 結合 Momentum 與 RMSProp 的想法，會根據梯度平均與平方梯度平均，對不同參數使用自適應更新。這讓它在稀疏梯度或不同尺度參數上常比普通 SGD 更容易訓練。

【錯誤選項解析】
A：錯。SGD 通常不自動為每個參數調整學習率，除非加上額外策略。
B：錯。Batch GD 是使用整批資料計算梯度，不代表自適應學習率。
C：對。Adam 會自動調整每個參數的學習率/更新幅度。
D：錯。普通梯度下降使用固定或手動設定學習率。

【名詞解釋】
- Adam：Adaptive Moment Estimation，自適應優化器。
- Learning Rate：控制參數更新步幅的超參數。
- Momentum：利用過去梯度方向平滑更新。
- RMSProp：根據平方梯度調整學習率。
- SGD：隨機梯度下降。

【記憶】
優化器口訣：**「Adam 會自己調每個參數步伐」**。看到自動調整學習率，優先選 Adam。''',
'official_114_2_subject3_20':'''【考點】
Interaction Features（互動特徵）的建立方式。互動特徵用來表示兩個或多個特徵之間的組合效果，常透過乘積、交叉、比值或組合項建立。

【正解】
C。將兩個或多個特徵進行乘積或交互組合。

【為什麼】
若模型需要捕捉「商品價格」與「顧客滿意度」之間的互動效果，單獨使用價格或滿意度可能不足。建立 price × satisfaction 這類交互項，可讓模型學到「價格在不同滿意度下影響不同」的關係。這在迴歸、分類與表格特徵工程中都很常見。

【錯誤選項解析】
A：錯。單一特徵平方是多項式特徵之一，但不是兩個特徵間的互動。
B：錯。對數轉換改變特徵分布與尺度，不是建立互動特徵。
C：對。乘積或交互組合正是 interaction features 的核心。
D：錯。標準化只調整尺度，不建立特徵間關係。

【名詞解釋】
- Interaction Feature：表示多個特徵共同作用的組合特徵。
- Feature Engineering：設計或轉換特徵以提升模型表現。
- Product Term：兩特徵相乘形成的交互項。
- Polynomial Feature：包含平方項與交互項的特徵擴展。
- Standardization：將特徵調整到相近尺度。

【記憶】
互動特徵口訣：**「想看兩個特徵一起影響，就做交叉或相乘」**。''',
'official_114_2_subject3_30':'''【考點】
跨語言部署造成模型效能下降與 F1-score 解讀。英文模型部署到西班牙文後 F1 從 0.91 降到 0.58，最合理是語言轉移/領域轉移導致模型無法正確辨識關鍵情緒詞，進而影響 recall 或 precision。

【正解】
C。語言轉移造成召回率下降，模型無法正確辨識關鍵情緒詞彙。

【為什麼】
情感分析高度依賴語言詞彙、語法、慣用語與文化脈絡。模型若主要在英文資料上訓練，直接套到西班牙文可能無法理解情緒詞、否定語或語氣，導致大量正負情緒樣本漏判，召回率下降，F1-score 隨之降低。這是跨語言泛化失敗的典型情況。

【錯誤選項解析】
A：錯。macro F1 可用於類別不平衡評估，不應因分數下降就改用 micro F1 掩蓋問題。
B：錯。部署在西班牙文資料集表現變差不是「西班牙文語料過擬合且偏高」。
C：對。語言轉移導致關鍵詞辨識失敗，會影響 recall 與 F1。
D：錯。MSE 是回歸常用指標，不適合取代分類 F1 評估情感分類。

【名詞解釋】
- Macro F1：各類別 F1 平均，重視每類表現。
- Recall：真正樣本中被找出的比例。
- Cross-lingual Transfer：跨語言遷移。
- Domain Shift：訓練與部署資料分布不同。
- Sentiment Analysis：情感分析，判斷文本情緒。

【記憶】
跨語言口訣：**「英文學得好，不代表西文看得懂」**。語言換了、F1 暴跌，先想語言/資料分布轉移。''',
'S1_03':'''【考點】
NLP 前處理中的詞形還原（Lemmatization）。Lemmatization 會把單詞還原成字典原形，並盡量保留語意與詞性資訊。

【正解】
B。將單詞還原為字典原形，保留語意。

【為什麼】
英文中同一詞可能有不同變化，例如 running、ran、runs 可還原為 run；better 可能還原為 good。Lemmatization 通常會參考詞性與字典，因此比 stemming 更精準，能保留較自然的語意形式。它常用於搜尋、文字分類與傳統 NLP 前處理。

【錯誤選項解析】
A：錯。去除停用詞是 stopword removal，不是 lemmatization。
B：對。詞形還原就是還原成字典原形。
C：錯。計算詞頻權重是 TF、TF-IDF 等方法。
D：錯。將文字轉為數字向量是 vectorization 或 embedding。

【名詞解釋】
- Lemmatization：詞形還原，將詞還原為 lemma。
- Lemma：字典原形。
- Stemming：詞幹提取，通常較粗略。
- Stopword Removal：移除常見功能詞。
- Vectorization：將文字轉成數值特徵。

【記憶】
詞形還原口訣：**「變化詞回字典原形」**。running → run，目的不是算權重，也不是轉向量。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
