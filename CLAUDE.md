# CLAUDE.md

這個 repo 是一個 **Obsidian vault**（"Claudian"）。當你（Claude Code）在這裡工作時請遵守以下慣例：

## Vault 慣例
- 筆記都是 Markdown，放在 `Notes/`、`Daily/` 等資料夾。
- 筆記之間用 Obsidian 雙向連結 `[[筆記標題]]`（不是 `.md` 路徑連結，因為 `app.json` 設了 `useMarkdownLinks: false`）。
- 連結用**最短**形式（`newLinkFormat: shortest`）：直接寫標題即可，不用寫路徑。
- 分類用 `#tag`，metadata 放在檔案最上方的 YAML frontmatter（`type`、`tags`、`date`、`status`…）。
- 圖片 / 附件放 `Attachments/`。
- 新範本放 `Templates/`，沿用既有 frontmatter 風格。

## 不要動的東西
- `.obsidian/workspace.json` 等本機狀態檔已被 `.gitignore` 排除，不要硬加進版控。
- 不要改 `.obsidian/` 設定，除非使用者明確要求。

## 編輯筆記時
- 新增筆記時補上合理的 frontmatter 與至少一個雙向連結，避免製造孤兒筆記。
- 保持中文（除非使用者另有指示）。
