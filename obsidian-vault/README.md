# RA Xray AI — Obsidian 醫療文獻知識庫

這是把本專題整理出的 **40 篇 PubMed 文獻** 轉成的 Obsidian vault：每篇一張帶 metadata 的筆記、10 張概念筆記（MOC）、Dataview 儀表板與筆記模板。所有資料 **According to PubMed**，每篇附 DOI。

## 內容結構

```
obsidian-vault/
├─ 000-文獻總覽-MOC.md     ← 從這裡開始（總表 + Dataview 動態表格）
├─ Dashboard-依群組.md      ← 三大群組分類
├─ Dashboard-研究缺口.md    ← 研究缺口與本專題定位
├─ literature/             ← 40 篇逐篇文獻筆記（YAML metadata + 雙向連結）
├─ concepts/               ← 10 張概念筆記（SvH、ICC、Grad-CAM、多模態融合…）
└─ templates/              ← 新增文獻時用的模板
```

## 怎麼在 Obsidian 打開（產生醫療整理）

1. 開 Obsidian → **Open folder as vault** → 選這個 `obsidian-vault/` 資料夾。
2. 安裝兩個外掛（Settings → Community plugins）：
   - **Dataview**：啟用 `000-文獻總覽-MOC.md` 裡的動態表格（依權威排序、篩外部驗證…）。
   - **Templater**（選用）：搭配 `templates/literature-note.md` 快速新增文獻。
3. 從 `000-文獻總覽-MOC.md` 進入，用 **Graph view** 看文獻與概念的關聯網。
4. 點任一概念（如 `[[Grad-CAM]]`）→ 右側 **Backlinks** 會列出所有引用它的文獻——這就是「醫療整理」的核心：概念為節點、文獻為證據。

## 怎麼把這些文獻「丟進」另一個 Claude Code session

那個 session（`session_01PJkgzXFkvGmATKpWAgtxuJ`）若連到**同一個 GitHub repo**，最乾淨的方式是讓它直接讀本 repo：

**方法 A（建議）— 讓對方 session 拉這個 repo**
```
git pull
# 文獻原始分析在 docs/lit/A、B、C 與 docs/07
# Obsidian vault 在 obsidian-vault/
```
然後給它這段提示：
> 「讀取 `obsidian-vault/` 與 `docs/lit/`，這是 40 篇 RA 影像 AI 的 PubMed 文獻整理（含 metadata 與 DOI）。請維持 Obsidian 格式（YAML frontmatter + `[[雙向連結]]` + 標籤），協助我：(1) 補上每篇的精讀摘要；(2) 擴充概念筆記；(3) 產生一份依 CLAIM/TRIPOD+AI 的方法學對照表。所有引用須附 DOI，不確定處標『需進一步確認』。」

**方法 B — 直接把資料夾內容貼/上傳**
把 `obsidian-vault/` 壓縮上傳，或把 `000-文獻總覽-MOC.md` + `docs/07-文獻回顧總覽與最權威分析.md` 貼進對話，請它依同一格式延伸。

**方法 C — 重新產生**
本 vault 由 `scripts/build_obsidian_vault.py` 產生（資料即程式）。對方 session 可直接 `python scripts/build_obsidian_vault.py` 重建，或修改 `PAPERS` 清單擴充後重跑。

## 重要聲明
所有文獻資訊 According to PubMed，引用務必附 DOI。本知識庫為研究整理用途、非醫療建議；臨床敘述需由懂醫學/放射者最終把關。標「需進一步確認」者為原始分析未明載，未予編造。
