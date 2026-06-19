---
title: "多階段深度學習（UNet+YOLOv7+ViT）預測 Overall Sharp Score"
authors: "Moradmand H, Ren L"
year: 2025
journal: "Scientific Reports"
doi: "10.1038/s41598-025-86073-0"
pmid: "39870749"
cluster: imaging-scoring
study_design: "多階段管線"
sample: "訓練 679 / 外部 291"
external_validation: "有（外部 291 例）"
authority: B
tags: [paper, imaging-scoring, authority/B, vision-transformer, regression, SvH]
source: PubMed
---
# 多階段深度學習（UNet+YOLOv7+ViT）預測 Overall Sharp Score

> **🥈 B 高品質（外部驗證/頂級期刊）**　|　群組：自動影像評分
> According to PubMed — [DOI](https://doi.org/10.1038/s41598-025-86073-0)

| 欄位 | 內容 |
|------|------|
| 作者 / 年份 | Moradmand H, Ren L（2025） |
| 期刊 | Scientific Reports |
| 研究設計 | 多階段管線 |
| 樣本 | 訓練 679 / 外部 291 |
| 外部驗證 | 有（外部 291 例） |
| 主要結果 | 關節偵測 99%；OSS：RMSE 9.73、MAE 5.35、ICC 0.702（Sharp<50 最佳） |

## 對本專題的啟示
PubMed 首篇用 ViT 做 OSS 回歸。高分區誤差大、ICC 中等——說明整圖回歸對小樣本不利。

## 相關概念
[[Sharp-van-der-Heijde-score]]、[[Joint-detection-then-score]]、[[ICC-and-Bland-Altman]]

## 我的筆記
-

---
*來源 According to PubMed。引用請附 [DOI](https://doi.org/10.1038/s41598-025-86073-0)。標「需進一步確認」者為原始分析未明載，未予編造。*
