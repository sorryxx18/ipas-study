#!/usr/bin/env python3
import json
import pathlib
import datetime

base = pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
guide_path = base / 'guide_s3.json'
state_path = base / 'rewrite_state.json'

guide = json.loads(guide_path.read_text())
state = json.loads(state_path.read_text())

contents = {
71: '''# Attention Mechanism 注意力機制

## 1. 核心概念

**注意力機制（Attention Mechanism）** 是讓模型在處理一串輸入時，能動態決定「目前應該重點看哪一部分」的技術。它最早在序列到序列任務中被廣泛使用，後來成為 Transformer 與大型語言模型的核心概念。

在傳統 RNN / LSTM 中，模型通常把前面資訊壓縮進隱藏狀態，當序列很長時，早期資訊容易被淡忘。注意力機制解決的問題是：不要把所有資訊平均看待，而是根據目前任務，給不同位置不同權重。例如翻譯句子時，產生某個目標詞時，模型會更關注來源句中最相關的詞。

注意力機制的直覺可以用三個角色理解：**Query（查詢）** 代表目前要找什麼；**Key（鍵）** 代表每個輸入位置可被比對的索引；**Value（值）** 代表真正要取出的資訊。模型會計算 Query 和各個 Key 的相似度，經過 softmax 得到注意力權重，再用這些權重加總 Value。

在科目三中，重點不是背複雜公式，而是理解 Attention 的功能：處理長距離依賴、讓模型聚焦重要位置、支援平行化，並成為 Transformer 取代 RNN 的關鍵基礎。

## 2. 考試重點

- **核心目的**：讓模型根據任務動態關注輸入序列中重要位置，而不是平均處理全部資訊。
- **解決問題**：改善長序列中資訊遺失與長距離依賴難以捕捉的問題。
- **Query / Key / Value**：Query 問「我要找什麼」，Key 用來比對相關性，Value 是被加權取出的內容。
- **注意力權重**：通常由相似度分數經 softmax 轉成機率分布，權重越高表示越重要。
- **Self-Attention**：同一序列內部不同位置彼此互相關注，是 Transformer 的核心。
- **和 RNN 差異**：Attention 可直接連結遠距位置，Transformer 也能平行處理序列。
- **可解釋性限制**：注意力權重可提供線索，但不一定等於完整因果解釋。
- **常見應用**：機器翻譯、文本摘要、問答、語音、影像與多模態模型。

## 3. 名詞解釋

- **注意力機制（Attention Mechanism）**：根據相關性分配權重，讓模型聚焦重要資訊的技術。
- **Query（查詢）**：目前位置或任務想要尋找的資訊表示。
- **Key（鍵）**：每個輸入位置供 Query 比對相關性的表示。
- **Value（值）**：被注意力權重加總後輸出的資訊內容。
- **Self-Attention（自注意力）**：同一序列內部各位置互相關注的注意力機制。
- **Softmax**：將分數轉成總和為 1 的權重分布的函數。

## 4. 常見陷阱

**陷阱1：以為 Attention 只是可視化工具**
> ❌ 誤解：Attention 的主要用途是畫出模型看哪裡。  
> ✅ 正確：Attention 是模型運算機制，用來加權整合資訊，可視化只是附帶分析方式。

**陷阱2：把 Query / Key / Value 當資料庫欄位**
> ❌ 誤解：Q、K、V 是人工定義的欄位名稱。  
> ✅ 正確：它們是由模型學出的向量表示，用來計算相關性與取出資訊。

**陷阱3：以為注意力權重等於絕對解釋**
> ❌ 誤解：權重最高的位置就是模型決策唯一原因。  
> ✅ 正確：注意力權重可提供參考，但不能完整代表模型所有內部推理。

**陷阱4：以為 Attention 只能用在 NLP**
> ❌ 誤解：Attention 只適用文字。  
> ✅ 正確：Attention 也可用於影像、語音、時間序列與多模態任務。

## 5. 考題怎麼問

**問法1：問長序列中如何捕捉遠距關係**  
→ 答注意力機制或 Self-Attention。

**問法2：問 Q、K、V 的角色**  
→ Query 用來查詢，Key 用來比對，Value 是加權輸出內容。

**問法3：問 Transformer 為何能取代 RNN**  
→ 答 Self-Attention 可捕捉長距依賴並支援平行運算。

**問法4：問注意力權重代表什麼**  
→ 答不同輸入位置對目前輸出的相對重要性。

## 6. 記憶口訣

- **「Q 問、K 配、V 取」**：Query 問要找什麼，Key 配對，Value 被取出。
- **「不是全都看，是重點看」**：Attention 的核心是加權聚焦。
- **「Self-Attention 讓字跟字互看」**：同一句內各位置彼此建立關係。

## 7. 官方指引對應線索

此主題屬於科目三深度學習、序列模型與 Transformer 架構範圍。考試常從 RNN 長距依賴限制、Query-Key-Value、Self-Attention 與 Transformer 優勢命題，要求理解注意力機制如何讓模型聚焦重要資訊並支援平行化。''',
72: '''# Transformer 架構

## 1. 核心概念

**Transformer** 是以 Self-Attention 為核心的深度學習架構，最早在自然語言處理任務中大幅提升機器翻譯效果，後來成為 BERT、GPT 與多數大型語言模型的基礎。它的重要性在於：不再依賴 RNN 逐步處理序列，而是透過注意力機制一次建模序列中所有位置的關係。

Transformer 的基本結構包含**編碼器（Encoder）**與**解碼器（Decoder）**。Encoder 負責讀入輸入序列並建立上下文表示；Decoder 負責根據已生成內容與 Encoder 輸出逐步產生目標序列。BERT 主要使用 Encoder 架構，適合理解任務；GPT 主要使用 Decoder 架構，適合生成任務。

Transformer 的關鍵元件包括：**Multi-Head Attention**、**Positional Encoding**、**Feed-Forward Network**、**Residual Connection** 與 **Layer Normalization**。由於 Self-Attention 本身不含順序概念，所以必須加入位置編碼讓模型知道詞序。

科目三考 Transformer 時，通常不是要求完整推導公式，而是要求理解它為什麼比 RNN 更適合長序列與大規模訓練：可平行化、能捕捉長距依賴、可透過多頭注意力同時學不同關係。

## 2. 考試重點

- **核心技術**：Transformer 以 Self-Attention 為核心，不依賴 RNN 逐步傳遞隱藏狀態。
- **平行化優勢**：序列各位置可同時計算，訓練效率優於 RNN / LSTM。
- **長距依賴**：Self-Attention 可直接連結序列中遠距位置。
- **位置編碼必要性**：Attention 本身不懂順序，所以需要 Positional Encoding。
- **Encoder / Decoder 分工**：Encoder 做理解與表示；Decoder 做生成。
- **Multi-Head Attention**：多個注意力頭可從不同角度學習關係。
- **BERT vs GPT**：BERT 偏 Encoder、雙向理解；GPT 偏 Decoder、自回歸生成。
- **主要成本**：Self-Attention 計算量隨序列長度增加，長文本成本高。

## 3. 名詞解釋

- **Transformer**：以 Self-Attention 為核心的序列建模架構。
- **Encoder（編碼器）**：將輸入序列轉成上下文表示的模組。
- **Decoder（解碼器）**：根據上下文與已生成內容產生輸出序列的模組。
- **Multi-Head Attention（多頭注意力）**：同時使用多組注意力頭學習不同關係。
- **Positional Encoding（位置編碼）**：加入詞序資訊，彌補 Attention 不含順序的限制。
- **Residual Connection（殘差連接）**：讓訊息跨層傳遞，改善深層模型訓練穩定性。

## 4. 常見陷阱

**陷阱1：以為 Transformer 完全不需要順序資訊**
> ❌ 誤解：Transformer 不處理詞序。  
> ✅ 正確：Self-Attention 本身不含順序，需靠位置編碼補充順序資訊。

**陷阱2：把 BERT 和 GPT 架構混為一談**
> ❌ 誤解：BERT 和 GPT 都是同一種用法。  
> ✅ 正確：BERT 主要用 Encoder 做理解；GPT 主要用 Decoder 做生成。

**陷阱3：以為 Transformer 一定比所有模型都好**
> ❌ 誤解：任何資料都應該用 Transformer。  
> ✅ 正確：Transformer 強大但成本高，資料量、任務、硬體與延遲都要考量。

**陷阱4：忽略長序列計算成本**
> ❌ 誤解：Transformer 處理長文本沒有代價。  
> ✅ 正確：Self-Attention 通常會隨序列長度帶來較高記憶體與計算成本。

## 5. 考題怎麼問

**問法1：問 Transformer 核心機制**  
→ 答 Self-Attention / Multi-Head Attention。

**問法2：問為什麼能平行訓練**  
→ 答不需像 RNN 逐步處理，可同時計算序列位置關係。

**問法3：問位置編碼作用**  
→ 答補充詞序資訊，因為 Attention 本身不具順序概念。

**問法4：問 BERT / GPT 差異**  
→ BERT 偏理解、Encoder；GPT 偏生成、Decoder / 自回歸。

## 6. 記憶口訣

- **「Transformer 靠注意力，不靠逐步記憶」**：和 RNN 最大差別。
- **「沒有位置編碼，字就沒有順序」**：位置資訊是必考點。
- **「BERT 讀懂，GPT 續寫」**：理解型與生成型模型的直覺分法。

## 7. 官方指引對應線索

此主題屬於科目三深度學習、自然語言處理與大型模型架構範圍。考試常從 Self-Attention、位置編碼、Encoder/Decoder、BERT/GPT 差異與 Transformer 相對 RNN 的優勢命題，重點是理解架構角色與適用限制。''',
73: '''# BERT

## 1. 核心概念

**BERT（Bidirectional Encoder Representations from Transformers）** 是以 Transformer Encoder 為基礎的預訓練語言模型，特色是能利用上下文雙向理解文字。它不像傳統單向語言模型只看左邊或右邊，而是同時考慮詞彙前後文，因此特別適合文本理解任務。

BERT 的核心訓練方式是**遮罩語言模型（Masked Language Modeling, MLM）**：在句子中隨機遮住部分詞，讓模型根據上下文預測被遮住的詞。早期 BERT 也使用下一句預測（Next Sentence Prediction, NSP）來學習句子關係。透過大規模預訓練後，BERT 可再針對分類、問答、命名實體辨識、語意相似度等任務微調。

BERT 的重要性在於把「預訓練 + 微調」變成 NLP 主流流程。企業不一定要從零訓練語言模型，而是可以使用預訓練 BERT，再用少量領域資料微調到特定任務，例如金融文件分類、客服意圖辨識、醫療文本標註。

科目三考 BERT 時，重點在於它使用 Transformer Encoder、雙向上下文、MLM 預訓練，以及適合理解型任務；不要把它和 GPT 的自回歸生成架構混淆。

## 2. 考試重點

- **架構基礎**：BERT 使用 Transformer Encoder，不是 Decoder。
- **雙向上下文**：能同時利用詞彙左側與右側上下文進行理解。
- **MLM 訓練**：隨機遮住詞，讓模型根據上下文預測被遮住的詞。
- **預訓練 + 微調**：先用大量語料預訓練，再用任務資料微調。
- **適合任務**：文本分類、問答、命名實體辨識、語意相似度、情感分析。
- **不擅長原生長篇生成**：BERT 主要是理解模型，不是像 GPT 一樣逐字生成長文。
- **和 GPT 差異**：BERT 雙向理解；GPT 自回歸生成。
- **導入限制**：需考量領域語料、微調資料、算力、模型大小與延遲。

## 3. 名詞解釋

- **BERT**：基於 Transformer Encoder 的雙向預訓練語言模型。
- **Transformer Encoder**：負責將輸入文字轉換成上下文表示的架構。
- **遮罩語言模型（MLM）**：遮住部分詞，要求模型預測被遮住內容的訓練方法。
- **微調（Fine-tuning）**：在預訓練模型基礎上，用特定任務資料再訓練。
- **命名實體辨識（NER）**：辨識文本中的人名、地名、組織、日期等實體。
- **語意表示（Semantic Representation）**：模型產生的上下文語意向量。

## 4. 常見陷阱

**陷阱1：把 BERT 當成文字生成模型**
> ❌ 誤解：BERT 主要用來像 GPT 一樣生成長篇文章。  
> ✅ 正確：BERT 主要適合理解型任務，例如分類、問答、NER。

**陷阱2：忽略雙向上下文特色**
> ❌ 誤解：BERT 只看前面的詞來預測下一個詞。  
> ✅ 正確：BERT 透過 MLM 同時利用左右上下文。

**陷阱3：把 BERT 和 Transformer 完全切開**
> ❌ 誤解：BERT 是和 Transformer 無關的模型。  
> ✅ 正確：BERT 是建立在 Transformer Encoder 上的預訓練模型。

**陷阱4：以為預訓練模型不用領域調整**
> ❌ 誤解：拿通用 BERT 就能完美處理所有專業文本。  
> ✅ 正確：金融、醫療、法律等領域通常仍需要領域資料微調或專門模型。

## 5. 考題怎麼問

**問法1：問 BERT 架構**  
→ 答 Transformer Encoder。

**問法2：問 BERT 的訓練任務**  
→ 答 Masked Language Modeling，根據上下文預測被遮住的詞。

**問法3：問 BERT 適合哪類任務**  
→ 答文本理解、分類、問答、NER、語意相似度。

**問法4：問 BERT 和 GPT 差異**  
→ BERT 雙向理解；GPT 自回歸生成。

## 6. 記憶口訣

- **「BERT 讀懂上下文，GPT 接著往下寫」**：分辨理解與生成。
- **「遮住再猜，是 BERT 的預訓練」**：MLM 是核心。
- **「BERT 是 Encoder 派」**：看到 Encoder、雙向、理解任務就想到 BERT。

## 7. 官方指引對應線索

此主題屬於科目三 Transformer、預訓練語言模型與 NLP 應用範圍。考試常從 BERT 的 Encoder 架構、雙向上下文、MLM、預訓練與微調流程，以及 BERT 和 GPT 的差異命題。'''
}

for seg in guide['segments']:
    if seg.get('id') in contents:
        seg['content'] = contents[seg['id']]

comp = set(state['s3'].get('completed', []))
fail = set(state['s3'].get('failed', []))
for i in (71, 72, 73):
    comp.add(i)
    fail.discard(i)
state['s3']['completed'] = sorted(comp)
state['s3']['failed'] = sorted(fail)
ft = {str(k): v for k, v in state['s3'].get('failedTitles', {}).items()}
for i in (71, 72, 73):
    ft.pop(str(i), None)
state['s3']['failedTitles'] = ft
state['lastUpdated'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')

guide_path.write_text(json.dumps(guide, ensure_ascii=False, indent=2))
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
print('updated S3 ids 71,72,73 directly by Hermes; no Claude Code subprocess used')
