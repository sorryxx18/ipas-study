#!/usr/bin/env python3
import json, pathlib, datetime
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path=base/'questions.json'
data=json.loads(path.read_text())
qs=data['questions'] if isinstance(data,dict) and 'questions' in data else data
byid={q['id']:q for q in qs}
# 修正明顯選項污染
byid['official_115_1_subject3_48']['options']['D']='模型過擬合（Overfitting）'
explanations={
'official_114_2_subject3_43':'''【考點】
VGG16 中各層 FLOPs 運算量分布。VGG16 的主要計算成本集中在卷積層，因為卷積層需要在大量空間位置、通道與卷積核上重複乘加運算。

【正解】
A。卷積層（Conv2d）。

【為什麼】
VGG16 雖然全連接層參數量很多，但 FLOPs 不一定最多。卷積層在高解析度 feature map 上執行多個 3×3 卷積，每個輸出像素都需要對輸入通道與卷積核做大量乘加，因此整體運算量主要集中於 Conv2d。模型壓縮與硬體加速時，常優先分析卷積層的計算成本。

【錯誤選項解析】
A：對。VGG16 的 FLOPs 主要來自卷積層。
B：錯。全連接層參數多，但在 VGG16 中 FLOPs 通常少於全部卷積層總和。
C：錯。ReLU 只是逐元素 max(0,x)，運算量很低。
D：錯。池化層只做局部最大值或平均，運算量遠低於卷積。

【名詞解釋】
- FLOPs：浮點運算次數，用來估算模型計算量。
- Conv2d：二維卷積層。
- Linear：全連接層。
- ReLU：非線性激活函數。
- MaxPool2d：最大池化層。

【記憶】
VGG16 口訣：**「參數多看 FC，運算多看 Conv」**。問 FLOPs，多半選卷積層。''',
'official_115_1_subject1_21':'''【考點】
RAG token 成本優化。題目限制不更換模型、不影響回答品質，且成本主要集中輸入 tokens，因此應優先壓縮重複前綴與對話歷史，而不是只縮短輸出。

【正解】
B。將 System Prompt 改為 Prompt Caching 或靜態前綴重用，並對對話歷史實作摘要壓縮，以保留語意而非完整對話。

【為什麼】
目前每次請求有固定 500 tokens system prompt、完整對話歷史約 8,000 tokens、前 10 筆檢索文件約 6,000 tokens。輸入成本明顯高於輸出。Prompt caching 可降低重複 system prompt/靜態前綴成本；歷史摘要可保留關鍵語意但大幅減少 token。這比強迫回答變短更符合「不影響品質」與「輸入成本為主」的條件。

【錯誤選項解析】
A：錯。輸出平均只有 300 tokens，且強制 200 可能影響回答品質，無法主要解決輸入成本。
B：對。針對主要成本來源：靜態前綴與對話歷史輸入 tokens。
C：錯。Batch API 可降低非即時批次成本，但不一定適合互動式 RAG，也未處理輸入 token 膨脹。
D：錯。要求簡短只能略降輸出，無法有效處理大量輸入 tokens。

【名詞解釋】
- RAG：檢索增強生成。
- Prompt Caching：重用相同前綴以降低成本/延遲。
- Context Summarization：對話歷史摘要壓縮。
- Input Tokens：送入模型的 token。
- Retrieval Chunk：檢索文件片段。

【記憶】
RAG 成本口訣：**「成本在輸入，就砍重複前綴與長歷史；不是只叫模型回答短一點」**。''',
'official_115_1_subject3_48':'''【考點】
訓練曲線與驗證曲線落差判讀。當訓練表現明顯優於驗證表現，例如 training=0.81、validation=0.72，通常代表模型對訓練資料學得較好，但泛化到驗證資料較差，也就是過擬合。

【正解】
D。模型過擬合（Overfitting）。

【為什麼】
若訓練曲線值高於驗證曲線值，表示模型在訓練資料上的表現比未見資料好。這種 train-validation gap 是 overfitting 的典型訊號。過擬合常見原因包括模型太複雜、資料不足、正則化不夠或訓練太久。此題原 D 選項在 JSON 中混入下一段 AOI 題幹，已修正為「模型過擬合（Overfitting）」。

【錯誤選項解析】
A：錯。學習率太低通常造成收斂慢，不直接解釋訓練高、驗證低的落差。
B：錯。批次大小太大可能影響泛化或訓練動態，但不是最直接原因。
C：錯。低度擬合通常訓練與驗證表現都差，而不是訓練明顯高於驗證。
D：對。訓練表現高、驗證表現低，是過擬合典型現象。

【名詞解釋】
- Overfitting：模型過度貼合訓練資料，泛化差。
- Validation Curve：驗證集表現曲線。
- Generalization Gap：訓練與驗證表現差距。
- Regularization：降低過擬合的方法。
- Epoch：完整看過訓練資料一次。

【記憶】
曲線判讀口訣：**「訓練好、驗證差，就是過擬合」**。''',
'S1_24':'''【考點】
多模態 AI 的核心優勢。多模態 AI 能同時整合文字、圖像、語音、影片、感測器等不同資料來源，對複雜情境做更全面理解。

【正解】
B。能整合語音、圖像、文字等多種資訊，更全面理解複雜情境。

【為什麼】
單一模態模型只看一種資料，例如只看文字或只看影像。多模態模型可把不同來源互補起來，例如醫療系統同時看影像、病歷文字與生命徵象；客服系統同時看語音、文字與情緒。這種整合能力能提升上下文理解與決策品質，但不代表訓練一定更快、資料需求更少或架構更簡單。

【錯誤選項解析】
A：錯。多模態通常更複雜，訓練不一定更快。
B：對。整合多種資訊是核心優勢。
C：錯。多模態常需要更多且對齊的資料。
D：錯。多模態架構通常更複雜，包含編碼器、融合層與對齊機制。

【名詞解釋】
- Multimodal AI：多模態 AI，整合多種資料型態。
- Modality：模態，如文字、影像、語音。
- Fusion：融合，把不同模態表示結合。
- Cross-modal Alignment：跨模態對齊。
- Context Understanding：情境理解。

【記憶】
多模態口訣：**「文字看不夠，就加圖像、語音一起理解」**。''',
'official_115_1_subject3_20':'''【考點】
PyTorch CrossEntropyLoss 的輸出層設計。CrossEntropyLoss 內部已包含 LogSoftmax 與 NLLLoss，因此模型輸出應是未經 softmax 的 logits，輸出維度等於類別數。

【正解】
C。不使用任何激活函數，直接輸出未經正規化的 logits，輸出維度設為 3 對應三個類別。

【為什麼】
貓、狗、鳥是三分類單標籤任務，最後一層應輸出 3 個 logits。PyTorch 的 nn.CrossEntropyLoss 會在內部對 logits 做 log-softmax 並計算交叉熵。如果模型先手動加 Softmax，會造成數值穩定性與 loss 計算問題；Sigmoid 則較適合多標籤或二元獨立輸出。

【錯誤選項解析】
A：錯。三分類不能輸出維度 1，ReLU 也不是分類輸出激活。
B：錯。Sigmoid 讓每類獨立，不適合單標籤三分類搭配 CrossEntropyLoss。
C：對。輸出 3 個 raw logits，交給 CrossEntropyLoss 處理。
D：錯。不要在 CrossEntropyLoss 前先做 Softmax。

【名詞解釋】
- Logits：未正規化分數。
- CrossEntropyLoss：PyTorch 多類別分類損失。
- Softmax：把 logits 轉成機率分布。
- Single-label Classification：每筆樣本只屬於一個類別。
- Activation Function：激活函數。

【記憶】
PyTorch 分類口訣：**「CrossEntropyLoss 吃 logits，不要先 softmax」**。''',
'official_114_2_subject1_7':'''【考點】
物件偵測中的 IoU 與 mAP。IoU 閾值越高，代表預測框必須與真實框有更高重疊比例，才算偵測正確，因此定位要求更嚴格。

【正解】
A。預測邊界框與真實邊界框的重疊程度越高，模型偵測結果越精準。

【為什麼】
IoU 是預測框與真實框交集面積除以聯集面積。若 mAP 評估時設定 IoU=0.75，會比 IoU=0.5 更嚴格，要求預測框位置更貼近真實框。高 IoU 閾值下仍能取得高 mAP，表示模型不只分類對，框的位置也準。

【錯誤選項解析】
A：對。IoU 閾值高代表要求框重疊更高、定位更精準。
B：錯。誤差越大 IoU 越低，不會讓 mAP 上升。
C：錯。高 IoU 閾值主要提高定位正確標準，不必然描述 precision 降、recall 升。
D：錯。IoU 與真實框大小及重疊區域有關。

【名詞解釋】
- IoU：Intersection over Union，交集除以聯集。
- mAP：mean Average Precision，物件偵測常用指標。
- Bounding Box：邊界框。
- Object Detection：物件偵測。
- Localization：定位能力。

【記憶】
IoU 口訣：**「門檻越高，框要疊得越準」**。''',
'S1_27':'''【考點】
持續學習（Continual Learning）的核心概念。模型部署後仍能隨時間吸收新資料、新任務或新環境變化，持續更新能力，而不是只訓練一次就結束。

【正解】
A。模型在部署後能隨時間從新資料中學習更新。

【為什麼】
真實世界資料會變，例如使用者行為、設備狀態、語言用法、詐欺手法都可能改變。Continual Learning 希望模型在面對新資料時能持續學習，同時避免災難性遺忘，不把舊知識完全覆蓋。它是處理長期部署與資料漂移的重要概念。

【錯誤選項解析】
A：對。持續從新資料中學習，是 continual learning 的核心。
B：錯。持續學習仍可能需要訓練/更新，只是不是一次性訓練完。
C：錯。一次用最大資料集訓練是靜態訓練，不是持續學習。
D：錯。使用者持續輸入標註資料可能是資料來源之一，但不是完整定義。

【名詞解釋】
- Continual Learning：持續學習。
- Catastrophic Forgetting：學新任務時忘記舊任務。
- Data Drift：資料分布隨時間改變。
- Online Learning：線上學習。
- Model Update：模型更新。

【記憶】
持續學習口訣：**「部署後世界會變，模型也要能跟著學」**。''',
'official_114_2_subject3_5':'''【考點】
CNN 第一層卷積層的主要功能。卷積層會用多個濾波器在影像局部區域滑動，自動提取邊緣、紋理、角點等局部特徵。

【正解】
A。自動提取輸入影像中的局部特徵。

【為什麼】
CNN 的核心是 convolution filter。第一層卷積通常學到低階視覺特徵，例如邊緣、方向、顏色變化與簡單紋理；後續層再組合成更高階圖案與物件特徵。這讓 CNN 特別適合影像瑕疵檢測，因為表面刮痕、斑點等常具有局部視覺模式。

【錯誤選項解析】
A：對。卷積層主要自動提取局部特徵。
B：錯。降維通常由 pooling 或 stride 等操作負責，非第一層卷積的主要定義。
C：錯。增加參數不是目的，卷積其實透過權重共享降低參數量。
D：錯。整合所有特徵並輸出分類通常是後段全連接層或分類頭。

【名詞解釋】
- Convolutional Layer：卷積層。
- Filter/Kernel：卷積核。
- Local Feature：局部特徵。
- Weight Sharing：權重共享。
- Feature Map：特徵圖。

【記憶】
CNN 卷積口訣：**「濾波器滑過影像，抓局部邊緣與紋理」**。''',
'official_115_1_subject3_47':'''【考點】
CNN 模型建立結果判讀。此題依賴附圖與描述 A–F，但目前 JSON 未保留附圖與描述內容；依官方答案 B，可知正確描述組合為 C、E、F。

【正解】
B。描述 C、描述 E、描述 F。

【為什麼】
因題目缺少附圖與 A–F 原文，目前無法逐句校準每個描述。但可先根據官方答案建立刷題可用解析：遇到這類「參考模型建立結果」題，通常要檢查 model summary 中各層輸出 shape、參數量、activation、卷積/池化/flatten/dense 的連接順序，以及最後輸出是否符合分類任務。之後若補回附圖與描述 A–F，需重新核對 C/E/F 各自對應內容。

【錯誤選項解析】
A：錯。官方答案不是 A、C，因此描述 A 至少不屬於完整正確組合。
B：對。官方答案指定描述 C、E、F。
C：錯。包含描述 A/D，與官方答案不符。
D：錯。包含描述 D 且缺少 C，與官方答案不符。

【名詞解釋】
- Model Summary：模型摘要，顯示層、輸出形狀與參數量。
- CNN：卷積神經網路。
- Flatten：將特徵圖展平成向量。
- Dense：全連接層。
- Output Shape：每層輸出的張量形狀。

【記憶】
缺圖題先記：**官方答案 B = C、E、F；補回附圖後要再校準每個描述**。''',
'official_115_1_subject1_26':'''【考點】
Responsible AI 中的可解釋性。授信審核是高風險自動化決策，被拒絕申請人需要具體理由，核心能力就是 explainability，能說明哪些特徵如何影響決策。

【正解】
D。系統必須具備可解釋性能力，能提供特徵貢獻說明。

【為什麼】
金融授信涉及個人權益與監理要求。若 AI 拒絕貸款，申請人與監理單位需要知道理由，例如負債比、信用紀錄、收入穩定性、逾期紀錄等特徵如何影響結果。可解釋性可支援申訴、稽核、公平性檢查與合規文件。這不是要求速度、隨機性或 100% 準確率。

【錯誤選項解析】
A：錯。刪除個資是隱私/資料保存議題，不是提供拒絕理由的核心。
B：錯。隨機調整決策會降低一致性與合規性。
C：錯。任何模型都難保證 100% 準確率，且題目問理由說明。
D：對。特徵貢獻與決策理由屬於可解釋性。

【名詞解釋】
- Responsible AI：負責任 AI。
- Explainability：可解釋性。
- Feature Contribution：特徵貢獻。
- Adverse Action Reason：授信拒絕原因說明。
- Auditability：可稽核性。

【記憶】
授信拒絕題口訣：**「被拒要說原因，核心就是可解釋性」**。'''
}
for qid,exp in explanations.items(): byid[qid]['explanation']=exp
if isinstance(data,dict) and 'questions' in data:
    data['questions']=qs
    data.setdefault('meta',{})['last_explanation_fix']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
else: data=qs
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('updated explanations:', ', '.join(explanations))
