# 科目三《機器學習技術與應用》 — 考試出題側重分析

本報告針對題庫中屬於本科目的 130 題，逐題以語意判讀方式（非關鍵字計分）對應至《機器學習技術與應用》共 96 個讀書指引段落，統計各段落命中題數，並比對目前讀書進度，藉此找出「常考但還沒讀」的優先段落。少數題目內容橫跨兩個知識點，會同時列在兩個段落下，因此段落命中次數加總（131）會略高於題數（130）。

> 判斷方式：逐題閱讀題目、選項與詳解中的「必要名詞」，依實際考點語意對應段落，而非關鍵字出現次數計分。

## TOP20 出題熱區總覽

| 段落ID | 標題 | 命中題數 | 讀書進度 |
|---|---|---|---|
| 48 | 特徵工程 Feature Engineering | 11 | 已完成 |
| 41 | K-Fold 交叉驗證 (Stratified / LOOCV) | 8 | 已完成 |
| 31 | Ridge / Lasso 正則化 | 6 | 已完成 |
| 64 | CNN 卷積神經網路 | 5 | 已完成 |
| 65 | CNN 架構 LeNet / AlexNet / VGG / ResNet | 5 | 已完成 |
| 86 | Fairness 公平性 Statistical Parity | 5 | 已完成 |
| 19 | 穩定訓練策略 Training Stability | 4 | 已完成 |
| 43 | 分類評估指標 Precision / Recall / F1 / AUC / ROC | 4 | 已完成 |
| 63 | Activation Functions 激活函數 | 4 | 已完成 |
| 68 | Batch Normalization / Dropout | 4 | 已完成 |
| 14 | 損失函數分類與設計 | 3 | 已完成 |
| 16 | 梯度下降 GD / SGD / Mini-batch | 3 | 已完成 |
| 17 | 進階優化器 Momentum / Adagrad / RMSprop / Adam | 3 | 已完成 |
| 36 | Gradient Boosting / XGBoost | 3 | 已完成 |
| 42 | Bias-Variance 偏差-變異權衡 | 3 | 已完成 |
| 45 | 超參數調整 Grid / Random / Bayesian Search | 3 | 已完成 |
| 54 | PCA 主成分分析 | 3 | 已完成 |
| 69 | Transfer Learning 遷移學習 | 3 | 已完成 |
| 85 | Explainability SHAP / Grad-CAM / LIME | 3 | 已完成 |
| 91 | Homomorphic Encryption 同態加密 | 3 | 已完成 |

## 逐段詳細列表

### 1. 機率基礎 Probability
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 2. 統計推論 Statistical Inference
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_23`：以隨機抽樣模擬多情境估計發電量機率分布(蒙地卡羅方法)
  - `official_115_1_subject3_1`：以蒙地卡羅方法模擬市場情境估算投資組合風險值(VaR)

### 3. 條件機率 Conditional Probability
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_41`：以蒙地卡羅模擬估算擲骰子條件機率P(A|B)

### 4. 貝氏定理 Bayes Theorem
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_22`：以貝氏定理計算購買機率的條件機率推論
  - `S3_01`：貝氏定理中P(A)稱為先驗機率(Prior)

### 5. 期望值與變異數 Expectation & Variance
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 6. 常態分布 Normal Distribution
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 7. 假設檢定 Hypothesis Testing
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `S3_21`：假設檢定中p值<α應拒絕虛無假設H0

### 8. 相關性與共變數 Correlation & Covariance
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 9. 向量與矩陣 Vectors & Matrices
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_33`：逐一成對比對客戶相似度的演算法時間複雜度為O(n²)
  - `official_114_2_subject3_40`：NumPy向量內積(np.dot)運算結果判讀

