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
'official_114_2_subject1_21': '''【考點】
多模態 AI 在模態缺失（Missing Modality）情境下的魯棒性設計。題目關鍵字是「僅有影像但缺少文本」、「維持模型效能」，因此重點不是簡單填空或丟棄資料，而是讓模型在訓練與推論時就能適應某些模態不存在的狀況。

【正解】
B。訓練具備模態缺失感知能力的模型，使其適應缺失狀況。

【為什麼】
多模態模型通常整合影像、文字、語音、感測器等不同資料來源。真實場景中常會遇到某些模態缺失，例如有影像但沒有文字說明，或有文字但影像無法取得。最穩健的做法是在模型設計與訓練階段納入模態缺失情境，例如 modality dropout、缺失 mask、跨模態對齊或能動態選擇可用模態的架構，讓模型在部分輸入缺失時仍能合理推論。

【錯誤選項解析】
A：錯。零向量或固定向量填充雖然簡單，但容易讓模型誤判缺失模態的意義，也無法真正學會缺失情境下的推論策略。
B：對。讓模型具備模態缺失感知能力，能在訓練與推論時處理缺失，是維持效能最可靠的策略。
C：錯。生成模型補全缺失模態有時可用，但生成內容可能不準、成本高，也可能引入幻覺或偏差；題目問最有效維持效能，應優先選能適應缺失的模型設計。
D：錯。直接捨棄缺少模態的樣本會浪費資料，且在推論階段若遇到缺失仍無法處理。

【名詞解釋】
- 多模態 AI：同時整合文字、影像、語音、表格或感測器等多種資料模態的 AI。
- 模態缺失：某一種資料來源在訓練或推論時不存在或不可用。
- Modality Dropout：訓練時刻意隨機移除某些模態，提升模型對缺失模態的適應能力。
- Missing Modality Robustness：模型在部分模態缺失時仍能維持合理表現的能力。

【記憶】
多模態缺資料口訣：**「不要硬塞、不要全丟，要讓模型知道缺了什麼」**。看到缺少影像/文字/語音，優先想到缺失感知與魯棒訓練。''',

'official_114_2_subject1_15': '''【考點】
MLOps 中 Model Registry 的角色。題目問「Model Registry 最常用於哪一個階段」，重點是集中保存模型版本、訓練資訊、評估結果與部署狀態，而不是資料版本、運算資源或上線監控本身。

【正解】
C。用於集中管理模型版本、訓練紀錄與部署狀態。

【為什麼】
Model Registry 是 MLOps 流程中管理模型生命週期的重要元件。它通常記錄每個模型版本的來源、訓練參數、評估指標、模型檔案、審核狀態與部署環境，例如 staging、production、archived。團隊可透過 Model Registry 追蹤哪個模型已上線、哪個版本可回滾、哪個模型通過審核。

【錯誤選項解析】
A：錯。設定運算資源與執行環境較接近訓練平台、容器、排程器或基礎設施管理，不是 Model Registry 的主要用途。
B：錯。可重複使用的資料與特徵版本較接近 Feature Store 或資料版本管理，不是 Model Registry 的核心功能。
C：對。Model Registry 正是集中管理模型版本、訓練紀錄、評估結果與部署狀態。
D：錯。追蹤模型上線後表現與漂移屬於 Model Monitoring；Registry 可記錄部署狀態，但不是主要監控工具。

【名詞解釋】
- MLOps：將模型開發、訓練、部署、監控與維運工程化的流程。
- Model Registry：集中管理模型版本、訓練資訊、評估結果與部署狀態的系統。
- Feature Store：管理與重用特徵資料的系統。
- Model Monitoring：模型上線後監控效能、資料漂移與服務狀態。
- Rollback：模型出問題時切回先前穩定版本。

【記憶】
MLOps 工具分工：**Feature Store 管特徵，Model Registry 管模型版本，Monitoring 管上線表現**。看到「模型版本、訓練紀錄、部署狀態」就選 Model Registry。''',

