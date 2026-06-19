# 文獻分析 C：可解釋性、其他影像模態與方法學/報告規範

> 分析代理 C 產出，日期 2026-06-19。專題情境：RA 手部 X 光 AI 評分（TISF 高中科展）。
> 所有 PubMed 內容均標註出處與 DOI 連結。**According to PubMed**，以下文章資訊取自 PubMed 檢索。
> 數字若為文章原文報告者均註明來源；本代理無法確認之處標「需進一步確認」，未引用之數字一律不編造。

---

## 0. 檢索說明與限制

- 工具：PubMed MCP（search / metadata / full-text / related）。
- 本面向部分高度專指的查詢（如「saliency map clinical validation」「Grad-CAM musculoskeletal」）在 PubMed 回傳 0–1 篇，因 PubMed 主收生醫文獻，純方法學/電腦視覺的 saliency 批判性論文（如 Adebayo 等「Sanity Checks for Saliency Maps」、Arun 等「saliency 在醫療影像定位不可靠」）多在 NeurIPS/arXiv，不在 PubMed 索引內。**故「saliency 不可靠」的核心批判性實證在本次 PubMed 檢索中未能直接取得對應文章，標為「需進一步確認」，建議由負責 arXiv/CS 文獻的代理補強。**
- 本報告共納入 13 篇 PubMed 文章，分布：影像模態 DL（4）、可解釋性實作案例（3）、報告/評估規範（6）。

---

## 1. 一句話總結（三個面向）

1. **其他影像模態 DL**：MRI（OMERACT RAMRIS：erosion/osteitis/synovitis）與超音波（軟骨厚度/滑膜炎）的自動評分已達「接近專家、可重現」的研究級成熟度，但仍以單中心、中等樣本為主，外部驗證不足。
2. **可解釋性**：Grad-CAM / saliency 在現有醫療影像論文中幾乎都被當成「事後合理化」展示（模型有看對區域），少有把熱區與臨床標註逐一量化比對者——「看起來對」並不等於模型可靠或定位準確。
3. **報告與評估規範**：已有成熟的階梯式規範體系——CLAIM（影像 AI 報告）、TRIPOD+AI / PROBAST-AI（預測模型報告與偏誤）、DECIDE-AI（早期臨床評估）、CONSORT-AI / SPIRIT-AI（試驗）——核心一致要求：外部驗證、判讀者間信度（ICC）、ground truth 來源透明、錯誤案例分析。

---

## 2. 文獻對比總表