### 10. 特徵值分解 Eigendecomposition
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 11. OLS 最小平方法
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_24`：殘差圖系統性彎曲顯示異常值或非線性關係違反迴歸假設
  - `official_115_1_subject3_5`：殘差圖擴散現象代表殘差變異數不一致(異質變異)

### 12. 損失函數 Loss Functions
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `S3_19`：損失函數在機器學習中的作用：量化預測與真實值差距引導優化

### 13. 可行域與凸性 Convexity
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_3`：非凸目標函數優化易陷入局部最優解

### 14. 損失函數分類與設計
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_2`：希望模型對極端高價物件更敏感應選用MSE損失函數
  - `official_115_1_subject3_10`：迴歸(MSE)與二元分類(Binary Cross-Entropy)應選用不同損失函數
  - `official_115_1_subject3_20`：CrossEntropyLoss內含Softmax，輸出層應直接輸出未正規化logits

### 15. 損失函數對學習行為的影響
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 16. 梯度下降 GD / SGD / Mini-batch
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_12`：調整學習率(Learning Rate)改善收斂速度不穩定問題
  - `official_115_1_subject3_11`：以Mini-batch梯度下降平衡梯度穩定性與GPU吞吐量
  - `S3_28`：Mini-batch梯度下降在計算效率與梯度準確性間取得平衡

### 17. 進階優化器 Momentum / Adagrad / RMSprop / Adam
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_17`：Adam優化器內建動量(Momentum)設計機制
  - `official_115_1_subject3_9`：Adam結合一階動量與自適應學習率改善訓練穩定性
  - `S3_02`：Adam優化器能自動調整每個參數的學習率

### 18. 收斂判準 Convergence Criteria
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_8`：學習率過高導致損失函數震盪或發散，無法穩定收斂

### 19. 穩定訓練策略 Training Stability
- 命中題數：4
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_31`：驗證損失震盪時以耐心值(Patience)設定早期停止較為適當
  - `official_114_2_subject3_50`：Matplotlib繪圖樣式判讀訓練/驗證損失曲線
  - `official_115_1_subject3_50`：梯度裁剪(Gradient Clipping)插入位置與限制梯度範數避免Loss變NaN
  - `S3_07`：Early Stopping目的：驗證效能停滯時提前終止訓練防過擬合

### 20. ML脈絡應用 ML Context
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 21. ML基本結構與特徵空間
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 22. 任務類型與標籤型態
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 23. 模型假設空間 Hypothesis Space
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 24. 資料分割與評估準則 Precision / Recall
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 25. 監督式學習 Supervised Learning
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_28`：訓練樣本僅涵蓋高活躍顧客導致取樣偏差，新會員預測失準

### 26. 非監督式學習 Unsupervised Learning
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 27. 強化式學習 Reinforcement Learning (MDP)
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 28. 強化式學習任務類型與訓練流程
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_31`：RL獎勵設計被鑽漏洞(reward hacking)，應改為以任務完成度塑形獎勵

### 29. 強化式學習應用場景
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 30. 線性迴歸 Linear Regression
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 31. Ridge / Lasso 正則化
- 命中題數：6
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_2`：L1(Lasso)正則化使部分權重收斂為零，產生稀疏模型
  - `official_114_2_subject3_32`：高相關特徵中希望自動篩選代表特徵：採用L1(Lasso)正則化
  - `official_115_1_subject3_7`：L1正則化面對高相關特徵時隨機保留其一，導致特徵清單不穩定
  - `official_115_1_subject3_13`：以L2權重衰減(Weight Decay)從降低複雜度角度緩解文本分類過擬合
  - `official_115_1_subject3_33`：希望保留所有特徵解釋力且控制過擬合，應選用Ridge(L2)而非Lasso
  - `S3_09`：L2正則化(Ridge)懲罰過大係數，讓權重平滑分散

### 32. 邏輯迴歸 Logistic Regression (Sigmoid / Softmax)
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `S3_26`：邏輯迴歸輸出層使用Sigmoid函數

