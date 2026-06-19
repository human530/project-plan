# 文獻分析 A：自動影像損傷評分（RA 手部 X 光 → Sharp–van der Heijde 分數）

> 子領域：用深度學習從手部（含足部）X 光自動產生 RA 的 Sharp–van der Heijde（SvH）／modified total Sharp score（mTSS）損傷分數。
> 文獻全部來自 PubMed（According to PubMed），每篇均附 DOI 連結。本份共納入 10 篇（5 篇種子 + 5 篇擴充），涵蓋整圖回歸、逐關節偵測後評分、影像配準量化、以及基準競賽與 viewpoint。
> 製表日期：2026-06-19。標示「需進一步確認」者為摘要未明載、需讀全文核實之處。

---

## 1. 一句話總結本子領域現況

According to PubMed，自動化 RA 手部 X 光 SvH/mTSS 評分已從「逐關節偵測＋分類」走向「端到端多階段（分割→偵測→回歸，含 Vision Transformer）」與「影像配準量化進展」三條路線並進，**RA2-DREAM 競賽（Sun 等 2022）建立了公認基準**，而**目前唯一完成獨立外部驗證並證實能偵測個體縱向進展的是 AuRA（Venäläinen 等 2025）**；整體仍受限於樣本小、單中心、缺乏外部驗證，且高分（重度破壞）病例誤差偏大。

---

## 2. 文獻對比總表

