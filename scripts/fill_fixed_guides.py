#!/usr/bin/env python3
import json
import pathlib
import re

BASE = pathlib.Path(__file__).resolve().parents[1]
EXTRACTED = BASE / "extracted_guides"

TERM_DEFS = {
    "AI": "人工智慧，讓系統能執行感知、推論、學習、決策或生成等智慧型任務。",
    "NLP": "自然語言處理，處理文字與語音語言資料的 AI 技術。",
    "Word2Vec": "把詞轉為向量的詞嵌入方法，讓語意相近的詞在向量空間中靠近。",
    "GloVe": "以全域詞共現統計建立詞向量的方法。",
    "TF-IDF": "衡量詞在文件中重要性的文字表示方法，兼顧詞頻與文件區辨度。",
    "N-gram": "以連續 n 個詞或字組成的序列表示，常用於傳統語言模型。",
    "BERT": "雙向 Transformer 編碼器模型，適合理解型 NLP 任務。",
    "GPT": "自迴歸 Transformer 生成模型，適合生成、對話與續寫。",
    "Prompt Engineering": "設計提示詞以引導生成式 AI 產生符合需求輸出的技巧。",
    "Fine-tuning": "使用特定任務或領域資料微調既有模型。",
    "LoRA": "低秩適配微調方法，只訓練少量額外參數以節省成本。",
    "PEFT": "參數高效微調，只調整少部分參數或附加模組。",
    "RAG": "檢索增強生成，先查資料再讓模型依據資料回答。",
    "Vector Database": "向量資料庫，儲存 embedding 並支援相似度檢索。",
    "MLOps": "機器學習運維，涵蓋資料、訓練、部署、監控與版本管理。",
    "Model Drift": "模型上線後資料或關係改變，造成效能下降。",
    "A/B Testing": "將不同版本交給不同使用者群組，比較實際效果的實驗設計。",
    "SHAP": "解釋模型預測的特徵貢獻方法。",
    "Grad-CAM": "用熱區圖解釋 CNN 在影像中關注的位置。",
    "LIME": "以局部近似模型解釋單筆預測的方法。",
    "Federated Learning": "聯邦學習，資料不離開本地，只交換模型更新。",
    "Knowledge Graph": "知識圖譜，以節點和邊表示實體與關係。",
    "ASR": "自動語音辨識，將語音轉成文字。",
    "TTS": "文字轉語音，將文字轉成可聽語音。",
    "Probability": "機率，用數值描述事件發生可能性。",
    "Bayes": "貝氏方法，用先驗、似然與證據更新後驗機率。",
    "Expectation": "期望值，隨機變數的平均水準。",
    "Variance": "變異數，描述資料或隨機變數的分散程度。",
    "Normal Distribution": "常態分布，鐘形連續分布，常見於統計推論。",
    "Hypothesis Testing": "假設檢定，用樣本資料判斷假設是否可被拒絕。",
    "Correlation": "相關性，衡量兩變數線性關聯程度。",
    "Covariance": "共變數，衡量兩變數共同變動方向。",
    "OLS": "最小平方法，最小化殘差平方和估計線性迴歸參數。",
    "Loss Functions": "損失函數，用來衡量模型預測與真實答案的差距。",
    "Convexity": "凸性，保證局部最佳可作為全域最佳的重要條件。",
    "GD": "梯度下降，沿損失函數負梯度方向更新參數。",
    "SGD": "隨機梯度下降，每次用單筆或小批資料近似梯度。",
    "Momentum": "在梯度更新中加入動量，降低震盪並加速收斂。",
    "Adam": "結合 Momentum 與 RMSprop 概念的自適應最佳化器。",
    "Precision": "精確率，預測為正的樣本中真正為正的比例。",
    "Recall": "召回率，所有真正為正的樣本中被找出的比例。",
    "F1": "Precision 與 Recall 的調和平均。",
    "AUC": "ROC 曲線下面積，衡量模型排序能力。",
    "ROC": "不同閾值下 TPR 與 FPR 的關係曲線。",
    "MAE": "平均絕對誤差，對離群值較不敏感。",
    "MSE": "平均平方誤差，會放大大誤差。",
    "RMSE": "均方根誤差，與目標變數同量綱。",
    "R²": "決定係數，衡量模型解釋變異的比例。",
    "K-Fold": "K 折交叉驗證，把資料分 K 份輪流驗證。",
    "SMOTE": "少數類過採樣技術，用合成樣本處理類別不平衡。",
    "Linear Regression": "線性迴歸，以線性關係預測連續數值。",
    "Ridge": "L2 正則化迴歸，壓小權重降低過擬合。",
    "Lasso": "L1 正則化迴歸，可使部分權重為 0 並具特徵選擇效果。",
    "Logistic Regression": "邏輯迴歸，用 sigmoid 或 softmax 處理分類。",
    "Decision Tree": "決策樹，以條件切分形成可解釋分類或迴歸規則。",
    "Random Forest": "隨機森林，多棵決策樹集成以降低變異。",
    "AdaBoost": "逐步提高錯分樣本權重的 boosting 方法。",
    "XGBoost": "高效梯度提升樹，常用於結構化資料。",
    "SVM": "支援向量機，尋找最大間隔分類邊界。",
    "KNN": "最近鄰方法，依鄰近樣本投票或平均預測。",
    "Naive Bayes": "樸素貝氏分類器，假設特徵條件獨立。",
    "K-means": "以群中心反覆更新進行分群的方法。",
    "DBSCAN": "密度式分群，可找任意形狀群集與雜訊點。",
    "PCA": "主成分分析，以最大變異方向進行線性降維。",
    "t-SNE": "非線性降維視覺化方法，強調局部鄰近關係。",
    "UMAP": "非線性降維方法，兼顧局部與部分全域結構。",
    "Apriori": "用頻繁項集找關聯規則的方法。",
    "FP-Growth": "以 FP-tree 壓縮交易資料的關聯規則方法。",
    "Isolation Forest": "異常偵測方法，異常點較容易被隨機切割孤立。",
    "One-Class SVM": "只用正常資料學邊界，再判斷新資料是否異常。",
    "Neural Network": "類神經網路，由多層神經元與權重組成，可學非線性關係。",
    "Backpropagation": "反向傳播，用鏈式法則計算各層參數梯度。",
    "Activation Functions": "激活函數，引入非線性能力。",
    "CNN": "卷積神經網路，擅長影像特徵擷取。",
    "RNN": "遞迴神經網路，處理序列資料但長距離依賴較困難。",
    "LSTM": "改良 RNN 的長短期記憶網路，可保留較長序列資訊。",
    "GRU": "門控循環單元，較簡化的 RNN 改良架構。",
    "Batch Normalization": "批次正規化，穩定訓練並加速收斂。",
    "Dropout": "訓練時隨機關閉部分神經元以降低過擬合。",
    "Transfer Learning": "遷移學習，把既有模型知識用到新任務。",
    "Attention": "注意力機制，讓模型聚焦重要輸入資訊。",
    "Transformer": "以注意力機制為核心的序列模型架構。",
    "Quantization": "量化，降低權重或 activation 精度以節省部署資源。",
    "GAN": "生成對抗網路，由生成器與判別器對抗訓練。",
    "Diffusion Models": "擴散模型，從噪聲逐步還原資料的生成模型。",
    "YOLO": "即時物件偵測模型，一次預測物件位置與類別。",
    "R-CNN": "區域式卷積神經網路物件偵測系列。",
    "Policy Gradient": "強化學習中直接最佳化策略的方法。",
    "PPO": "近端策略最佳化，限制策略更新幅度以穩定訓練。",
    "Differential Privacy": "差分隱私，用隨機噪聲降低個人資料被反推風險。",
    "Homomorphic Encryption": "同態加密，可在密文上運算並保護資料內容。",
    "Edge AI": "邊緣 AI，在裝置端或近資料端進行推論。",
    "AutoML": "自動化模型選擇、特徵處理與超參數搜尋。",
    "Responsible AI": "負責任 AI，強調公平、透明、隱私、安全與問責。",
    "Fairness": "公平性，避免模型對族群產生不合理偏差。",
    "Human-in-the-Loop": "人在迴路中，讓人參與標註、審核、修正或決策。",
}