### 33. 決策樹 Decision Tree (Gini / Entropy)
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_8`：資訊增益(Information Gain)用於決策樹特徵選擇分裂

### 34. Random Forest (Bagging)
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_28`：隨機森林可處理非線性關係並提供整體特徵重要性供稽核
  - `S3_04`：隨機森林使用的集成技術是Bagging

### 35. AdaBoost
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 36. Gradient Boosting / XGBoost
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_18`：XGBoost相較GBDT加入正則化、缺失值處理與並行化訓練
  - `official_115_1_subject3_16`：XGBoost目標函數加入樹複雜度懲罰項(L2)以防過擬合
  - `S3_22`：XGBoost屬於Boosting集成學習方式

### 37. SVM 支援向量機 (Kernel Trick)
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `S3_14`：SVM核函數作用：映射高維空間使線性不可分資料變可分

### 38. KNN 最近鄰
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 39. Naive Bayes 樸素貝氏
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_14`：Naive Bayes條件機率受訓練資料分布影響誤判促銷郵件為垃圾信

### 40. 訓練 / 驗證 / 測試集分割
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 41. K-Fold 交叉驗證 (Stratified / LOOCV)
- 命中題數：8
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_1`：以交叉驗證評估模型對新資料的泛化穩定度
  - `official_114_2_subject3_29`：工況變化下改採時間序列交叉驗證/滑動視窗驗證動態更新驗證集
  - `official_114_2_subject3_34`：小樣本嚴重不平衡資料採用分層留一法交叉驗證
  - `official_114_2_subject3_47`：KNN搭配交叉驗證程式碼(cross_val_score)正確性判讀
  - `official_115_1_subject3_27`：行為模式隨時間改變，改採滾動窗口驗證(Rolling Window Validation)
  - `official_115_1_subject3_44`：LDA降維在交叉驗證外先做導致資料洩漏，應納入CV流程中
  - `official_115_1_subject3_45`：以StratifiedKFold確保交叉驗證各折類別比例與原始資料一致
  - `S3_15`：K-Fold交叉驗證主要目的：更可靠估計泛化效能

### 42. Bias-Variance 偏差-變異權衡
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_26`：擴增特徵變數提升表達能力不屬於降低模型複雜度的防過擬合作法
  - `official_115_1_subject3_30`：訓練AUC遠高於驗證AUC且跨折差異大，屬於高變異(High Variance)
  - `official_115_1_subject3_48`：訓練0.81顯著大於驗證0.72，判斷為模型過擬合(Overfitting)

### 43. 分類評估指標 Precision / Recall / F1 / AUC / ROC
- 命中題數：4
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_16`：由Precision=0.8, Recall=0.6計算F1分數
  - `official_115_1_subject3_32`：F1-score為Precision與Recall的調和平均，對較小值敏感
  - `S3_05`：F1 Score計算公式(Precision與Recall調和平均)
  - `S3_24`：AUC-ROC中AUC越接近1代表模型區分正負類能力越強

### 44. 迴歸評估指標 MAE / MSE / RMSE / R²
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_15`：線性迴歸R²=0.85代表85%變異可被模型解釋
  - `official_114_2_subject3_38`：程式碼計算的評估指標為MSE

### 45. 超參數調整 Grid / Random / Bayesian Search
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_11`：Random Search相較Grid Search更能有效搜尋高維參數空間
  - `official_115_1_subject3_34`：Grid Search總訓練模型數計算(含5-Fold交叉驗證)
  - `S3_13`：Bayesian Optimization相較Grid Search能智慧選擇下一組超參數

### 46. 模型選擇原則
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `S3_30`：選擇機器學習模型最重要考量：資料類型/任務性質/資料量

### 47. 資料不平衡處理 SMOTE / ClassWeight
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_19`：3%罕見病例情境中Accuracy最不適合作為評估指標
  - `official_115_1_subject3_12`：類別極不平衡下Accuracy無法反映對少數類(肺癌陽性)的偵測能力