| # | 作者年份 | 期刊 | 資料量／來源 | 方法 | 任務 | 主要結果指標 | 外部驗證 | 主要限制 | DOI |
|---|---------|------|------------|------|------|------------|---------|---------|-----|
| 1 | Moradmand & Ren 2025 | Sci Rep | 訓練 679 例、外部測試 291 例（來源需進一步確認） | 4 階段：影像前處理→UNet 手部分割→YOLOv7 關節偵測→自建 ViT 回歸 | 整圖回歸 Overall Sharp Score（OSS） | 關節偵測 99% 準確率；OSS：Huber 4.9、RMSE 9.73、MAE 5.35、ICC 0.702（P<0.001，於 Sharp<50 表現最佳） | 有（外部 291 例） | 高分（≥50）誤差大；ICC 中等；單一資料管線細節需確認 | [DOI](https://doi.org/10.1038/s41598-025-86073-0) |
| 2 | Venäläinen 等 2025 | Rheumatology (Oxford) | 訓練 367 例（2 個既有臨床研究，源自 RA2-DREAM）；外部驗證 205 例（Turku 大學醫院）；縱向 54 例 | AuRA 演算法（RA2-DREAM 期間開發），預測 SvH 總分（手＋足） | 整圖回歸 SvH 總分 + 縱向進展偵測 | 外部 RMSE 23.6（優於兩個 DREAM 頂尖解法 35.0 / 35.6）；縱向變化與專家相關 Pearson R=0.74（P<0.001） | **有（真正外部 + 縱向）** | 樣本仍偏小；高分區仍是誤差主來源（雖相對較佳） | [DOI](https://doi.org/10.1093/rheumatology/keae215) |
| 3 | Sun 等 2022 | JAMA Netw Open | 674 影像組 / 562 病人（2 個臨床研究）：訓練 367、leaderboard 119、最終 188 | 國際群眾外包競賽（RA2-DREAM）；13 個最終演算法 + baseline | 三個子挑戰：整體損傷、JSN、erosion 之 SvH 量化 | 加權 RMSE：整體 0.44（Team Shirin）、JSN 0.38（HYL-YFG）、erosion 0.43（Gold Therapy）；獨立驗證 concordance 0.71/0.78/0.82 | 有（post-challenge 獨立驗證集） | 各子挑戰最佳為不同團隊、方法異質；非單一可部署模型 | [DOI](https://doi.org/10.1001/jamanetworkopen.2022.27423) |
| 4 | Miyama 等 2022 | Arthritis Res Ther | 226 影像 / 40 RA 病人（Kyushu 大學） | DeepLabCut 偵測 + 4 種分類模型（含「對側同名關節脈絡」） | 逐關節偵測 + 二元分類（intact SHS=0 vs ≥1） | 偵測率 erosion 98.0% / JSN 97.3%；最佳（對側比較）F=0.70(erosion)/0.81(JSN)、PR-AUC 0.73/0.85；erosion 勝過骨科醫師 | 無（單中心、交叉驗證） | 僅二元分類非完整分數；樣本小、單中心 | [DOI](https://doi.org/10.1186/s13075-022-02914-7) |
| 5 | Izumi 等 2024 | Sci Rep | 260 手部 X 光（PIP/MP 標註，Keio 大學） | 多個 SSD 偵測模型 ensemble（每種特殊發現各一） | 偵測 ankylosis／subluxation/dislocation（mTSS 大分項） | MP/PIP 偵測率 >99.8%；ensemble 在 accuracy/recall/precision/specificity/F/IoU 均優於個別模型 | 無（5-fold CV、單中心） | 僅偵測特殊發現、尚未產生 erosion/JSN 完整分數 | [DOI](https://doi.org/10.1038/s41598-024-58242-0) |
| 6 | Izumi 等 2023 | PLoS One | 216 手部 X 光（Keio 大學，2015 年就診） | AlexNet/ResNet/DenseNet/ViT 比較，腕關節 subluxation/ankylosis 分類 | 逐關節分類（subluxation/ankylosis） | 腕關節：accuracy 0.97/0.89、AUC 0.92/0.85（subluxation/ankylosis）；陽性樣本極少（21 subluxation、42 ankylosis 影像） | 無（5-fold CV、單中心） | 正樣本極少、類別不平衡；僅腕關節 | [DOI](https://doi.org/10.1371/journal.pone.0281088) |
| 7 | Wang 等 2023 | Comput Med Imaging Graph | 手指關節影像對（Hokkaido，數量需進一步確認） | 深度 intra-subject 剛性配準網路 | 影像配準量化 JSN「進展」（非分數） | Euclidean 距離 MSE 0.0031、SD 0.0661 mm、mismatch 0.48%；達次像素精度，附對位視覺化；程式碼開源 | 無（同院資料） | 量化進展而非 SvH 分數；需配對追蹤影像 | [DOI](https://doi.org/10.1016/j.compmedimag.2023.102273) |
| 8 | Hirano 等 2019 | Rheumatol Adv Pract | 216 影像 / 108 RA 病人（訓練/驗證 186、測試 30；擴增至 11,160 關節影像）（Osaka/RIKEN） | 兩步：關節偵測 + CNN 逐關節評分 | 逐關節序數評分（JSN 0–4、erosion） | 偵測敏感度 95.3%；exact agreement JSN 49.3–65.4%、erosion 70.6–74.1%；每影像相關係數 JSN 0.72–0.88、erosion 0.54–0.75 | 無（單中心、保留測試集） | 測試集小（30）；exact agreement 偏低 | [DOI](https://doi.org/10.1093/rap/rkz047) |
| 9 | Üreten & Maraş 2022 | J Digit Imaging | 手部 X 光（數量需進一步確認，回溯性） | YOLOv4 偵測手部 + 預訓練 VGG-16 遷移學習分類 | 影像級分類（RA / OA / normal），**非 SvH 評分** | RA vs normal：acc 90.7%、AUC 0.97；OA vs normal：acc 90.8%、AUC 0.96；三類 acc 80.6% | 無 | 僅做疾病分類、不產生損傷分數；與本主題關聯較弱（背景對照） | [DOI](https://doi.org/10.1007/s10278-021-00564-w) |
| 10 | Bird, Oakden-Rayner 等 2022 | Arthritis Res Ther | 觀點論文（無新資料） | Viewpoint / 評論 | 論述 AI 取代/改良 RA 放射評分之前景與限制 | 無量化指標；主張 AI 可提升對輕度疾病的敏感度與效率 | 不適用 | 觀點性質、無實證；作者群為知名醫學 AI 團隊（Adelaide AIML） | [DOI](https://doi.org/10.1186/s13075-022-02972-x) |

---

## 3. 逐篇之間的對比分析

### 3.1 方法路線差異

**(A) 整圖回歸（image-level regression）**
- Moradmand & Ren 2025（#1）與 RA2-DREAM 系列（#3、#2）屬此路線：最終直接回歸一個整體分數（OSS / SvH 總分）。
- 優點：流程相對單純、與臨床「總分」直接對應、可端到端。缺點：可解釋性差、對「哪一關節壞」無定位；且高分病例（重度破壞）樣本稀少導致誤差大——#1 明言僅在 Sharp<50 表現最好，#2 也指出改善主要來自「降低高分區誤差」。
- #1 是 PubMed 中**首度將 Vision Transformer 用於 OSS 回歸**（According to PubMed [DOI](https://doi.org/10.1038/s41598-025-86073-0)）。

**(B) 逐關節偵測後評分（detect-then-score）**
- Miyama 2022（#4，DeepLabCut）、Hirano 2019（#8，偵測+CNN）、Izumi 2024（#5，SSD ensemble）、Izumi 2023（#6，多 backbone 比較）皆先偵測/定位各標的關節，再對每個關節分類或評分。
- 優點：可定位、可解釋、貼近 SvH 原始「逐關節」定義、容易加入臨床先驗（#4 用「對側同名關節脈絡」比較，是設計亮點）。缺點：誤差會跨階段累積；多數只做二元（intact vs 非 intact）或特殊發現（ankylosis/subluxation），**尚未組合出完整 SvH 總分**（#5、#6 作者自述為「邁向自動評分系統的一步」）。
- #8（Hirano）是少數做到完整序數評分（JSN 0–4 + erosion）者，但 exact agreement 偏低、測試集僅 30。

**(C) 影像配準量化進展（registration-based progression）**
- Wang 2023（#7）路線獨特：不評絕對分數，而以剛性配準量化同一病人前後追蹤影像的 JSN「變化」，達次像素精度並提供對位視覺化。
- 優點：對「進展偵測」這個臨床真正關心的問題最直接、精度極高、可審視可靠度。缺點：需配對追蹤影像、輸出非 SvH 分數，與分類/回歸路線不可直接比較。

**(D) 基準與背景**
- #3（RA2-DREAM）是**唯一的公開競賽基準**，提供標準化資料切分與加權 RMSE 評分，是後續方法（含 #2 AuRA）的共同參照系。
- #9（Üreten）只做 RA/OA/normal 影像分類、不產生損傷分數，僅作為「偵測+遷移學習」技術背景對照。
- #10（Oakden-Rayner 團隊 viewpoint）提供領域論述：主張現行 SvH 對「今日較輕症譜」可能已不夠敏感，AI 應發揮對細微變異的敏感度，而非僅複製人工分數。

### 3.2 效能高低與可比性

- **指標不可直接互比**：#1 用 RMSE/MAE/ICC（整圖 OSS）、#2/#3 用（加權）RMSE（SvH 總分）、#4/#5/#6/#8 用 F-measure/PR-AUC/AUC/exact agreement（逐關節）、#7 用 mm 級配準誤差。任務尺度與評分權重不同，跨論文比數字會誤導。
- 在**同一基準（RA2-DREAM 量綱）**下才有可比性：#2 報告 AuRA 外部 RMSE 23.6 顯著優於兩個 DREAM 頂尖解法（35.0、35.6）（According to PubMed [DOI](https://doi.org/10.1093/rheumatology/keae215)）；而 #3 競賽內加權 RMSE 已低至 0.38–0.44（不同加權尺度，與 #2 的 23.6 非同一量綱，不可直接相減）。
- **逐關節路線**中，#4 的 erosion 分類「勝過骨科醫師」是強結果，但屬二元分類、單中心；#8 的完整序數評分相關係數 0.72–0.88（JSN）尚可、erosion 0.54–0.75 偏弱。
- 一致觀察：**高分/重度破壞與 erosion 是共同難點**（#1 高分誤差、#8 erosion 較弱、#3 各子挑戰由不同團隊奪冠暗示無單一全能方法）。

### 3.3 資料規模與外部驗證的影響

- 樣本普遍很小：#4 40 人、#5 260 影像、#6 216 影像、#8 108 人。小樣本 + 單中心使結果樂觀且難外推。
- **外部驗證是分水嶺**：絕大多數（#4、#5、#6、#7、#8、#9）僅交叉驗證或同院保留集，**無真正外部驗證**。只有 #1（外部 291 例）與 #2（Turku 醫院 205 例外部 + 54 例縱向）做了外部驗證；其中 #2 還是唯一驗證「個體縱向進展偵測」者。
- #3 RA2-DREAM 雖樣本最大且有 post-challenge 獨立驗證，但輸出是「多個團隊各自的演算法」而非單一可部署模型——這正是 #2 的補位價值（把 DREAM 期間方法工程化、外部驗證、Docker 釋出）。

---

## 4. 「最具權威性」評選

### 第一權威：Sun 等 2022, JAMA Network Open — RA2-DREAM Challenge（PMID 36036935）
[DOI](https://doi.org/10.1001/jamanetworkopen.2022.27423)

理由：
- **基準地位**：是本子領域唯一的國際群眾外包基準競賽（674 影像組/562 病人、標準化訓練/leaderboard/最終切分、加權 RMSE 評分、post-challenge 獨立驗證），後續多數工作（包含本份最強的 #2）都以它為參照。
- **期刊層級高**：JAMA Network Open（頂級綜合醫學期刊）。
- **設計嚴謹**：以 Bayes factor + bootstrapping 評估可重現性，並用獨立驗證集確認 concordance（0.71/0.78/0.82）。
- **團隊權威**：Sage Bionetworks（DREAM 系列主辦）、UAB、Mount Sinai、IBM 等，作者群為醫學 AI 競賽與風濕領域權威。

### 第二權威：Venäläinen 等 2025, Rheumatology (Oxford) — AuRA 外部驗證（PMID 38597875）
[DOI](https://doi.org/10.1093/rheumatology/keae215)

理由：
- **唯一完成真正外部驗證 + 縱向進展驗證**：在獨立 Turku 醫院 205 例上 RMSE 23.6，**顯著優於兩個 RA2-DREAM 頂尖解法**；並證明能偵測個體層級的縱向變化（Pearson R=0.74）。這是領域最稀缺、最有臨床意義的證據。
- **可重現/可部署**：演算法以 Docker（elolab/aura）公開釋出。
- **期刊層級**：Rheumatology (Oxford) 為風濕科權威期刊；且為 Validation Study，正面回應了全領域「缺乏外部驗證」的最大弱點。

> 註：若單看「方法新穎度」，#1（首度 ViT 做 OSS 回歸）值得一提；但其 ICC 0.702 屬中等、外部資料來源細節需進一步確認，權威性不及上述兩篇之「基準 + 外部/縱向驗證」。

---

## 5. 對高中專題（TISF）的可借鏡點與務實落地建議

**整體策略建議（小樣本 + 免費 Colab）：採「逐關節偵測後評分」而非整圖回歸。**
理由：整圖回歸（#1）需要大樣本才壓得住高分區誤差，且 ViT 在免費 Colab 上訓練吃力；逐關節路線（#4、#8）在數百張影像、單卡上即可做出像樣結果，且可解釋、貼近 SvH 定義、易於做消融與展示。

具體可借鏡點：
1. **兩階段管線是穩健範式**：偵測（定位關節）→ 分類/序數評分。Hirano（#8）用「先偵測再對每個關節 CNN 評分」，並透過裁切單一關節把 186 張影像擴增成 11,160 張關節影像——這是小樣本下擴充訓練量的關鍵技巧，直接可抄。
2. **善用臨床先驗：對側比較**：Miyama（#4）的「對側同名關節脈絡比較」在小樣本下就勝過骨科醫師，且幾乎不增加運算量。我們可實作「左右手同名關節成對輸入」當作強 baseline 的差異化亮點。
3. **偵測器選型對齊免費資源**：YOLO（#1 用 YOLOv7、#9 用 YOLOv4）在 Colab 上有成熟、輕量、易上手的實作；DeepLabCut（#4）亦可。建議用 YOLO 系列做關節偵測，避免自建 UNet 分割增加負擔。
4. **先做「二元 / 少類別」再談完整分數**：#5、#6 都坦言只先做 ankylosis/subluxation 或 intact-vs-非 intact，是合理的階段性目標。專題可設定「JSN 是否異常」或「erosion 0/1/2 三級」這種縮小版任務，先把 pipeline 跑通。
5. **務必留「外部 / 跨來源」測試**：全領域最大弱點就是缺外部驗證（#3、#10 都點出）。即使是高中專題，只要能用「不同來源的小批影像」做哪怕極小的外部測試，並如實報告掉分，學術嚴謹度就會明顯勝出。可考慮公開資料集（需進一步確認可用性與授權）。
6. **指標要對齊任務**：分類用 F1/AUC/PR-AUC（注意類別不平衡，#6 正樣本極少→必用 PR 曲線而非僅 accuracy）；若做序數評分，報 exact agreement + 與專家的相關係數/ICC（對齊 #1、#8）。
7. **進階加分（選做）**：若有同一受試者的前後追蹤影像，可參考 Wang（#7）的配準量化「進展」概念做小型 demo；其程式碼開源，但需配對影像，資料取得是門檻（需進一步確認）。
8. **資料與算力現實**：免費 Colab GPU 與時限下，建議影像縮放、凍結預訓練 backbone 只微調頂層（遷移學習，如 #9 的 VGG-16）、用 5-fold CV 報告均值±標準差（對齊 #5、#6 的做法），以小樣本取得穩定可信的數字。

---

## 附註：方法論與引用聲明

- 本份所有文獻資訊與數據均來自 PubMed（According to PubMed），每篇於表格與內文均附 DOI 連結。
- 數字均取自 PubMed 摘要/metadata；凡摘要未明載者已標「需進一步確認」，未作任何臆測或編造。
- 納入 10 篇：種子 5 篇（39870749、36192761、38565576、37531811、36510330）＋ 擴充 5 篇（36036935 RA2-DREAM、38597875 AuRA、31872173 Hirano、35018539 Üreten、36780446 Izumi 2023）。
