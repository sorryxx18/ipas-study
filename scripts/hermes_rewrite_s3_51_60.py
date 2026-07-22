#!/usr/bin/env python3
import json, pathlib, datetime, shutil
base=pathlib.Path('/Users/leifhuang/.claude/projects/-Users-leifhuang/ipas_study')
guide_path=base/'guide_s3.json'; state_path=base/'rewrite_state.json'
backup_dir=base/'backups'/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-before-rewrite-s3-51-60')
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(guide_path, backup_dir/'guide_s3.json'); shutil.copy2(state_path, backup_dir/'rewrite_state.json')
guide=json.loads(guide_path.read_text(encoding='utf-8')); state=json.loads(state_path.read_text(encoding='utf-8'))
contents={
51: '''# K-means 聚類

## 1. 核心概念

**K-means** 是最常見的非監督式分群方法，目標是把資料分成 K 群，讓同群資料彼此相近、不同群資料相對分開。它會反覆執行兩件事：先把每筆資料分配到最近的群中心，再用群內資料平均重新計算中心，直到群中心變化很小或達到迭代上限。

K-means 適合群集大致呈圓形、大小相近、以距離衡量相似度合理的資料。因為它依賴距離，因此特徵尺度非常重要，通常需要標準化。K 值需事先指定，可用 elbow method、silhouette score 或業務知識輔助選擇。

## 2. 考試重點

- 非監督式學習，沒有標籤。
- 需事先指定群數 K。
- 反覆分配樣本與更新中心。
- 目標是最小化群內平方距離。
- 對初始中心、離群值、特徵尺度敏感。
- 適合球狀/凸形、大小相近的群。
- 不適合任意形狀群集或密度差很大的資料。

## 3. 名詞解釋

- **Centroid**：群中心，群內樣本平均位置。
- **Inertia / WCSS**：群內平方距離總和。
- **Elbow Method**：觀察 K 增加時誤差下降轉折點。
- **Silhouette Score**：衡量群內緊密與群間分離程度。
- **Initialization**：初始中心選擇，會影響結果。

## 4. 常見陷阱

**陷阱1：K-means 自動決定 K**
> ❌ 誤解：演算法會自動找最佳群數。  
> ✅ 正確：K 要先指定或用方法輔助選擇。

**陷阱2：未標準化就用距離分群**
> ❌ 誤解：各特徵單位不同不影響。  
> ✅ 正確：大尺度特徵會主導距離。

**陷阱3：所有形狀都適合 K-means**
> ❌ 誤解：任意形狀群都可分好。  
> ✅ 正確：K-means 偏好球狀群，非凸形狀可考慮 DBSCAN。

## 5. 考題怎麼問

**問法1：無標籤客戶分群用什麼**  
→ K-means 是常見方法之一。

**問法2：K-means 為何要標準化**  
→ 因為依距離計算相似度。

**問法3：如何選 K**  
→ Elbow method、Silhouette score 或業務知識。

## 6. 記憶口訣

- **「先給 K，找中心，反覆搬家」**。
- **「K-means 靠距離，尺度要先齊」**。
- **「球狀群好用，怪形狀別硬套」**。

## 7. 官方指引對應線索

對應科目三非監督式學習與分群演算法。官方指引強調 K-means 用於無標籤資料分群，考試常從群數 K、群中心更新、距離尺度、elbow/silhouette 與適用限制命題。''',
52: '''# Hierarchical Clustering 層次聚類

## 1. 核心概念

**層次聚類** 會建立資料之間由近到遠的階層結構，常用樹狀圖（dendrogram）呈現。最常見的是凝聚式方法：一開始每筆資料都是一群，逐步合併最相近的群，直到所有資料合為一群或達到指定群數。

與 K-means 不同，層次聚類不一定要一開始指定 K，而是可先看 dendrogram 再決定切在哪一層。它適合探索資料階層關係，但大型資料計算成本較高，且不同 linkage 方法會得到不同結果。

## 2. 考試重點

- 建立階層式群集結構。
- 常用 dendrogram 視覺化。
- 凝聚式：由小群逐步合併。
- 可依樹狀圖決定群數。
- linkage 影響分群結果。
- 計算成本較高，不一定適合超大型資料。

## 3. 名詞解釋

- **Dendrogram**：樹狀圖，表示群集合併順序與距離。
- **Agglomerative Clustering**：凝聚式層次聚類。
- **Linkage**：群與群距離定義。
- **Single Linkage**：看最近點距離。
- **Complete Linkage**：看最遠點距離。
- **Average Linkage**：看平均距離。

## 4. 常見陷阱

**陷阱1：以為層次聚類一定不用距離**
> ❌ 誤解：它不是距離模型。  
> ✅ 正確：仍依距離/相似度與 linkage 合併。

**陷阱2：linkage 不影響結果**
> ❌ 誤解：選哪種 linkage 都一樣。  
> ✅ 正確：single、complete、average 可能產生不同群形。

**陷阱3：大型資料直接套用**
> ❌ 誤解：層次聚類和 K-means 一樣適合大資料。  
> ✅ 正確：層次聚類通常計算與記憶體成本較高。

## 5. 考題怎麼問

**問法1：想看群集階層關係用什麼**  
→ 層次聚類與 dendrogram。

**問法2：不用先指定 K 的分群探索方法**  
→ 層次聚類可先建樹再切群。

**問法3：single linkage 是什麼**  
→ 兩群中最近兩點距離。

## 6. 記憶口訣

- **「層次聚類先長樹，再切群」**。
- **「linkage 定距離，樹形跟著變」**。
- **「看階層用樹狀圖」**。

## 7. 官方指引對應線索

對應科目三非監督式分群。考試常從 dendrogram、凝聚式流程、linkage 差異、是否需先指定群數與計算成本命題。''',
53: '''# DBSCAN

## 1. 核心概念

**DBSCAN** 是密度式分群方法，依資料點周圍密度形成群集。它不需要事先指定群數，能找出任意形狀的群，並能把密度不足的點標為雜訊或異常點。

DBSCAN 由兩個重要參數控制：ε（eps）表示鄰域半徑，MinPts 表示形成核心點所需的最少鄰居數。若某點在 ε 範圍內有足夠鄰居，就是核心點；由核心點密度相連的資料形成同一群。

## 2. 考試重點

- 不需指定群數。
- 可找任意形狀群集。
- 可識別雜訊/離群點。
- 參數 eps 與 MinPts 很關鍵。
- 對不同密度資料表現較弱。
- 距離式方法，特徵需適當縮放。

## 3. 名詞解釋

- **DBSCAN**：基於密度的分群方法。
- **eps / ε**：鄰域半徑。
- **MinPts**：核心點所需最少鄰居數。
- **Core Point**：核心點，鄰域內點數足夠。
- **Border Point**：邊界點，靠近核心點但自身密度不足。
- **Noise Point**：雜訊點，不屬於任何群。

## 4. 常見陷阱

**陷阱1：DBSCAN 需要指定 K**
> ❌ 誤解：所有分群都要先給群數。  
> ✅ 正確：DBSCAN 不需指定 K。

**陷阱2：不同密度資料也能完美處理**
> ❌ 誤解：DBSCAN 對任何密度都穩。  
> ✅ 正確：若各群密度差異大，單一 eps 很難設定。

**陷阱3：不用標準化**
> ❌ 誤解：密度式分群不受尺度影響。  
> ✅ 正確：eps 依距離計算，尺度仍重要。

## 5. 考題怎麼問

**問法1：想找任意形狀群且辨識雜訊**  
→ 答 DBSCAN。

**問法2：DBSCAN 兩個重要參數**  
→ eps 與 MinPts。

**問法3：哪種點會成為 noise**  
→ 不在核心點密度可達範圍內的點。

## 6. 記憶口訣

- **「DBSCAN 看密度，不先問幾群」**。
- **「eps 畫圈，MinPts 數人」**。
- **「怪形狀與雜訊，是它強項」**。

## 7. 官方指引對應線索

對應科目三非監督式學習與異常偵測。考試常從密度式分群、eps/MinPts、核心點、雜訊點、任意形狀群集與和 K-means 差異命題。''',
54: '''# PCA 主成分分析

## 1. 核心概念

**PCA（Principal Component Analysis，主成分分析）** 是線性降維方法，目標是在保留最多資料變異的前提下，把高維資料投影到較低維空間。它會找出資料變異最大的方向，稱為主成分。

PCA 常透過共變數矩陣的特徵值分解或 SVD 實作。第一主成分解釋最多變異，第二主成分在與第一主成分正交的方向上解釋次多變異。PCA 常用於降維、視覺化前處理、去除冗餘特徵與降低噪音。

## 2. 考試重點

- 線性降維方法。
- 找最大變異方向。
- 主成分彼此正交。
- 特徵值代表解釋變異量。
- 常需先標準化。
- 可用 explained variance ratio 選維度。
- 降維後可降低計算成本，但解釋性可能下降。

## 3. 名詞解釋

- **PCA**：主成分分析。
- **Principal Component**：主成分，最大變異方向。
- **Explained Variance**：被主成分解釋的變異量。
- **Eigenvalue**：特徵值，代表該方向變異大小。
- **Eigenvector**：特徵向量，主成分方向。
- **SVD**：奇異值分解，可用於 PCA。

## 4. 常見陷阱

**陷阱1：PCA 是非線性降維**
> ❌ 誤解：PCA 可抓任意彎曲流形。  
> ✅ 正確：PCA 是線性投影。

**陷阱2：PCA 一定提升模型準確率**
> ❌ 誤解：降維必定改善分類。  
> ✅ 正確：可能降低噪音，也可能丟失有用資訊。

**陷阱3：不需標準化**
> ❌ 誤解：原始尺度不影響主成分。  
> ✅ 正確：大尺度特徵會主導變異方向。

## 5. 考題怎麼問

**問法1：PCA 保留什麼**  
→ 最大資料變異。

**問法2：主成分間關係**  
→ 彼此正交。

**問法3：如何決定保留幾維**  
→ 看累積 explained variance ratio。

## 6. 記憶口訣

- **「PCA 找最大變異方向」**。
- **「先標準化，再看主成分」**。
- **「降維省成本，也可能丟資訊」**。

## 7. 官方指引對應線索

對應科目三線性代數、矩陣分解與非監督式降維。考試常從最大變異、特徵值/特徵向量、標準化、解釋變異率與 PCA 限制命題。''',
55: '''# t-SNE

## 1. 核心概念

**t-SNE** 是非線性降維視覺化方法，特別擅長把高維資料投影到 2D 或 3D，讓局部鄰近關係更容易被觀察。它重視「原本高維中相近的點，在低維也盡量相近」。

t-SNE 常用於文字 embedding、影像特徵、單細胞資料等高維表示的探索視覺化。但它主要是視覺化工具，不適合直接用來解讀全局距離、群大小或當作穩定特徵工程。

## 2. 考試重點

- 非線性降維。
- 主要用於視覺化。
- 強調局部鄰近結構。
- 對 perplexity、learning rate、random seed 敏感。
- 全局距離與群大小不一定可信。
- 通常不適合當正式下游模型特徵。
- 大資料計算成本較高。

## 3. 名詞解釋

- **t-SNE**：t-distributed Stochastic Neighbor Embedding。
- **Perplexity**：控制有效鄰居數的參數。
- **Embedding Visualization**：嵌入視覺化。
- **Local Structure**：局部鄰近關係。
- **Nonlinear Dimensionality Reduction**：非線性降維。

## 4. 常見陷阱

**陷阱1：把 t-SNE 圖上距離當全局距離**
> ❌ 誤解：圖上兩群距離遠代表原始空間一定遠。  
> ✅ 正確：t-SNE 主要保局部，全球距離未必可靠。

**陷阱2：群大小可直接比較**
> ❌ 誤解：圖上群比較大代表原始群變異更大。  
> ✅ 正確：t-SNE 視覺化可能扭曲群大小。

**陷阱3：結果完全穩定**
> ❌ 誤解：每次跑都一定一樣。  
> ✅ 正確：受 random seed 與參數影響。

## 5. 考題怎麼問

**問法1：高維資料想做 2D 視覺化**  
→ t-SNE 是常見選項。

**問法2：t-SNE 主要保留什麼**  
→ 局部鄰近關係。

**問法3：t-SNE 圖上群距離可否過度解讀**  
→ 不宜，全球距離不一定可靠。

## 6. 記憶口訣

- **「t-SNE 看鄰居，不看地圖比例尺」**。
- **「適合畫圖探索，不宜硬當特徵」**。
- **「參數種子一改，圖形可能變」**。

## 7. 官方指引對應線索

對應科目三非監督式降維與資料視覺化。考試常從 t-SNE 的非線性、局部結構、視覺化用途、參數敏感與不可過度解讀全局距離命題。''',
56: '''# UMAP

## 1. 核心概念

**UMAP** 是非線性降維方法，常用於高維資料視覺化與表示學習。相較 t-SNE，UMAP 通常速度較快，並試圖兼顧局部鄰近與部分全域結構，因此在大資料視覺化中常見。

UMAP 的重要參數包含 n_neighbors 與 min_dist。n_neighbors 影響局部/全局取捨；min_dist 影響低維點之間的緊密程度。和 t-SNE 一樣，UMAP 視覺化結果仍需謹慎解讀，不應把圖上距離當成絕對真實距離。

## 2. 考試重點

- 非線性降維方法。
- 常用於高維資料 2D/3D 視覺化。
- 通常比 t-SNE 快。
- 可較好保留部分全域結構。
- n_neighbors 控制鄰域尺度。
- min_dist 控制群集緊密度。
- 結果受參數與隨機性影響。

## 3. 名詞解釋

- **UMAP**：Uniform Manifold Approximation and Projection。
- **n_neighbors**：鄰居數參數。
- **min_dist**：低維嵌入最小距離傾向。
- **Manifold**：流形，高維資料可能位於的低維結構。
- **Embedding**：低維表示。

## 4. 常見陷阱

**陷阱1：UMAP 圖完全等於原始資料結構**
> ❌ 誤解：圖上距離與大小都可直接解讀。  
> ✅ 正確：UMAP 仍是降維近似，需謹慎解讀。

**陷阱2：參數不重要**
> ❌ 誤解：n_neighbors/min_dist 怎麼設都差不多。  
> ✅ 正確：它們會明顯影響視覺化形狀。

**陷阱3：UMAP 永遠優於 t-SNE**
> ❌ 誤解：UMAP 新所以一定更好。  
> ✅ 正確：取決於資料、目的與參數設定。

## 5. 考題怎麼問

**問法1：常用且較快的非線性降維視覺化方法**  
→ UMAP。

**問法2：n_neighbors 影響什麼**  
→ 局部與全局結構取捨。

**問法3：UMAP 結果是否可當絕對距離**  
→ 不宜過度解讀。

## 6. 記憶口訣

- **「UMAP 快速看高維，參數決定視角」**。
- **「n_neighbors 看範圍，min_dist 看緊密」**。
- **「降維圖是近似，不是地圖真相」**。

## 7. 官方指引對應線索

對應科目三非監督式降維與視覺化。考試常從 UMAP 與 t-SNE 比較、局部/全局結構、參數敏感性與降維結果解讀命題。''',
57: '''# Apriori 關聯規則

## 1. 核心概念

**Apriori** 是關聯規則探勘方法，用於找出交易資料中經常一起出現的項目組合，例如「買尿布的人也常買啤酒」。它先找頻繁項集，再從頻繁項集產生規則。

Apriori 的核心性質是：若一個項集是頻繁的，它的所有子集也必定頻繁；反過來，若某項集不頻繁，包含它的更大項集也不可能頻繁。這能大幅減少搜尋空間。

## 2. 考試重點

- 用於購物籃分析與關聯規則。
- 先找頻繁項集，再產生規則。
- Support 衡量項集出現比例。
- Confidence 衡量 A 發生時 B 發生比例。
- Lift 衡量是否高於獨立情況。
- Apriori property 用於剪枝。
- 項目多時候選集可能爆炸。

## 3. 名詞解釋

- **Frequent Itemset**：頻繁項集。
- **Association Rule**：關聯規則，如 A → B。
- **Support**：支持度，A 和 B 同時出現比例。
- **Confidence**：信賴度，A 出現時 B 出現比例。
- **Lift**：提升度，規則相對獨立情況的強度。
- **Apriori Property**：頻繁項集的子集也頻繁。

## 4. 常見陷阱

**陷阱1：Confidence 高就一定有強關聯**
> ❌ 誤解：confidence 高代表規則一定有價值。  
> ✅ 正確：若 B 本來就常出現，confidence 可能高但 lift 不高。

**陷阱2：把關聯當因果**
> ❌ 誤解：A→B 表示 A 造成 B。  
> ✅ 正確：關聯規則只表示共現，不證明因果。

**陷阱3：忽略 support**
> ❌ 誤解：少數幾筆形成的高 confidence 規則很可靠。  
> ✅ 正確：support 太低可能不穩定。

## 5. 考題怎麼問

**問法1：購物籃找常一起買的商品**  
→ Apriori 或 FP-Growth。

**問法2：A 出現時 B 出現比例是什麼**  
→ Confidence。

**問法3：衡量規則是否高於獨立情況**  
→ Lift。

## 6. 記憶口訣

- **「Support 看常不常，Confidence 看準不準，Lift 看有沒有超出偶然」**。
- **「關聯不是因果」**。
- **「不頻繁的子集，上層不用找」**。

## 7. 官方指引對應線索

對應科目三非監督式學習與關聯規則。考試常從 Apriori、頻繁項集、support/confidence/lift、購物籃分析與關聯不等於因果命題。''',
58: '''# FP-Growth

## 1. 核心概念

**FP-Growth** 是關聯規則探勘方法，用 FP-tree 壓縮交易資料，再從樹中挖掘頻繁項集。它和 Apriori 一樣用於購物籃分析，但通常比 Apriori 更有效率，因為不需要反覆產生大量候選項集。

FP-Growth 的流程包含兩步：先掃描交易資料建立頻繁項目與 FP-tree，再從條件模式基遞迴挖掘頻繁項集。它適合項目多、交易量大時降低候選集爆炸問題。

## 2. 考試重點

- 用於頻繁項集與關聯規則。
- 使用 FP-tree 壓縮交易資料。
- 避免 Apriori 大量候選集產生。
- 通常效率較 Apriori 好。
- 仍需設定最小 support。
- 結果可再產生 association rules。

## 3. 名詞解釋

- **FP-Growth**：Frequent Pattern Growth。
- **FP-tree**：頻繁模式樹，壓縮交易資料。
- **Conditional Pattern Base**：條件模式基。
- **Frequent Pattern**：頻繁模式。
- **Minimum Support**：最小支持度門檻。

## 4. 常見陷阱

**陷阱1：FP-Growth 和分類模型混淆**
> ❌ 誤解：FP-Growth 用來預測標籤。  
> ✅ 正確：它用於頻繁項集與關聯規則，不是監督式分類。

**陷阱2：不需 support 門檻**
> ❌ 誤解：FP-tree 會自動找出所有有用規則。  
> ✅ 正確：仍需最小支持度等門檻控制結果。

**陷阱3：關聯規則代表因果**
> ❌ 誤解：一起買就代表前者造成後者。  
> ✅ 正確：只表示共現關係。

## 5. 考題怎麼問

**問法1：比 Apriori 少產生候選集的方法**  
→ FP-Growth。

**問法2：FP-Growth 用什麼結構壓縮交易**  
→ FP-tree。

**問法3：FP-Growth 用於什麼任務**  
→ 頻繁項集/關聯規則探勘。

## 6. 記憶口訣

- **「Apriori 生候選，FP-Growth 建樹挖模式」**。
- **「FP-tree 壓交易，少爆候選集」**。
- **「關聯規則看共現，不看因果」**。

## 7. 官方指引對應線索

對應科目三非監督式學習與關聯規則。考試常從 FP-tree、頻繁項集、與 Apriori 效率差異、support 門檻與購物籃分析命題。''',
59: '''# Isolation Forest 異常偵測

## 1. 核心概念

**Isolation Forest** 是異常偵測方法，核心直覺是：異常點通常少且和多數資料不同，因此用隨機切割時更容易被快速孤立。它建立多棵隨機樹，觀察樣本被隔離所需的平均路徑長度；越短代表越可能異常。

Isolation Forest 適合高維或大量資料中的無監督異常偵測，例如詐欺候選、設備故障、資安異常。它不需要正常分布假設，也不依賴距離密度估計，但 contamination 參數會影響異常比例判定。

## 2. 考試重點

- 無監督異常偵測。
- 異常點較容易被隨機切割孤立。
- 路徑越短，越可能異常。
- 適合高維與大量資料。
- contamination 控制預期異常比例。
- 輸出通常是 anomaly score。
- 異常不一定代表錯誤，也可能是重要事件。

## 3. 名詞解釋

- **Isolation Forest**：以隨機孤立樣本進行異常偵測的方法。
- **Anomaly Score**：異常分數。
- **Path Length**：樣本在樹中被隔離所需路徑長度。
- **Contamination**：預期資料中異常比例。
- **Outlier**：離群值。

## 4. 常見陷阱

**陷阱1：異常點一定是錯誤資料**
> ❌ 誤解：偵測到 anomaly 就刪除。  
> ✅ 正確：可能是詐欺、故障、罕見但重要事件，需人工/業務確認。

**陷阱2：contamination 不影響結果**
> ❌ 誤解：異常比例參數可隨便設。  
> ✅ 正確：它會影響判定閾值與異常數量。

**陷阱3：需要標籤才能用**
> ❌ 誤解：沒有異常標籤不能做。  
> ✅ 正確：Isolation Forest 可無監督使用。

## 5. 考題怎麼問

**問法1：無標籤找異常交易候選**  
→ Isolation Forest 可用。

**問法2：Isolation Forest 為何能找異常**  
→ 異常點較容易被隨機切割孤立。

**問法3：路徑長度短代表什麼**  
→ 較可能異常。

## 6. 記憶口訣

- **「異常點孤單，隨機一切就分開」**。
- **「路徑越短，越像異常」**。
- **「異常先標記，不急著刪除」**。

## 7. 官方指引對應線索

對應科目三非監督式學習與異常偵測。考試常從 Isolation Forest、路徑長度、contamination、無標籤異常偵測與異常解讀命題。''',
60: '''# One-Class SVM

## 1. 核心概念

**One-Class SVM** 是異常偵測方法，通常只用「正常資料」訓練模型，學出一個包住正常樣本的邊界。新資料若落在邊界外，就可能被判為異常。

它適合異常樣本很少、很難收集，但正常資料相對充足的場景，例如設備正常狀態監控、資安異常偵測或品質檢測。透過 kernel trick，One-Class SVM 可學習非線性正常區域。

限制是它對特徵尺度、kernel、nu、gamma 等參數敏感，大資料訓練成本也可能較高。若正常資料本身分布很複雜或含有污染異常，邊界可能不穩。

## 2. 考試重點

- 常用於無監督/半監督異常偵測。
- 主要用正常資料學正常邊界。
- 邊界外樣本視為異常候選。
- 可用 kernel 處理非線性邊界。
- 需標準化特徵。
- nu 影響異常比例與支援向量比例。
- gamma 影響 RBF 邊界複雜度。
- 大資料成本較高。

## 3. 名詞解釋

- **One-Class SVM**：用單一類別資料學正常邊界的 SVM。
- **Novelty Detection**：新奇偵測，判斷新樣本是否偏離正常。
- **Kernel**：核函數，隱式映射到高維特徵空間。
- **nu**：控制異常比例上限與支援向量比例的參數。
- **gamma**：RBF kernel 影響範圍參數。
- **Decision Boundary**：正常區域邊界。

## 4. 常見陷阱

**陷阱1：需要大量異常標籤**
> ❌ 誤解：One-Class SVM 必須有很多異常樣本。  
> ✅ 正確：通常只用正常資料或以正常資料為主。

**陷阱2：不需標準化**
> ❌ 誤解：SVM 類方法不受尺度影響。  
> ✅ 正確：距離與 kernel 對尺度敏感，需標準化。

**陷阱3：nu/gamma 隨便設**
> ❌ 誤解：參數不太影響邊界。  
> ✅ 正確：參數會強烈影響異常判定。

## 5. 考題怎麼問

**問法1：只有正常資料，要偵測未來異常**  
→ One-Class SVM。

**問法2：One-Class SVM 學什麼**  
→ 學正常資料所在區域的邊界。

**問法3：為何要標準化**  
→ 因為 kernel/距離對尺度敏感。

## 6. 記憶口訣

- **「只看正常，畫出邊界」**。
- **「邊界之外，異常候選」**。
- **「One-Class SVM 怕尺度，參數要調好」**。

## 7. 官方指引對應線索

對應科目三異常偵測與傳統機器學習演算法。考試常從正常資料建模、kernel、nu/gamma、標準化、與 Isolation Forest 的差異命題。'''
}
for seg in guide['segments']:
    if seg.get('id') in contents:
        seg['content']=contents[seg['id']]
        seg['round']=max(int(seg.get('round',0) or 0),2)
s3=state.setdefault('s3',{})
comp=set(s3.get('completed',[])); fail=set(s3.get('failed',[]))
for i in contents: comp.add(i); fail.discard(i)
s3['completed']=sorted(comp); s3['failed']=sorted(fail)
ft={str(k):v for k,v in s3.get('failedTitles',{}).items()}
for i in contents: ft.pop(str(i),None)
s3['failedTitles']=ft
state['lastUpdated']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
guide_path.write_text(json.dumps(guide,ensure_ascii=False,indent=2),encoding='utf-8')
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'backup: {backup_dir}')
print('updated S3 ids 51-60 directly by Hermes; no Claude Code subprocess used')