### 48. 特徵工程 Feature Engineering
- 命中題數：11
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_9`：距離基礎模型(KNN/SVM)前處理關鍵：特徵縮放
  - `official_114_2_subject3_20`：以特徵乘積/交互組合建立互動特徵(價格x滿意度)
  - `official_114_2_subject3_25`：傳統信用評分卡開發流程(分箱/IV/PSI)，排除生成式模型特徵學習
  - `official_114_2_subject3_48`：標準化程式碼判讀(mean/std調整，非特徵選擇)
  - `official_115_1_subject3_24`：高基數類別特徵以One-Hot編碼最容易造成維度爆炸
  - `official_115_1_subject3_25`：距離特徵右偏適合Log轉換，屋齡若呈線性關係轉換反而破壞結構
  - `official_115_1_subject3_26`：滑動窗口(Sliding Window)用於建立時間序列滯後特徵
  - `official_115_1_subject3_46`：像素/255正規化與One-hot標籤搭配softmax的資料前處理判讀
  - `S3_08`：One-Hot Encoding適合無序類別特徵
  - `S3_20`：特徵選擇主要目的：移除冗餘特徵降低維度提升效能
  - `S3_27`：缺失值處理常見做法：均值/中位數/眾數填補或模型預測補值

### 49. 模型部署與監控 Data Drift / A/B Test
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 50. 模型評估選擇小結
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 51. K-means 聚類
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_15`：K-means對K值、初始化與離群值敏感，難處理非凸群集
  - `S3_10`：K-means選擇最佳K值常用肘部法則(Elbow Method)

### 52. Hierarchical Clustering 層次聚類
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 53. DBSCAN
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_4`：DBSCAN中鄰域不足以形成核心點的資料點歸類為雜訊點

### 54. PCA 主成分分析
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_35`：PCA特徵值計算解釋變異比例，決定保留主成分數
  - `official_114_2_subject3_46`：PCA降噪程式碼修正(n_components設定錯誤)
  - `S3_11`：PCA核心數學原理：找到最大化變異量的正交方向

### 55. t-SNE
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_6`：t-SNE保留局部結構適合視覺化，不適合作為模型輸入特徵

### 56. UMAP
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 57. Apriori 關聯規則
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 58. FP-Growth
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 59. Isolation Forest 異常偵測
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_29`：僅有正常資料缺乏故障標註，屬非監督/半監督異常偵測

### 60. One-Class SVM
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 61. Neural Network 類神經網路
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_49`：Keras Sequential模型Dense層參數量計算

### 62. Backpropagation 反向傳播
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 63. Activation Functions 激活函數
- 命中題數：4
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_27`：線性激活函數限制模型表達力，改用ReLU引入非線性
  - `official_115_1_subject3_40`：10類別One-Hot標籤單標籤分類應用softmax+categorical_crossentropy
  - `S3_03`：ReLU激活函數優點：計算簡單且緩解梯度消失
  - `S3_18`：多類別分類輸出層應使用Softmax激活函數

### 64. CNN 卷積神經網路
- 命中題數：5
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_5`：CNN第一層卷積層負責提取局部特徵
  - `official_114_2_subject3_6`：CNN透過局部感受野與參數共享降低參數量與運算複雜度
  - `official_115_1_subject3_4`：水平翻轉資料擴增造成手寫數字語意不一致(6變9)
  - `official_115_1_subject3_18`：池化層降低特徵圖空間維度，減少參數與計算量
  - `official_115_1_subject3_41`：RandomHorizontalFlip破壞b/d/p/q字母方向語意，導致辨識錯誤率偏高

### 65. CNN 架構 LeNet / AlexNet / VGG / ResNet
- 命中題數：5
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_42`：VGG16中全連接層(Linear)參數量最多
  - `official_114_2_subject3_43`：VGG16中卷積層(Conv2d)運算量(FLOPs)最多
  - `official_114_2_subject3_44`：VGG16架構敘述判讀(卷積層數/全連接層數/總參數量)
  - `official_115_1_subject3_17`：深層CNN梯度消失，改採ResNet殘差連接改善梯度傳遞
  - `official_115_1_subject3_49`：50層深網路欲避免梯度消失，優先選用ResNet殘差連接架構

