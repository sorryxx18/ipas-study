# official_115_1_subject3_48 原圖可見證據

- 原圖實際檔案：`webapp/images/exam_pages/q46_48_fig.png`（題庫 `image` 欄位為相對網址，專案根目錄下無同名檔）。
- 圖名：`Training and Validation Accuracy for CIFAR-10 with CNN`。
- 橫軸：Epochs，顯示 0～9。
- 縱軸：Accuracy。
- 藍線：Train Accuracy；紅線：Validation Accuracy。
- Epoch 6：訓練準確率約 0.81，驗證準確率約 0.72，兩者出現明顯落差。
- 藍線整體持續上升；紅線較波動，在 Epoch 5 約 0.80 後，Epoch 6 明顯降至約 0.72，後續回升但 Epoch 9 又低於訓練線。
- 依題目指定的 Epoch 6 落差，可支持「訓練表現優於驗證表現，最可能為過擬合」；圖本身不足以單獨證明學習率或批次大小是直接原因。
