# B — 多模態臨床決策輔助文獻分析（RA AI 專題）

> 文獻分析代理 B：多模態臨床決策輔助（multimodal clinical decision support）
> 來源：以下所有文獻內容均 **According to PubMed**（基於從 PubMed 檢索之文章），每篇均附 DOI 連結。
> 製表日期：2026-06-19。共納入 14 篇（2 篇種子 + 12 篇擴充）。

---

## 1. 一句話總結現況

According to PubMed，目前 RA（類風濕性關節炎）的 AI/ML 研究多半仍以「單一資料源」為主（影像、臨床、實驗室或組學擇一），而真正將影像 + 臨床指標（DAS28、CRP/ESR）+ 實驗室（anti-CCP、RF）+ 組學融合的「多模態臨床決策輔助」仍處於早期、小樣本、外部驗證稀缺的階段；表現最佳者出現在「多模態超音波深度學習評分」（AUC 約 0.87–0.95、含外部測試）與「血漿蛋白質體 / 代謝體 + 臨床」治療反應預測（AUROC 0.80–0.88），但跨族群可重現性與可解釋性仍是公認瓶頸。

---

## 2. 文獻對比總表

> AUC/AUROC 等數字均為各原文所報告值；樣本數以原文為準。可解釋性、外部驗證欄若原文未明述則標「需進一步確認」。