### 66. RNN 遞迴神經網路
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 67. LSTM / GRU
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_7`：LSTM最適合應用於電力需求時間序列預測
  - `S3_06`：LSTM主要解決RNN的梯度消失問題

### 68. Batch Normalization / Dropout
- 命中題數：4
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_39`：程式碼實現的正則化技術為Dropout
  - `official_115_1_subject3_47`：CNN程式碼中BatchNorm/Dropout/Flatten功能描述正確性判讀
  - `S3_12`：Batch Normalization對每層輸入標準化，加速收斂穩定訓練
  - `S3_23`：Dropout原理：訓練時隨機關閉部分神經元防過擬合

### 69. Transfer Learning 遷移學習
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_30`：跨語言情感分析F1驟降：語言遷移造成召回率下降
  - `official_114_2_subject3_45`：VGG16遷移學習：凍結卷積層只訓練分類器程式碼判讀
  - `official_115_1_subject3_42`：凍結所有預訓練權重僅訓練新分類頭，屬於特徵萃取(Feature Extraction)策略

### 70. Fine-tuning 微調
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_43`：微調時使用極小學習率避免破壞預訓練模型已學好的特徵表示

### 71. Attention Mechanism 注意力機制
- 命中題數：2
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_21`：多頭注意力(Multi-head Attention)可從不同表示子空間捕捉多樣關聯
  - `official_115_1_subject3_3`：Transformer Attention層Q x WQ矩陣維度相容性計算

### 72. Transformer 架構
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_19`：Transformer的Self-Attention任意token直接關聯且可平行運算，優於BiLSTM

### 73. BERT
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_23`：BERT(Encoder)無法逐步生成後續文字，較不適合生成任務，GPT-2(Decoder)適合

### 74. GPT 系列
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_23`：BERT(Encoder)無法逐步生成後續文字，較不適合生成任務，GPT-2(Decoder)適合

### 75. LoRA / PEFT 參數高效微調
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_35`：LoRA降低rank但套用更多層，維持可訓練參數量不變以省記憶體

### 76. 模型壓縮技術：量化、知識蒸餾、剪枝與混合精度訓練
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_21`：32-bit浮點權重轉8-bit整數且不重新訓練，屬於模型量化(Quantization)

### 77. RAG 檢索增強生成
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_115_1_subject3_22`：RAG檢索語意不準：採混合搜尋(向量+BM25)並以RRF融合排序

### 78. GAN 生成對抗網路與 Autoencoder 自編碼器
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 79. Diffusion Models 擴散模型
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 80. Object Detection YOLO / R-CNN
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 81. Semantic Segmentation
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 82. 強化學習進階 Policy Gradient / PPO
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 83. Federated Learning 聯邦學習
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 84. Differential Privacy 差分隱私
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `S3_25`：去識別化目的：移除可識別個人欄位保護隱私同時保留可用性

### 85. Explainability SHAP / Grad-CAM / LIME
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_14`：醫療腫瘤判讀情境中可解釋性最為關鍵
  - `official_115_1_subject3_37`：SHAP值計算單筆預測特徵貢獻，實現貸款拒絕的局部可解釋性
  - `S3_17`：SHAP和LIME主要用於解釋模型預測結果

