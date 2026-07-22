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
'S1_28': '''【考點】
電腦視覺（Computer Vision）的典型應用場景判斷。題目問哪個場景最適合使用電腦視覺，關鍵是資料型態是否為影像或影片。

【正解】
B。製造業生產線的缺陷自動偵測。

【為什麼】
電腦視覺擅長處理影像與影片，例如分類、物件偵測、瑕疵檢測、臉部辨識、醫學影像判讀等。製造業生產線的缺陷自動偵測通常會拍攝產品影像，再由 CNN、YOLO、影像分類或分割模型判斷是否有瑕疵，因此是最典型的電腦視覺應用。

【錯誤選項解析】
A：錯。分析客戶文字評論情感屬於自然語言處理（NLP）與情感分析，不是電腦視覺。
B：對。缺陷自動偵測需要分析產品影像，最適合使用電腦視覺。
C：錯。預測股票價格走勢通常屬於時間序列預測、統計建模或金融機器學習。
D：錯。自動回覆電子郵件主要涉及 NLP、對話系統或生成式 AI。

【名詞解釋】
- 電腦視覺：讓機器理解影像或影片內容的 AI 技術。
- CNN：卷積神經網路，常用於影像分類與特徵擷取。
- YOLO：常見即時物件偵測模型，可定位影像中的物件。
- 瑕疵檢測：判斷產品影像中是否有刮痕、破損、髒污或尺寸異常。
- NLP：自然語言處理，用於文字理解、分類、摘要、問答等。

【記憶】
應用判斷口訣：**「看影像選 CV，看文字選 NLP，看時間選時間序列」**。製造瑕疵照片/影片就是電腦視覺。''',

'official_114_2_subject3_40': '''【考點】
NumPy 向量運算與內積。題目依附圖程式碼判斷資料處理結果，正確重點是 np.dot(v1, v2) 會計算兩個向量的內積，若 v1=[1,2,3]、v2=[4,5,6]，結果為 1×4 + 2×5 + 3×6 = 32。

【正解】
C。np.dot(v1, v2) 結果為 np.int64(32)。

【為什麼】
在 NumPy 中，v1 * v2 代表逐元素相乘，結果會是每一個位置相乘後的陣列；np.dot(v1, v2) 對一維向量則代表內積，會把逐元素乘積加總。若附圖是常見 v1=[1,2,3]、v2=[4,5,6]，則 dot 結果是 4+10+18=32。

【錯誤選項解析】
A：錯。計算矩陣反矩陣通常使用 np.linalg.inv(A)，不是本題正確描述。
B：錯。v1 * v2 若為 [1,2,3] * [4,5,6]，結果應是 array([4,10,18])，不是 array([5,7,9])；[5,7,9] 比較像 v1+v2。
C：對。np.dot(v1, v2) 為向量內積，結果為 32。
D：錯。np.linalg.eig 是計算特徵值與特徵向量的函式，和本題向量內積結果不符。

【名詞解釋】
- NumPy：Python 常用的數值運算套件。
- Element-wise Multiplication：逐元素相乘，對應位置分別相乘。
- Dot Product：向量內積，逐元素相乘後加總。
- np.dot：NumPy 中計算內積、矩陣乘法等的函式。
- np.linalg.eig：計算矩陣特徵值與特徵向量的函式。

【記憶】
NumPy 口訣：**「星號逐項乘，dot 乘完再相加」**。看到 np.dot(v1, v2)，就算內積。''',

'S1_17': '''【考點】
資料標準化（Standardization）的目的。題目問主要目的，重點是讓不同特徵尺度一致，避免模型或距離計算被大數值特徵主導。

【正解】
B。讓各特徵的尺度一致，避免模型偏向大數值特徵。

【為什麼】
Standardization 通常指 Z-score 標準化，將特徵轉換為平均值 0、標準差 1。當不同特徵尺度差異很大時，例如年齡是 0–100，收入是幾萬到幾十萬，模型訓練、距離計算或梯度下降可能會受到大尺度特徵影響。標準化能讓特徵在相近尺度上被模型處理。

【錯誤選項解析】
A：錯。標準化不保證資料變成正態分布，它只是調整平均值與標準差；若原資料嚴重偏態，標準化後仍可能偏態。
B：對。標準化的主要目的就是統一尺度，降低大數值特徵不合理主導模型的風險。
C：錯。刪除異常值屬於 outlier handling，不是標準化的主要功能。
D：錯。增加訓練資料量屬於資料蒐集或資料增強，和標準化無關。

【名詞解釋】
- Standardization：常指 Z-score 標準化，將資料轉為平均值 0、標準差 1。
- Normalization：常指把資料縮放到固定範圍，例如 0 到 1。
- Feature Scaling：調整特徵尺度的資料前處理方法。
- Z-score：用 (x - mean) / std 計算標準化值。
- Gradient Descent：梯度下降，特徵尺度差異過大時可能影響收斂。

【記憶】
標準化口訣：**「不同單位先同尺度」**。標準化不是讓資料變常態，也不是刪異常值。''',

