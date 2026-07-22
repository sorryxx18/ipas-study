#!/usr/bin/env python3
import json
import pathlib
import datetime

base = pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
path = base / 'questions.json'
data = json.loads(path.read_text())
questions = data['questions'] if isinstance(data, dict) and 'questions' in data else data
byid = {q['id']: q for q in questions}

explanations = {
'official_115_1_subject1_15': '''【考點】
多代理人（Multi-Agent）系統的容錯設計與 Orchestrator 職責。題目關鍵字是「Worker 回傳品質不符合預期」、「系統容錯」、「任務可靠性」，因此重點不是讓所有模型一致，而是要有結果評估、重試、重新分派與失敗紀錄。

【正解】
B。Orchestrator 具備結果評估能力，對不合格結果觸發重試（Retry）或重新分配給不同 Worker，並記錄失敗原因供後續改善。

【為什麼】
在多代理人架構中，Orchestrator 不只是把任務丟給 Worker，更要負責任務拆解、結果檢查、錯誤處理與流程收斂。當某個 Worker 輸出品質不佳時，可靠做法是由 Orchestrator 判斷結果是否合格，必要時重試、改派其他 Worker，並記錄失敗原因，才能避免單一 Worker 失誤導致整體任務失敗。

【錯誤選項解析】
A：錯。直接採用品質不合格的輸出雖可降低延遲，但犧牲正確性與可靠性，和題目要求的「容錯」相反。
B：對。包含結果評估、Retry、重新分配與失敗紀錄，完整對應容錯與任務可靠性。
C：錯。統一使用相同 LLM 可能降低輸出差異，但不能保證品質，也沒有處理 Worker 失敗或結果不合格的機制。
D：錯。任何 Worker 失敗就中止任務，缺乏容錯能力；可靠系統應先嘗試重試、替代路徑或降級處理。

【名詞解釋】
- Multi-Agent System：由多個代理人協作或分工完成任務的系統。
- Orchestrator Agent：負責任務規劃、分派、協調、結果檢查與錯誤處理的代理人。
- Worker Agent：負責執行特定子任務的代理人。
- Retry：任務失敗或品質不足時重新嘗試執行。
- Fault Tolerance：系統在部分元件失敗時仍能維持功能或完成任務的能力。

【記憶】
多代理人容錯口訣：**「評估結果 → 重試 / 改派 → 記錄原因」**。看到 Orchestrator 與 Worker 品質不穩，優先選能檢查、重試、改派的機制。''',

'official_114_2_subject1_22': '''【考點】
資料漂移（Data Drift）的偵測方法。題目已明確說「輸入特徵分佈與原始訓練資料不同」，問的是如何偵測並確認分佈是否變化，因此要選比較分佈差異的統計方法。

【正解】
D。計算輸入特徵分佈間的 KL 散度（KL Divergence）。

【為什麼】
Data Drift 指模型上線後，輸入資料的機率分佈和訓練時不同。要確認分佈是否改變，應比較訓練期與上線期特徵分佈的差異。KL Divergence 可衡量兩個機率分佈的差距，因此最符合「偵測並確認資料分佈是否發生變化」。

【錯誤選項解析】
A：錯。定期重新訓練可能是發現漂移後的應對策略，但題目問的是「偵測並確認分佈是否變化」，不是問修復方法。
B：錯。提升模型複雜度不會直接偵測資料分佈差異，反而可能增加過擬合風險。
C：錯。增加測試資料量可能讓評估更穩，但不能直接判斷目前輸入分佈是否和訓練分佈不同。
D：對。KL Divergence 是比較兩個機率分佈差異的方式，可用於資料漂移偵測。

【名詞解釋】
- Data Drift：上線後輸入特徵分佈和訓練資料分佈不同。
- Concept Drift：輸入特徵與標籤之間的關係改變，即使輸入分佈相似，模型也可能失準。
- KL Divergence：衡量兩個機率分佈差異的指標，常用於分佈變化偵測。
- Model Monitoring：模型上線後追蹤資料、效能與服務狀態的流程。

【記憶】
題目問「分佈有沒有變」→ 選分佈距離，例如 KL Divergence。題目問「變了怎麼辦」→ 才考慮重訓、調整模型或資料管線。''',

'official_114_2_subject3_17': '''【考點】
優化演算法中的動量（Momentum）概念，特別是 Adam 的一階矩估計。題目關鍵字是「內建動量的設計機制」，要分辨 Adam、RMSProp、Adagrad 與 SGD+Momentum 的定位。

【正解】
B。Adam。

【為什麼】
Adam（Adaptive Moment Estimation）同時使用一階矩估計與二階矩估計。一階矩估計可視為梯度的指數移動平均，具有 momentum-like 的效果；二階矩估計則類似 RMSProp 對平方梯度做自適應調整。因此 Adam 內建了動量概念與自適應學習率調整，是本題答案。

【錯誤選項解析】
A：錯。SGD+Momentum 確實使用 Momentum，但它是「在 SGD 外加 Momentum 的變體」；題目問的是哪種優化演算法內建動量設計，官方答案指向 Adam 內建一階矩估計。
B：對。Adam 內建一階矩（momentum-like）與二階矩估計，是自適應動量估計演算法。
C：錯。RMSProp 主要追蹤平方梯度的移動平均，用於自適應調整學習率；它不是以一階動量為主要設計。
D：錯。Adagrad 會累積歷史梯度平方，讓常出現的特徵學習率下降，但沒有內建 momentum 概念。

【名詞解釋】
- Momentum：利用過去梯度方向的累積，讓更新方向更平滑，減少震盪。
- Adam：Adaptive Moment Estimation，結合一階矩與二階矩估計的優化器。
- RMSProp：利用平方梯度移動平均調整各參數學習率。
- Adagrad：根據歷史梯度平方累積調整學習率，適合稀疏特徵但學習率可能快速變小。

【記憶】
Adam = **Momentum + RMSProp 的直覺組合**：一階矩像 Momentum，二階矩像 RMSProp。看到「內建動量 / adaptive moment」優先想到 Adam。''',

'official_114_2_subject3_18': '''【考點】
XGBoost 相對傳統 GBDT 的技術改進。題目要求「同時反映主要技術改進」，要選出正則化、缺失值處理與並行化這組 XGBoost 特色。

【正解】
A。引入正則化項（Regularization）以抑制過擬合，並支援缺失值自動處理與並行化訓練。

【為什麼】
XGBoost 是對梯度提升決策樹（GBDT）的工程與演算法強化版本。它在目標函數中加入正則化項以控制模型複雜度、降低過擬合；支援缺失值自動學習預設方向；並透過並行化、快取最佳化等方式提升訓練效率。這些都是 XGBoost 相對傳統 GBDT 的代表性改進。

【錯誤選項解析】
A：對。正則化、缺失值處理、並行化訓練都是 XGBoost 的重要特色。
B：錯。XGBoost 仍是 boosting 的樹模型，不是改成 Random Forest。Random Forest 屬於 bagging 架構。
C：錯。XGBoost 的弱學習器通常仍是決策樹，不是用神經網路取代弱分類器。
D：錯。Batch Normalization 常見於深度神經網路訓練，不是 XGBoost 相對 GBDT 的主要改進。

【名詞解釋】
- GBDT：Gradient Boosting Decision Tree，逐步訓練多棵樹修正前一輪殘差的 boosting 方法。
- XGBoost：eXtreme Gradient Boosting，強化版梯度提升樹，加入正則化、缺失值處理與高效訓練實作。
- Regularization：限制模型複雜度，降低過擬合風險。
- Missing Value Handling：模型自動學習缺失值往哪個分支走。
- Parallelization：利用平行化提升訓練效率。

【記憶】
XGBoost 常考三件事：**正則化防過擬合、缺失值自動處理、訓練效率高**。看到 Random Forest、Neural Network、BatchNorm 通常是混淆選項。''',

'S3_04': '''【考點】
集成學習方法的分類：Bagging、Boosting、Stacking 與 Voting。題目問 Random Forest 使用哪種集成技術，關鍵是「多棵決策樹 + bootstrap 抽樣 + 投票 / 平均」。

【正解】
C。Bagging。

【為什麼】
Random Forest 是 Bagging 的典型代表。它會從訓練資料中進行 bootstrap sampling，訓練多棵決策樹；每棵樹也會在分裂時隨機選取部分特徵。分類時用多數決投票，迴歸時用平均。這樣能降低單棵決策樹高變異、容易過擬合的問題。

【錯誤選項解析】
A：錯。Boosting 是逐步訓練模型，讓後面的模型修正前面模型錯誤，例如 AdaBoost、GBDT、XGBoost；Random Forest 不是 Boosting。
B：錯。Stacking 是訓練多個不同模型後，再用另一個 meta-model 學習如何整合輸出；Random Forest 沒有這種第二層 meta-model。
C：對。Random Forest 使用 Bagging，也就是 Bootstrap Aggregating。
D：錯。Voting only 只描述最後投票整合的動作，沒有說明 Random Forest 的核心 bootstrap 抽樣與多樹訓練機制。

【名詞解釋】
- Random Forest：隨機森林，由多棵決策樹組成的集成模型。
- Bagging：Bootstrap Aggregating，透過重抽樣訓練多個模型，再投票或平均。
- Bootstrap Sampling：從資料集中有放回抽樣產生多個訓練子集。
- Boosting：序列式訓練弱模型，逐步修正錯誤。
- Stacking：用第二層模型整合多個基模型輸出。

【記憶】
Random Forest = **Bagging + 隨機特徵 + 多樹投票**。看到「隨機森林」先選 Bagging，不要只看到投票就選 Voting。'''
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
