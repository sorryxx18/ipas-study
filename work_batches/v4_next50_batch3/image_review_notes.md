# 第4批50題圖片審查備註

## official_115_1_subject3_40
可見題幹：28×28手寫數字攤平為784維，分0～9共10類，標籤已轉One-Hot。
可見程式：
- `Dense(64, activation='relu', input_shape=(784,))`
- `Dense(10, activation='___(A)___')`
- `model.compile(loss='___(B)___', optimizer='adam')`
選項顯示正解組合為 `softmax, categorical_crossentropy`。10個互斥類別且標籤為One-Hot，輸出層10單元softmax、損失categorical crossentropy相符；不可誤寫成sparse categorical crossentropy，後者通常搭配整數類別標籤。

## official_115_1_subject3_41
可見PyTorch transform：
- `RandomHorizontalFlip(p=0.5)`
- `RandomRotation(15)`
- `ColorJitter(brightness=0.3)`
- `ToTensor()`
題幹指出部署時辨識「b/d/p/q」錯誤率異常偏高。核心可見風險是水平鏡像可能改變字母方向語義，卻沿用原標籤，製造語義錯標。旋轉15度可能較強但不是上述鏡像字母混淆的最直接根因；ColorJitter調亮度，不等於改灰階筆畫標籤；ToTensor順序不是此方向語義問題。

## official_115_1_subject3_43
圖片同頁可見ResNet50遷移學習程式：
- `resnet50(pretrained=True)`
- 對所有既有參數設 `requires_grad=False`
- `model.fc = nn.Linear(2048, 2)`
- Adam只接收 `model.fc.parameters()`，`lr=1e-4`
第43題文字問微調時為何通常採很小學習率（如1e-4）；可見選項D是避免更新步伐過大、破壞預訓練模型原本已學得的良好特徵表示。不可聲稱小學習率直接避免OOM、加速整體收斂或讓loss強制歸零。

## official_115_1_subject3_46
可見程式：
- `x_train, x_test = x_train / 255.0, x_test / 255.0`
- `y_train = tf.keras.utils.to_categorical(y_train, 10)`
- `y_test = tf.keras.utils.to_categorical(y_test, 10)`
可判讀：
- 影像若原為0～255，除255後縮放到0～1，不是0～31，也不是z-score標準化。
- 一致縮放通常可改善數值尺度與訓練穩定性，可能有助泛化，但其主要目的不是直接避免梯度爆炸／消失。
- `to_categorical(...,10)`把整數標籤轉為長度10的One-Hot向量，批次shape通常由 `(n,)` 變為 `(n,10)`。
- 10類One-Hot標籤適合搭配10單元softmax輸出與categorical crossentropy。
- 組合題應逐項核對來源選項，不可自行假設正確敘述組合。
