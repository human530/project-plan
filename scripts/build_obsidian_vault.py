"""把已整理的 PubMed 文獻轉成 Obsidian 醫療文獻知識庫（vault）。

產出：obsidian-vault/ 下的逐篇文獻筆記（含 YAML frontmatter + 雙向連結 + 標籤）、
概念筆記（MOC）、Dataview 儀表板、文獻筆記模板。

資料來源：本 repo docs/lit/A、B、C 三份 PubMed 文獻分析（According to PubMed）。
凡原始分析標「需進一步確認」者，此處於對應欄位沿用該標註，不臆造。
執行：python scripts/build_obsidian_vault.py
"""
from __future__ import annotations

import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "obsidian-vault")

# 權威分級：A=領域基準/最高權威, B=高品質(外部驗證/頂級期刊), C=一般實證/小樣本, R=回顧/觀點/規範
PAPERS = [
    # ---------- 群 A：自動影像損傷評分 ----------
    dict(key="Sun2022_RA2DREAM", title="RA2-DREAM Challenge：群眾外包自動量化 RA 手足 X 光損傷",
         authors="Sun D, 等", year=2022, journal="JAMA Network Open",
         doi="10.1001/jamanetworkopen.2022.27423", pmid="36036935",
         cluster="imaging-scoring", design="國際競賽 + 獨立驗證", sample="674 影像組 / 562 病人",
         ext_val="有（post-challenge 獨立驗證 concordance 0.71/0.78/0.82）",
         results="加權 RMSE：整體 0.44、JSN 0.38、erosion 0.43（不同團隊奪冠）",
         authority="A", tags=["imaging-scoring", "benchmark", "SvH", "dataset"],
         concepts=["RA2-DREAM-Challenge", "Sharp-van-der-Heijde-score"],
         note="本領域唯一公開基準，也是本專題主資料集（Synapse syn20545111）來源。後續方法的共同參照系。"),
    dict(key="Venalainen2025_AuRA", title="AuRA：自動 RA X 光評分的外部與縱向驗證",
         authors="Venäläinen MS, 等", year=2025, journal="Rheumatology (Oxford)",
         doi="10.1093/rheumatology/keae215", pmid="38597875",
         cluster="imaging-scoring", design="外部驗證 + 縱向", sample="訓練 367 / 外部 205 / 縱向 54",
         ext_val="有（真正外部 Turku 醫院 + 縱向，最稀缺）",
         results="外部 RMSE 23.6（勝 DREAM 頂尖 35.0/35.6）；縱向變化 Pearson R=0.74",
         authority="A", tags=["imaging-scoring", "external-validation", "SvH", "longitudinal"],
         concepts=["RA2-DREAM-Challenge", "Sharp-van-der-Heijde-score", "External-validation"],
         note="全領域唯一完成真正外部 + 縱向驗證者。Docker 公開可重現。回應領域最大弱點。"),
    dict(key="Moradmand2025_ViT", title="多階段深度學習（UNet+YOLOv7+ViT）預測 Overall Sharp Score",
         authors="Moradmand H, Ren L", year=2025, journal="Scientific Reports",
         doi="10.1038/s41598-025-86073-0", pmid="39870749",
         cluster="imaging-scoring", design="多階段管線", sample="訓練 679 / 外部 291",
         ext_val="有（外部 291 例）",
         results="關節偵測 99%；OSS：RMSE 9.73、MAE 5.35、ICC 0.702（Sharp<50 最佳）",
         authority="B", tags=["imaging-scoring", "vision-transformer", "regression", "SvH"],
         concepts=["Sharp-van-der-Heijde-score", "Joint-detection-then-score", "ICC-and-Bland-Altman"],
         note="PubMed 首篇用 ViT 做 OSS 回歸。高分區誤差大、ICC 中等——說明整圖回歸對小樣本不利。"),
    dict(key="Miyama2022_Contextual", title="DeepLabCut 偵測 + 對側關節脈絡分類（勝過骨科醫師）",
         authors="Miyama K, 等", year=2022, journal="Arthritis Research & Therapy",
         doi="10.1186/s13075-022-02914-7", pmid="36192761",
         cluster="imaging-scoring", design="偵測 + 分類（單中心 CV）", sample="226 影像 / 40 病人",
         ext_val="無",
         results="偵測率 98.0%/97.3%；對側比較 F=0.70/0.81；erosion 勝骨科醫師",
         authority="B", tags=["imaging-scoring", "joint-detection", "contralateral", "erosion"],
         concepts=["Joint-detection-then-score"],
         note="設計亮點：左右手對側同名關節比較，在小樣本即勝過醫師。本專題可抄此差異化亮點。"),
    dict(key="Hirano2019_PerJoint", title="兩步法：關節偵測 + CNN 逐關節序數評分",
         authors="Hirano T, 等", year=2019, journal="Rheumatology Advances in Practice",
         doi="10.1093/rap/rkz047", pmid="31872173",
         cluster="imaging-scoring", design="偵測 + 逐關節評分", sample="216 影像 / 108 病人（擴增至 11,160 關節）",
         ext_val="無",
         results="偵測敏感度 95.3%；相關係數 JSN 0.72–0.88、erosion 0.54–0.75",
         authority="C", tags=["imaging-scoring", "per-joint", "ordinal", "data-augmentation"],
         concepts=["Joint-detection-then-score", "Sharp-van-der-Heijde-score"],
         note="關鍵技巧：單關節裁切把 186 張擴增成 11,160 關節影像——小樣本擴量法，直接可抄。"),
    dict(key="Izumi2024_SSD", title="SSD ensemble 偵測 ankylosis/subluxation（mTSS 特殊發現）",
         authors="Izumi K, 等", year=2024, journal="Scientific Reports",
         doi="10.1038/s41598-024-58242-0", pmid="38565576",
         cluster="imaging-scoring", design="偵測 ensemble（單中心 5-fold）", sample="260 手部 X 光",
         ext_val="無", results="MP/PIP 偵測率 >99.8%；ensemble 各指標優於個別模型",
         authority="C", tags=["imaging-scoring", "detection", "ensemble"],
         concepts=["Joint-detection-then-score"],
         note="僅偵測特殊發現、尚未組完整分數；作者自述為「邁向自動評分的一步」。階段性目標範例。"),
    dict(key="Izumi2023_Backbones", title="多 backbone 比較腕關節 subluxation/ankylosis 分類",
         authors="Izumi K, 等", year=2023, journal="PLoS One",
         doi="10.1371/journal.pone.0281088", pmid="36780446",
         cluster="imaging-scoring", design="分類（單中心 5-fold）", sample="216 手部 X 光",
         ext_val="無", results="腕關節 accuracy 0.97/0.89、AUC 0.92/0.85；正樣本極少",
         authority="C", tags=["imaging-scoring", "classification", "class-imbalance"],
         concepts=["Joint-detection-then-score"],
         note="正樣本極少→必用 PR 曲線而非 accuracy。類別不平衡的警示案例。"),
    dict(key="Wang2023_Registration", title="深度配準量化 JSN 進展（次像素精度）",
         authors="Wang H, 等", year=2023, journal="Computerized Medical Imaging and Graphics",
         doi="10.1016/j.compmedimag.2023.102273", pmid="37531811",
         cluster="imaging-scoring", design="影像配準（同院資料）", sample="手指關節影像對",
         ext_val="無", results="配準 MSE 0.0031、mismatch 0.48%；次像素精度，程式碼開源",
         authority="C", tags=["imaging-scoring", "registration", "progression"],
         concepts=["Joint-detection-then-score"],
         note="路線獨特：量化前後追蹤的 JSN「變化」而非絕對分數。需配對追蹤影像。進階 demo 參考。"),
    dict(key="Ureten2022_Classify", title="YOLOv4 + VGG-16 遷移學習：RA/OA/normal 影像分類",
         authors="Üreten K, Maraş HH", year=2022, journal="Journal of Digital Imaging",
         doi="10.1007/s10278-021-00564-w", pmid="35018539",
         cluster="imaging-scoring", design="偵測 + 遷移學習分類", sample="需進一步確認",
         ext_val="無", results="RA vs normal acc 90.7% AUC 0.97；非 SvH 評分",
         authority="C", tags=["imaging-scoring", "transfer-learning", "classification"],
         concepts=["Transfer-learning"],
         note="僅做疾病分類、不產生損傷分數。作為「偵測 + 遷移學習」技術背景對照。"),
    dict(key="Bird2022_Viewpoint", title="AI 與 RA 放射評分的未來（觀點）",
         authors="Bird A, Oakden-Rayner L, 等", year=2022, journal="Arthritis Research & Therapy",
         doi="10.1186/s13075-022-02972-x", pmid="36510330",
         cluster="imaging-scoring", design="觀點 / Viewpoint", sample="無新資料",
         ext_val="不適用", results="主張 AI 應提升對輕症的敏感度，而非僅複製人工分數",
         authority="R", tags=["imaging-scoring", "viewpoint", "perspective"],
         concepts=["Sharp-van-der-Heijde-score"],
         note="知名醫學 AI 團隊（Adelaide AIML）論述。可作引言的方法學立場。"),

    # ---------- 群 B：多模態臨床決策 ----------
    dict(key="WangZ2025_Metabolite", title="血漿代謝體 + 臨床 ML 預測骨破壞（CjBM）",
         authors="Wang Z, 等", year=2025, journal="Arthritis Research & Therapy",
         doi="10.1186/s13075-025-03576-x", pmid="40399914",
         cluster="multimodal-cds", design="多模態 ML（單中心）", sample="60 RA",
         ext_val="無（與既往模型比較）", results="CjBM AUC 0.800；加入代謝體顯著改善（P=0.035）",
         authority="C", tags=["multimodal", "metabolomics", "radiographic-progression", "SHAP"],
         concepts=["Multimodal-fusion", "Sharp-van-der-Heijde-score"],
         note="種子文獻。示範「在臨床模型上加一個模態並用 P 值證明增益」——本專題多模態核心論證。"),
    dict(key="Gan2025_Differential", title="隨機森林 + SHAP 鑑別 RA-SS vs SS-PA",
         authors="Gan M, 等", year=2025, journal="Frontiers in Immunology",
         doi="10.3389/fimmu.2025.1614631", pmid="40698089",
         cluster="multimodal-cds", design="LASSO + RF（單中心 7:3）", sample="106 + 135",
         ext_val="無", results="RF AUC 0.854；關鍵特徵 anti-CCP/RF/侵蝕關節數/anti-SSA/CRP",
         authority="C", tags=["multimodal", "differential-diagnosis", "SHAP", "labs"],
         concepts=["Multimodal-fusion", "Explainability-SHAP"],
         note="種子文獻。臨床 + 實驗室 + 放射學特徵融合 + SHAP，工具門檻低（可借鏡 late fusion）。"),
    dict(key="Zhou2022_RATING", title="RATING：多模態超音波深度學習自動評 RA 活動度",
         authors="Zhou Z, 等", year=2022, journal="Patterns (Cell Press)",
         doi="10.1016/j.patter.2022.100592", pmid=None,
         cluster="multimodal-cds", design="DL + 讀者研究（前瞻+外部）", sample="1244 影像",
         ext_val="有（外部測試 + 讀者研究）",
         results="外部 85.0%；讀者研究使醫師 41.4%→64.0%",
         authority="A", tags=["multimodal", "ultrasound", "human-AI", "self-supervised"],
         concepts=["Multimodal-fusion", "Explainability-SHAP"],
         note="多模態方向最權威。證明「決策輔助」真實臨床增益，而非僅離線 AUC。"),
    dict(key="HeX2024_USActivity", title="多模態超音波深度學習評 RA 活動度（動態優於靜態）",
         authors="He X, 等", year=2024, journal="Rheumatology (Oxford)",
         doi="10.1093/rheumatology/kead366", pmid=None,
         cluster="multimodal-cds", design="DL（ResNet，兩測試佇列）", sample="1244 影像",
         ext_val="有（兩測試佇列）", results="AUC 0.74–0.95；動態 PD 優於多數資深醫師",
         authority="B", tags=["multimodal", "ultrasound", "doppler"],
         concepts=["Multimodal-fusion"],
         note="影像端到端高精度量化的代表。仍屬影像單模態、未融合臨床。"),
    dict(key="HeS2025_Proteomics", title="血漿蛋白質體 + 臨床預測 RA 治療反應",
         authors="He S, 等", year=2025, journal="Nature Communications",
         doi="10.1038/s41467-025-62032-1", pmid=None,
         cluster="multimodal-cds", design="ML 縱貫佇列 + 獨立驗證", sample="278 RA + 60 高風險 + 99 HC",
         ext_val="有（獨立佇列 ELISA）", results="治療反應 AUROC 0.88/0.82",
         authority="A", tags=["multimodal", "proteomics", "treatment-response", "external-validation"],
         concepts=["Multimodal-fusion", "External-validation"],
         note="組學方向最權威：高表現 + 外部驗證 + 清楚臨床轉化路徑。"),
    dict(key="Yoosuf2022_Multiomics", title="多組學預測 anti-TNF 反應",
         authors="Yoosuf N, 等", year=2022, journal="Rheumatology (Oxford)",
         doi="10.1093/rheumatology/keab521", pmid=None,
         cluster="multimodal-cds", design="ML 多組學", sample="39 女性 RA",
         ext_val="部分（基因表現獨立佇列重現）", results="高預測效用（AUC 需進一步確認）；EPPK1/CHI3L1 標記",
         authority="C", tags=["multimodal", "multi-omics", "treatment-response"],
         concepts=["Multimodal-fusion"],
         note="樣本極小（n=39）、單性別，易過擬合。組學融合的探索性案例。"),
    dict(key="Salehi2024_bDMARD", title="基線臨床 ML 預測 bDMARD 反應（巢式 CV）",
         authors="Salehi F, 等", year=2024, journal="Journal of Clinical Medicine",
         doi="10.3390/jcm13133890", pmid=None,
         cluster="multimodal-cds", design="XGBoost/AdaBoost（巢式 CV）", sample="154 RA",
         ext_val="無（巢式 CV）", results="初始反應 AUROC 0.91；DAS28-ESR 為關鍵（SHAP）",
         authority="C", tags=["clinical", "treatment-response", "nested-CV", "SHAP"],
         concepts=["Explainability-SHAP", "External-validation"],
         note="示範巢式交叉驗證防過擬合 + SHAP。小樣本嚴謹流程範例。"),
    dict(key="Bouget2022_TNFi", title="臨床 + 血液 ML 預測 TNFi 反應（含外部驗證）",
         authors="Bouget V, 等", year=2022, journal="RMD Open",
         doi="10.1136/rmdopen-2022-002442", pmid=None,
         cluster="multimodal-cds", design="多種 ML（獨立外部佇列）", sample="161 + 118",
         ext_val="有（ABIRISK 外部）", results="CatBoost 訓練 AUROC 0.72；外部 0.70/0.71",
         authority="B", tags=["clinical", "treatment-response", "external-validation"],
         concepts=["External-validation"],
         note="外部驗證後 AUC 微降——示範「內部 vs 外部」誠實落差。"),
    dict(key="Myasoedova2022_MTX", title="臨床 + 基因體（160 SNP）預測 MTX 反應",
         authors="Myasoedova E, 等", year=2022, journal="Arthritis Care & Research",
         doi="10.1002/acr.24834", pmid=None,
         cluster="multimodal-cds", design="監督式 ML（獨立驗證）", sample="643",
         ext_val="有（獨立驗證佇列）", results="訓練 AUC 0.84；SNP 增益相對有限",
         authority="B", tags=["multimodal", "genomics", "treatment-response"],
         concepts=["Multimodal-fusion"],
         note="基因增益有限。多模態「不必然加越多越好」的證據之一。"),
    dict(key="Sysojev2025_Genotype", title="全基因型對 MTX 結局預測增益可忽略（反面證據）",
         authors="Sysojev AÖ, 等", year=2025, journal="Journal of Internal Medicine",
         doi="10.1111/joim.20087", pmid=None,
         cluster="multimodal-cds", design="多種 ML（大型登錄）", sample="2432 早期 RA",
         ext_val="內部評估", results="AUC ~0.62；基因貢獻可忽略",
         authority="B", tags=["multimodal", "genomics", "negative-result"],
         concepts=["Multimodal-fusion"],
         note="關鍵反面證據：大樣本下常見基因變異對 MTX 反應幾無增益。避免盲目堆模態。"),
    dict(key="Kalweit2021_AdaptiveNet", title="自適應 RNN 預測下次就診 DAS28 活動度",
         authors="Kalweit M, 等", year=2021, journal="PLoS One",
         doi="10.1371/journal.pone.0252289", pmid=None,
         cluster="multimodal-cds", design="RNN（大型多中心登錄）", sample=">9500 病人 / 65000 visits",
         ext_val="大型多中心（SCQM）", results="準確率 75.6%；回歸 MSE 0.9；勝傳統 ML",
         authority="B", tags=["clinical", "longitudinal", "disease-activity"],
         concepts=["Multimodal-fusion"],
         note="縱貫多模態的大樣本範例（臨床 + 病人報告 + 實驗室 + 用藥）。"),
    dict(key="Baloun2025_D2T", title="臨床 + 病人報告預測難治型 D2T RA",
         authors="Baloun J, 等", year=2025, journal="Scientific Reports",
         doi="10.1038/s41598-025-18298-y", pmid=None,
         cluster="multimodal-cds", design="多種 ML（大型登錄）", sample="8543 RA",
         ext_val="內部驗證", results="AUC 0.656–0.832；SHAP（疾病活動度/HAQ/療程）",
         authority="C", tags=["clinical", "difficult-to-treat", "SHAP"],
         concepts=["Explainability-SHAP"],
         note="純臨床、AUC 範圍寬。SHAP 可解釋輸出範例。"),
    dict(key="MoralesIvorra2024_Thermo", title="手部熱像 + CRP 評估 RA 發炎（前瞻外部驗證）",
         authors="Morales-Ivorra I, 等", year=2024, journal="Diagnostics",
         doi="10.3390/diagnostics14131394", pmid=None,
         cluster="multimodal-cds", design="ML 熱像（前瞻多中心）", sample="77 RA",
         ext_val="有（前瞻 3 院）", results="ThermoDAI 與 CDAI/DAS28 相關 ρ≈0.78–0.83",
         authority="C", tags=["multimodal", "thermography", "low-cost", "external-validation"],
         concepts=["Multimodal-fusion"],
         note="低成本新興影像 + CRP 的簡易多模態。前瞻驗證精神值得學習。"),
    dict(key="Labinsky2023_CDSS", title="AI flare 預測 + 臨床決策支援系統（CDSS）試點",
         authors="Labinsky H, 等", year=2023, journal="Diagnostics",
         doi="10.3390/diagnostics13010148", pmid=None,
         cluster="multimodal-cds", design="CDSS 可用性試點", sample="10 病例 / 5 醫師",
         ext_val="試點", results="復發預測敏感 72%/特異 76%/AUROC 0.80；提升醫師信心",
         authority="C", tags=["CDSS", "flare", "human-AI", "usability"],
         concepts=["Multimodal-fusion"],
         note="CDSS 精神範例：AI 輸出如何嵌入醫師決策流程。"),
    dict(key="Shi2024_Review", title="精準風濕病 ML 綜述（趨勢與瓶頸）",
         authors="Shi Y, 等", year=2024, journal="Frontiers in Immunology",
         doi="10.3389/fimmu.2024.1409555", pmid=None,
         cluster="multimodal-cds", design="綜述", sample="不適用",
         ext_val="不適用", results="多模態 + 深度學習為趨勢；過擬合/泛化/可解釋性為瓶頸",
         authority="R", tags=["review", "multimodal", "precision-medicine"],
         concepts=["Multimodal-fusion"],
         note="綜述旁證：明確警告小樣本 + 缺多元族群會高估表現。"),
    dict(key="Bilgin2025_Review", title="AI 於 RA/axSpA/PsA 管理綜述",
         authors="Bilgin E, 等", year=2025, journal="Therapeutic Advances in Musculoskeletal Disease",
         doi="10.1177/1759720X251343579", pmid=None,
         cluster="multimodal-cds", design="綜述", sample="不適用",
         ext_val="不適用", results="強調多模態 AI 為未來方向",
         authority="R", tags=["review", "multimodal"],
         concepts=["Multimodal-fusion"],
         note="綜述旁證：多模態 AI 的領域共識。"),
    dict(key="Forrest2026_SHIMMER", title="SHIMMER：常規檢驗 + EHR 跨七病 spectral 模型",
         authors="Forrest IS, 等", year=2026, journal="Med",
         doi="10.1016/j.medj.2026.101150", pmid=None,
         cluster="multimodal-cds", design="ML（跨病）", sample="需進一步確認",
         ext_val="需進一步確認", results="以常規檢驗 + EHR 示範可攜式臨床決策（含 RA）",
         authority="R", tags=["review", "EHR", "CDSS"],
         concepts=["Multimodal-fusion"],
         note="旁證：低成本常規資料也能做臨床決策示範。"),

    # ---------- 群 C：可解釋性、其他模態、方法學規範 ----------
    dict(key="Schlereth2024_RAMRIS", title="CNN 自動評手部 MRI（RAMRIS：erosion/osteitis/synovitis）",
         authors="Schlereth M, 等", year=2024, journal="RMD Open",
         doi="10.1136/rmdopen-2024-004273", pmid="38886001",
         cluster="methodology", design="CNN（含獨立外部驗證）", sample="內部 211 + 外部 220 MRI",
         ext_val="有（獨立外部世代）", results="macro-AUC 92%/91%/85%；與人工 Spearman 90%/78%/69%",
         authority="B", tags=["MRI", "RAMRIS", "external-validation"],
         concepts=["External-validation", "ICC-and-Bland-Altman"],
         note="模態對照組。示範「外部驗證 + 與人工相關係數」的嚴謹評估，科展應仿效。"),
    dict(key="Fiorentino2021_USCartilage", title="CNN 自動量測超音波軟骨厚度",
         authors="Fiorentino MC, 等", year=2021, journal="Computers in Biology and Medicine",
         doi="10.1016/j.compbiomed.2021.105117", pmid="34968861",
         cluster="methodology", design="CNN 回歸", sample="38 受試者",
         ext_val="無", results="平均絕對差 0.032 mm ≈ 觀察者內變異 0.036 mm",
         authority="C", tags=["ultrasound", "observer-variability"],
         concepts=["ICC-and-Bland-Altman"],
         note="設計亮點：把自動量測誤差與「觀察者內變異」對照——人類一致性上限的比較法。"),
    dict(key="Ostergaard2025_Review", title="RA 臨床試驗影像回顧（2025）",
         authors="Østergaard M, 等", year=2025, journal="Skeletal Radiology",
         doi="10.1007/s00256-025-05004-2", pmid="40762694",
         cluster="methodology", design="敘事回顧", sample="不適用",
         ext_val="不適用", results="US/MRI 為 truthful/reproducible/sensitive；AI 為未來方向",
         authority="A", tags=["review", "imaging", "MRI", "ultrasound"],
         concepts=["External-validation"],
         note="影像模態最權威回顧（Østergaard 為 RAMRIS 創建者）。界定各模態證據位階。"),
    dict(key="Roemer2024_Perspective", title="半定量 MRI 評分演進與 AI 的審慎立場",
         authors="Roemer FW, 等", year=2024, journal="Osteoarthritis and Cartilage",
         doi="10.1016/j.joca.2024.01.001", pmid=None,
         cluster="methodology", design="Perspective", sample="不適用",
         ext_val="不適用", results="評分系統需效度/信度/反應性；AI 仍須驗證與法規核可",
         authority="R", tags=["review", "MRI", "regulation"],
         concepts=["External-validation"],
         note="提供「評分系統效度三要件」框架。對 AI 臨床使用持審慎態度。"),
    dict(key="Schmidt2025_GradCAM", title="YOLOv8 偵測主動脈剝離（Grad-CAM 定性佐證）",
         authors="Schmidt（需進一步確認）, 等", year=2025, journal="Eur J Vasc Endovasc Surg",
         doi="10.1016/j.ejvs.2025.08.054", pmid=None,
         cluster="methodology", design="DL（多中心外部驗證）", sample="1138 CT",
         ext_val="有（外部 AUC 0.970）", results="Grad-CAM 顯示聚焦解剖相關區域（定性，非定量比對）",
         authority="B", tags=["explainability", "grad-cam", "external-validation"],
         concepts=["Grad-CAM"],
         note="正面範例：外部驗證 + Grad-CAM 並陳；但 Grad-CAM 僅定性佐證。"),
    dict(key="Bayesian2026_Uncertainty", title="Bayesian CNN：不確定性與 saliency 連動揭露偽特徵",
         authors="需進一步確認, 等", year=2026, journal="Computers in Biology and Medicine",
         doi="10.1016/j.compbiomed.2025.111419", pmid=None,
         cluster="methodology", design="CNN + MC dropout", sample="ALL-IDB2（10-fold）",
         ext_val="無", results="高不確定性案例其 saliency 呈分散/非聚焦注意力",
         authority="C", tags=["explainability", "uncertainty", "saliency"],
         concepts=["Grad-CAM"],
         note="關鍵啟示：不確定性 + saliency 連看可揭露「看錯地方」。支持加做不確定性分析。"),
    dict(key="Patient2025_Attitudes", title="病患對可解釋 AI 的偏好（43 國 13806 人）",
         authors="需進一步確認, 等", year=2025, journal="JAMA Network Open",
         doi="10.1001/jamanetworkopen.2025.14452", pmid=None,
         cluster="methodology", design="跨國問卷", sample="13806 病患",
         ext_val="不適用", results="70.2% 寧換略低準確度也要可解釋 AI；72.9% 偏好醫師主導",
         authority="B", tags=["explainability", "patient-preference", "ethics"],
         concepts=["Grad-CAM"],
         note="動機/社會意義論述：為何要做可解釋的 RA 評分 AI。"),
    dict(key="PedRheum2025_Review", title="兒童風濕 AI 回顧（強調 XAI 與人類監督）",
         authors="需進一步確認, 等", year=2025, journal="Current Opinion in Rheumatology",
         doi="10.1097/BOR.0000000000001087", pmid=None,
         cluster="methodology", design="敘事回顧", sample="不適用",
         ext_val="不適用", results="反覆強調需 explainable AI + 人類監督",
         authority="R", tags=["review", "explainability"],
         concepts=["Grad-CAM"],
         note="領域對 XAI 與人為監督的共識陳述。"),
    dict(key="Liu2020_CONSORT_AI", title="CONSORT-AI：AI 臨床試驗報告規範",
         authors="Liu X, 等", year=2020, journal="Lancet Digital Health",
         doi="10.1016/S2589-7500(20)30218-1", pmid=None,
         cluster="methodology", design="Delphi 共識", sample="168 利害關係人",
         ext_val="不適用", results="CONSORT 上新增 14 項 AI 條目（含人–AI 互動、錯誤案例分析）",
         authority="A", tags=["guideline", "reporting", "CONSORT-AI"],
         concepts=["Reporting-guidelines"],
         note="規範類最高權威之一。科展可借「錯誤案例分析」條目。"),
    dict(key="Vasey2022_DECIDE_AI", title="DECIDE-AI：AI 早期臨床評估規範",
         authors="Vasey B, 等", year=2022, journal="Nature Medicine",
         doi="10.1038/s41591-022-01772-9", pmid=None,
         cluster="methodology", design="Delphi 共識", sample="123/138 人",
         ext_val="不適用", results="27 項條目；強調準確度高 ≠ 臨床有用、human factors",
         authority="A", tags=["guideline", "reporting", "DECIDE-AI"],
         concepts=["Reporting-guidelines"],
         note="點明「研究級準確度尚非臨床有用」的界線。討論章引用。"),
    dict(key="Collins2024_TRIPOD_AI", title="TRIPOD+AI：臨床預測模型報告規範",
         authors="Collins GS, 等", year=2024, journal="BMJ",
         doi="10.1136/bmj.q824", pmid=None,
         cluster="methodology", design="報告指引", sample="不適用",
         ext_val="不適用", results="涵蓋迴歸與 ML 的臨床預測模型報告 checklist",
         authority="A", tags=["guideline", "reporting", "TRIPOD-AI"],
         concepts=["Reporting-guidelines"],
         note="本專題最對口的規範（評分=預測模型）。方法章應逐項對照。"),
    dict(key="Collins2021_PROBAST_AI", title="TRIPOD-AI / PROBAST-AI 協議",
         authors="Collins GS, 等", year=2021, journal="BMJ Open",
         doi="10.1136/bmjopen-2020-048008", pmid=None,
         cluster="methodology", design="方法協議", sample="不適用",
         ext_val="不適用", results="建立 AI 預測模型報告指引 + 偏誤風險工具",
         authority="R", tags=["guideline", "PROBAST-AI", "risk-of-bias"],
         concepts=["Reporting-guidelines"],
         note="PROBAST-AI 可作偏誤風險自評表，放科展附錄。"),
    dict(key="Bhandari2023_CLAIM", title="以 CLAIM 評 glioma MRI AI 文獻品質",
         authors="Bhandari A, 等", year=2023, journal="Neuroradiology",
         doi="10.1007/s00234-023-03126-9", pmid=None,
         cluster="methodology", design="文獻品質評估", sample="138 篇",
         ext_val="不適用", results="平均僅 20/42；弱點集中於資料/ground truth/效能驗證",
         authority="B", tags=["guideline", "CLAIM", "quality"],
         concepts=["Reporting-guidelines"],
         note="示範用 CLAIM 量化報告品質。科展自評 CLAIM 分數展現嚴謹（目標 >20/42）。"),
]