| # | 作者, 年份 | 期刊 | 樣本數 | 模態組合 | 預測目標 | 模型 | 主要結果 | 可解釋性 | 外部驗證 | 主要限制 | DOI |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Wang Z, 2025（種子）| Arthritis Res Ther | 60 RA | 血漿代謝體 + 臨床（MTX、CRP）| 骨破壞 / mTSS 放射學進展（RRP）| 多種 ML；GNB 選核心代謝物，建 CjBM | CjBM AUC 0.800；高 BERS vs 低 BERS OR=0.01 | 核心代謝物重要性排序（特徵層級）| 與既往模型比較，無獨立外部佇列 | 樣本極小（n=60）、單中心、易過度配適 | [DOI](https://doi.org/10.1186/s13075-025-03576-x) |
| S2 | Gan M, 2025（種子）| Front Immunol | 106 RA-SS + 135 SS-PA | 臨床 + 實驗室（anti-CCP、RF、anti-SSA）+ 放射學（侵蝕關節數）| 鑑別 RA-SS vs SS-PA | LASSO 選特徵 + RF/4 種 ML | RF AUC 0.854 (95%CI 0.747–0.944)，優於 LR | SHAP（anti-CCP、RF、侵蝕數、anti-SSA、CRP）| 7:3 內部驗證，無外部佇列 | 單中心、回溯、樣本中等、無外部驗證 | [DOI](https://doi.org/10.3389/fimmu.2025.1614631) |
| A1 | Zhou Z, 2022 | Patterns (Cell Press) | 1244 訓練 + 前瞻+外部測試 | 多模態超音波（灰階+能量都卜勒）| RA 活動度自動評分（EULAR-OMERACT）| 深度學習 RATING（知識引導 + 自監督）| 準確率前瞻 86.1%、外部 85.0%；讀者研究使 10 名放射醫師平均 41.4%→64.0% | 生成可解釋特徵輔助決策 | 有（外部測試集 + 讀者研究）| 影像單模態為主、未融合臨床/實驗室 | [DOI](https://doi.org/10.1016/j.patter.2022.100592) |
| A2 | He X, 2024 | Rheumatology (Oxford) | 1244 影像，測試 152/354 | 多模態超音波（靜/動態灰階 + 靜/動態 PD）| RA 活動度評分（0–3）| 深度學習（ResNet）| AUC 0.74–0.95（依分數）；動態模型優於靜態、優於多數資深醫師 | 與 12 名醫師對比 | 兩個測試佇列 | 僅影像模態、無臨床融合 | [DOI](https://doi.org/10.1093/rheumatology/kead366) |
| A3 | He S, 2025 | Nat Commun | 278 RA + 60 高風險 + 99 HC | 血漿蛋白質體 + 臨床（DAS28-CRP）| 治療反應（MTX+LEF / MTX+HCQ）、發病、活動度 | ML（蛋白質體特徵）| AUROC 0.88 (MTX+LEF)、0.82 (MTX+HCQ)；獨立佇列 ELISA 驗證 | 蛋白質特徵層級 | 有（獨立佇列 ELISA）| 仍偏組學單域，影像未納入 | [DOI](https://doi.org/10.1038/s41467-025-62032-1) |
| A4 | Yoosuf N, 2022 | Rheumatology (Oxford) | 39 女性 RA | 多組學（轉錄體 + 流式細胞 + 血漿蛋白）| anti-TNF 反應（EULAR）| ML（以轉錄體為主）| 高預測效用（具體 AUC 需進一步確認）；EPPK1、CHI3L1/YKL-40 為標記，獨立佇列重現基因表現 | 生物標記/基因表現 | 部分（基因表現於獨立佇列重現）| 樣本極小（n=39）、單性別、易過擬合 | [DOI](https://doi.org/10.1093/rheumatology/keab521) |
| A5 | Salehi F, 2024 | J Clin Med | 154 RA | 基線臨床（含 DAS28-ESR）| bDMARD 反應（6 月初始 / 12 月持續）| XGBoost、AdaBoost 等 5 種；巢式 CV | 初始反應 AUROC 0.91 (XGBoost)；持續反應 0.84 (AdaBoost) | SHAP（DAS28-ESR 為關鍵）| 巢式交叉驗證，無外部佇列 | 單中心、無外部驗證、樣本中等 | [DOI](https://doi.org/10.3390/jcm13133890) |
| A6 | Bouget V, 2022 | RMD Open | 161（ESPOIR）+ 118（ABIRISK）| 臨床 + 常規血液（DAS28、淋巴球等）| TNFi 反應（EULAR、ΔDAS28）| 線性回歸/RF/XGBoost/CatBoost | CatBoost 訓練 AUROC 0.72；外部 ABIRISK 0.70/0.71 | 特徵選擇（DAS28、淋巴球、ALT…）| 有（獨立 ABIRISK 佇列）| AUC 中等、純臨床、無影像/組學 | [DOI](https://doi.org/10.1136/rmdopen-2022-002442) |
| A7 | Myasoedova E, 2022 | Arthritis Care Res | 643（336 訓練 + 307 驗證）| 臨床 + 基因體（160 SNP）| MTX 反應（EULAR, 3 月）| 監督式 ML（5×10-fold CV）| 訓練 AUC 0.84；驗證準確率 76%（敏感 72%/特異 77%）| 特徵重要性（SNP + DAS28）| 有（獨立驗證佇列）| 基因增益有限、無影像 | [DOI](https://doi.org/10.1002/acr.24834) |
| A8 | Sysojev AÖ, 2025 | J Intern Med | 2432 早期 RA | 臨床 + 全基因型（imputed genotype）| MTX 治療結局（EULAR primary 等）| 多種 ML | AUC ~0.62；EULAR primary 0.67；基因貢獻可忽略 | — | 大型登錄資料、內部評估 | 預測力低、基因近乎無增益（反面證據）| [DOI](https://doi.org/10.1111/joim.20087) |
| A9 | Kalweit M, 2021 | PLoS One | >9500 病人 / 65000 visits | 臨床 + 病人報告 + 實驗室 + 用藥（縱貫）| 下次就診 DAS28-BSR 活動度（分類+回歸）| AdaptiveNet（自適應 RNN）| 準確率 75.6%；回歸 MSE 0.9；勝傳統 ML >7% | — | 大型多中心登錄（SCQM）| 特異度低、用藥角色小、無影像 | [DOI](https://doi.org/10.1371/journal.pone.0252289) |
| A10 | Baloun J, 2025 | Sci Rep | 8543 RA（641 D2T / 1825 緩解）| 臨床 + 病人報告（DAS28-ESR、CDAI、CRP、HAQ）| 難治型 D2T RA 風險 | LASSO/ridge/SVM/RF/XGBoost | AUC 0.656–0.832 | SHAP（疾病活動度、HAQ、療程）| 大型登錄（ATTRA），內部驗證 | 純臨床、無影像/組學、AUC 範圍寬 | [DOI](https://doi.org/10.1038/s41598-025-18298-y) |
| A11 | Morales-Ivorra I, 2024 | Diagnostics | 77 RA（前瞻 12 週）| 手部熱像（thermography）+ CRP | 關節發炎/疾病活動度（ThermoJIS/ThermoDAI）| 預訓練 ML 熱像指標 | ThermoDAI 與 CDAI/SDAI/DAS28-CRP 相關 ρ≈0.78–0.83；ThermoJIS AUROC 0.67 | 指標化輸出 | 有（前瞻外部驗證，多中心 3 院）| 樣本小、熱像為新興模態 | [DOI](https://doi.org/10.3390/diagnostics14131394) |
| A12 | Labinsky H, 2023 | Diagnostics | 縱貫常規 + 10 病例 vignette / 5 醫師 | 臨床常規（CDSS）| RA 復發（flare）風險預測 + CDSS | AI flare 預測工具 + RCM CDSS | 敏感 72%/特異 76%/AUROC 0.80；提升醫師決策信心、降低偏差 | CDSS 可用性 SUS 82 | 試點，無大型外部佇列 | 樣本/病例少、為可用性試點 | [DOI](https://doi.org/10.3390/diagnostics13010148) |

> 另有 3 篇綜述/旁證（不計入 12 篇主表，供脈絡參考）：
> - Shi Y, 2024（Front Immunol，精準風濕病 ML 綜述，指出多模態 + 深度學習為趨勢，但過擬合/泛化/可解釋性為瓶頸）[DOI](https://doi.org/10.3389/fimmu.2024.1409555)
> - Bilgin E, 2025（Ther Adv Musculoskelet Dis，AI 於 RA/axSpA/PsA 管理綜述，強調多模態 AI 為未來）[DOI](https://doi.org/10.1177/1759720X251343579)
> - Forrest IS, 2026（Med，SHIMMER：以常規檢驗 + EHR 跨七種病的 spectral 模型，含 RA，示範可攜式臨床決策）[DOI](https://doi.org/10.1016/j.medj.2026.101150)

---

## 3. 逐篇對比分析

### 3.1 哪些模態組合最具預測力？
According to PubMed，依「報告 AUC/AUROC 高低 + 是否含外部驗證」綜合：

- **影像（多模態超音波）深度學習** 表現最突出且最穩健：Zhou Z 2022 RATING 外部測試準確率 85.0% 並有讀者研究 [DOI](https://doi.org/10.1016/j.patter.2022.100592)；He X 2024 多模態 US AUC 高達 0.95 [DOI](https://doi.org/10.1093/rheumatology/kead366)。兩者皆來自北京協和同一團隊，影像品質與標註一致性高。
- **組學 + 臨床（蛋白質體/代謝體）治療反應預測** 次之但臨床轉化價值高：He S 2025 血漿蛋白質體 AUROC 0.88/0.82 且有獨立佇列 ELISA 驗證 [DOI](https://doi.org/10.1038/s41467-025-62032-1)；種子 S1 代謝體 + 臨床 CjBM AUC 0.800 [DOI](https://doi.org/10.1186/s13075-025-03576-x)。
- **純臨床 + 實驗室（DAS28、CRP、anti-CCP、RF）** 在「鑑別診斷」與「短期反應」可達中高表現：種子 S2 RF AUC 0.854（鑑別 RA-SS/SS-PA）[DOI](https://doi.org/10.3389/fimmu.2025.1614631)；Salehi 2024 bDMARD 初始反應 AUROC 0.91 [DOI](https://doi.org/10.3390/jcm13133890)。但這類數值多為**內部驗證**，外部驗證後常下滑（見 Bouget 2022 由 0.72 降至 0.70 [DOI](https://doi.org/10.1136/rmdopen-2022-002442)）。

**小結**：單看數字，影像多模態 US 與組學 + 臨床最具預測力；但若以「真正多源融合」嚴格定義，目前尚無一篇同時融合「影像 + 臨床 + 實驗室 + 組學」四域並完成外部驗證——這是本領域明顯空白。

### 3.2 影像在多模態中扮演的角色
- 影像（尤其 US 的灰階 + 能量都卜勒、動態 vs 靜態）是目前**最能被深度學習端到端高精度量化**的模態，且 He X 2024 顯示動態 PD 模型優於多數資深醫師 [DOI](https://doi.org/10.1093/rheumatology/kead366)。
- 但目前影像研究**多為「影像單模態」**，尚未與 DAS28/CRP/anti-CCP/組學系統性融合；RATING 的價值在於「人機協作」提升醫師判讀，而非多源融合 [DOI](https://doi.org/10.1016/j.patter.2022.100592)。
- 放射學評分（如 mTSS / van der Heijde-Sharp、骨侵蝕關節數）在 S1、S2 中是作為**預測目標或臨床特徵**而非深度學習影像輸入——這正是把「影像 SvH 評分」延伸成多模態決策的接口。
- 新興影像模態：手部熱像（A11）成本低、可前瞻外部驗證，與 CRP 結合即構成簡易多模態 [DOI](https://doi.org/10.3390/diagnostics14131394)；功能性腦影像（pain markers）在 PreCePRA 試驗預測治療反應 balanced accuracy 達 95.4%（A 旁證 BrainInsights，需進一步確認其 RA 子樣本數）。

### 3.3 單模態 vs 多模態的增益
- **正向增益**：S1 顯示在既有臨床模型上「加入代謝體 BERS 可顯著改善判別」（P=0.035）[DOI](https://doi.org/10.1186/s13075-025-03576-x)；S2 的 LASSO + 多源特徵（臨床 + 實驗室 + 放射學）達 AUC 0.854 [DOI](https://doi.org/10.3389/fimmu.2025.1614631)。
- **增益有限/無增益（重要反面證據）**：Sysojev 2025 在 2432 人大型佇列中，加入全基因型對 MTX 結局預測「貢獻可忽略」（AUC 仍 ~0.62）[DOI](https://doi.org/10.1111/joim.20087)；Myasoedova 2022 加入 160 SNP 後 AUC 0.84，但 SNP 增益相對 baseline DAS28 有限 [DOI](https://doi.org/10.1002/acr.24834)。→ **「多加一個模態不必然有增益」**，基因體在 MTX 反應上的增量價值偏弱。
- **啟示**：增益高度依賴「新增模態是否帶來與目標正交的資訊」。代謝體/蛋白質體（反映即時代謝/發炎狀態）增益較明確；常見基因變異（靜態）增益較弱。

### 3.4 過度配適 / 小樣本問題（本領域共通弱點）
- 最高 AUC 的多模態研究往往**樣本最小**：S1 n=60、A4 n=39、A11 n=77、A12 試點——這些 AUC 0.80–0.95 的數字有**樂觀偏誤**風險，Shi 2024 綜述明確警告「小樣本 + 缺乏多元族群測試會高估模型表現」[DOI](https://doi.org/10.3389/fimmu.2024.1409555)。
- **緩解做法（文獻示範）**：自監督預訓練（RATING）、巢式交叉驗證（Salehi 2024）、獨立外部佇列（Bouget 2022、He S 2025、Myasoedova 2022）、前瞻驗證（Morales-Ivorra 2024）。**有外部/前瞻驗證者，其數字可信度應優先採信。**
- 凡 n<100 且無外部驗證之 AUC，本報告均視為「需進一步確認」之探索性結果。

---

## 4. 「最具權威性」評選

### 🥇 第一名（影像多模態方向）：Zhou Z et al., 2022, *Patterns* (Cell Press) — RATING 系統
[DOI](https://doi.org/10.1016/j.patter.2022.100592)

理由：
1. **方法學最嚴謹**：1244 張影像訓練、含**前瞻測試集 + 獨立外部測試集**（外部 85.0%），並以自監督預訓練解小樣本問題——直接針對本領域最大弱點。
2. **臨床效度有實證**：讀者研究中讓 10 名放射醫師平均準確率自 41.4% 提升至 64.0%，證明「決策輔助」的真實增益，而非僅報告離線 AUC。
3. **期刊權威**：刊於 Cell Press 的 *Patterns*（資料科學旗艦），影響力與審查標準高；團隊為北京協和（PUMCH），影像標註權威。
4. 與本專題「影像 → 臨床決策」主軸最契合，是「可解釋影像 AI 輔助醫師」的標竿。

### 🥈 第二名（組學 + 臨床、治療反應方向）：He S et al., 2025, *Nature Communications*
[DOI](https://doi.org/10.1038/s41467-025-62032-1)

理由：
1. **頂級期刊 + 縱貫設計**：278 RA + 60 高風險 + 99 HC 縱貫佇列，涵蓋發病前、活動度、治療反應多任務。
2. **治療反應預測 AUROC 0.88/0.82 並以獨立佇列 ELISA 驗證**——少數同時具高表現與外部驗證者。
3. 提供可落地的血漿蛋白質生物標記，臨床轉化路徑清楚。

> 種子 S1（CjBM, AUC 0.800）與 S2（RF, AUC 0.854）方法新穎、可解釋性佳（SHAP），但**樣本小且無獨立外部佇列**，權威性次於上述兩篇；可作為「多模態融合可行性」的概念驗證引用。

---

## 5. 對我們專題的啟示（從「影像 SvH 評分」延伸為多模態臨床決策）

我們既有的核心是**影像 SvH / van der Heijde-Sharp 放射學評分**。文獻顯示，把它延伸為多模態臨床決策的路徑與可行性如下：

### 5.1 高中科展範圍內務實可做（建議優先）
1. **影像評分 + 結構化臨床/實驗室的「晚期融合（late fusion）」**：把 SvH 評分當成一個特徵，串接 DAS28、CRP/ESR、anti-CCP、RF，用**樹模型（RF/XGBoost）+ SHAP** 預測「是否為快速放射學進展（RRP）」。此路徑在 S1、S2、Salehi、Baloun 均被驗證可行且可解釋，且工具門檻低（scikit-learn / XGBoost）。[S1 DOI](https://doi.org/10.1186/s13075-025-03576-x)、[S2 DOI](https://doi.org/10.3389/fimmu.2025.1614631)
2. **嚴守防過擬合流程**：巢式交叉驗證（仿 Salehi 2024 [DOI](https://doi.org/10.3390/jcm13133890)）、固定 train/test 切分、回報信賴區間；樣本小時**優先採用表格 ML 而非深度學習**。
3. **以 SHAP 做可解釋輸出**：對應 S2、Baloun、Salehi 的做法，產出「哪些特徵推升 RRP 風險」的個案級解釋，契合 CDSS 精神（A12 Labinsky [DOI](https://doi.org/10.3390/diagnostics13010148)）。
4. **單模態 vs 多模態增益的對照實驗**：明確比較「僅影像 SvH」vs「影像 + 臨床 + 實驗室」的 AUC，重現 S1「加入新模態是否顯著改善（P 值）」的論證——這是科展最有說服力的科學問句。
5. **低成本新興影像補強（選配）**：若取得不易，可參考熱像（A11）這類低成本模態作為多模態示範 [DOI](https://doi.org/10.3390/diagnostics14131394)。

### 5.2 列為「未來展望」（超出高中科展務實範圍）
1. **影像端到端深度學習（US 灰階 + 能量都卜勒）**：如 RATING / He X 需大量標註影像、自監督預訓練與算力，建議列未來展望而非主實驗。[A1 DOI](https://doi.org/10.1016/j.patter.2022.100592)、[A2 DOI](https://doi.org/10.1093/rheumatology/kead366)
2. **組學融合（代謝體/蛋白質體/基因體）**：LC-MS、蛋白質體平台成本高；但可在討論中引用 He S 2025、S1 說明「組學增益方向」。注意 Sysojev 2025 提醒**常見基因變異增益可忽略** [DOI](https://doi.org/10.1111/joim.20087)，避免盲目堆疊基因模態。
3. **真正四域融合 + 外部驗證的 CDSS**：本領域尚無此標竿（空白），可作為本專題「研究缺口與長期目標」的定位語。
4. **前瞻 / 外部驗證**：科展階段難做，但應在限制與展望中明列，呼應 Morales-Ivorra 2024 的前瞻驗證精神 [DOI](https://doi.org/10.3390/diagnostics14131394)。

### 5.3 一句定位
> 把「影像 SvH 評分」當成多模態決策的**錨點特徵**，以晚期融合 + 樹模型 + SHAP 做「快速放射學進展」的可解釋預測，並用單模態 vs 多模態對照量化影像 + 臨床的增益——這是文獻支持、工具可及、且填補「四域融合尚屬空白」研究缺口的務實切入點。

---

*所有引用內容 According to PubMed；DOI 連結如上。標示「需進一步確認」者為原文未明確報告之數值，未予編造。*
