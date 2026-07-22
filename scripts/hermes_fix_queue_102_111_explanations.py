#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_114_2_subject1_24':'''【考點】
對抗性攻擊（Adversarial Attack）的防禦範圍。題目問「並非針對此種攻擊型態」的技術，重點是區分模型輸入擾動防禦與一般網路安全防護。

【正解】
D。在模型部署環境中強化網路防火牆，以阻擋來自未授權來源的網路連線。

【為什麼】
對抗性攻擊是攻擊者對模型輸入加入微小但惡意的擾動，使模型誤判。有效防禦通常包含對抗訓練、輸入檢測、資料前處理、模型魯棒性提升與輸出規則約束。防火牆可阻擋未授權連線，屬於基礎資安防護，但不能從根本上提升模型對惡意特徵擾動的魯棒性。

【錯誤選項解析】
A：錯。輸入前處理可過濾部分異常或不合理輸入，與防禦輸入攻擊有關。
B：錯。對抗樣本訓練是典型對抗攻擊防禦方法。
C：錯。規則引擎可在推論後限制不合理結果，屬於防護鏈的一部分。
D：對。防火牆是網路層防護，不是針對模型對抗擾動脆弱性的技術手段。

【名詞解釋】
- Adversarial Attack：對輸入加入微小擾動造成模型誤判。
- Adversarial Training：用對抗樣本訓練以提升魯棒性。
- Robustness：模型面對噪音或攻擊時仍穩定的能力。
- Rule Engine：以業務規則限制模型輸出。
- Firewall：網路連線存取控制設備。

【記憶】
口訣：**「對抗攻擊打模型輸入，防火牆守網路入口」**。問模型脆弱性，別選純網路防火牆。''',
'S1_13':'''【考點】
AI 倫理中的公平性（Fairness）。公平性關注模型結果是否對不同群體造成不合理差別待遇或歧視。

【正解】
B。模型預測是否對不同族群一致對待，不造成歧視。

【為什麼】
AI 系統可能因訓練資料偏差、標籤偏差或特徵代理變數，對性別、年齡、族群、地區等群體產生不公平結果。公平性不是指運算資源平均分配，也不是免費或開源，而是模型決策在不同群體間是否合理、可接受、符合法規與倫理。

【錯誤選項解析】
A：錯。訓練速度分配不是 AI fairness 的核心。
B：對。公平性重點是避免模型對不同族群歧視或差別待遇。
C：錯。免費使用屬於商業模式或可近用性，不是本題公平性定義。
D：錯。開源可提升透明度，但不等於公平性。

【名詞解釋】
- Fairness：模型對不同群體的決策是否公平。
- Bias：偏差，可能來自資料、標籤或模型。
- Discrimination：不合理差別待遇。
- Protected Attribute：受保護屬性，如性別、年齡、族群。
- Statistical Parity：不同群體正向決策比例相近的公平指標。

【記憶】
公平性口訣：**「不同族群，不要被模型不合理差別對待」**。''',
'official_114_2_subject1_33':'''【考點】
Word2Vec 的 CBOW 與 Skip-gram 差異。Skip-gram 用中心詞預測周圍詞，通常較適合捕捉低頻詞與罕見詞的語意關係；CBOW 用周圍詞預測中心詞，訓練較快但對低頻詞較弱。

【正解】
C。採用 Skip-gram 模型，利用中心詞預測周圍詞語，能更有效學習低頻詞關係。

【為什麼】
資料量龐大且希望有效捕捉罕見詞語意時，Skip-gram 較合適。它會讓每個中心詞去預測上下文，因此即使罕見詞出現次數少，也能透過上下文學到較細緻的語意向量。CBOW 平均上下文預測中心詞，速度通常較快，但對罕見詞表示較容易被高頻詞影響。

【錯誤選項解析】
A：錯。Skip-gram 是對的方向，但隨機初始化權重不是提升低頻詞捕捉的關鍵策略。
B：錯。CBOW + TF-IDF 不是 Word2Vec 標準低頻詞最佳策略。
C：對。Skip-gram 用中心詞預測周圍詞，較能學低頻詞關係。
D：錯。CBOW 較快但通常不如 Skip-gram 適合罕見詞。

【名詞解釋】
- Word2Vec：學習詞向量的模型家族。
- Skip-gram：用中心詞預測上下文。
- CBOW：用上下文預測中心詞。
- Low-frequency Word：低頻詞，出現次數少的詞。
- Word Embedding：將詞表示成向量。

【記憶】
Word2Vec 口訣：**「罕見詞找 Skip-gram；速度快找 CBOW」**。''',
'S3_05':'''【考點】
F1 Score 的公式。F1 是 Precision 與 Recall 的調和平均，用來在精確率與召回率之間取得平衡。

【正解】
B。2 × Precision × Recall / (Precision + Recall)。

