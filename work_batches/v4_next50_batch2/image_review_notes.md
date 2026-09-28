# 下一批50題圖片審查備註

## official_114_2_subject3_46
- 圖片是2列×10欄，共20張低解析灰階手寫數字縮圖。
- 每張都有明顯像素化與雜訊；部分輪廓仍可辨識，但圖內沒有原圖／PCA重建前後對照標籤。
- 解析可說明PCA以主成分保留主要變異、捨棄較小成分後重建以達降噪；不可聲稱圖中直接顯示了PCA前後比較或特定保留維度。

## official_114_2_subject3_49
可見程式：
- `model = Sequential()`
- `Input(shape=(X_train.shape[1],))`
- 第一層 `Dense(10, activation="relu")`
- 第二層 `Dense(10, activation="relu")`
- 輸出層 `Dense(1, activation="sigmoid")`
- compile使用 `binary_crossentropy`、`adam`、`accuracy`

摘要：
- 第一Dense輸出 `(None, 10)`，Param為空格1；若輸入特徵數為d，參數量=`d×10+10`。
- 第二Dense輸出 `(None, 10)`，Param為空格2；參數量=`10×10+10=110`。
- 第三Dense輸出 `(None, 1)`，Param=`10×1+1=11`。
- 單一sigmoid輸出搭配binary_crossentropy支持二元分類判讀。

## official_114_2_subject3_50
- 標題：`Training and Validation Loss`。
- x軸：`Epochs`，約0～100；y軸：`Loss`。
- Training Loss：藍色實線，從約0.655快速下降，之後緩降至約0.402。
- Validation Loss：紅色虛線，從約0.618快速下降，約十多個epoch後在0.45～0.47附近波動。
- 圖例位於右上：藍色實線=`Training Loss`，紅色虛線=`Validation Loss`。
- 解析程式選項時，應核對title、xlabel、ylabel、label、color及linestyle；不可自行聲稱圖上有網格或其他未顯示元素。