### 86. Fairness 公平性 Statistical Parity
- 命中題數：5
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_13`：標籤偏差(Label Bias)源自標記資料本身帶有主觀偏見
  - `official_115_1_subject3_38`：男女通過率差異明顯，不符合統計均等(Statistical Parity)公平定義
  - `official_115_1_subject3_39`：不可用性別欄位限制下，仍可於訓練中加入公平性懲罰項(In-processing)
  - `S3_16`：AI演算法偏見最常見來源：訓練資料本身歷史偏差或樣本不均衡
  - `S3_29`：公平性指標Demographic Parity定義：不同群體正面預測比例相同

### 87. Responsible AI 負責任AI
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 88. MLOps 機器學習運維
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 89. Model Monitoring 模型監控
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 90. AutoML 自動機器學習
- 命中題數：1
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_10`：AutoML最適合缺乏專職工程師快速比較多模型的情境

### 91. Homomorphic Encryption 同態加密
- 命中題數：3
- 讀書進度：已完成
- 標記：✅ 常考且已讀完 → 沒問題
- 命中題目：
  - `official_114_2_subject3_36`：同態加密使資料在加密狀態下仍可運算，訓練於未解密資料上完成
  - `official_114_2_subject3_37`：跨銀行風控平台加密方案組合：同態加密+非對稱加密+雜湊+對稱加密
  - `official_115_1_subject3_36`：雲端不解密即可運算加密資料，符合同態加密特性

### 92. Multi-Agent Systems 多智能體
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 93. Human-in-the-Loop HITL
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 94. Edge AI 邊緣運算AI
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 95. 科目3 總複習 Review
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

### 96. 深度學習框架 TensorFlow / PyTorch / JAX
- 命中題數：0
- 讀書進度：已完成
- 標記：⭕ 完全沒考過 → 可以先跳過或最後讀

## 整體觀察

本科目（科目三）130 題中，出題最集中的段落是特徵工程 Feature Engineering(48，11題)與K-Fold交叉驗證(41，8題)，其次是Ridge/Lasso正則化(31)、CNN卷積神經網路(64)與CNN經典架構(65)。整體來看科目三的考題高度集中在「模型驗證方法論」(交叉驗證、資料洩漏、Bias-Variance、過擬合防治)與「CNN/深度學習基礎」兩大群，這與官方考試大量出現程式碼判讀題（VGG16參數量、cross_val_score、PCA降噪、StratifiedKFold等）直接相關——這類題目本質是在檢驗考生是否真的懂交叉驗證與特徵工程的實作細節，而不只是背定義。

由於科目三讀書進度已100%完成（96段全數讀完），因此本科目沒有🔥「常考但尚未讀」的段落，全部命中段落都標記為✅已讀完。但仍有 41 個段落（占96段近43%）完全沒有被260題題庫命中過，包括機率基礎(1)、常態分布(6)、相關性與共變數(8)、特徵值分解(10)、多項ML基礎概念段落(20-24)、多個非監督式學習演算法(AdaBoost/KNN/UMAP/Apriori/FP-Growth/One-Class SVM等)、RNN(66)、GAN/Diffusion(78-79)、YOLO/R-CNN物件偵測(80)、語義分割(81)、聯邦學習(83)、以及MLOps/模型監控/多智能體/HITL/Edge AI等應用治理段落(87-89, 92-94)。這些雖然目前沒有實測題目命中，但多屬於官方學習指引明確列出的核心考點，建議仍按進度完整複習，不宜完全略過。

需要特別提醒的落差：蒙地卡羅方法(Monte Carlo)在官方考題中至少出現3次（風險估算VaR、發電量模擬、擲骰子條件機率），但《科目三學習指引》96段全文搜尋不到「蒙地卡羅」或「Monte Carlo」字樣，只能勉強掛在機率基礎/統計推論/條件機率段落下；另外取樣偏差(Sampling Bias)、演算法時間複雜度(O(n²))、去識別化(De-identification)、資料增強(Data Augmentation)等考點在96段指引中也都沒有專門段落。這些是指引內容相對於實際出題的明確缺口，建議額外筆記補充。