CN_DEFS = {
    "人工智慧": "讓機器具備感知、學習、推論、決策或生成能力的技術總稱。",
    "電腦視覺": "讓電腦理解影像與影片內容的 AI 技術。",
    "影像分類": "判斷整張影像屬於哪個類別。",
    "物件偵測": "同時找出物件位置與類別。",
    "語義分割": "把影像中每個像素分到語義類別。",
    "實例分割": "同時區分物件類別與不同個體。",
    "提示工程": "設計輸入提示以控制生成式模型輸出。",
    "災難性遺忘": "模型學新任務時遺失舊任務能力。",
    "資料品質": "資料正確性、完整性、一致性、即時性與代表性。",
    "特徵工程": "把原始資料轉換成模型可有效學習的特徵。",
    "模型選型": "依任務、資料、可解釋性、成本與部署條件選擇模型。",
    "模型監控": "追蹤上線模型效能、漂移、錯誤與資源狀態。",
    "可解釋性": "能說明模型預測原因或特徵影響。",
    "偏見": "資料或模型導致對某些族群不公平的系統性差異。",
    "公平性": "模型對不同群體或情境不應有不合理差別待遇。",
    "資料隱私": "保護個人或敏感資料不被不當蒐集、使用或洩漏。",
    "資料治理": "管理資料來源、品質、權限、生命週期與合規。",
    "預測維護": "用資料預測設備故障以提前維修。",
    "推薦系統": "依使用者、物品與情境預測偏好並推薦內容。",
    "異常偵測": "找出與正常行為顯著不同的樣本或事件。",
    "時間序列": "按時間排序的資料，例如銷售、感測器或股價。",
    "成本效益": "衡量 AI 導入成本與可量化/不可量化效益是否合理。",
    "變革管理": "處理流程、組織、角色與文化改變以落地新系統。",
    "模型壓縮": "降低模型大小或計算量以利部署。",
    "知識蒸餾": "讓小模型學習大模型輸出以保留效能並降低成本。",
    "綠色AI": "降低 AI 訓練與推論能耗及碳排的設計取向。",
    "機率": "描述不確定事件發生可能性的數值。",
    "統計推論": "用樣本推論母體特性或判斷假設。",
    "條件機率": "在已知某事件發生下，另一事件發生的機率。",
    "貝氏定理": "利用新證據更新事件後驗機率的公式。",
    "假設檢定": "用樣本資料判斷統計假設是否合理。",
    "梯度消失": "深層網路反向傳播時梯度過小，前面層難以更新。",
    "殘差連接": "讓輸入跨層加到輸出，改善深層網路訓練。",
    "過擬合": "模型過度記住訓練資料，導致泛化能力差。",
    "欠擬合": "模型太簡單，連訓練資料規律都學不好。",
    "資料不平衡": "不同類別樣本數差異過大，模型易偏向多數類。",
    "同態加密": "允許在加密資料上運算，解密後得到對應明文結果。",
    "邊緣運算": "在接近資料來源的裝置或節點處理資料，降低延遲與傳輸。",
}

