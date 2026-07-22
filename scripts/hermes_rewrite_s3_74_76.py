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
74: '''# GPT 系列

## 1. 核心概念

**GPT（Generative Pre-trained Transformer）** 是以 Transformer Decoder 為基礎的生成式語言模型系列。它的核心任務是根據前文預測下一個 token，因此能進行文章續寫、摘要、問答、程式碼生成、對話與多種文字生成任務。

GPT 的訓練流程通常包含大規模預訓練與後續對齊。預訓練階段使用大量文字資料學習語言規律與世界知識；後續可透過指令微調、RLHF 或其他偏好學習方式，讓模型更符合人類指令、對話格式與安全要求。和 BERT 不同，GPT 是自回歸模型，產生文字時會一步一步往後生成。

在科目三中，GPT 系列常和 Transformer、BERT、生成式 AI 與大型語言模型（LLM）一起考。重點是理解它的架構定位：GPT 偏 Decoder、單向自回歸、適合生成；BERT 偏 Encoder、雙向理解、適合分類與抽取式理解任務。

GPT 的優點是泛化能力強、能處理多種語言任務、可作為基礎模型；限制是生成內容可能有幻覺、訓練與推論成本高、需要大量資料與算力，且在高風險場景需加上檢索、工具、權限與人工覆核。

## 2. 考試重點

- **架構基礎**：GPT 使用 Transformer Decoder，不是 Encoder。
- **訓練目標**：自回歸預測下一個 token，也就是根據前文生成後文。
- **生成任務**：適合文本生成、對話、摘要、翻譯、程式碼生成與問答。
- **和 BERT 差異**：BERT 雙向理解；GPT 單向自回歸生成。
- **預訓練模型**：先在大規模語料上學習，再透過指令微調或對齊改善可用性。
- **大型語言模型限制**：可能幻覺、資料過時、推理不穩、成本高且不可完全信任。
- **部署風險**：需注意資料外洩、prompt injection、不當輸出與版權問題。
- **應用治理**：高風險應用需檢索增強、來源引用、人工覆核與安全護欄。

## 3. 名詞解釋

- **GPT**：Generative Pre-trained Transformer，以 Transformer Decoder 為主的生成式語言模型。
- **自回歸（Autoregressive）**：根據已生成或已知前文逐步預測下一個 token。
- **Token**：模型處理文字的基本單位，可是字、詞片段或符號。
- **大型語言模型（LLM）**：以大量文字資料訓練、具備多任務語言能力的模型。
- **指令微調（Instruction Tuning）**：用指令與回覆資料訓練模型遵循人類指令。
- **幻覺（Hallucination）**：模型生成看似合理但事實錯誤或無來源的內容。

## 4. 常見陷阱

**陷阱1：把 GPT 和 BERT 用途搞反**
> ❌ 誤解：GPT 主要用於雙向理解，BERT 主要用於長文生成。  
> ✅ 正確：GPT 偏生成；BERT 偏理解。

**陷阱2：以為 GPT 產生的內容一定正確**
> ❌ 誤解：大型模型回答自然，就代表事實正確。  
> ✅ 正確：GPT 可能幻覺，重要任務需查證、引用來源或人工覆核。

**陷阱3：忽略自回歸生成特性**
> ❌ 誤解：GPT 一次看完整答案再輸出。  
> ✅ 正確：GPT 是逐 token 生成，後續輸出依賴前面已生成內容。

**陷阱4：只看模型能力，不看部署風險**
> ❌ 誤解：把 GPT 接到企業資料庫就能直接上線。  
> ✅ 正確：需要權限控管、資料遮罩、安全提示、工具限制與監控。

## 5. 考題怎麼問

**問法1：問 GPT 的架構**  
→ 答 Transformer Decoder / 自回歸生成。

**問法2：問 GPT 和 BERT 差異**  
→ GPT 生成、單向；BERT 理解、雙向。

**問法3：問大型語言模型風險**  
→ 答幻覺、資料外洩、偏見、成本、prompt injection 與不可解釋。

**問法4：問如何提升企業應用可靠性**  
→ 答檢索增強、來源引用、人工覆核、權限控管與安全護欄。

## 6. 記憶口訣

- **「GPT 續寫，BERT 讀懂」**：生成與理解要分清。
- **「Decoder 派，往後猜」**：GPT 根據前文預測下一個 token。
- **「自然不等於正確」**：生成式模型一定要查證。

## 7. 官方指引對應線索

此主題屬於科目三 Transformer、預訓練語言模型、生成式 AI 與大型語言模型範圍。考試常從 GPT 架構、下一詞預測、與 BERT 差異、生成式應用與模型風險命題。''',
75: '''# LoRA / PEFT 參數高效微調

## 1. 核心概念

**PEFT（Parameter-Efficient Fine-Tuning，參數高效微調）** 是一類讓大型模型在少量可訓練參數下適應新任務的方法。它的目的不是重新訓練整個模型，而是在凍結大部分原模型參數的情況下，只訓練少量新增參數或低秩矩陣，以降低訓練成本、記憶體需求與部署負擔。

**LoRA（Low-Rank Adaptation）** 是最常見的 PEFT 方法之一。它的核心想法是：原本模型的權重矩陣不直接大幅更新，而是在特定層旁邊加入低秩矩陣來學習任務差異。因為新增參數量很少，所以可以用較少 GPU 記憶體完成微調，也方便針對不同任務保存多組 adapter。

在大型語言模型時代，完整微調（Full Fine-tuning）成本很高，且每個任務都複製一份完整模型不實際。LoRA / PEFT 讓企業能用較低成本把基礎模型調整到客服、法律、醫療、程式碼或內部知識等特定任務。

科目三重點是理解 LoRA / PEFT 解決的問題：不是提高模型理論上限，而是讓大型模型微調更省資源、更容易部署與管理。它常和 fine-tuning、RAG、prompt engineering 做比較。

## 2. 考試重點

- **PEFT 目的**：只訓練少量參數，降低微調大型模型的成本與記憶體需求。
- **LoRA 核心**：用低秩矩陣學習權重更新，不直接訓練全部原模型參數。
- **凍結基礎模型**：大部分 pretrained model 參數保持不變，只訓練 adapter 或低秩參數。
- **適用情境**：需要讓大型模型適應特定任務，但資源不足以完整微調。
- **和 Full Fine-tuning 差異**：完整微調更新全部或大量參數；LoRA 只更新少量新增參數。
- **和 Prompt Engineering 差異**：Prompt 不改模型參數；LoRA 會訓練額外參數。
- **和 RAG 差異**：RAG 透過檢索外部知識；LoRA 透過訓練改變模型行為。
- **主要限制**：若任務需要大量新知識或高事實準確性，仍可能需要 RAG、資料治理或更完整訓練。

## 3. 名詞解釋

- **PEFT**：Parameter-Efficient Fine-Tuning，只訓練少量參數的微調方法集合。
- **LoRA**：Low-Rank Adaptation，以低秩矩陣學習任務差異的 PEFT 方法。
- **Adapter**：插入模型中的小型可訓練模組，用於特定任務調整。
- **Full Fine-tuning**：更新整個模型或大量參數的完整微調。
- **低秩矩陣（Low-rank Matrix）**：用較少維度近似大型權重更新的矩陣表示。
- **凍結參數（Frozen Parameters）**：訓練時不更新的原模型參數。

## 4. 常見陷阱

**陷阱1：以為 LoRA 是壓縮模型本體**
> ❌ 誤解：LoRA 直接把原模型變小。  
> ✅ 正確：LoRA 通常是在凍結原模型旁加入少量可訓練參數，主要降低微調成本。

**陷阱2：把 LoRA 和 RAG 混為一談**
> ❌ 誤解：LoRA 會即時查詢外部文件。  
> ✅ 正確：RAG 才是檢索外部知識；LoRA 是訓練 adapter 改變模型行為。

**陷阱3：以為 PEFT 永遠等同完整微調效果**
> ❌ 誤解：PEFT 一定和 full fine-tuning 一樣好。  
> ✅ 正確：PEFT 成本低，但效果仍取決於任務、資料品質與模型容量。

**陷阱4：以為 prompt 和 LoRA 都不改模型**
> ❌ 誤解：LoRA 只是換提示詞。  
> ✅ 正確：Prompt engineering 不改參數；LoRA 會訓練額外參數。

## 5. 考題怎麼問

**問法1：問如何低成本微調大型模型**  
→ 答 PEFT 或 LoRA。

**問法2：問 LoRA 訓練哪些參數**  
→ 答低秩 adapter / 少量新增參數，基礎模型多數凍結。

**問法3：比較 LoRA 與 RAG**  
→ LoRA 是微調；RAG 是檢索外部知識。

**問法4：比較 LoRA 與 Prompt Engineering**  
→ Prompt 不改參數；LoRA 會訓練參數。

## 6. 記憶口訣

- **「大模型不全動，小矩陣來適應」**：LoRA 的核心。
- **「Prompt 不訓練，LoRA 有參數」**：兩者差異。
- **「RAG 查資料，LoRA 改行為」**：不要混淆檢索與微調。

## 7. 官方指引對應線索

此主題屬於科目三大型模型微調、模型部署與資源效率範圍。考試常從大型模型客製化、微調成本、Full Fine-tuning 與 PEFT 差異、LoRA 和 RAG/Prompt 的比較命題。''',
76: '''# Quantization 量化

## 1. 核心概念

**量化（Quantization）** 是把模型中的權重或運算從高精度數值表示轉成低精度表示的技術，例如從 FP32 轉成 FP16、INT8，甚至更低位元。它的主要目的在於降低模型大小、記憶體使用量、推論延遲與硬體成本。

深度學習模型通常使用浮點數表示參數，但在部署階段不一定需要完整高精度。若把權重轉成低精度，模型檔案會變小，運算可能更快，也更容易部署到手機、邊緣裝置或高流量推論服務。這對大型語言模型和即時推論系統特別重要。

量化可分為**訓練後量化（Post-Training Quantization, PTQ）** 與 **量化感知訓練（Quantization-Aware Training, QAT）**。PTQ 是模型訓練完後再轉低精度，流程較簡單；QAT 在訓練過程模擬量化誤差，通常效果較穩但成本較高。

科目三常把 Quantization 和模型壓縮、部署最佳化、邊緣 AI、LLM 推論成本放在一起考。重點是知道量化能省資源，但可能造成精度下降，因此需要校準與重新驗證。

## 2. 考試重點

- **核心目的**：降低模型大小、記憶體需求、推論延遲與運算成本。
- **低精度表示**：常見從 FP32 降到 FP16、INT8 或更低位元。
- **PTQ**：訓練後量化，流程簡單，但精度可能下降較多。
- **QAT**：量化感知訓練，在訓練中模擬量化誤差，通常精度較穩。
- **適用情境**：邊緣裝置、手機、即時推論、高流量 API、大型模型部署。
- **主要風險**：精度下降、某些硬體不支援、不同層對量化敏感度不同。
- **和剪枝差異**：剪枝移除權重或通道；量化降低數值精度。
- **部署驗證**：量化後需重新測準確率、延遲、記憶體與實際硬體效能。

## 3. 名詞解釋

- **量化（Quantization）**：將模型參數或運算轉成低精度表示的技術。
- **FP32**：32 位元浮點數，訓練中常見但資源需求較高。
- **FP16**：16 位元浮點數，常用於加速與減少記憶體。
- **INT8**：8 位元整數表示，常見於推論加速與邊緣部署。
- **PTQ**：Post-Training Quantization，模型訓練完成後再量化。
- **QAT**：Quantization-Aware Training，在訓練時考慮量化效果的方法。

## 4. 常見陷阱

**陷阱1：以為量化一定不影響準確率**
> ❌ 誤解：只是改數字格式，模型效果不會變。  
> ✅ 正確：低精度可能造成資訊損失，必須重新驗證準確率。

**陷阱2：把量化和剪枝混淆**
> ❌ 誤解：量化是刪掉不重要權重。  
> ✅ 正確：剪枝才是移除權重；量化是降低數值精度。

**陷阱3：只看模型檔案大小**
> ❌ 誤解：檔案變小就代表部署一定更快。  
> ✅ 正確：實際速度取決於硬體是否支援低精度運算與執行框架。

**陷阱4：忽略校準資料**
> ❌ 誤解：PTQ 不需要代表性資料。  
> ✅ 正確：許多 PTQ 方法需要校準資料估計數值範圍，資料不代表會影響效果。

## 5. 考題怎麼問

**問法1：問降低模型記憶體與推論成本**  
→ 答量化、模型壓縮或低精度推論。

**問法2：問 FP32 轉 INT8 是什麼**  
→ 答 Quantization。

**問法3：問 PTQ 和 QAT 差異**  
→ PTQ 訓練後轉換；QAT 訓練時模擬量化。

**問法4：問量化後要做什麼**  
→ 答重新驗證準確率、延遲、記憶體與硬體支援。

## 6. 記憶口訣

- **「量化不是刪掉，是降精度」**：和剪枝分開記。
- **「FP32 太重，INT8 省資源」**：量化的部署直覺。
- **「量化後必驗證」**：省資源不能犧牲不可接受的準確率。

## 7. 官方指引對應線索

此主題屬於科目三模型壓縮、模型部署、邊緣 AI 與推論最佳化範圍。考試常從大型模型部署成本、低精度推論、PTQ/QAT 差異、量化與剪枝比較，以及量化後驗證需求命題。'''
}

for seg in guide['segments']:
    if seg.get('id') in contents:
        seg['content'] = contents[seg['id']]

comp = set(state['s3'].get('completed', []))
fail = set(state['s3'].get('failed', []))
for i in (74, 75, 76):
    comp.add(i)
    fail.discard(i)
state['s3']['completed'] = sorted(comp)
state['s3']['failed'] = sorted(fail)
ft = {str(k): v for k, v in state['s3'].get('failedTitles', {}).items()}
for i in (74, 75, 76):
    ft.pop(str(i), None)
state['s3']['failedTitles'] = ft
state['lastUpdated'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')

guide_path.write_text(json.dumps(guide, ensure_ascii=False, indent=2))
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
print('updated S3 ids 74,75,76 directly by Hermes; no Claude Code subprocess used')
