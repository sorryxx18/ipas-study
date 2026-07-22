#!/usr/bin/env python3
import json
import pathlib
import datetime

base = pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path = base / 'questions.json'
data = json.loads(path.read_text())
questions = data['questions'] if isinstance(data, dict) and 'questions' in data else data
byid = {q['id']: q for q in questions}

# Repair obvious option contamination in this question.
byid['official_114_2_subject3_41']['options']['D'] = 'A_and_B.sum() / B.sum()'

explanations = {
'S1_08': '''【考點】
Transformer 架構的核心機制。題目問「核心機制」，重點是 Transformer 不靠 RNN 的遞迴，也不是 CNN 的卷積，而是透過 Self-Attention 讓序列中各 token 彼此建立關聯。

【正解】
C。自注意力機制（Self-Attention）。

【為什麼】
Transformer 的核心設計是 Self-Attention。它讓每個 token 都能根據 Query、Key、Value 計算和其他 token 的關聯權重，進而整合整個序列的上下文資訊。這使 Transformer 能有效處理長距離依賴，也比傳統 RNN 更容易平行化訓練。

【錯誤選項解析】
A：錯。卷積運算是 CNN 的核心，常用於影像與局部特徵擷取，不是 Transformer 的核心。
B：錯。遞迴結構是 RNN / LSTM / GRU 的特色；Transformer 的優勢之一就是不依賴遞迴傳遞。
C：對。Self-Attention 是 Transformer 的核心機制，能讓序列中每個 token 關注其他 token。
D：錯。決策樹分裂是樹模型的概念，和 Transformer 架構無關。

【名詞解釋】
- Transformer：以 Self-Attention 為核心的深度學習架構，常用於 NLP 與生成式 AI。
- Self-Attention：序列中每個 token 和其他 token 計算關聯權重的機制。
- Token：模型處理文字時的基本單位，可是字、詞或子詞。
- RNN：以遞迴方式逐步處理序列的神經網路。
- CNN：以卷積擷取局部特徵的神經網路。

【記憶】
Transformer 口訣：**「不遞迴、不卷積，核心是自注意力」**。看到 Transformer 核心機制，直接選 Self-Attention。''',

'official_114_2_subject3_41': '''【考點】
條件機率公式與 Monte Carlo 模擬計數。題目定義事件 A 為擲出偶數，事件 B 為擲出大於 3，要求 P(A∣B)，所以分母必須是事件 B 發生的次數。

【正解】
D。A_and_B.sum() / B.sum()。

【為什麼】
條件機率公式為 P(A∣B) = P(A ∩ B) / P(B)。在 Monte Carlo 模擬中，A_and_B.sum() 代表同時滿足 A 與 B 的次數，B.sum() 代表 B 發生的次數。因此 P(A∣B) 應寫成 A_and_B.sum() / B.sum()。以骰子來看，B = {4,5,6}，其中同時為偶數的是 {4,6}，所以理論值為 2/3。

【錯誤選項解析】
A：錯。A.sum() * B.sum() 是兩個事件次數相乘，不符合條件機率公式，分母會被放大。
B：錯。A.sum() + B.sum() 是事件次數相加，也不是條件機率的分母。
C：錯。A_and_B.sum() / A.sum() 是 P(B∣A)，不是 P(A∣B)。它把條件事件放反了。
D：對。P(A∣B) 的分母是 B 發生的次數，因此為 A_and_B.sum() / B.sum()。

【名詞解釋】
- 條件機率：在事件 B 已發生的條件下，事件 A 發生的機率。
- P(A∣B)：A given B，公式為 P(A ∩ B) / P(B)。
- Monte Carlo 方法：用大量隨機模擬估計機率或數值的方法。
- A_and_B：同時滿足事件 A 和事件 B 的布林條件或計數。
- 布林遮罩：用 True/False 表示資料是否符合條件的陣列。

【記憶】
條件機率口訣：**「問 A given B，分母一定是 B」**。看到 P(A∣B)，不要把 A 和 B 放反。''',

'official_114_2_subject1_37': '''【考點】
大型模型訓練時的 GPU 記憶體壓力處理。題目限制「模型架構固定、不能更換硬體、要維持效能與收斂品質」，因此應降低單卡負載並分散資料，而不是刪資料、亂調學習率或污染測試集。

【正解】
B。採用較小的批次大小（Batch Size）並搭配資料分片（Data Sharding）分散訓練負載。

【為什麼】
訓練大型語音合成模型時，GPU 記憶體主要受模型參數、梯度、activation 與 batch size 影響。在模型架構不能改、硬體不能換的情況下，降低 batch size 可直接減少單次前向/反向傳播所需記憶體；Data Sharding 則能將資料分散到多台 GPU 或多個 worker，降低單一裝置負擔並維持分散式訓練效率。

【錯誤選項解析】
A：錯。減少訓練資料量可能傷害模型泛化能力，且不一定解決單次 batch 記憶體不足問題。
B：對。較小 batch size 能降低單卡記憶體，資料分片能分散訓練負載，是最合理的工程策略。
C：錯。增加學習率和記憶體壓力無直接關係，還可能造成訓練不穩或發散。
D：錯。測試資料集不能拿來訓練，否則會造成資料洩漏，破壞最終評估公正性。

【名詞解釋】
- Batch Size：每次訓練更新使用的樣本數；越大通常越耗 GPU 記憶體。
- Data Sharding：將資料切分到不同裝置或節點，以分散訓練負載。
- GPU Memory：儲存模型參數、梯度、activation 與 batch 資料的記憶體。
- Distributed Training：用多張 GPU 或多台機器共同訓練模型。
- Test Set：最終評估模型泛化能力的資料，不應參與訓練。

【記憶】
GPU 爆記憶體口訣：**「先降 batch，再分資料；別動測試集」**。題目限制不能換硬體或模型，就選 batch size / sharding 類方法。''',

'official_115_1_subject1_11': '''【考點】
Self-Attention 的核心功能。題目問的是 Transformer 中自注意力如何建模長距離依賴，重點是每個 token 能和序列中其他 token 建立關聯並分配權重。

【正解】
B。讓序列中每個 token 能與其他所有 token 建立關聯，並根據重要性分配權重。

【為什麼】
Self-Attention 會為序列中的每個 token 計算它和其他 token 的關聯程度，並依重要性加權整合資訊。這讓模型能直接捕捉遠距離關係，例如句首詞和句尾詞之間的語意依賴，而不必像 RNN 一樣逐步傳遞隱藏狀態。因此 Self-Attention 是 Transformer 能處理長距離依賴與平行化訓練的核心。

【錯誤選項解析】
A：錯。這描述的是 RNN 類模型透過 hidden state 遞迴傳遞上下文，不是 Self-Attention。
B：對。Self-Attention 的核心就是 token 之間互相關注並分配權重。
C：錯。局部運算較接近 CNN 或局部卷積；Self-Attention 可關注整個序列，不限相鄰詞。
D：錯。把整個序列壓縮為固定長度表示較接近早期 encoder 或 pooling 概念，不是 Self-Attention 的核心功能。

【名詞解釋】
- Self-Attention：序列內 token 彼此計算注意力權重的機制。
- Token：文字或序列被模型切分後的基本單位。
- Attention Weight：模型分配給不同 token 的重要性權重。
- Long-range Dependency：序列中距離很遠的元素仍互相關聯的現象。
- RNN：透過遞迴逐步處理序列的模型。

【記憶】
Self-Attention 口訣：**「每個 token 看所有 token，再決定誰重要」**。看到長距離依賴與權重分配，就選 Self-Attention。''',

'official_114_2_subject3_27': '''【考點】
激活函數的非線性作用。題目說使用線性激活函數後模型訓練準確率停滯，懷疑無法學到複雜特徵，因此要改用非線性激活函數，典型答案是 ReLU。

【正解】
D。改用 ReLU（Rectified Linear Unit）激活函數，以引入非線性並提升模型表達能力。

【為什麼】
如果神經網路各層都只使用線性激活函數，多層線性轉換疊在一起仍等價於一個線性模型，無法有效學習複雜非線性特徵。ReLU 能引入非線性，讓深度網路學習更複雜的函數關係，且相較 Sigmoid 在深層網路中較不容易出現嚴重梯度消失，因此常作為隱藏層激活函數。

【錯誤選項解析】
A：錯。只增加卷積層但仍使用線性激活，多層線性組合仍難以表達複雜非線性；關鍵是要引入非線性。
B：錯。灰階化可能降低輸入維度或運算量，但不解決模型缺乏非線性表達能力的問題。
C：錯。Sigmoid 也能引入非線性，但在深層網路中容易梯度消失；題目要改善深度模型表達與訓練，ReLU 更合適。
D：對。ReLU 能引入非線性並提升模型表達能力，是常用且合適的調整。

【名詞解釋】
- Activation Function：激活函數，讓神經網路具備非線性表達能力。
- ReLU：輸出 max(0, x) 的激活函數，常用於深度網路隱藏層。
- 線性激活：不引入非線性，多層堆疊仍可能等價於單層線性模型。
- Gradient Vanishing：梯度消失，深層網路訓練時梯度變得太小而難以更新。
- Model Expressiveness：模型表達複雜函數或特徵關係的能力。

【記憶】
激活函數口訣：**「沒有非線性，深層也像線性」**。題目說線性激活學不動，就選 ReLU 引入非線性。'''
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
print('repaired option D for official_114_2_subject3_41')