DOMAIN_RULES = [
    (["NLP", "Word2Vec", "GloVe", "TF-IDF", "N-gram", "BERT", "GPT", "語言", "文本", "情感"], "自然語言與生成式 AI"),
    (["Computer Vision", "影像", "Object", "YOLO", "Segmentation", "ViT", "CNN", "R-CNN"], "電腦視覺與影像 AI"),
    (["專案", "規劃", "導入", "成本", "風險", "治理", "變革", "人才", "組織"], "AI 專案導入與治理"),
    (["MLOps", "CI/CD", "監控", "Drift", "部署", "A/B", "AutoML", "Cloud", "GPU", "TPU"], "AI 系統建置與營運"),
    (["倫理", "公平", "Bias", "Privacy", "GDPR", "個資", "Responsible", "AI Act", "安全", "Adversarial"], "負責任 AI、法規與安全"),
    (["機率", "統計", "Bayes", "常態", "Hypothesis", "Correlation", "Variance", "Probability"], "機率統計基礎"),
    (["Loss", "梯度", "GD", "SGD", "Adam", "優化", "Convexity", "收斂"], "最佳化與訓練穩定性"),
    (["Regression", "Decision", "Random", "SVM", "KNN", "Bayes", "Boost", "XGBoost", "Lasso", "Ridge"], "傳統機器學習演算法"),
    (["K-means", "Clustering", "DBSCAN", "PCA", "t-SNE", "UMAP", "Apriori", "FP-Growth", "Isolation", "One-Class"], "非監督學習與異常偵測"),
    (["Neural", "Backpropagation", "Activation", "Batch", "Dropout", "Transfer", "Fine-tuning"], "深度學習訓練方法"),
    (["Attention", "Transformer", "LoRA", "Quantization", "RAG", "GAN", "Diffusion"], "深度學習與生成式模型"),
    (["Reinforcement", "Policy", "PPO", "MDP", "強化"], "強化學習"),
]


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    text = re.sub(r"[\uf000-\uf8ff]+", "", text)
    return text


