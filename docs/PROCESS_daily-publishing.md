# 每日發布流程 SOP

## 網站發布

### 每日內容發布流程
1. 撰寫內容：`content/daily/YYYY-MM-DD.md`
2. 執行腳本：`./scripts/publish-daily.sh`
3. Git 操作：`git add . && git commit -m "Update: YYYY-MM-DD"`
4. 推送部署：`git push && wrangler deploy`

### 說明
- `publish-daily.sh` 會生成頁面
- 需要先 git add + commit + push 才會觸發 wrangler deploy
- 兩個命令需要分開執行（wrangler 依賴 git push 後的內容）

## 《AI 管理學》書籍發布

### PDF 發送流程
1. 確認 PDF 位置：`docs/ai-management-book/book.pdf`
2. 使用 CLI 發送到 Telegram：
   ```bash
   openclaw message send --channel telegram --target 605187761 --media "docs/ai-management-book/book.pdf" --message "📄"
   ```
3. **注意**：只能用相對路徑，絕對路徑會被阻擋

### 書籍輸出格式
- PDF：`book.pdf` (1.7MB) ✅ 已完成
- EPUB：`book.epub` ✅ 已完成
- HTML：`book.html` ✅ 已完成
