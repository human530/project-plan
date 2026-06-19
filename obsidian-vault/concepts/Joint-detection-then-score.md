---
tags: [concept]
---
# Joint detection then score

「偵測後評分」路線：先用偵測器（YOLO/DeepLabCut/SSD）定位各標的關節，再逐關節分類/評分後加總。比整圖回歸更適合小樣本——可定位、可解釋、貼近 SvH 定義，並可用單關節裁切擴量。代表：[[Miyama2022_Contextual]]、[[Hirano2019_PerJoint]]、[[Izumi2024_SSD]]。