def load_corpus(subject: int) -> str:
    p = EXTRACTED / ("subject1.txt" if subject == 1 else "subject3.txt")
    return p.read_text(errors="ignore") if p.exists() else ""

CORPUS = {1: load_corpus(1), 3: load_corpus(3)}


def find_pdf_snippet(title: str, subject: int) -> str:
    corpus = CORPUS[subject]
    if not corpus:
        return ""
    # Try English/CJK tokens, longest first.
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9+\-/²]*|[\u4e00-\u9fff]{2,}", title)
    stop = {"科目", "總複習", "概覽", "總覽", "應用", "方法", "基礎", "進階"}
    tokens = [t for t in tokens if t not in stop]
    tokens = sorted(set(tokens), key=len, reverse=True)
    for tok in tokens[:6]:
        m = re.search(re.escape(tok), corpus, re.I)
        if m:
            start = max(0, m.start() - 250)
            end = min(len(corpus), m.end() + 550)
            snippet = clean_text(corpus[start:end])
            # Avoid table-of-contents only snippets where possible.
            if len(snippet) > 120:
                return snippet[:520]
    return ""


def infer_domain(title: str) -> str:
    for keys, domain in DOMAIN_RULES:
        if any(k.lower() in title.lower() for k in keys):
            return domain
    return "核心概念與應用判斷"


def terms_for_title(title: str):
    found = []
    for t in TERM_DEFS:
        if re.search(r"(?<![A-Za-z])" + re.escape(t) + r"(?![A-Za-z])", title, re.I):
            found.append((t, TERM_DEFS[t]))
    for t in CN_DEFS:
        if t in title:
            found.append((t, CN_DEFS[t]))
    domain = infer_domain(title)
    domain_defaults = {
        "自然語言與生成式 AI": ["NLP", "BERT", "GPT", "TF-IDF"],
        "電腦視覺與影像 AI": ["CNN", "YOLO", "Grad-CAM"],
        "AI 專案導入與治理": ["資料治理", "成本效益", "變革管理"],
        "AI 系統建置與營運": ["MLOps", "Model Drift", "A/B Testing"],
        "負責任 AI、法規與安全": ["Responsible AI", "Fairness", "Differential Privacy"],
        "機率統計基礎": ["Probability", "Expectation", "Variance"],
        "最佳化與訓練穩定性": ["Loss Functions", "GD", "Adam"],
        "傳統機器學習演算法": ["Decision Tree", "SVM", "Random Forest"],
        "非監督學習與異常偵測": ["K-means", "PCA", "Isolation Forest"],
        "深度學習訓練方法": ["Neural Network", "Backpropagation", "Dropout"],
        "深度學習與生成式模型": ["Transformer", "Attention", "RAG"],
        "強化學習": ["Policy Gradient", "PPO"],
    }
    for t in domain_defaults.get(domain, []):
        if t in TERM_DEFS and all(x[0] != t for x in found):
            found.append((t, TERM_DEFS[t]))
    return found[:5]


