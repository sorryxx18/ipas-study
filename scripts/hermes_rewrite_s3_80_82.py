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
80: '''# Object Detection YOLO / R-CNN

## 1. 核心概念

**物件偵測（Object Detection）** 是電腦視覺中用來同時回答「影像中有什麼物件」以及「物件在哪裡」的任務。它比影像分類更進一步：分類只輸出整張圖的類別；物件偵測需要輸出類別與邊界框（Bounding Box）。

物件偵測常用於自動駕駛、安防監控、智慧製造瑕疵檢測、零售貨架辨識、醫療影像標記與交通違規偵測。模型必須在影像中找出多個物件，並為每個物件預測位置與類別，因此評估時通常同時看定位準確度與分類準確度。

常見架構可分為兩類：**Two-stage detector** 與 **One-stage detector**。R-CNN 系列屬於 two-stage，先產生候選區域，再分類與修正邊界框，通常精度較高但速度較慢。YOLO（You Only Look Once）屬於 one-stage，直接在一次前向傳播中預測邊界框與類別，速度快，適合即時偵測。

科目三重點是能比較 YOLO 與 R-CNN 的差異，理解物件偵測和影像分類、語意分割的不同，以及知道常見指標如 IoU、mAP 的用途。

## 2. 考試重點

- **任務定義**：物件偵測要同時預測物件類別與位置。
- **Bounding Box**：用矩形框標示物件位置，常以 x、y、寬、高表示。
- **YOLO 特性**：one-stage，速度快，適合即時偵測。
- **R-CNN 特性**：two-stage，先找候選區域再分類，通常較精細但較慢。
- **和分類差異**：分類只判斷整張圖類別；偵測要找出多個物件位置。
- **和分割差異**：偵測輸出框；分割輸出每個像素的類別或物件遮罩。
- **IoU**：衡量預測框和真實框重疊程度。
- **mAP**：常用於評估物件偵測模型整體表現。

## 3. 名詞解釋

- **Object Detection（物件偵測）**：找出影像中物件類別與位置的任務。
- **Bounding Box（邊界框）**：框住物件位置的矩形。
- **YOLO**：You Only Look Once，one-stage 即時物件偵測模型系列。
- **R-CNN**：Region-based CNN，先產生候選區域再做分類與定位的模型系列。
- **IoU（Intersection over Union）**：預測框與真實框重疊面積除以聯集面積。
- **mAP（mean Average Precision）**：物件偵測常用整體評估指標。

## 4. 常見陷阱

**陷阱1：把物件偵測當成影像分類**
> ❌ 誤解：物件偵測只要回答圖片中有沒有貓。  
> ✅ 正確：物件偵測還要框出貓在哪裡，且可偵測多個物件。

**陷阱2：把 YOLO 和 R-CNN 速度特性搞反**
> ❌ 誤解：R-CNN 是即時偵測代表，YOLO 是慢但精細。  
> ✅ 正確：YOLO 通常速度快；R-CNN 系列通常較精細但較慢。

**陷阱3：以為邊界框等於像素級分割**
> ❌ 誤解：框出物件就等於知道每個像素屬於誰。  
> ✅ 正確：偵測給框；分割才給像素級遮罩。

**陷阱4：只看分類正確率**
> ❌ 誤解：類別判對就代表物件偵測成功。  
> ✅ 正確：框的位置也要準確，因此要看 IoU、mAP 等指標。

## 5. 考題怎麼問

**問法1：問影像中物件在哪裡**  
→ 答 Object Detection / Bounding Box。

**問法2：問即時偵測模型**  
→ 看到「即時」「一次看完」→ 答 YOLO。

**問法3：問候選區域兩階段方法**  
→ 答 R-CNN / Fast R-CNN / Faster R-CNN。

**問法4：問偵測模型評估指標**  
→ 答 IoU、Precision、Recall、mAP。

## 6. 記憶口訣

- **「分類說是什麼，偵測說在哪裡」**：分類和偵測分清楚。
- **「YOLO 快，一眼看完」**：one-stage 即時偵測直覺。
- **「R-CNN 先找區域再判斷」**：two-stage 的核心流程。

## 7. 官方指引對應線索

此主題屬於科目三電腦視覺與深度學習應用範圍。考試常從影像分類、物件偵測、語意分割差異，YOLO/R-CNN 架構比較，以及 IoU/mAP 評估指標命題。''',
81: '''# Semantic Segmentation

## 1. 核心概念

**語意分割（Semantic Segmentation）** 是電腦視覺中對影像每一個像素進行分類的任務。它不只判斷影像中有什麼，也不只是用框標出位置，而是要判斷每個像素屬於哪個類別，例如道路、天空、車輛、行人、建築或背景。

語意分割和物件偵測的差異在於輸出精細度。物件偵測輸出邊界框，適合回答「物件在哪一塊區域」；語意分割輸出像素級分類圖，適合需要精細邊界的任務，例如自動駕駛道路場景理解、醫療影像器官區域標註、衛星影像土地覆蓋分類、工業瑕疵區域定位。

語意分割通常使用全卷積網路（FCN）、U-Net、DeepLab 等架構。U-Net 因為能結合下採樣的語意資訊與上採樣的細節資訊，常用於醫療影像分割。模型輸出通常是一張與原圖尺寸相同或可還原到原圖尺寸的類別圖。

科目三重點是分清楚影像分類、物件偵測、語意分割與實例分割：分類是整張圖；偵測是框；語意分割是每個像素的類別；實例分割則進一步區分同類別中的不同個體。

## 2. 考試重點

- **任務定義**：語意分割是像素級分類，每個像素都要有類別。
- **輸出形式**：輸出 segmentation mask 或 label map，不是單一類別或邊界框。
- **和物件偵測差異**：偵測輸出框；分割輸出像素級區域。
- **和實例分割差異**：語意分割不區分同類別不同個體；實例分割會區分。
- **常見應用**：自動駕駛、醫療影像、衛星影像、工業瑕疵、背景去除。
- **常見架構**：FCN、U-Net、DeepLab。
- **評估指標**：Pixel Accuracy、IoU、mIoU、Dice coefficient。
- **資料需求**：需要像素級標註，標註成本通常高於分類與偵測。

## 3. 名詞解釋

- **Semantic Segmentation（語意分割）**：將影像每個像素分類到語意類別的任務。
- **Segmentation Mask（分割遮罩）**：標示每個像素類別的圖。
- **U-Net**：常用於醫療影像分割的編碼器-解碼器式網路。
- **mIoU（mean Intersection over Union）**：分割任務常用平均交並比指標。
- **Dice Coefficient**：衡量預測區域與真實區域重疊程度的指標，醫療影像常用。
- **Instance Segmentation（實例分割）**：不只分像素類別，還區分同類別不同物件個體。

## 4. 常見陷阱

**陷阱1：把語意分割和物件偵測混淆**
> ❌ 誤解：用框框出車輛就是語意分割。  
> ✅ 正確：語意分割要對每個像素分類，輸出像素級遮罩。

**陷阱2：以為語意分割會區分每一台車**
> ❌ 誤解：所有分割都會分出車 A、車 B、車 C。  
> ✅ 正確：語意分割只標為「車」類別；實例分割才區分不同個體。

**陷阱3：忽略標註成本**
> ❌ 誤解：分割資料和分類資料一樣容易準備。  
> ✅ 正確：像素級標註非常耗時，資料成本高。

**陷阱4：只用 Accuracy 評估**
> ❌ 誤解：Pixel Accuracy 高就一定代表分割好。  
> ✅ 正確：類別不平衡時 Accuracy 可能誤導，需看 mIoU、Dice 等指標。

## 5. 考題怎麼問

**問法1：問每個像素屬於哪個類別**  
→ 答 Semantic Segmentation。

**問法2：問醫療影像器官輪廓標註**  
→ 答語意分割 / U-Net / Dice coefficient。

**問法3：問同類別物件是否區分個體**  
→ 語意分割不區分；實例分割會區分。

**問法4：問分割評估指標**  
→ 答 IoU、mIoU、Dice coefficient。

## 6. 記憶口訣

- **「分類看整張，偵測畫框，分割塗像素」**：三種 CV 任務分清楚。
- **「語意不分個體，實例才分你我」**：語意分割 vs 實例分割。
- **「醫療分割常 U-Net，評估常 Dice」**：常考組合。

## 7. 官方指引對應線索

此主題屬於科目三電腦視覺、影像分析與深度學習應用範圍。考試常從分類、偵測、語意分割、實例分割差異，以及 U-Net、mIoU、Dice 等架構與指標命題。''',
82: '''# 強化學習進階 Policy Gradient / PPO

## 1. 核心概念

**強化學習（Reinforcement Learning, RL）** 是讓代理人（Agent）在環境中透過行動與回饋學習策略的方法。基礎強化學習常介紹狀態、行動、獎勵與價值函數；進階方法則更關注如何直接學習策略，尤其是 **Policy Gradient** 與 **PPO（Proximal Policy Optimization）**。

**Policy Gradient** 的核心想法是直接調整策略參數，讓會帶來高累積獎勵的行動機率上升，低獎勵行動機率下降。它和 value-based 方法不同：value-based 方法通常先估計某狀態或行動的價值，再間接選動作；policy-based 方法則直接學一個從狀態到行動機率的策略。

**PPO** 是常見且穩定的 policy gradient 類演算法。它透過限制每次策略更新幅度，避免新策略和舊策略差太多，降低訓練崩壞風險。PPO 常用於機器人控制、遊戲、自動決策，也常出現在大型語言模型對齊訓練（例如 RLHF）的討論中。

科目三重點不是推導 PPO 公式，而是理解它為何存在：強化學習需要在探索與利用之間平衡，策略更新太大會不穩，PPO 用 clipped objective 限制更新幅度，讓訓練更穩定。

## 2. 考試重點

- **Policy Gradient**：直接最佳化策略，使高報酬行動機率上升。
- **和 value-based 差異**：Policy-based 直接學策略；value-based 先估價值再選動作。
- **策略（Policy）**：定義在某狀態下選擇各行動的機率或規則。
- **PPO 目的**：限制策略更新幅度，提升訓練穩定性。
- **Clipping 概念**：避免新舊策略差異過大，減少訓練崩壞。
- **適用任務**：連續控制、遊戲、機器人、複雜決策、RLHF。
- **主要挑戰**：樣本效率低、訓練不穩、獎勵設計困難、探索成本高。
- **RLHF 關聯**：人類偏好可轉成獎勵模型，再用 PPO 類方法調整語言模型行為。

## 3. 名詞解釋

- **Policy（策略）**：代理人在狀態下選擇行動的規則或機率分布。
- **Policy Gradient**：用梯度方法直接最佳化策略參數的強化學習方法。
- **PPO**：Proximal Policy Optimization，限制策略更新幅度的強化學習演算法。
- **Reward（獎勵）**：環境對行動結果給出的回饋訊號。
- **Exploration / Exploitation**：探索新行動與利用已知好行動之間的取捨。
- **RLHF**：Reinforcement Learning from Human Feedback，用人類偏好訓練或調整模型。

## 4. 常見陷阱

**陷阱1：把 Policy Gradient 當成 Q-learning**
> ❌ 誤解：Policy Gradient 一定先學 Q 值再選最大值。  
> ✅ 正確：Policy Gradient 是直接最佳化策略機率。

**陷阱2：以為 PPO 是完全不同於強化學習的模型**
> ❌ 誤解：PPO 是一種神經網路架構。  
> ✅ 正確：PPO 是強化學習演算法，用於穩定更新策略。

**陷阱3：忽略獎勵設計問題**
> ❌ 誤解：只要套 PPO 就能學到正確行為。  
> ✅ 正確：獎勵設計不良會導致模型學到錯誤或投機行為。

**陷阱4：以為更新越大學越快越好**
> ❌ 誤解：策略每次大幅更新能更快收斂。  
> ✅ 正確：更新太大可能使訓練崩壞，PPO 正是用來限制更新幅度。

## 5. 考題怎麼問

**問法1：問直接最佳化策略的方法**  
→ 答 Policy Gradient。

**問法2：問 PPO 的核心目的**  
→ 答限制策略更新幅度、提升訓練穩定性。

**問法3：問 RLHF 常見強化學習演算法**  
→ 答 PPO 類方法。

**問法4：問強化學習困難點**  
→ 答獎勵設計、探索成本、樣本效率、訓練穩定性。

## 6. 記憶口訣

- **「Policy 直接學怎麼做」**：Policy Gradient 不先繞去估 Q 值。
- **「PPO 不讓策略跑太遠」**：限制更新幅度是核心。
- **「獎勵設錯，學得越好越糟」**：RL 成敗常在 reward design。

## 7. 官方指引對應線索

此主題屬於科目三強化學習、策略最佳化與大型模型對齊相關範圍。考試常從 policy-based vs value-based、PPO 穩定更新、探索與利用、獎勵設計及 RLHF 應用命題。'''
}

for seg in guide['segments']:
    if seg.get('id') in contents:
        seg['content'] = contents[seg['id']]

comp = set(state['s3'].get('completed', []))
fail = set(state['s3'].get('failed', []))
for i in (80, 81, 82):
    comp.add(i)
    fail.discard(i)
state['s3']['completed'] = sorted(comp)
state['s3']['failed'] = sorted(fail)
ft = {str(k): v for k, v in state['s3'].get('failedTitles', {}).items()}
for i in (80, 81, 82):
    ft.pop(str(i), None)
state['s3']['failedTitles'] = ft
state['lastUpdated'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')

guide_path.write_text(json.dumps(guide, ensure_ascii=False, indent=2))
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
print('updated S3 ids 80,81,82 directly by Hermes; no Claude Code subprocess used')