'official_115_1_subject3_25': '''【考點】
特徵轉換與資料分布判斷。Log 轉換適合右偏、長尾、乘法關係或非線性遞減特徵，但不應無差別套用在所有連續變數上。

【正解】
A。屋齡與房價若呈線性關係，Log 轉換反而破壞此結構。

【為什麼】
距離捷運站距離可能呈右偏分布，且房價對距離的影響可能不是線性，因此 Log 轉換能壓縮極端大值並改善模型表現。但屋齡若原本和房價呈較線性的關係，強行做 Log 轉換會改變特徵與目標之間的關係，反而使模型更難學習。因此特徵轉換要依資料分布與目標關係決定，不是所有特徵都套同一處理。

【錯誤選項解析】
A：對。若屋齡和房價原本接近線性，Log 轉換可能破壞有效結構。
B：錯。Log 轉換會壓縮大值，但不代表所有特徵都失去鑑別能力；是否有幫助取決於資料分布與目標關係。
C：錯。Log 轉換可以用於有單位的正值連續變數，例如金額、距離、流量；不是因為有單位就不能用。
D：錯。不同特徵可以使用不同轉換；重點是各自是否適合，而不是所有特徵必須一致。

【名詞解釋】
- Log 轉換：對數轉換，常用於壓縮右偏或長尾分布。
- 右偏分布：資料多集中在小值，少數極大值拉長右尾。
- Feature Transformation：對特徵做數學轉換以改善模型學習。
- 線性關係：特徵和目標之間可近似用直線關係表示。
- Box-Cox：一類可尋找合適次方轉換的統計方法。

【記憶】
特徵轉換口訣：**「右偏可取 log，線性別亂改」**。轉換不是全部套用，而是看分布與目標關係。''',

'official_115_1_subject1_3': '''【考點】
Word2Vec 的 CBOW 與 Skip-gram 差異。題目強調「數十億 token」與「大量長尾詞」，要判斷訓練效率與低頻詞品質的取捨。

【正解】
B。CBOW 訓練速度較快、整體語意平滑，但對低頻詞的向量品質較差；Skip-gram 以中心詞預測周圍詞，對長尾詞累積更多訓練樣本，向量品質較優。

【為什麼】
CBOW 是用上下文詞預測中心詞，通常訓練速度較快，對高頻詞和整體語意表現穩定，但對低頻詞的表示較容易被平均化。Skip-gram 則用中心詞預測周圍詞，對每個中心詞產生多個訓練樣本，通常對低頻詞或長尾詞能學到較好的向量表示，但訓練成本較高。

【錯誤選項解析】
A：錯。CBOW 透過上下文平均雖然訓練快，但通常對低頻詞不如 Skip-gram。
B：對。這正確描述 CBOW 訓練效率較高、Skip-gram 對長尾詞表示較佳的取捨。
C：錯。Skip-gram 通常訓練較慢，因為它要用中心詞預測多個上下文詞。
D：錯。兩者對低頻詞表現並不完全相同，差異不只是 batch 組織方式，而是訓練目標不同。

【名詞解釋】
- Word2Vec：將詞轉成向量表示的模型家族。
- CBOW：Continuous Bag of Words，用上下文預測中心詞。
- Skip-gram：用中心詞預測周圍上下文詞。
- Long-tail Terms：出現次數很少但種類很多的長尾詞彙。
- Word Embedding：詞向量，將詞表示成可計算語意相似度的向量。

【記憶】
Word2Vec 口訣：**「CBOW 快，Skip-gram 顧長尾」**。大量資料要效率看 CBOW，低頻詞品質看 Skip-gram。'''
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