def bullets_for(title: str, subject: int):
    domain = infer_domain(title)
    title_main = title
    if "總複習" in title or "Review" in title:
        return {
            "concept": f"本段是科目{subject}的總複習，用來把前面各主題串成考前判斷框架。重點不是背單一名詞，而是能看到題幹後判斷考的是概念、流程、限制、評估指標或應用情境。",
            "points": ["用主題地圖回顧高頻考點", "把名詞、指標、流程和應用案例放在同一張表比較", "優先修正錯題與容易混淆的相近概念", "練習從題幹關鍵字反推考點"],
            "traps": ["只背定義，沒有練習情境判斷", "看到熟悉名詞就選，忽略題目問的是目的或限制", "沒有整理錯題原因，導致同型題重複錯"],
            "exam": ["問最適合的技術或流程", "比較兩個相近名詞", "判斷導入情境下的風險或指標", "從錯誤做法找改善策略"],
        }
    if subject == 1:
        return {
            "concept": f"{title_main}屬於「{domain}」範圍。科目一重視應用規劃、導入判斷、風險治理與商業情境；讀本段時要把技術名詞連到實際場景、資料條件、限制與導入流程。",
            "points": [f"理解 {title_main} 的目的與適用情境", "判斷導入時需要哪些資料、流程與利害關係人", "分辨此技術和相近技術的差異", "掌握效益、風險、治理與評估方式"],
            "traps": ["只記技術名詞，忽略題幹的產業情境", "把模型訓練問題誤判成專案治理問題，或反過來", "沒有區分可解釋性、隱私、公平性、安全性等治理面向", "忽略資料品質、標註成本與部署維運限制"],
            "exam": ["給一個企業導入案例，問最適合的 AI 技術或流程", "問資料、模型、部署、治理哪一環最關鍵", "問某種風險的改善策略", "比較兩個應用或技術名詞的差異"],
        }
    return {
        "concept": f"{title_main}屬於「{domain}」範圍。科目三重視機器學習原理、演算法選擇、評估指標、訓練限制與模型部署；讀本段時要能說出數學/演算法直覺，也要能判斷適用情境。",
        "points": [f"理解 {title_main} 的核心目的與輸入輸出", "掌握常見公式、流程或演算法步驟", "知道何時適用、何時不適用", "能和相近方法、評估指標或模型架構做比較"],
        "traps": ["把分類、迴歸、分群、降維、生成等任務類型混淆", "只背公式，沒有連到資料型態與模型假設", "忽略過擬合、資料不平衡、漂移、計算成本等限制", "混淆評估指標的使用情境"],
        "exam": ["問演算法適用情境或限制", "問評估指標代表的意義", "給訓練失敗症狀，問原因與改善方式", "比較兩個模型或方法的差異"],
    }


def make_content(seg: dict, subject: int) -> str:
    title = seg["title"]
    info = bullets_for(title, subject)
    terms = terms_for_title(title)
    snippet = find_pdf_snippet(title, subject)
    term_lines = [f"- **{t}**：{d}" for t, d in terms]
    if not term_lines:
        term_lines = [f"- **{infer_domain(title)}**：本段在考試中通常要求判斷目的、適用情境、限制與和其他概念的差異。"]
    src = f"\n\n## 7. 官方指引對應線索\n{snippet}" if snippet else ""
    return "\n".join([
        f"# {title}",
        "",
        "## 1. 核心概念",
        info["concept"],
        "",
        "## 2. 考試重點",
        *[f"- {x}" for x in info["points"]],
        "",
        "## 3. 名詞解釋",
        *term_lines,
        "",
        "## 4. 常見陷阱",
        *[f"- {x}" for x in info["traps"]],
        "",
        "## 5. 考題怎麼問",
        *[f"- {x}" for x in info["exam"]],
        "",
        "## 6. 記憶口訣",
        f"先判斷本題屬於「{infer_domain(title)}」，再看題幹問的是目的、流程、適用情境、限制，還是評估方式。",
        src,
    ]).strip()


def fill_file(filename: str, subject: int):
    path = BASE / filename
    data = json.loads(path.read_text())
    changed = 0
    for seg in data["segments"]:
        new = make_content(seg, subject)
        if seg.get("content") != new:
            seg["content"] = new
            changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return changed, len(data["segments"])

if __name__ == "__main__":
    for fn, sub in [("guide_s1.json", 1), ("guide_s3.json", 3)]:
        changed, total = fill_file(fn, sub)
        print(fn, "changed", changed, "total", total)