'official_114_2_subject3_31': '''【考點】
Early Stopping 的正確使用方式，尤其是驗證集損失波動時如何設定 Patience。題目關鍵字是「訓練集損失持續下降」、「驗證集損失波動」、「最佳泛化能力」，因此應監控驗證集，而不是訓練集或測試集。

【正解】
B。監控驗證集損失並設定適度的耐心值（Patience），在連續多輪未改善後再停止訓練。

【為什麼】
Early Stopping 的目的是在模型開始過擬合前停止訓練，以保留泛化能力。判斷依據應是驗證集表現，因為驗證集用來模擬未見資料。若驗證損失因季節性或噪音而週期性波動，不能只看到一輪變差就停止，而要設定 Patience，允許模型有幾輪沒有改善；若連續多輪都沒有更好，再停止並保留最佳驗證表現的模型。

【錯誤選項解析】
A：錯。訓練集損失最低通常代表模型更擬合訓練資料，可能已經過擬合，不能保證泛化能力。
B：對。使用驗證集損失搭配 Patience，能避免因短期波動過早停止，也能控制過擬合。
C：錯。測試集應保留給最後一次客觀評估，不能拿來調整早停，否則會污染測試結果。
D：錯。合併所有資料後失去驗證依據，無法判斷泛化能力，也無法合理使用 Early Stopping。

【名詞解釋】
- Early Stopping：當驗證表現長時間沒有改善時停止訓練，以避免過擬合。
- Patience：容忍驗證指標連續多少輪未改善後才停止的設定。
- Validation Set：用於模型選擇、調參與早停判斷的資料集。
- Test Set：最後評估模型泛化能力的資料集，不應用於調參。
- Overfitting：模型過度擬合訓練資料，導致新資料表現變差。

【記憶】
早停口訣：**「看驗證，不看訓練；測試留最後；波動用 Patience」**。題目出現驗證集波動，就選監控驗證損失並設定耐心值。''',

'S3_17': '''【考點】
模型可解釋性（Explainable AI, XAI）工具的用途。SHAP 和 LIME 都是用來說明黑箱模型為什麼做出某個預測，幫助使用者理解特徵對結果的影響。

【正解】
B。解釋模型預測結果，提升可解釋性。

【為什麼】
SHAP 與 LIME 都屬於模型解釋工具。SHAP 以 Shapley value 觀念估計每個特徵對預測結果的貢獻；LIME 則在單一樣本附近建立一個簡單可解釋的局部模型，近似黑箱模型在該點附近的行為。兩者主要目的是讓人理解模型判斷依據，支援除錯、稽核、信任與風險管理。

【錯誤選項解析】
A：錯。SHAP 和 LIME 不會讓模型訓練更快；它們是在模型訓練後或預測後用來解釋結果。
B：對。兩者都用於解釋模型預測結果，提升可解釋性。
C：錯。自動標注訓練資料屬於資料標註、弱監督或主動學習等議題，不是 SHAP/LIME 的主要功能。
D：錯。防止資料外洩需要隱私保護、加密、存取控管或差分隱私；SHAP/LIME 主要處理可解釋性。

【名詞解釋】
- XAI：Explainable AI，可解釋 AI，讓人理解模型決策依據的方法。
- SHAP：用 Shapley value 估計各特徵對預測結果的貢獻。
- LIME：用局部簡單模型近似黑箱模型，解釋單一預測。
- 黑箱模型：內部決策邏輯不易直接理解的模型，例如深度學習或複雜集成模型。
- Local Explanation：針對單一樣本預測原因的解釋。

【記憶】
SHAP / LIME 口訣：**「不是加速、不是防洩漏，是解釋為什麼這樣預測」**。看到 SHAP、LIME，直接聯想到可解釋性。''',

'S1_12': '''【考點】
AI 專案可行性評估中的技術前提。題目問「技術層面最關鍵的前提條件」，重點是資料是否足夠、品質是否良好、是否能支撐模型訓練與評估。

【正解】
B。有足夠且高品質的訓練資料。

【為什麼】
AI 模型的表現高度依賴資料。若資料量不足、品質差、標註錯誤、欄位缺漏、代表性不足或和實際應用場景不一致，即使使用再先進的演算法，也很難得到可靠模型。因此企業在評估 AI 導入可行性時，技術面最基本的門檻是是否擁有足夠且高品質的訓練資料。

【錯誤選項解析】
A：錯。企業規模大不代表資料品質好，也不代表 AI 專案技術上可行；小公司若有高品質資料也能導入 AI。
B：對。足夠且高品質的訓練資料是模型訓練與評估的核心前提。
C：錯。有自己的 AI 研究部門不是必要條件；可透過外部顧問、雲端服務或既有工具導入，但資料仍是基本門檻。
D：錯。競爭對手已導入 AI 只能說明市場趨勢，不能證明本企業資料、流程與技術條件足夠。

【名詞解釋】
- AI 可行性評估：評估問題是否適合 AI、資料是否足夠、技術是否可行、效益是否合理的過程。
- 訓練資料：用來讓模型學習規律與參數的資料。
- 資料品質：資料的正確性、完整性、一致性、代表性與標註品質。
- 標註資料：包含正確答案或分類標籤的資料，常用於監督式學習。
- Garbage In, Garbage Out：輸入資料品質差，模型輸出也會差。

【記憶】
AI 導入先問三件事：**「有沒有資料、資料好不好、資料能不能代表真實情境」**。技術可行性不是看公司大不大，而是看資料能不能支撐模型。'''
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
