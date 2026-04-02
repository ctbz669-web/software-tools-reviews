# CTBZ_SOP.md - 草台班子專案必讀規則

如果任務和以下任何內容有關：
- `daily.ctbzai.com`
- 草台班子日記 / 運營日記 / `ctbz-daily`
- 草台班子 Logo / mascot / 品牌資產
- 網站發布 / Cloudflare Pages / Obsidian 同步

那麼除了正常啟動流程外，**還要主動讀這些文件**：

1. `MEMORY.md`
   - 長期決策與工作流總結
2. `memory/YYYY-MM-DD.md`（今天 + 昨天，必要時往前追）
   - 最近實際發生的變更、錯誤與修復
3. `/tmp/caotaibanzi-media/DEPLOY_SOP.md`
   - 網站正確部署方式
4. `/tmp/caotaibanzi-media/SITE_STRUCTURE_SPEC.md`
   - 首頁固定區塊、canonical 資產、結構規範
5. `/Users/kevin/Library/Mobile Documents/iCloud~md~obsidian/Documents/ctbz-daily/README.md`
   - Obsidian 內部完整版日記規則

### 草台班子專案核心規則（摘要）
- `ctbz-daily/` = **內部完整版、私人內容**，先寫這裡
- `daily.ctbzai.com` = **公開精簡版**，必須去除機密 / 敏感資訊後再發布
- 如果 Kevin 說「紀錄日記」：
  1. 先更新 Obsidian `ctbz-daily/`
  2. 再整理網站版並發布
- Logo canonical：`/tmp/caotaibanzi-media/assets/canonical/ctbzai-logo-canonical.png`
- Mascot canonical：`/tmp/caotaibanzi-media/assets/canonical/ctbzai-mascot-canonical.png`
- 不要直接拿聊天預覽圖 / JPG / 假透明圖覆蓋站點資產
- `git push` **不等於網站已部署**
- 真正發布 `daily.ctbzai.com` 還要執行：
  `CLOUDFLARE_ACCOUNT_ID=fe517553706a3fa550fa0216cb18393f wrangler pages deploy site --project-name=caotaibanzi-media`

**🎭 Voice Storytelling:** If you have `sag` (ElevenLabs TTS), use voice for stories, movie summaries, and "storytime" moments! Way more engaging than walls of text. Surprise people with funny voices.

**📝 Platform Formatting:**

- **Discord/WhatsApp:** No markdown tables! Use bullet lists instead
- **Discord links:** Wrap multiple links in `<>` to suppress embeds: `<https://example.com>`
- **WhatsApp:** No headers — use **bold** or CAPS for emphasis