| # | 作者・年份 | 期刊 | 主題類別 | 樣本／設計 | 主要發現或規範重點 | 與本專題關聯 | DOI |
|---|---|---|---|---|---|---|---|
| 1 | Schlereth 2024 | RMD Open | 模態DL：hand MRI RAMRIS | 內部 211 MRI／112 病人（14,906 ROI）+ 外部 220 MRI／75 病人（11,040 ROI），5-fold CV，**含獨立外部驗證** | CNN 自動評 erosion/osteitis/synovitis；macro-AUC 92%/91%/85%；與人工 Spearman 90%/78%/69% | 模態對照組；示範「外部驗證 + 與人工相關係數」這套嚴謹評估，正是科展應仿效的標準 | [DOI](https://doi.org/10.1136/rmdopen-2024-004273) |
| 2 | Fiorentino 2021 | Comput Biol Med | 模態DL：US 軟骨厚度 | 38 受試者掌指關節 US，CNN 回歸距離場 + 後處理 | 平均絕對差 0.032 mm，與專家標註差異約等於觀察者**內**變異（0.036 mm） | 示範「自動量測 vs 觀察者變異」比較法；強調 US 高 intra/inter-observer 變異問題 | [DOI](https://doi.org/10.1016/j.compbiomed.2021.105117) |
| 3 | Østergaard 2025 | Skeletal Radiol | 模態回顧：RA 臨床試驗影像 | 敘事性回顧（Review） | US/MRI 對發炎「truthful、reproducible、sensitive to change」且有效度驗證評分系統；MRI 可評結構破壞進展；AI 為未來方向 | **本面向最權威的影像模態回顧（Østergaard 為 RAMRIS 創建者之一）**；界定各模態的證據位階 | [DOI](https://doi.org/10.1007/s00256-025-05004-2) |
| 4 | Roemer 2024 | Osteoarthritis Cartilage | 模態回顧：半定量 MRI 評分演進 | Perspective（1993–2023 文獻） | 半定量 MRI 評分（WORMS/MOAKS 等）已證 valid/reliable/responsive；**AI 目前仍須驗證與法規核可才能用於臨床試驗** | 提供「評分系統效度三要件（效度/信度/反應性）」框架；對 AI 持審慎態度，可作科展引言的方法學立場 | [DOI](https://doi.org/10.1016/j.joca.2024.01.001) |
| 5 | Schmidt(YOLOv8) 2025 | Eur J Vasc Endovasc Surg | 可解釋性實作：CT 主動脈剝離 | 多中心 5 院、1,138 CT（569/569），含**外部驗證** | AUC 0.964（內）/0.970（外）；**Grad-CAM 顯示模型聚焦於解剖/臨床相關區域**以佐證可解釋性 | 正面範例：外部驗證 + Grad-CAM 同時呈現；但 Grad-CAM 為「定性佐證」而非定量比對 | [DOI](https://doi.org/10.1016/j.ejvs.2025.08.054) |
| 6 | (Bayesian CNN) 2026 | Comput Biol Med | 可解釋性實作：白血病血片 | ALL-IDB2，10-fold CV，3 個預訓練 CNN + MC dropout | VGG16 acc 98.65%；**高不確定性案例的 saliency 呈現「分散/非聚焦」注意力（疑似偽特徵）** | 關鍵啟示：把不確定性與 saliency 連動，可揭露模型「看錯地方」；支持科展加做不確定性分析 | [DOI](https://doi.org/10.1016/j.compbiomed.2025.111419) |
| 7 | (病患態度調查) 2025 | JAMA Netw Open | 可解釋性需求面 | 43 國 74 院 13,806 病患問卷 | **70.2% 病患寧可換取略低準確度也要可解釋 AI**；72.9% 偏好醫師主導決策 | 佐證「可解釋性」對使用者信任的重要性，可寫入科展動機/社會意義 | [DOI](https://doi.org/10.1001/jamanetworkopen.2025.14452) |
| 8 | (兒童風濕 AI 回顧) 2025 | Curr Opin Rheumatol | 可解釋性立場：rheumatology | 敘事回顧 | 反覆強調需更多 explainable AI 與人類監督；涵蓋影像、ML 分層、LLM | 領域內對 XAI 與人為監督的共識陳述，可引用支持研究設計 | [DOI](https://doi.org/10.1097/BOR.0000000000001087) |
| 9 | Liu 2020 | Lancet Digit Health | 規範：CONSORT-AI（試驗報告） | 共識（Delphi 103 人＋會議 31 人＋試行 34 人） | CONSORT 2010 之上新增 14 項 AI 專屬條目：描述 AI 介入、輸入/輸出處理、**人–AI 互動、錯誤案例分析** | 若日後做前瞻評估的最高標準；科展可借「錯誤案例分析」條目 | [DOI](https://doi.org/10.1016/S2589-7500(20)30218-1) |
| 10 | Vasey 2022 | Nat Med | 規範：DECIDE-AI（早期臨床評估） | 共識（Delphi 123/138 人） | 17 項 AI 專屬 + 10 項通用報告條目，聚焦小規模真實臨床、安全性、**human factors** | 連接「研究級準確度」與「臨床有用」的橋樑；點明準確度高 ≠ 臨床有益 | [DOI](https://doi.org/10.1038/s41591-022-01772-9) |
| 11 | Collins 2024 | BMJ | 規範：TRIPOD+AI（預測模型報告） | 編輯/公告（更新版指引） | TRIPOD+AI：涵蓋迴歸與 ML 的臨床預測模型報告指引（更新自 TRIPOD-AI） | **預測/評分模型報告的核心規範**；科展應對照其 checklist 撰寫方法章 | [DOI](https://doi.org/10.1136/bmj.q824) |
| 12 | Collins 2021 | BMJ Open | 規範：TRIPOD-AI/PROBAST-AI 協議 | 方法協議（含 2 篇系統回顧 + Delphi） | 建立 AI 預測模型的**報告指引（TRIPOD-AI）與偏誤風險工具（PROBAST-AI）** | 提供「偏誤風險」自評框架，可用於科展自我檢核 | [DOI](https://doi.org/10.1136/bmjopen-2020-048008) |
| 13 | Bhandari 2023 | Neuroradiology | 規範應用：CLAIM 評 glioma MRI AI | 138 篇文獻以 CLAIM（42 項）評分 | 平均僅 **20/42**（範圍 10–31）；薄弱處集中於**資料蒐集、資料管理、ground truth、AI 效能驗證** | 直接示範用 CLAIM 量化報告品質；科展可自評 CLAIM 分數展現嚴謹 | [DOI](https://doi.org/10.1007/s00234-023-03126-9) |

> 註：表中第 5、6、11 篇之第一作者姓名在 metadata 中需進一步確認（第 11 篇為 TRIPOD+AI 公告，作者群以 Collins/Moons 為首；第 5、6 篇主作者名以「需進一步確認」處理，DOI 為準）。

---

## 3. 對比分析

### 3.1 可解釋性方法在臨床上的可信度與侷限：為何「Grad-CAM 看起來對」不等於模型可靠

- **現況是「定性佐證」而非「定量驗證」**：在本次 PubMed 可取得的實作論文中（YOLOv8 主動脈剝離，[DOI](https://doi.org/10.1016/j.ejvs.2025.08.054)），Grad-CAM 的角色是「展示模型聚焦於解剖相關區域」以增加說服力，屬事後合理化（post-hoc rationalisation）；論文並未把熱區與逐一臨床標註做重疊度（如 IoU、pointing game）量化。這是領域通病。
- **「看對地方」與「判對」是兩件事**：模型可能因背景捷徑（如影像來源醫院、攝影參數、體位）而正確分類，但熱區恰巧落在病灶附近；反之熱區漂亮也可能伴隨錯誤決策。白血病 Bayesian CNN 研究（[DOI](https://doi.org/10.1016/j.compbiomed.2025.111419)）提供關鍵反證：**高不確定性的錯分案例其 saliency 呈現分散、非聚焦的注意力**，顯示注意力圖能揭露「看錯地方」，但前提是要連同不確定性一起檢視，而非只挑漂亮的成功案例展示。
- **方法學上的已知弱點（需進一步確認，建議由 CS/arXiv 代理補實證來源）**：saliency 對模型參數/標籤隨機化不敏感（sanity check 失敗）、不同 XAI 方法熱區彼此不一致、對輸入擾動不穩定、定位精度低於弱監督偵測。這些核心批判文獻不在 PubMed 索引內，本報告不就具體數字下結論。
- **對科展的結論**：Grad-CAM 應作為「除錯與偵測捷徑學習的工具」，不可作為「模型可靠性的證明」。要支持可靠性，需另以**外部驗證 + ICC + 錯誤案例分析**佐證（見 3.3）。

### 3.2 不同影像模態評分自動化的成熟度

- **手部 MRI（RAMRIS）最成熟**：Schlereth 2024（[DOI](https://doi.org/10.1136/rmdopen-2024-004273)）是少數**含獨立外部世代驗證**者，erosion 表現（AUC 92%、Spearman 90%）優於 osteitis、synovitis（69–78%），反映「滑膜炎主觀性高、標註一致性較低」的本質難度。
- **超音波軟骨厚度可量化但樣本小**：Fiorentino 2021（[DOI](https://doi.org/10.1016/j.compbiomed.2021.105117)）僅 38 人，但以「自動量測誤差 ≈ 觀察者內變異（0.032 vs 0.036 mm）」這個對照設計值得學習；US 的高 inter/intra-observer 變異是自動化的主要動機。
- **回顧層級的定位**：Østergaard 2025（[DOI](https://doi.org/10.1007/s00256-025-05004-2)）界定 US/MRI 為臨床試驗中 truthful/reproducible/sensitive-to-change 的工具，AI 為「有趣的未來可能」；Roemer 2024（[DOI](https://doi.org/10.1016/j.joca.2024.01.001)）對半定量評分自動化更直白——**AI 目前仍需驗證與法規核可方能用於臨床試驗**。對科展而言，X 光（Sharp/SvdH）相對 MRI/US 是更可控、標註更一致的入門模態。

### 3.3 報告規範對科展嚴謹度的要求

四套規範構成完整階梯，核心要求高度一致：

- **CLAIM**（影像 AI 報告，42 項）：Bhandari 2023（[DOI](https://doi.org/10.1007/s00234-023-03126-9)）顯示即使已發表論文平均也僅得 20/42，弱點集中在**資料蒐集、資料管理、ground truth 定義、效能驗證**——這正是科展最容易被評審質疑之處。
- **TRIPOD+AI / TRIPOD-AI / PROBAST-AI**（預測模型報告與偏誤）：Collins 2024（[DOI](https://doi.org/10.1136/bmj.q824)）、Collins 2021（[DOI](https://doi.org/10.1136/bmjopen-2020-048008)）。評分模型屬「預測模型」，本套最對口；PROBAST-AI 可作偏誤自評。
- **DECIDE-AI**（早期臨床評估）：Vasey 2022（[DOI](https://doi.org/10.1038/s41591-022-01772-9)）強調**準確度高 ≠ 臨床有用**，須評 human factors 與安全性。
- **CONSORT-AI / SPIRIT-AI**（試驗報告）：Liu 2020（[DOI](https://doi.org/10.1016/S2589-7500(20)30218-1)）——若未做前瞻試驗則不適用，但其「**錯誤案例分析**」條目對科展極有價值。

共同硬性要求：**(a) 外部/獨立驗證；(b) 判讀者間信度（ICC / κ）量化 ground truth 品質；(c) ground truth 來源與標註流程透明；(d) 錯誤案例分析；(e) 資料分割無洩漏。**

---

## 4. 「最具權威性」評選

依面向分別評選，並選出本報告整體最權威者：

- **影像模態回顧最權威：Østergaard 2025（Skeletal Radiology）** [DOI](https://doi.org/10.1007/s00256-025-05004-2)。理由：Mikkel Østergaard 為 OMERACT RAMRIS 評分系統的核心建立者與 RA 影像領域最具代表性的權威之一；該文為 2025 最新、聚焦臨床試驗影像的全模態回顧，界定各模態證據位階，正中本面向需求。
- **報告/評估規範最權威（也是本報告整體最權威）：CONSORT-AI（Liu 2020, Lancet Digital Health）** [DOI](https://doi.org/10.1016/S2589-7500(20)30218-1) 與 **DECIDE-AI（Vasey 2022, Nature Medicine）** [DOI](https://doi.org/10.1038/s41591-022-01772-9) 並列為規範類最高權威。理由：兩者均發表於頂級期刊、以大規模多方利害關係人 Delphi 共識制定、被 EQUATOR Network 收錄為國際標準，影響力與引用度遠超應用型論文。**若僅選一篇對應「評分/預測模型」最對口者，則 TRIPOD+AI（Collins 2024, BMJ）** [DOI](https://doi.org/10.1136/bmj.q824) 為本專題最該優先遵循的規範。
- **可解釋性面向**：本次 PubMed 未檢得權威的 saliency 批判性實證論文（核心文獻在 CS/arXiv），故此面向**不指定 PubMed 內最權威者，標為需進一步確認**，建議由負責方法學/CS 文獻的代理補強（如 Sanity Checks for Saliency Maps、saliency 定位不可靠之放射影像研究）。

---

## 5. 對本專題的可操作建議

1. **報告規範採用組合**：以 **CLAIM**（逐項 42 點自評，目標明顯高於文獻平均 20/42）為主軸撰寫方法與結果章；以 **TRIPOD+AI** 對齊預測/評分模型報告；以 **PROBAST-AI** 做偏誤風險自評表；在討論章引用 **DECIDE-AI** 說明「研究級準確度尚非臨床有用」的界線。把 CLAIM 自評表直接放入科展附錄，是展現嚴謹的高 CP 值做法。
2. **Ground truth 與信度（必做）**：至少兩位標註者，計算 **ICC 或加權 κ** 報告判讀者間信度，並把模型表現與此「人類一致性上限」並列比較（仿 Fiorentino「誤差 ≈ 觀察者內變異」、Schlereth「與人工 Spearman 相關」）。
3. **驗證設計（必做）**：嚴格 patient-level 分割避免洩漏；若可能，取**獨立外部資料**做一次外部驗證（仿 Schlereth）。報告信賴區間，勿只報單點 AUC/accuracy。
4. **可解釋性的正確用法**：Grad-CAM 用於**除錯與偵測捷徑學習**，而非當成可靠性證明。具體做法：(a) 隨機抽樣展示成功與失敗案例的熱區（不可只挑漂亮的）；(b) 若行有餘力，量化熱區與關節/病灶 ROI 的重疊（IoU / pointing game）而非僅肉眼判斷；(c) 加做**不確定性分析**（如 MC dropout），檢查高不確定性案例是否伴隨分散注意力（仿白血病 Bayesian CNN 研究）。
5. **限制章誠實陳述**：明列「Grad-CAM 看似合理 ≠ 模型可靠」「樣本/單中心限制」「saliency 方法學已知弱點（引用 CS 文獻，待補）」，並引用 Roemer 2024 與 Østergaard 2025 之審慎立場，避免過度宣稱臨床可用。
6. **動機與社會意義**：引用 JAMA Netw Open 病患調查（70.2% 偏好可解釋 AI）強化「為何要做可解釋的 RA 評分 AI」的論述。

---

### 附：本報告引用之 13 篇 DOI 清單（According to PubMed）

1. [10.1136/rmdopen-2024-004273](https://doi.org/10.1136/rmdopen-2024-004273)
2. [10.1016/j.compbiomed.2021.105117](https://doi.org/10.1016/j.compbiomed.2021.105117)
3. [10.1007/s00256-025-05004-2](https://doi.org/10.1007/s00256-025-05004-2)
4. [10.1016/j.joca.2024.01.001](https://doi.org/10.1016/j.joca.2024.01.001)
5. [10.1016/j.ejvs.2025.08.054](https://doi.org/10.1016/j.ejvs.2025.08.054)
6. [10.1016/j.compbiomed.2025.111419](https://doi.org/10.1016/j.compbiomed.2025.111419)
7. [10.1001/jamanetworkopen.2025.14452](https://doi.org/10.1001/jamanetworkopen.2025.14452)
8. [10.1097/BOR.0000000000001087](https://doi.org/10.1097/BOR.0000000000001087)
9. [10.1016/S2589-7500(20)30218-1](https://doi.org/10.1016/S2589-7500(20)30218-1)
10. [10.1038/s41591-022-01772-9](https://doi.org/10.1038/s41591-022-01772-9)
11. [10.1136/bmj.q824](https://doi.org/10.1136/bmj.q824)
12. [10.1136/bmjopen-2020-048008](https://doi.org/10.1136/bmjopen-2020-048008)
13. [10.1007/s00234-023-03126-9](https://doi.org/10.1007/s00234-023-03126-9)