【為什麼】
Precision 衡量預測為正的樣本中有多少是真的正；Recall 衡量實際正類中有多少被找出。F1 使用調和平均，因此若 Precision 或 Recall 任一很低，F1 也會被拉低。這比單純相加或相乘更適合評估分類器在不平衡資料下的正類辨識能力。

【錯誤選項解析】
A：錯。Precision + Recall 只是相加，不是 F1。
B：對。F1 = 2PR/(P+R)。
C：錯。Precision × Recall 不是 F1。
D：錯。這是 Accuracy 正確率公式。

【名詞解釋】
- Precision：預測為正中真正為正的比例。
- Recall：實際正類被找出的比例。
- F1 Score：Precision 與 Recall 的調和平均。
- Accuracy：整體正確率。
- Harmonic Mean：調和平均，會懲罰極低值。

【記憶】
F1 口訣：**「F1 等於 2PR 除以 P 加 R」**。看到 TP+TN 那個是 Accuracy。''',
'official_115_1_subject1_2':'''【考點】
LoRA（Low-Rank Adaptation）的參數高效微調。LoRA 會凍結原始大模型權重，只訓練少量低秩矩陣，降低可訓練參數量與 GPU 記憶體需求。

【正解】
C。凍結原始預訓練權重，僅在各層加入低秩分解的可訓練矩陣，大幅降低可訓練參數量與 GPU 記憶體需求。

【為什麼】
完整微調 70B 模型需要保存大量梯度、optimizer state 與 activation，GPU 記憶體成本極高。LoRA 假設權重更新可用低秩矩陣近似，把訓練集中在少量 adapter 參數上，原模型大多凍結。因此能在有限資源下做領域微調，並保留原模型能力。

【錯誤選項解析】
A：錯。知識蒸餾是訓練小模型模仿大模型，不是 LoRA。
B：錯。剪枝移除權重參數，和 LoRA 加低秩可訓練矩陣不同。
C：對。這正是 LoRA 的核心優勢。
D：錯。稀疏注意力降低長序列計算成本，不是 LoRA 的主要概念。

【名詞解釋】
- LoRA：低秩適應，參數高效微調方法。
- Fine-tuning：在特定資料上微調模型。
- Freeze：凍結原模型權重，不更新。
- Low-rank Matrix：低秩矩陣，用較少參數近似更新。
- Adapter：插入模型中的小型可訓練模組。

【記憶】
LoRA 口訣：**「大模型不動，只訓練小低秩矩陣」**。''',
'official_115_1_subject1_17':'''【考點】
多模態資料的模型架構選擇。不同模態有不同結構：影像適合 CNN/ResNet，文字適合 Transformer/BERT，時序感測資料適合 LSTM、GRU 或 Temporal CNN。

【正解】
D。影像模態用 CNN、文字模態用 Transformer、時序模態用 LSTM 或 Temporal CNN。

【為什麼】
胸腔 X 光是影像資料，CNN 擅長局部空間特徵擷取；臨床診斷筆記是文字序列，Transformer 擅長上下文語意；心率與血氧是時間序列，LSTM 或 Temporal CNN 可捕捉時間依賴與趨勢。多模態系統常先分別抽取各模態特徵，再進行融合。

【錯誤選項解析】
A：錯。LSTM 不適合作為影像主架構，BERT 也不是時序感測資料的直接標準選擇。
B：錯。TF-IDF 不適合影像，ResNet 是影像模型不是文字模型。
C：錯。Transformer 很通用，但原始 BERT 不能直接處理任意影像與數值時序。
D：對。各模態對應架構最合理。

【名詞解釋】
- Multimodal Learning：同時處理多種資料模態。
- CNN：擅長影像空間特徵。
- Transformer：擅長文字與序列上下文建模。
- LSTM：適合時間序列與長短期依賴。
- Temporal CNN：沿時間維度做卷積的時序模型。

【記憶】
多模態口訣：**「影像 CNN、文字 Transformer、時序 LSTM/TCN」**。''',
'official_114_2_subject1_28':'''【考點】
混合型資料的特徵工程。連續型特徵與類別型特徵應依型態採用不同處理方式，並可加入交互特徵提升模型表現。

【正解】
C。對連續特徵做標準化，類別特徵採用目標編碼，並生成交互特徵提升模型表現。

【為什麼】
連續特徵常需要標準化，讓不同尺度的數值欄位可比較；類別特徵可用 one-hot、target encoding 等方法轉換成模型可用形式。若資料中存在特徵互動，例如地區與坪數共同影響價格，生成交互特徵可提升預測能力。此選項同時照顧不同型態資料與特徵關係。

【錯誤選項解析】
A：錯。Label Encoding 對無序類別可能引入錯誤大小順序。
B：錯。把所有連續特徵都離散化可能損失數值資訊，不是最合適通用流程。
C：對。依資料型態處理並加入交互特徵最完整。
D：錯。忽略類別型變量會浪費可能重要資訊。

