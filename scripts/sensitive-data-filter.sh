#!/bin/bash
# sensitive-data-filter.sh
# 自動過濾日誌檔案中的敏感資訊

LOG_DIR="${1:-/Volumes/WorkData/ctbzai/openclaw-workspace/memory}"
BACKUP_DIR="${LOG_DIR}/.sensitive-backups"

# 創建備份目錄
mkdir -p "$BACKUP_DIR"

# 敏感資訊匹配模式（使用 grep -E 相容的正則）
PATTERN_APIKEY='sk-[a-zA-Z0-9_-]{20,}'
PATTERN_MINIMAX='sk-(api|cp)-[a-zA-Z0-9_-]{20,}'
PATTERN_GEMINI='AIza[0-9A-Za-z_-]{30,}'
PATTERN_XAI='xai-[a-zA-Z0-9_-]{40,}'
PATTERN_BEARER='Bearer[[:space:]]+[a-zA-Z0-9_-]{20,}'

echo "🔍 掃描敏感資訊: $LOG_DIR"

# 掃描並處理所有日誌檔案
find "$LOG_DIR" -type f \( -name "*.md" -o -name "*.json" -o -name "*.txt" \) | while read -r file; do
  # 檢查是否包含敏感資訊
  if grep -qE "$PATTERN_APIKEY|$PATTERN_MINIMAX|$PATTERN_GEMINI|$PATTERN_XAI|$PATTERN_BEARER" "$file" 2>/dev/null; then
    echo "⚠️  發現敏感資訊: $file"
    
    # 備份
    backup_file="$BACKUP_DIR/$(basename "$file").$(date +%Y%m%d_%H%M%S).bak"
    cp "$file" "$backup_file"
    
    # 替換敏感資訊
    sed -i.tmp -E "s/$PATTERN_APIKEY/[REDACTED_API_KEY]/g; s/$PATTERN_MINIMAX/[REDACTED_API_KEY]/g; s/$PATTERN_GEMINI/[REDACTED_API_KEY]/g; s/$PATTERN_XAI/[REDACTED_API_KEY]/g; s/$PATTERN_BEARER/Bearer [REDACTED_TOKEN]/g" "$file" 2>/dev/null
    rm -f "$file.tmp"
    
    echo "✅ 已處理並備份"
  fi
done

echo "✅ 掃描完成。備份位置: $BACKUP_DIR"
