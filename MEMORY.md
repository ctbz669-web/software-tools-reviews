# MEMORY.md - Long-Term Memory

_Only keep durable rules, stable preferences, and repeated decisions here._

---

## 快速索引

| 主題 | 位置 |
|------|------|
| 用戶偏好 | ## Kevin |
| 模型狀態 | ## Models |
| 瀏覽器設定 | ## Browser |
| 草台班子規則 | ## 草台班子 |
| 影片規範 | ## Video |
| 檔案發送 | ## Messaging |
| 檔案驗收 | ## 檔案操作二次確認規則 |
| 工作目錄 | ## 工作檔案儲存規則 |
| 日記發布 | ## 每日日記發布 SOP |
| 專案記憶 | ## 專案記憶 |

---

## Kevin 基本資料
- **Name:** Kevin
- **Telegram ID:** 605187761
- **工作目錄:** /Volumes/WorkData/ctbzai/ (外接 NVMe)
- **主要語言:** 中文

### Kevin 偏好
- Kevin prefers direct, executable answers with minimal fluff
- 喜歡宏觀框架和方法論
- 不喜歡太實操容易過時的內容
- 重視系統思維

---

## Models
**2026-04-03 更新**：Kimi 有空參數 bug（tool call 收到 `{"command":""}` 空字串），所有 agent 已改用 `minimax/MiniMax-M2.7`。

- **問題**：kimi/kimi-code 和 kimi-coding/k2p5 都有問題
- **PR 狀態**：OpenClaw PR #50152 和 #44888 尚未 merge
- **解法**：切換到 MiniMax-M2.7

### Agent 模型設定
- 所有 12 個 agent 的 primary model 已改為 `minimax/MiniMax-M2.7`
- 主 session 維持 MiniMax-M2.7

---

## Browser
- Browser tasks default to **OpenClaw browser `user` profile**, meaning Kevin's real signed-in Chrome.

---

## 草台班子 / ctbz
- 詳細規則請參閱 `CTBZ_SOP.md`

---

## Video
- Subtitles should be **at most 2 lines**.

---

## Path Discipline
- `read` / `write` / `edit` / `exec` → use absolute paths by default
- message / media sending → use workspace-relative paths by default
- Only break this rule if a specific tool requires a different format

---

## Messaging (Telegram & Discord)

### 檔案發送規則（通用）
OpenClaw 的檔案發送機制**跨平台一致**，適用於 Telegram、Discord 等所有通道：

- **只能用相對路徑**，絕對路徑被阻擋
- workspace：`/Volumes/WorkData/ctbzai/`
- 指令：`openclaw message send --channel telegram --target <chat_id> --media <相對路徑> --message <文字>`

### 正確範例
```bash
# Telegram 發送 PDF
openclaw message send --channel telegram --target 605187761 --media "docs/ai-management-book/book.pdf" --message "📄"
```

### 錯誤範例
```
❌ 絕對路徑（如 `/Volumes/...`）會被阻擋
❌ ~ 路徑會被阻擋
```

---

## 檔案操作二次確認規則

**所有涉及檔案的工作，都必須二次確認才算真正完成。**

| 階段 | 動作 | 說明 |
|------|------|------|
| **第一次確認** | 執行完成 | 工具執行成功、命令退出碼為 0 |
| **第二次確認** | 人工驗證 | 檢查檔案真的存在，大小合理、內容正確 |

### 觸發時機
- ✅ 寫入/建立檔案
- ✅ 修改/刪除檔案
- ✅ 複製/移動檔案
- ✅ 下載/壓縮/解壓縮
- ✅ 編譯/轉換格式

### 未二次確認的後果
❌ 不視為完成 ❌ 不可進行下一步 ❌ 不可發送或發布

---

## 工作檔案儲存規則

### 主要儲存位置
**`/Volumes/WorkData/ctbzai/`**

### 目錄結構
```
/Volumes/WorkData/ctbzai/
├── docs/                    # 文件與文稿（包含 AI 管理學）
├── projects/                # 專案
├── memory/                  # 每日記憶
├── openclaw-workspace/      # OpenClaw workspace
└── ...
```

### 規則
1. **產出檔案優先放 `/Volumes/WorkData/ctbzai/`**，而非 workspace
2. **按需建立子目錄**，保持分類清晰
3. **Workspace** 僅作為 Telegram/Discord 發送前的暫存

---

## 每日日記發布 SOP

### 正確流程

**Step 1. 先寫 Obsidian 內部完整版（最重要）**
- 路徑：`/Users/kevin/Library/Mobile Documents/iCloud~md~obsidian/Documents/ctbz-daily/YYYY-MM-DD.md`
- 要求：比網站版更詳細，完整記錄

**Step 2. 再整理網站公開版**
- 來源：從 Obsidian 版整理
- 原則：刪除敏感資訊，保留對外有價值的內容
- 輸出：HTML 放在 `site/daily/YYYY-MM-DD/index.html`

**Step 2.5. 檢查品牌形象資產（如果首頁有變更）**
- Logo 必須是 PNG 格式（透明背景）
- Brand-hero 需要壓縮（建議 1500px 寬，80% 品質）

**Step 3. 發布到網站**
```bash
CLOUDFLARE_ACCOUNT_ID=fe517553706a3fa550fa0216cb18393f wrangler pages deploy site/ --project-name caotaibanzi-media --branch main
```

### 驗收清單
- [ ] Obsidian 版已更新（比網站版更詳細）
- [ ] 網站版已去敏感
- [ ] 網站首頁已出現入口
- [ ] Logo 是 PNG 格式（透明背景）
- [ ] Brand-hero 已壓縮
- [ ] wrangler deploy 成功

### 禁止事項
- ❌ 不要先寫網站版，再補 Obsidian 版
- ❌ 不要把私人內容原封不動發到網站
- ❌ 不要漏記錯誤與解法

---

## 專案記憶

### caotaibanzi-media
- 專案記憶：`projects/caotaibanzi-media/memory.md`
- GitHub: https://github.com/ctbz669-web/caotaibanzi-media
- 網站: https://daily.ctbzai.com

### 《AI 管理學》
- 專案記憶：`docs/ai-management-book/memory.md`

---

## 技術筆記

### OpenClaw exec-approvals
- 位置：`/Users/kevin/.openclaw/exec-approvals.json`
- 設定：`security: "full"`, `ask: "off"`

### Discord exec approval
- 已啟用：`channels.discord.allowFrom = ["user:839364717624426516"]`

### Cloudflare
- Account ID: `fe517553706a3fa550fa0216cb18393f`

---

## 待解決
- 封面設計 - 中文文字渲染問題（AI 圖像生成工具無法正確顯示中文）

---

_Last updated: 2026-04-03_
