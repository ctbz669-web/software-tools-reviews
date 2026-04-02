# HEARTBEAT.md

## Startup Self-Check (每次 session 開始時執行)

```markdown
# 開機自我檢查清單

## 1. 必須讀取的檔案（main session）
- [ ] Read MEMORY.md — 長期記憶，必須載入
- [ ] Read memory/YYYY-MM-DD.md — 今日記憶（如果存在）
- [ ] Read memory/YYYY-MM-DD.md — 昨日記憶（如果存在）

## 2. 驗證記憶完整性
- [ ] 如果上述檔案讀取失敗，嘗試 memory_search 搜尋關鍵資訊
- [ ] 如果 memory_search 也失敗，報告「記憶系統可能有问题」

## 3. 上下文足夠性判斷
- 如果 Kevin 問到過去的專案、決策或設定，優先用 memory_search
- 不要假設自己知道，要搜尋確認
```

---

## Heartbeat Tasks (心跳任務)

```markdown
# 任務檢查清單 — 每個 heartbeat 輪流檢查

## 每日檢查（rotate through these）
- Email? (如果 Gina 配置了)
- Calendar? (如果 GCal 配置了)
- 氣象? (如果相關)

## 記憶維護（每 2-3 天一次）
- Read recent memory/YYYY-MM-DD.md files
- Update MEMORY.md with distilled learnings
- Remove outdated info from MEMORY.md

## 專案健康檢查
- Check git status for uncommitted changes
- Check for stale sessions or processes
```

---

## 觸發條件

- 當 Kevin 說「記得...」或「之前說過...」→ 立即 memory_search
- 當 session 開始但沒有 recent context → 執行 startup self-check
- 當遇到模糊問題 → memory_search 而非猜測

---

## 記憶失敗時的 fallback

如果 memory_search 返回空結果或錯誤：
1. 嘗試直接讀取 `MEMORY.md` 和 `memory/*.md`
2. 如果都失敗，在回覆前明確告知「無法讀取長期記憶」

---

## 禁止事項

- ❌ 不要在沒有確認的情況下假裝記得
- ❌ 不要用猜測代替記憶搜尋
- ❌ 不要跳過 startup self-check（即使覺得不需要）
