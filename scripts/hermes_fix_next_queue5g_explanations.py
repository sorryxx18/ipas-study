#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
questions=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in questions}
explanations={
'S3_27':'''【考點】
缺失值（Missing Values）處理。題目問訓練資料中缺失值的常見做法，重點是依資料型態與缺失情況選擇填補、模型補值或少量刪除，而不是全部設 0 或完全不處理。

【正解】
B。以均值、中位數或眾數填補，或使用模型預測補值。

【為什麼】
缺失值若不處理，許多模型無法訓練或會產生偏誤。常見做法是數值型特徵用均值或中位數填補，類別型特徵用眾數或新增「未知」類別；更進階可用 KNN、迴歸模型或其他模型預測補值。實務上也會保留缺失指標欄位，讓模型知道該值原本是否缺失。

【錯誤選項解析】
A：錯。直接刪除整個資料集太極端；只有在缺失比例很低且刪除不影響代表性時，才可能刪除少量列或欄。
B：對。均值、中位數、眾數或模型預測補值，都是常見缺失值處理方式。
C：錯。全部設為 0 可能引入錯誤意義；0 可能是有效數值，不一定代表缺失。
D：錯。多數模型不會自動安全忽略缺失值；即使部分模型支援，也仍需理解缺失機制與風險。

【名詞解釋】
- Missing Value：資料中未觀測、未填寫或不可用的值。
- Imputation：缺失值填補。
- Mean/Median Imputation：用平均數或中位數填補數值欄位。
- Mode Imputation：用眾數填補類別欄位。
- Missing Indicator：記錄某欄位是否原本缺失的輔助特徵。

【記憶】
缺失值口訣：**「數值均中位，類別看眾數；不能亂補 0」**。看到缺失值處理，優先選合理填補或模型補值。''',
'official_115_1_subject3_34':'''【考點】
Grid Search 組合數與 K-fold 交叉驗證訓練次數計算。題目要把所有超參數候選值相乘，再乘上每組參數要做的 fold 數。

【正解】
D。3 × 4 × 5 × 3 × 3 × 5 = 2,700 個。

【為什麼】
Grid Search 會測試所有超參數組合。此題有 learning_rate 3 個、max_depth 4 個、n_estimators 5 個、subsample 3 個、colsample_bytree 3 個，因此參數組合數是 3×4×5×3×3 = 540。每一組參數又要完整進行 5-Fold 交叉驗證，所以總訓練次數為 540×5 = 2700。

【錯誤選項解析】
A：錯。Grid Search 不是把候選值數量相加，而是所有組合的笛卡兒積，要相乘。
B：錯。只算 n_estimators 或 fold，忽略其他超參數候選值。
C：錯。不能只取最大候選值數；Grid Search 會測全部組合。
D：對。所有候選值相乘後，再乘上 5-Fold 的 5 次訓練。

【名詞解釋】
- Grid Search：窮舉所有指定超參數組合的調參方法。
- Hyperparameter：訓練前設定的參數，例如 learning_rate、max_depth。
- K-Fold Cross Validation：把資料分成 K 份輪流驗證，每組參數需訓練 K 次。
- n_estimators：樹模型或 boosting 中樹的數量。
- colsample_bytree：每棵樹使用的特徵抽樣比例。

【記憶】
Grid Search 口訣：**「候選值用乘的，交叉驗證再乘 K」**。不要把超參數候選數相加。''',
'official_114_2_subject3_32':'''【考點】
L1 正則化（Lasso）與自動特徵選擇。題目希望避免過擬合，同時讓模型自動篩出較具代表性的特徵，關鍵是 L1 可讓部分係數變成 0。

【正解】
D。採用 L1 正則化（Lasso），透過懲罰項使部分特徵係數縮為 0。

【為什麼】
L1 正則化會對係數絕對值加總進行懲罰，具有稀疏化效果，能把部分不重要特徵的係數壓到 0，因此同時達到降低模型複雜度與特徵選擇的效果。相較之下，L2 正則化通常會縮小係數，但較少讓係數完全變成 0，因此保留大多數特徵。

【錯誤選項解析】
A：錯。Early Stopping 可避免訓練過久造成過擬合，但不能自動篩選特徵。
B：錯。移除多重共線性搭配 L2 可提升穩定性，但題目要「自動篩選」代表性特徵，L1 更直接。
C：錯。L2 會抑制權重幅度，但通常保留全部特徵，沒有明顯稀疏化。
D：對。L1/Lasso 可使部分係數為 0，達成特徵選擇。

【名詞解釋】
- L1 Regularization：對係數絕對值加總懲罰，常產生稀疏模型。
- Lasso：使用 L1 正則化的迴歸方法。
- L2 Regularization：對係數平方和懲罰，常使權重變小但不歸零。
- Feature Selection：選出較重要特徵、降低模型複雜度。
- Overfitting：模型過度擬合訓練資料，泛化能力變差。

【記憶】
正則化口訣：**「L1 會歸零，L2 只縮小」**。題目提到自動特徵篩選，就優先選 L1/Lasso。''',
'official_114_2_subject1_26':'''【考點】
多重共線性與 LASSO 正則化。題目問房間數與坪數高度相關時，如何降低共線性對模型參數估計的負面影響，選項中最適合的是含 L1 正則化的 LASSO。

【正解】
D。含 L1 正則化的 LASSO 迴歸模型。

【為什麼】
多重共線性會讓線性模型中相關特徵的係數估計不穩定。LASSO 透過 L1 懲罰可將部分係數壓到 0，達到變數選擇效果，能在高度相關特徵中保留較有代表性的特徵，降低模型複雜度。雖然 Ridge 也常用於共線性穩定化，但本題選項中給的是 LASSO，因此 D 最符合降低共線性與特徵選擇需求。

【錯誤選項解析】
A：錯。決策樹對特徵尺度與共線性較不敏感，但「不受影響」說法過度；題目問模型參數估計的負面影響，LASSO 更直接。
B：錯。傳統線性迴歸無正則化，面對多重共線性時係數容易不穩定。
C：錯。線性核 SVM 不是針對多重共線性與係數選擇的最直接方法。
D：對。LASSO 的 L1 正則化可降低複雜度並做特徵選擇。

【名詞解釋】
- Multicollinearity：多個特徵彼此高度相關，造成參數估計不穩。
- LASSO：Least Absolute Shrinkage and Selection Operator，使用 L1 正則化。
- L1 Regularization：可使部分係數歸零，具特徵選擇效果。
- Ridge Regression：使用 L2 正則化，通常縮小係數但不歸零。
- Linear Regression：線性迴歸，易受共線性影響。

【記憶】
共線性題口訣：**「相關太高，係數會飄；LASSO 可選特徵」**。看到 L1/LASSO，就想到係數歸零與特徵選擇。''',
'official_114_2_subject1_43':'''【考點】
生成式路徑與鑑別式路徑在低資源情境下的比較設計。題目要公平比較資料利用效率與泛化能力，因此應逐步減少標註資料比例，觀察模型在少量資料下的表現。

【正解】
B。在低資源情境（Low-resource Setting）下，逐步減少標註比例（100%、50%、10%），比較其 F1-score。

【為什麼】
方案 A 使用 VAE 建構潛在語意空間再接分類器，方案 B 使用 BERT Classifier 直接監督式分類。若要看兩種模型對標註資料的依賴程度與泛化能力，最合理是控制標註資料比例，觀察資料從充足到稀少時 F1-score 如何變化。這能突顯生成式表示學習與鑑別式分類器在低資源情境下的本質差異。

【錯誤選項解析】
A：錯。只用完整資料集比較 accuracy 與推論時間，難以看出低資源資料利用效率差異；accuracy 在類別不平衡時也可能不夠敏感。
B：對。逐步減少標註比例並比較 F1-score，能觀察兩路徑在低資源情境的泛化能力。
C：錯。GAN 生成文本會引入額外資料增強變因，干擾兩種原始模型設計的公平比較。
D：錯。只調模型參數量主要比較容量與過擬合敏感度，不是直接比較資料利用效率。

【名詞解釋】
- Low-resource Setting：標註資料有限的情境。
- VAE：變分自編碼器，可學習資料的潛在表示。
- BERT Classifier：以 BERT 表示接分類頭進行文本分類的鑑別式模型。
- F1-score：Precision 與 Recall 的調和平均，適合比較分類表現。
- Generalization：模型在未見資料上的泛化能力。

【記憶】
模型比較口訣：**「要比資料效率，就減少標註量看表現」**。低資源比較不要只看完整資料 accuracy。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
 data['questions']=questions
 data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=questions
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
