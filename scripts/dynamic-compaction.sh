#!/bin/bash
# dynamic-compaction.sh
# 根據任務類型動態調整 memoryFlush 閾值

# 讀取當前任務上下文 (從環境變量或檔案)
TASK_TYPE="${TASK_TYPE:-general}"
STATE_FILE="/Volumes/WorkData/ctbzai/openclaw-workspace/memory/compaction-state.json"

# 根據任務類型設定閾值
case "$TASK_TYPE" in
  "code-review"|"refactor"|"architecture")
    # 程式碼審查需要更多上下文
    SOFT_THRESHOLD=8000
    RESERVE_TOKENS=30000
    ;;
  "simple-chat"|"qa"|"search")
    # 簡單對話可以用較低閾值
    SOFT_THRESHOLD=2000
    RESERVE_TOKENS=15000
    ;;
  "writing"|"documentation")
    # 寫作類任務中等閾值
    SOFT_THRESHOLD=4000
    RESERVE_TOKENS=20000
    ;;
  *)
    # 預設值
    SOFT_THRESHOLD=4000
    RESERVE_TOKENS=20000
    ;;
esac

# 更新狀態檔案
cat > "$STATE_FILE" << EOF
{
  "taskType": "$TASK_TYPE",
  "softThresholdTokens": $SOFT_THRESHOLD,
  "reserveTokensFloor": $RESERVE_TOKENS,
  "lastUpdated": "$(date -Iseconds)"
}
EOF

echo "✅ Compaction 設定已更新:"
echo "   任務類型: $TASK_TYPE"
echo "   Soft Threshold: $SOFT_THRESHOLD"
echo "   Reserve Tokens: $RESERVE_TOKENS"

# 輸出給 openclaw.json 使用的配置
echo ""
echo "📋 請將以下配置加入 openclaw.json:"
echo '"
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": '"$RESERVE_TOKENS"',
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": '"$SOFT_THRESHOLD"'
        }
      }
    }
  }
"'
