#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
explanations={
'official_114_2_subject1_30':'''【考點】
不可否認性（Non-repudiation）與稽核追蹤。金融 AI 推論若要能日後法務追蹤，需證明某次推論紀錄確實存在、未被竄改，且可追溯責任，因此要使用雜湊與數位簽章。

【正解】
A。為每筆 AI 模型推論記錄其輸入與輸出結果的加密雜湊值，並簽署數位簽章以確保不可竄改性。

【為什麼】
Hash 可把推論輸入、輸出、模型版本、時間戳等紀錄轉成固定摘要，任何竄改都會造成 hash 改變。數位簽章可證明紀錄由特定系統或責任方產生，並防止事後否認。這正符合不可否認性、完整性與稽核要求。

【錯誤選項解析】
A：對。Hash + digital signature 是落實不可竄改與不可否認性的核心措施。
B：錯。降低延遲是效能優化，不能證明紀錄未被竄改或不可否認。
C：錯。主機備援提升可用性，不是不可否認性。
D：錯。負載平衡改善效能與可用性，不是法務稽核證據保全。

【名詞解釋】
- Non-repudiation：不可否認性，事後不能否認曾執行或產生某紀錄。
- Hash：雜湊摘要，用於檢查資料完整性。
- Digital Signature：數位簽章，用私鑰簽署、公開驗證來源。
- Audit Trail：稽核軌跡。
- Integrity：完整性，資料未遭竄改。

【記憶】
不可否認性口訣：**「要能追責與防竄改，就用 Hash + 數位簽章」**。''',
'S3_09':'''【考點】
L2 正則化（Ridge）的效果。L2 會在損失函數加入權重平方和懲罰，使過大的係數被壓小，讓權重更平滑分散，降低過擬合風險。

【正解】
B。懲罰過大的係數，讓權重平滑分散。

【為什麼】
L2 regularization 的懲罰項通常是 λΣw²。權重越大，懲罰越大，因此模型會傾向使用較小、較分散的權重，不會過度依賴少數特徵。它通常不會把係數壓成剛好 0；把係數變成 0、產生特徵選擇效果的是 L1/Lasso。

【錯誤選項解析】
A：錯。讓部分係數變為 0 是 L1 正則化的典型特性。
B：對。L2 會懲罰大權重，使係數平滑分散。
C：錯。L2 可降低過擬合風險，但不能完全防止過擬合。
D：錯。L2 主要是泛化控制，不是保證加快梯度下降。

【名詞解釋】
- L2 Regularization：權重平方懲罰。
- Ridge Regression：使用 L2 懲罰的線性迴歸。
- Weight Decay：深度學習中常見的 L2 類正則化。
- Overfitting：模型過度記住訓練資料。
- L1 Regularization：權重絕對值懲罰，常產生稀疏解。

【記憶】
L2 口訣：**「L2 壓小大權重，讓權重平滑分散；L1 才常歸零」**。''',
'official_114_2_subject3_29':'''【考點】
時間序列資料的驗證策略與長期泛化。設備工況會隨時間變化，固定舊驗證集無法反映現況，因此應採用 Time Series Cross Validation 或 Rolling Window Validation。

【正解】
D。採用時間序列交叉驗證或滑動視窗驗證，動態更新驗證資料以適應時間演進。

【為什麼】
工業設備資料常有 concept drift 或 data drift，例如季節、設備老化、維修、工況改變。若一直使用舊驗證集調參，模型可能只對過去環境有效。時間序列交叉驗證會尊重時間順序，用較早資料訓練、較晚資料驗證；rolling window 可逐步更新訓練與驗證窗口，更貼近實際部署情境。

【錯誤選項解析】
A：錯。固定驗證集無法反映環境變化；L2 不能解決驗證集過時。
B：錯。不使用驗證集會失去可靠模型選擇依據，early stopping 仍需驗證訊號。
C：錯。簡化模型可降低過擬合，但不能處理時間演進與工況變化。
D：對。動態時間序列驗證最能提升長期穩健性。

【名詞解釋】
- Time Series Cross Validation：依時間順序切分的交叉驗證。
- Rolling Window Validation：滑動視窗驗證。
- Concept Drift：目標關係隨時間改變。
- Data Drift：輸入資料分布改變。
- Generalization：泛化能力。

【記憶】
時間序列驗證口訣：**「資料會隨時間變，驗證也要跟著時間走」**。''',
'official_115_1_subject1_23':'''【考點】
小樣本瑕疵檢測、地端即時推論與資源受限導入策略。最合適的是 Transfer Learning 搭配模型壓縮/量化，部署於地端滿足延遲需求。

【正解】
B。採用預訓練模型 Transfer Learning，針對瑕疵樣本 Fine-tuning，並使用量化或蒸餾壓縮模型以符合延遲需求，部署於地端。

【為什麼】
瑕疵樣本 800 張不適合從零訓練大型 CNN；正常樣本多、瑕疵樣本少，第一階段應利用預訓練視覺模型學到的通用特徵，再用有限瑕疵資料微調。因地端無 GPU、100ms 即時要求，還需量化、蒸餾、模型剪枝或輕量架構，降低 CPU/邊緣裝置推論延遲。

【錯誤選項解析】
A：錯。從零訓練大型 CNN 需要大量資料與 GPU，且採購高階硬體不符合限制。
B：對。遷移學習 + 壓縮部署最符合樣本少、地端即時、預算中等。
C：錯。可先用遷移學習與資料增強導入，不必等到 10 萬瑕疵樣本。
D：錯。雲端 AutoML 不符合地端即時與連線限制。

【名詞解釋】
- Transfer Learning：遷移學習，利用預訓練模型。
- Fine-tuning：針對新任務微調模型。
- Quantization：量化，降低模型精度加速推論。
- Distillation：蒸餾，小模型學大模型。
- Edge Inference：地端/邊緣推論。

【記憶】
小樣本地端視覺口訣：**「樣本少用預訓練，地端慢就壓縮量化」**。''',
'official_115_1_subject1_14':'''【考點】
災難性遺忘與參數高效微調。LLM 在醫療語料 SFT 時若忘記原有能力，資源有限下最適合凍結大部分參數，只微調 LoRA 等少量新增模組。

【正解】
A。凍結大部分預訓練參數，僅對少量新增模組如 LoRA 層進行微調，控制更新範圍以減少對原有知識的干擾。

【為什麼】
災難性遺忘是模型在新任務訓練時覆蓋原本知識。全量更新大模型會大幅改動原權重，風險較高且資源成本大。LoRA/adapter 等 PEFT 方法讓原模型權重多數保持不動，只學少量任務相關參數，因此能有效率學習醫療問答，同時降低對通用能力的破壞。

【錯誤選項解析】
A：對。凍結大部分權重並微調少量模組，是資源有限下緩解遺忘的合適策略。
B：錯。提高學習率更可能破壞原有知識，導致不穩定或遺忘。
C：錯。只用醫療語料多輪訓練會更強化新任務、加劇遺忘。
D：錯。增加 batch size 不能直接保證保留舊知識。

【名詞解釋】
- Catastrophic Forgetting：災難性遺忘。
- SFT：監督式微調。
- LoRA：低秩適應，參數高效微調方法。
- PEFT：Parameter-Efficient Fine-Tuning。
- Freeze：凍結權重不更新。

【記憶】
緩解遺忘口訣：**「不要大改原模型，只訓練小模組」**。''',
'official_115_1_subject1_44':'''【考點】
RESTful API 上傳大型影像的 HTTP 方法與資料格式。5MB 高解析影像應使用 POST，將檔案放在 request body，以 multipart/form-data 或 application/octet-stream 傳輸。

【正解】
B。採用 HTTP POST 請求，將影像資料以 multipart/form-data 或 application/octet-stream 傳輸於 Request Body。

【為什麼】
GET 適合查詢資源，不應把大型影像塞進 URL query string，URL 長度有限且不適合承載二進位資料。POST request body 可承載較大檔案；multipart/form-data 適合表單檔案上傳，application/octet-stream 適合直接傳二進位檔案。這是影像推論 API 的常見設計。

【錯誤選項解析】
A：錯。Base64 放 URL 會膨脹資料、受 URL 長度限制，也不符合大型檔案最佳實踐。
B：對。POST body + multipart/form-data 或 octet-stream 最合適。
C：錯。PUT/XML 不適合一般影像即時分類上傳。
D：錯。要求客戶端下載模型不是 API 設計的資料傳輸格式解法。

【名詞解釋】
- HTTP POST：常用於提交資料或上傳檔案。
- multipart/form-data：檔案上傳常用格式。
- application/octet-stream：通用二進位資料格式。
- Request Body：HTTP 請求正文。
- Base64：把二進位轉文字，但會增加體積。

【記憶】
影像 API 口訣：**「大檔不要塞 URL，POST body 傳檔案」**。''',
'official_114_2_subject1_6':'''【考點】
N-gram 語言模型限制。N-gram 只根據固定長度前文估計下一詞，能捕捉局部片段，但難以建模長距離依賴與整體語意連貫。

【正解】
B。N-gram 模型僅根據固定長度的前序詞建立機率估計，難以捕捉長距離依賴關係。

【為什麼】
N-gram 假設下一個詞只依賴前 n-1 個詞，例如 trigram 只看前兩個詞。因此句子局部可能合理，但跨句、長句或需要前後語意一致的情境容易失去連貫。客服自動回覆需要理解整體意圖與上下文，N-gram 的固定窗口限制會造成回答片段化。

【錯誤選項解析】
A：錯。N-gram 計算量不是造成語意不連貫的主要原因。
B：對。固定長度上下文導致難以捕捉長距離依賴。
C：錯。缺乏 embedding 會限制語意泛化，但題目問句子整體連貫，B 更直接。
D：錯。N-gram 並非假設詞完全獨立，而是假設只依賴有限前文。

【名詞解釋】
- N-gram：由連續 n 個詞組成的語言模型單位。
- Long-range Dependency：長距離依賴。
- Markov Assumption：只依賴有限前文的假設。
- Language Model：估計文字序列機率的模型。
- Context Window：模型可利用的上下文範圍。

【記憶】
N-gram 口訣：**「只看前幾個詞，所以短片段合理、長語意不穩」**。''',
'S1_06':'''【考點】
靜態詞嵌入與上下文化詞嵌入差異。Word2Vec 是靜態詞嵌入，同一個詞無論出現在什麼語境，向量都相同；BERT、ELMo、GPT 會根據上下文產生不同表示。

【正解】
C。Word2Vec。

【為什麼】
Word2Vec 會為詞彙表中的每個詞學一個固定向量，例如 bank 在「river bank」和「bank account」中仍使用同一向量。BERT、ELMo、GPT 等模型會根據句子上下文產生 contextual embedding，同一詞在不同語境下向量可不同，因此能處理多義詞更好。

【錯誤選項解析】
A：錯。BERT 是上下文化表示，向量會受上下文影響。
B：錯。ELMo 也是 contextual embedding。
C：對。Word2Vec 是典型靜態詞嵌入。
D：錯。GPT 會依自回歸上下文產生表示，不是靜態詞向量。

【名詞解釋】
- Static Embedding：每個詞固定一個向量。
- Word2Vec：經典靜態詞嵌入方法。
- Contextual Embedding：依上下文改變的詞表示。
- BERT：雙向 Transformer 語言模型。
- Polysemy：多義詞現象。

【記憶】
詞嵌入口訣：**「Word2Vec 固定一詞一向量；BERT/ELMo/GPT 看上下文」**。''',
'S1_25':'''【考點】
AI 系統的倫理風險。倫理風險關注公平性、偏見、歧視、隱私、透明性與問責等問題；模型偏差導致特定族群受到不公平對待屬於典型倫理風險。

【正解】
C。模型偏差導致特定族群受到不公平對待。

【為什麼】
AI 系統可能因資料偏差或標籤偏差，對某些性別、年齡、族群、地區或弱勢群體產生較差結果。這不只是技術效能問題，也會造成社會不公平、法律風險與信任問題，因此屬於 AI ethics 的核心關注。

【錯誤選項解析】
A：錯。訓練時間過長是效能/成本問題，不是倫理風險核心。
B：錯。伺服器停機是可用性或維運風險。
C：對。偏差造成特定群體不公平，是典型倫理風險。
D：錯。API 費用過高是商業成本問題。

【名詞解釋】
- Ethical Risk：倫理風險。
- Bias：偏差。
- Fairness：公平性。
- Discrimination：歧視或不合理差別待遇。
- Accountability：問責，能追蹤與說明決策責任。

【記憶】
倫理風險口訣：**「影響人的公平、隱私、透明與權益，就是倫理問題」**。''',
'official_115_1_subject3_8':'''【考點】
學習率過大的直接影響。Learning rate 太大會讓參數更新步伐過大，在最優點附近來回跳動，造成 loss 震盪甚至發散。

【正解】
B。損失函數震盪或發散：每次更新步伐過大，參數在最優點兩側反覆跳越，無法穩定收斂。

【為什麼】
梯度下降每次會沿梯度方向更新參數，學習率控制步長。若步長太大，模型可能跨過最低點，下一次又從另一側跨回，導致 loss 震盪；更嚴重時參數越走越遠，loss 發散。題目已明確說調高學習率後訓練損失震盪，因此最直接原因是 learning rate 過大。

【錯誤選項解析】
A：錯。梯度消失是梯度逐層變小，不是調高學習率後震盪的直接描述。
B：對。學習率過大最典型現象就是震盪或發散。
C：錯。過擬合是訓練損失下降、驗證損失上升；但調高學習率造成訓練震盪是另一件事。
D：錯。死亡 ReLU 是 ReLU 神經元長期輸出 0，非本題直接現象。

【名詞解釋】
- Learning Rate：學習率，控制更新步幅。
- Oscillation：震盪，在最優點附近來回跳。
- Divergence：發散，loss 無法收斂甚至變大。
- Gradient Descent：梯度下降。
- Overfitting：訓練好但泛化差。

【記憶】
學習率口訣：**「步子太大會跳過最低點，loss 震盪或發散」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
