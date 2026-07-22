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
77: '''# RAG 檢索增強生成

## 1. 核心概念

**RAG（Retrieval-Augmented Generation，檢索增強生成）** 是把「外部知識檢索」和「生成式模型回答」結合的架構。它的核心目的，是讓大型語言模型在回答問題前先查詢可靠資料來源，再根據查到的內容生成回答，以降低幻覺、補足模型知識過時或不知道企業內部資料的問題。

RAG 的典型流程包含三步：第一，將文件切分成段落並轉成向量，建立向量資料庫或搜尋索引；第二，使用者提問時，系統根據問題檢索相關文件片段；第三，將檢索結果連同問題放入 LLM，要求模型根據資料回答。這樣模型不是憑記憶亂猜，而是以檢索到的內容為上下文。

RAG 常用於企業知識庫問答、法規查詢、客服文件、技術文件、醫療或金融內部資料查詢。和 fine-tuning 不同，RAG 主要解決「外部知識接入與可追溯來源」問題；fine-tuning 則偏向改變模型行為或任務能力。

科目三重點在於理解 RAG 的組成、優點與限制：它可以減少幻覺、更新知識較容易、可附來源，但仍受檢索品質、文件切分、embedding、提示設計與資料權限影響。

## 2. 考試重點

- **核心目的**：讓 LLM 回答前先檢索外部資料，降低幻覺並補足知識不足。
- **基本流程**：文件切分 → embedding → 建索引 → 查詢檢索 → LLM 根據上下文回答。
- **主要元件**：文件庫、embedding 模型、向量資料庫 / 搜尋引擎、retriever、generator。
- **和 fine-tuning 差異**：RAG 不一定改模型參數；fine-tuning 會訓練模型參數。
- **優點**：知識可更新、可引用來源、適合企業內部文件問答。
- **限制**：檢索不到正確資料時，生成答案仍可能錯誤。
- **關鍵品質因素**：文件切分大小、embedding 品質、檢索排序、上下文長度與提示設計。
- **安全重點**：需控管文件權限，避免使用者透過問答取得不該看的資料。

## 3. 名詞解釋

- **RAG**：Retrieval-Augmented Generation，檢索增強生成。
- **Retriever（檢索器）**：根據查詢找出相關文件片段的元件。
- **Generator（生成器）**：根據問題與檢索內容生成回答的語言模型。
- **Embedding（嵌入向量）**：把文字轉成可計算相似度的向量表示。
- **向量資料庫（Vector Database）**：儲存向量並支援相似度搜尋的資料庫。
- **Chunk（文件片段）**：將長文件切分後供檢索使用的小段文字。

## 4. 常見陷阱

**陷阱1：以為 RAG 會讓答案永遠正確**
> ❌ 誤解：加了檢索就不會幻覺。  
> ✅ 正確：若檢索錯誤、文件過時或提示設計不佳，LLM 仍可能回答錯。

**陷阱2：把 RAG 和 fine-tuning 混淆**
> ❌ 誤解：RAG 是重新訓練模型。  
> ✅ 正確：RAG 通常不改模型參數，而是把外部文件作為回答上下文。

**陷阱3：忽略文件切分品質**
> ❌ 誤解：把整份文件丟進向量庫就好。  
> ✅ 正確：切分太碎會失去上下文，太長會降低檢索精準度。

**陷阱4：忽略權限控管**
> ❌ 誤解：企業文件建成 RAG 後所有人都能問。  
> ✅ 正確：RAG 必須遵守文件權限，否則可能造成內部資料外洩。

## 5. 考題怎麼問

**問法1：問如何降低 LLM 幻覺並引用內部資料**  
→ 答 RAG / 檢索增強生成。

**問法2：問 RAG 流程**  
→ 答文件切分、向量化、檢索、把檢索結果交給 LLM 生成。

**問法3：問 RAG 和 fine-tuning 差異**  
→ RAG 接外部知識；fine-tuning 改模型參數。

**問法4：問 RAG 失敗原因**  
→ 答檢索不準、文件過時、chunk 切分不佳、權限或提示設計問題。

## 6. 記憶口訣

- **「先查資料，再讓模型說」**：RAG 的核心流程。
- **「RAG 查知識，LoRA 改行為」**：和微調分清楚。
- **「檢索錯，生成也會錯」**：RAG 成敗先看 retrieval。

## 7. 官方指引對應線索

此主題屬於科目三生成式 AI、大型語言模型應用與企業知識問答範圍。考試常從 LLM 幻覺、內部文件問答、檢索流程、RAG 與 fine-tuning 差異，以及資料權限治理命題。''',
78: '''# GAN 生成對抗網路

## 1. 核心概念

**GAN（Generative Adversarial Network，生成對抗網路）** 是一種生成模型，由兩個神經網路互相競爭訓練：**生成器（Generator）** 負責產生假資料，**判別器（Discriminator）** 負責判斷資料是真實還是生成。兩者在對抗中共同進步，最終讓生成器產生越來越逼真的資料。

GAN 的訓練直覺像「偽造者與鑑定師」。生成器努力做出看起來像真的圖片、聲音或資料；判別器則學著分辨真假。當生成器能騙過判別器時，代表生成品質提高。這種對抗訓練使 GAN 在影像生成、風格轉換、超解析度、資料增強與影像修復等任務中有重要應用。

GAN 的優勢是能產生高品質、逼真的樣本，但訓練不穩定也是常見問題。GAN 可能出現**模式崩潰（Mode Collapse）**，也就是生成器只會產生少數幾種類型的樣本，看似逼真但多樣性不足。

科目三考 GAN 時，重點通常不是推導損失函數，而是理解 Generator / Discriminator 的角色、對抗訓練流程、生成模型用途，以及 GAN 和 Diffusion Models 的差異。

## 2. 考試重點

- **核心組成**：GAN 由生成器 Generator 與判別器 Discriminator 組成。
- **生成器任務**：從隨機噪聲產生假資料，目標是騙過判別器。
- **判別器任務**：判斷輸入資料是真實資料還是生成資料。
- **訓練方式**：生成器與判別器進行對抗訓練，彼此提升。
- **常見應用**：影像生成、風格轉換、超解析度、影像修復、資料增強。
- **主要問題**：訓練不穩定、模式崩潰、評估困難。
- **模式崩潰**：生成器只產生少數樣式，缺乏多樣性。
- **和 Diffusion 差異**：GAN 透過對抗生成；Diffusion 透過逐步去噪生成。

## 3. 名詞解釋

- **GAN**：Generative Adversarial Network，生成對抗網路。
- **Generator（生成器）**：產生假資料的神經網路。
- **Discriminator（判別器）**：判斷資料真假的神經網路。
- **對抗訓練（Adversarial Training）**：兩個模型互相競爭、共同更新的訓練方式。
- **模式崩潰（Mode Collapse）**：生成器只產生少數類型樣本，缺乏多樣性。
- **資料增強（Data Augmentation）**：透過生成或變換資料增加訓練樣本多樣性。

## 4. 常見陷阱

**陷阱1：把生成器和判別器角色搞反**
> ❌ 誤解：判別器負責產生圖片，生成器負責判斷真假。  
> ✅ 正確：生成器產生假資料；判別器判斷真假。

**陷阱2：以為 GAN 訓練一定穩定**
> ❌ 誤解：兩個網路一起訓練自然會越來越好。  
> ✅ 正確：GAN 訓練常不穩定，可能出現震盪或模式崩潰。

**陷阱3：把 GAN 和 Diffusion 混為一談**
> ❌ 誤解：所有影像生成模型都是 GAN。  
> ✅ 正確：GAN 是對抗訓練；Diffusion 是加噪再逐步去噪。

**陷阱4：只看單張圖片逼真度**
> ❌ 誤解：生成圖片很像真的，就代表模型很好。  
> ✅ 正確：還要看多樣性、穩定性、是否模式崩潰與是否符合條件。

## 5. 考題怎麼問

**問法1：問兩個網路互相競爭的生成模型**  
→ 答 GAN。

**問法2：問 Generator / Discriminator 角色**  
→ Generator 產生假資料；Discriminator 判斷真假。

**問法3：問 GAN 常見問題**  
→ 答訓練不穩定、模式崩潰、評估困難。

**問法4：比較 GAN 和 Diffusion**  
→ GAN 對抗生成；Diffusion 逐步去噪生成。

## 6. 記憶口訣

- **「G 造假，D 抓假」**：Generator 與 Discriminator 的角色。
- **「越騙越真，越抓越準」**：GAN 的對抗訓練直覺。
- **「GAN 怕崩，Diffusion 慢去噪」**：常見差異。

## 7. 官方指引對應線索

此主題屬於科目三生成式模型與深度學習應用範圍。考試常從生成器、判別器、對抗訓練、模式崩潰、影像生成與 GAN / Diffusion 差異命題。''',
79: '''# Diffusion Models 擴散模型

## 1. 核心概念

**擴散模型（Diffusion Models）** 是一類生成模型，核心想法是先把真實資料逐步加入雜訊，學習這個加噪過程，然後反向學會從純噪聲逐步去噪，最後生成新的資料。近年許多高品質影像生成模型都以 diffusion 為核心。

擴散模型包含兩個方向：**正向擴散（Forward Diffusion）** 是逐步把資料加上噪聲，直到接近隨機噪聲；**反向去噪（Reverse Denoising）** 則是模型學習如何一步步移除噪聲，從噪聲還原成有意義的圖片或資料。這個過程讓模型能穩定生成細節豐富、多樣性高的內容。

和 GAN 相比，Diffusion Models 通常訓練較穩定、生成多樣性較好，但推論過程可能較慢，因為需要多步去噪。後續許多方法會透過加速採樣、latent diffusion 或更少步數的去噪改善效率。

科目三考 diffusion 時，重點是理解「加噪 → 學去噪 → 從噪聲生成」的流程，以及和 GAN 的差異。不要把 diffusion 理解成資料傳輸或一般影像濾鏡，它是生成模型的一種。

## 2. 考試重點

- **核心流程**：正向加噪，反向去噪，最後從噪聲生成資料。
- **正向擴散**：逐步把真實資料加入 Gaussian noise。
- **反向去噪**：模型學習預測或移除噪聲，逐步生成乾淨樣本。
- **常見應用**：文字生成影像、影像修復、超解析度、風格生成、資料生成。
- **和 GAN 差異**：GAN 靠生成器與判別器對抗；Diffusion 靠逐步去噪。
- **優點**：生成品質高、訓練相對穩定、多樣性佳。
- **限制**：推論可能較慢、採樣步驟多、運算成本高。
- **Latent Diffusion**：在壓縮後的 latent space 中去噪，以降低計算成本。

## 3. 名詞解釋

- **擴散模型（Diffusion Models）**：透過學習加噪與去噪過程來生成資料的模型。
- **正向擴散（Forward Diffusion）**：逐步向真實資料加入噪聲的過程。
- **反向去噪（Reverse Denoising）**：從噪聲逐步還原生成資料的過程。
- **Gaussian Noise（高斯噪聲）**：常用於擴散過程的隨機噪聲。
- **Sampling（採樣）**：從噪聲逐步生成資料樣本的過程。
- **Latent Diffusion**：在低維潛在空間中執行擴散生成的方法。

## 4. 常見陷阱

**陷阱1：把 Diffusion 當成 GAN 的另一個名字**
> ❌ 誤解：Diffusion 和 GAN 都是生成圖片，所以機制相同。  
> ✅ 正確：GAN 是對抗訓練；Diffusion 是學習逐步去噪。

**陷阱2：忽略推論速度問題**
> ❌ 誤解：Diffusion 生成品質高，所以一定部署成本低。  
> ✅ 正確：多步去噪可能造成推論較慢，需要採樣加速或 latent diffusion。

**陷阱3：以為正向擴散就是生成過程**
> ❌ 誤解：模型生成時是把圖片加噪。  
> ✅ 正確：正向是訓練概念；實際生成是從噪聲反向去噪。

**陷阱4：只記文字生成影像應用**
> ❌ 誤解：Diffusion 只用於文生圖。  
> ✅ 正確：也可用於影像修復、超解析度、語音、影片與資料生成。

## 5. 考題怎麼問

**問法1：問從噪聲逐步生成影像的模型**  
→ 答 Diffusion Models。

**問法2：問 Diffusion 的兩個方向**  
→ 正向加噪，反向去噪。

**問法3：比較 GAN 與 Diffusion**  
→ GAN 對抗訓練；Diffusion 去噪生成。

**問法4：問 Diffusion 的限制**  
→ 答推論慢、採樣步驟多、運算成本高。

## 6. 記憶口訣

- **「先加噪學壞，再去噪生成」**：Diffusion 的核心流程。
- **「GAN 對抗，Diffusion 去噪」**：最常考比較。
- **「品質高但步驟多」**：Diffusion 的優勢與成本。

## 7. 官方指引對應線索

此主題屬於科目三生成式 AI、影像生成與深度生成模型範圍。考試常從加噪 / 去噪流程、GAN 與 Diffusion 差異、文生圖應用、生成品質與推論成本命題。'''
}

for seg in guide['segments']:
    if seg.get('id') in contents:
        seg['content'] = contents[seg['id']]

comp = set(state['s3'].get('completed', []))
fail = set(state['s3'].get('failed', []))
for i in (77, 78, 79):
    comp.add(i)
    fail.discard(i)
state['s3']['completed'] = sorted(comp)
state['s3']['failed'] = sorted(fail)
ft = {str(k): v for k, v in state['s3'].get('failedTitles', {}).items()}
for i in (77, 78, 79):
    ft.pop(str(i), None)
state['s3']['failedTitles'] = ft
state['lastUpdated'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')

guide_path.write_text(json.dumps(guide, ensure_ascii=False, indent=2))
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
print('updated S3 ids 77,78,79 directly by Hermes; no Claude Code subprocess used')