AUTHORITY_LABEL = {
    "A": "🏆 A 最高權威 / 基準",
    "B": "🥈 B 高品質（外部驗證/頂級期刊）",
    "C": "🥉 C 一般實證 / 小樣本",
    "R": "📋 R 回顧 / 觀點 / 規範",
}
CLUSTER_LABEL = {
    "imaging-scoring": "自動影像評分",
    "multimodal-cds": "多模態臨床決策",
    "methodology": "可解釋性與方法學",
}


def w(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def yaml_list(items):
    return "[" + ", ".join(items) + "]"


def paper_note(p):
    raw_tags = ["paper", p["cluster"], f"authority/{p['authority']}"] + p["tags"]
    tags = list(dict.fromkeys(raw_tags))  # 去重並保留順序
    concepts = p.get("concepts", [])
    fm = f"""---
title: "{p['title']}"
authors: "{p['authors']}"
year: {p['year']}
journal: "{p['journal']}"
doi: "{p['doi']}"
pmid: "{p['pmid'] or ''}"
cluster: {p['cluster']}
study_design: "{p['design']}"
sample: "{p['sample']}"
external_validation: "{p['ext_val']}"
authority: {p['authority']}
tags: {yaml_list(tags)}
source: PubMed
---
"""
    concept_links = "、".join(f"[[{c}]]" for c in concepts) if concepts else "—"
    body = f"""# {p['title']}

> **{AUTHORITY_LABEL[p['authority']]}**　|　群組：{CLUSTER_LABEL[p['cluster']]}
> According to PubMed — [DOI](https://doi.org/{p['doi']})

| 欄位 | 內容 |
|------|------|
| 作者 / 年份 | {p['authors']}（{p['year']}） |
| 期刊 | {p['journal']} |
| 研究設計 | {p['design']} |
| 樣本 | {p['sample']} |
| 外部驗證 | {p['ext_val']} |
| 主要結果 | {p['results']} |

## 對本專題的啟示
{p['note']}

## 相關概念
{concept_links}

## 我的筆記
-

---
*來源 According to PubMed。引用請附 [DOI](https://doi.org/{p['doi']})。標「需進一步確認」者為原始分析未明載，未予編造。*
"""
    w(f"literature/{p['key']}.md", fm + body)


def build_moc():
    lines = ["---", "tags: [MOC, dashboard]", "---",
             "# 📚 文獻總覽 MOC（Map of Content）", "",
             "> RA Xray AI 專題的 PubMed 文獻知識庫。所有資料 According to PubMed，每篇附 DOI。",
             "> 共 %d 篇。建議安裝 Obsidian **Dataview** 外掛以啟用下方動態表格。" % len(PAPERS), "",
             "## 🔎 Dataview：依權威排序（需 Dataview 外掛）", "",
             "```dataview", "TABLE authority AS 權威, year AS 年, journal AS 期刊, cluster AS 群組",
             'FROM "literature"', "SORT authority ASC, year DESC", "```", "",
             "## 🔎 Dataview：只看有外部驗證的", "",
             "```dataview", "TABLE journal AS 期刊, sample AS 樣本, external_validation AS 外部驗證",
             'FROM "literature"', 'WHERE !contains(external_validation, "無") AND !contains(external_validation, "不適用")',
             "SORT year DESC", "```", "",
             "## 📋 靜態總表（無 Dataview 也可看）", "",
             "| 權威 | 文獻 | 年 | 期刊 | 群組 | 外部驗證 |",
             "|------|------|----|------|------|----------|"]
    for p in sorted(PAPERS, key=lambda x: (x["authority"], -x["year"])):
        lines.append(f"| {p['authority']} | [[{p['key']}]] | {p['year']} | {p['journal']} | "
                     f"{CLUSTER_LABEL[p['cluster']]} | {p['ext_val']} |")
    lines += ["", "## 🗂️ 概念筆記（MOC）",
              "- [[Sharp-van-der-Heijde-score]]", "- [[RA2-DREAM-Challenge]]",
              "- [[Joint-detection-then-score]]", "- [[Transfer-learning]]",
              "- [[ICC-and-Bland-Altman]]", "- [[Grad-CAM]]",
              "- [[Multimodal-fusion]]", "- [[Explainability-SHAP]]",
              "- [[External-validation]]", "- [[Reporting-guidelines]]", "",
              "## 🧭 主題儀表板", "- [[Dashboard-依群組]]", "- [[Dashboard-研究缺口]]", ""]
    w("000-文獻總覽-MOC.md", "\n".join(lines))


def build_cluster_dashboard():
    lines = ["# 🗂️ Dashboard：依群組", "", "> According to PubMed，每篇附 DOI。", ""]
    for cl, label in CLUSTER_LABEL.items():
        lines.append(f"## {label}")
        for p in sorted([x for x in PAPERS if x["cluster"] == cl],
                        key=lambda x: (x["authority"], -x["year"])):
            lines.append(f"- {p['authority']}｜[[{p['key']}]] — {p['title']} "
                         f"([DOI](https://doi.org/{p['doi']}))")
        lines.append("")
    w("Dashboard-依群組.md", "\n".join(lines))


def build_gap_dashboard():
    content = """# 🧭 Dashboard：研究缺口與本專題定位

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
"""
    w("Dashboard-研究缺口.md", content)


CONCEPTS = {
    "Sharp-van-der-Heijde-score": (
        "SvH / modified total Sharp score：逐關節量化 RA 損傷的臨床評分，分別評**骨侵蝕（erosion）**"
        "與**關節間隙狹窄（JSN）**再加總（手+腕 erosion 16 區 0–5、JSN 15 區 0–4，全身上限約 448）。"
        "準確但耗時、需專業、判讀者間有差異——本專題自動化的目標。\n\n相關：[[RA2-DREAM-Challenge]]、"
        "[[Joint-detection-then-score]]"),
    "RA2-DREAM-Challenge": (
        "本領域唯一公開國際基準競賽（674 影像組/562 病人，Synapse syn20545111）。"
        "標準化切分 + 加權 RMSE 評分。是本專題主資料集來源。代表文獻 [[Sun2022_RA2DREAM]]、"
        "外部驗證接力 [[Venalainen2025_AuRA]]。"),
    "Joint-detection-then-score": (
        "「偵測後評分」路線：先用偵測器（YOLO/DeepLabCut/SSD）定位各標的關節，再逐關節分類/評分後加總。"
        "比整圖回歸更適合小樣本——可定位、可解釋、貼近 SvH 定義，並可用單關節裁切擴量。"
        "代表：[[Miyama2022_Contextual]]、[[Hirano2019_PerJoint]]、[[Izumi2024_SSD]]。"),
    "Transfer-learning": (
        "遷移學習：用 ImageNet 預訓練骨幹（ResNet/EfficientNet/MobileNet）微調，於小樣本醫療影像收斂更快、"
        "更不易過擬合。策略：先凍結暖身再漸進式解凍微調。本專題 MVP 即採此法（見 src/raxray）。"),
    "ICC-and-Bland-Altman": (
        "一致性的正確量法。**ICC(2,1)** 衡量絕對一致性、**Bland–Altman** 看系統偏誤與一致性界限。"
        "關鍵：**相關係數高 ≠ 一致**，不可只用 Pearson。小樣本須附 bootstrap 95% CI。"
        "本專題已實作（src/raxray/evaluate.py）。參考 [[Schlereth2024_RAMRIS]]、[[Fiorentino2021_USCartilage]]。"),
    "Grad-CAM": (
        "梯度加權類別激活圖，顯示模型關注的影像區域。**重要侷限**：現有論文多為事後佐證、未量化，"
        "「看起來對 ≠ 模型可靠」。正確用法：當作除錯/偵測捷徑學習工具，展示成功與失敗案例，"
        "量化熱區與 ROI 重疊，並搭配不確定性分析。參考 [[Schmidt2025_GradCAM]]、[[Bayesian2026_Uncertainty]]。"),
    "Multimodal-fusion": (
        "多模態融合：結合影像 + 臨床（DAS28/CRP）+ 實驗室（anti-CCP/RF）+ 組學。"
        "建議從 **late fusion（後期融合）**起步（穩健、不易過擬合）。"
        "**增益須驗證**：新模態要帶正交資訊，並以單模態 baseline + 顯著性檢定證明。"
        "見 [[Dashboard-研究缺口]]、[[WangZ2025_Metabolite]]、[[Sysojev2025_Genotype]]（反面證據）。"),
    "Explainability-SHAP": (
        "SHapley Additive exPlanations：量化每個（表格）特徵對單一預測的貢獻，是多模態/CDSS 的標準可解釋工具。"
        "與影像端的 [[Grad-CAM]] 並列為「雙模態可解釋性」。參考 [[Gan2025_Differential]]、[[Salehi2024_bDMARD]]。"),
    "External-validation": (
        "外部驗證：在獨立來源資料上測試，是全領域最稀缺、最有價值的證據。內部 AUC 外推常下滑"
        "（[[Bouget2022_TNFi]] 0.72→0.70）。本專題即使是高中作品也安排跨來源小批外部測試。"
        "標竿 [[Venalainen2025_AuRA]]。"),
    "Reporting-guidelines": (
        "醫療 AI 報告規範階梯：**CLAIM**（影像 AI，42 項）、**TRIPOD+AI / PROBAST-AI**（預測模型 + 偏誤）、"
        "**DECIDE-AI**（早期臨床評估）、**CONSORT-AI / SPIRIT-AI**（試驗）。"
        "共同硬性要求：外部驗證、判讀者間信度（ICC/κ）、ground truth 透明、錯誤案例分析、無資料洩漏。"
        "對口文獻 [[Collins2024_TRIPOD_AI]]、[[Bhandari2023_CLAIM]]、[[Vasey2022_DECIDE_AI]]、[[Liu2020_CONSORT_AI]]。"),
}


def build_concepts():
    for name, body in CONCEPTS.items():
        content = f"""---
tags: [concept]
---
# {name.replace('-', ' ')}

{body}
"""
        w(f"concepts/{name}.md", content)


def build_template():
    content = """---
title: "<% tp.file.title %>"
authors: ""
year:
journal: ""
doi: ""
pmid: ""
cluster:
study_design: ""
sample: ""
external_validation: ""
authority:
tags: [paper]
source: PubMed
---
# <% tp.file.title %>

> According to PubMed — [DOI](https://doi.org/)

| 欄位 | 內容 |
|------|------|
| 作者 / 年份 |  |
| 期刊 |  |
| 研究設計 |  |
| 樣本 |  |
| 外部驗證 |  |
| 主要結果 |  |

## 對本專題的啟示


## 相關概念


## 我的筆記
-
"""
    w("templates/literature-note.md", content)


def main():
    for p in PAPERS:
        paper_note(p)
    build_moc()
    build_cluster_dashboard()
    build_gap_dashboard()
    build_concepts()
    build_template()
    print(f"已產生 Obsidian vault：{len(PAPERS)} 篇文獻 + {len(CONCEPTS)} 概念筆記 + MOC/儀表板/模板")
    print(f"輸出位置：{os.path.abspath(ROOT)}")


if __name__ == "__main__":
    main()