【名詞解釋】
- Standardization：標準化，轉成平均 0、標準差 1。
- Target Encoding：用目標統計量編碼類別。
- Label Encoding：以整數標籤表示類別。
- Interaction Feature：交互特徵，表示特徵共同作用。
- Categorical Feature：類別型特徵。

【記憶】
混合特徵口訣：**「連續看尺度，類別要編碼，有互動就交叉」**。''',
'official_115_1_subject3_28':'''【考點】
模型選擇：非線性關係與可解釋性需求。題目要求預測成交價、處理非線性、提供整體特徵重要性，因此 Random Forest Regression 最符合。

【正解】
B。使用隨機森林迴歸，可處理非線性關係，並提供整體特徵重要性作為解釋依據。

【為什麼】
隨機森林由多棵決策樹組成，可捕捉非線性與特徵交互關係，適合表格型房價資料。它也可提供 impurity-based 或 permutation feature importance，供業務與稽核了解哪些特徵整體影響較大。相較之下，羅吉斯迴歸是分類模型，K-means 是分群，SVR 雖能非線性但解釋整體特徵重要性較不直接。

【錯誤選項解析】
A：錯。Logistic Regression 是分類，不適合房價連續值迴歸；線性也難捕捉非線性。
B：對。Random Forest Regression 同時符合非線性與特徵重要性需求。
C：錯。K-means 是非監督分群，不是直接的迴歸模型選擇。
D：錯。SVR 可用 kernel 處理非線性，但用支持向量解釋整體特徵重要性不直觀。

【名詞解釋】
- Random Forest Regression：多棵決策樹集成的迴歸模型。
- Feature Importance：特徵重要性。
- Nonlinear Relationship：非線性關係。
- Regression：預測連續數值。
- Permutation Importance：打亂特徵觀察表現下降的解釋方法。

【記憶】
房價表格題口訣：**「要非線性又要特徵重要性，先想 Random Forest」**。''',
'official_114_2_subject3_24':'''【考點】
迴歸殘差圖解讀。殘差圖若出現極大殘差與系統性彎曲，代表可能有異常值、非線性關係或違反模型假設。

【正解】
C。模型存在異常值或非線性關係，違反迴歸假設。

【為什麼】
理想線性迴歸殘差應大致隨機分布在 0 附近，沒有明顯型態。若部分點殘差極大，可能是 outlier 或高影響點；若高價區殘差呈現彎曲系統性分布，表示線性模型未捕捉非線性關係，可能需要加入多項式、交互項、轉換目標或改用非線性模型。

【錯誤選項解析】
A：錯。殘差彎曲與極端點不一定是過擬合，較直接指向非線性或異常值。
B：錯。欠擬合可能造成系統性殘差，但題目同時提到極大殘差與高價區彎曲，C 更完整。
C：對。異常值與非線性關係是最合理解釋。
D：錯。殘差已呈現明顯結構，並非隨機分布。

【名詞解釋】
- Residual：真實值減預測值的誤差。
- Residual Plot：用來檢查迴歸假設的殘差圖。
- Outlier：異常值。
- Nonlinearity：非線性關係。
- Regression Assumption：線性、等變異、獨立等模型假設。

【記憶】
殘差圖口訣：**「隨機散開才好；有彎曲、有極端，就查非線性與異常值」**。''',
'official_115_1_subject3_38':'''【考點】
統計均等（Statistical Parity）。此公平性定義要求不同群體的正向決策比例大致相同；若男性通過率 55%、女性 30%，明顯不符合。

【正解】
C。不符合統計均等，因為不同群體的正向決策比例存在明顯差異。

【為什麼】
Statistical Parity 關注 P(\u005chat{Y}=1 | group) 是否在不同群體間相近。題目中男性應徵者面試通過率 55%，女性 30%，正向決策比例相差 25 個百分點，所以不符合統計均等。是否使用性別作為輸入不是唯一判準，因為其他特徵可能成為性別代理變數。

【錯誤選項解析】
A：錯。即使未使用性別，結果仍可能對不同群體不均等。
B：錯。兩群都有部分被錄取，不代表通過比例相同。
C：對。正向決策比例明顯不同，所以不符合統計均等。
D：錯。題目未提供女性預測準確率，且 statistical parity 看的是通過率比例。

【名詞解釋】
- Statistical Parity：不同群體正向決策比例應相近。
- Positive Decision Rate：正向決策比例，如通過率。
- Protected Group：受保護群體。
- Proxy Variable：可間接代表敏感屬性的變數。
- Fairness Metric：公平性衡量指標。

【記憶】
統計均等口訣：**「看各群體通過率，不是看有沒有用性別欄位」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
