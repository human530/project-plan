---
type: note
tags:
  - guide
  - claudian
---

# Claudian 使用說明

**Claudian** = Obsidian（你寫筆記）+ Claude Code（我幫你整理）+ git（版本控制）。
三者操作的是**同一個資料夾**，所以可以無縫接力。

## 它怎麼運作
```
你的電腦
 └─ project-plan/        ← 這個資料夾
     ├─ 用 Obsidian 打開 → 是一個 vault
     ├─ 用 Claude Code  → 是一個工作區
     └─ 用 git          → 有版本控制 / 雲端同步
```

## 典型工作流程

### A. 平常自己寫
1. 在 Obsidian 寫筆記、拉連結。
2. 想存檔／同步時：`git add . && git commit -m "..." && git push`。

### B. 請 Claude 幫忙
你可以叫我做這些事（我會直接改檔案再 commit）：
- 「把這週的 Daily 筆記整理成一篇週報」
- 「幫所有 #project 筆記補上 frontmatter 的 status 欄位」
- 「找出沒有任何雙向連結的孤兒筆記」
- 「把這篇長筆記拆成幾篇並互相連結」

### C. 兩邊同步
- 我改完 push 後，你在本地 `git pull` 就能在 Obsidian 看到。
- 你在本地改完 push 後，我這邊 `git pull` 就能接著做。

> ⚠️ 注意：我跑在**雲端臨時容器**，碰不到你本地的電腦，也無法幫你安裝 Obsidian 桌面程式。Obsidian app 本身要你自己到 [obsidian.md](https://obsidian.md) 下載。我能做的是維護這個 vault 的**內容與結構**。

## 命名小建議
- 筆記檔名盡量用有意義的標題，雙向連結才好打。
- 中文檔名 Obsidian 完全支援，雙向連結直接 `[[中文標題]]`。

回首頁：[[Welcome]]
