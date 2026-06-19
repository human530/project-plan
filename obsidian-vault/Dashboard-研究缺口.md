# 🧭 Dashboard：研究缺口與本專題定位

> 整合自 docs/07。According to PubMed。

## 三大研究缺口
1. **多數研究缺外部驗證** → 本專題安排跨來源小批外部測試並誠實報告掉分。
   - 正面範例：[[Venalainen2025_AuRA]]、[[Schlereth2024_RAMRIS]]、[[Bouget2022_TNFi]]
2. **Grad-CAM 多為事後佐證、未量化** → 本專題已實作關節區能量量化 + 隨機基準對照。
   - 參考：[[Schmidt2025_GradCAM]]、[[Bayesian2026_Uncertainty]]、[[Grad-CAM]]
3. **影像+臨床+實驗室+組學「四域融合」空白** → 以最小可行多模態示範切入。
   - 參考：[[WangZ2025_Metabolite]]、[[HeS2025_Proteomics]]、[[Multimodal-fusion]]

## 反面證據（避免盲目堆模態）
- [[Sysojev2025_Genotype]]：大樣本下全基因型對 MTX 反應增益可忽略。
- 原則：新增模態須帶來與目標正交的資訊，並以單模態 baseline + 顯著性檢定證明增益。

## 最該遵循的方法學規範
- [[Collins2024_TRIPOD_AI]]（評分=預測模型，最對口）
- [[Bhandari2023_CLAIM]]（CLAIM 42 項自評，目標 >20/42）
- [[Vasey2022_DECIDE_AI]]（準確 ≠ 臨床有用）
- [[Liu2020_CONSORT_AI]]（錯誤案例分析條目）
