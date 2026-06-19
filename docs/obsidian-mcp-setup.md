# 連結 Obsidian（Obsidian MCP 串接）

讓 Claude Code 透過 MCP 直接讀寫你本機 Obsidian vault 的設定指南。
連線方式採用 [`mcp-obsidian`](https://github.com/MarkusPfundstein/mcp-obsidian)，
它透過 Obsidian 的 **Local REST API** 社群外掛與正在運行的 Obsidian 溝通。

> ⚠️ 這些步驟必須在你**本機**執行（Obsidian 跑在你的電腦上）。
> 雲端/遠端的 Claude Code 工作階段無法連到你本機的 Obsidian。

## 架構

```
Claude Code  ──(stdio)──>  mcp-obsidian  ──(HTTPS, localhost)──>  Obsidian (Local REST API 外掛)
```

## 前置需求

- 已安裝 Obsidian，並開啟你的 vault
- [`uv` / `uvx`](https://docs.astral.sh/uv/)（用來執行 `mcp-obsidian`）
  - macOS / Linux：`curl -LsSf https://astral.sh/uv/install.sh | sh`

## 設定步驟

### 1. 安裝並啟用 Local REST API 外掛

1. 在 Obsidian 中：**Settings → Community plugins → Browse**
2. 搜尋 **「Local REST API」** → Install → Enable
3. 進入該外掛設定頁，**複製 API Key**
4. 記下連接埠（HTTPS 預設為 `27124`）

### 2. 設定環境變數

本 repo 的 [`.mcp.json`](../.mcp.json) 已設定好 `obsidian` MCP server，
並以環境變數帶入金鑰（**金鑰不會寫進 repo**）。在啟動 Claude Code 前設定：

```bash
export OBSIDIAN_API_KEY="貼上你剛剛複製的 API key"
# 以下為選填，未設定時用預設值
export OBSIDIAN_HOST="127.0.0.1"
export OBSIDIAN_PORT="27124"
```

> 想長期保存，可把上面三行加到你的 shell 設定檔（如 `~/.zshrc`），
> 或在本機 vault 根目錄建立未追蹤的 `.env` 檔。**請勿把 API key commit 進 git。**

### 3. 在 Claude Code 啟用此專案的 MCP server

1. 在本機 clone 此 repo 後，於專案目錄啟動 Claude Code
2. 首次會提示是否信任專案的 `.mcp.json` → 選擇允許
3. 用 `/mcp` 指令確認 `obsidian` server 狀態為已連線

### 4. 驗證

在 Claude Code 中試問：「列出我 Obsidian vault 裡的檔案」。
若回傳檔案清單即代表串接成功。

## 疑難排解

- **找不到 `uvx`**：執行 `which uvx`，把完整路徑填入 `.mcp.json` 的 `command`。
- **連線被拒 / 憑證錯誤**：Local REST API 預設用自簽憑證的 HTTPS（埠 `27124`）。
  確認 Obsidian 正在運行、外掛已啟用，且埠號一致。
- **401 未授權**：`OBSIDIAN_API_KEY` 與外掛設定頁顯示的金鑰不符，重新複製。

## 參考來源

- [MarkusPfundstein/mcp-obsidian (GitHub)](https://github.com/MarkusPfundstein/mcp-obsidian)
- [Obsidian MCP Setup 2026: Local REST API Complete Guide](https://mcp.directory/blog/obsidian-mcp-complete-guide-2026)
