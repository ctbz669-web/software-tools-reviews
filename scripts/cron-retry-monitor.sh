#!/bin/bash
# cron-retry-monitor.sh
# Cron 任務失敗重試監控

CRON_LOG="/Volumes/WorkData/ctbzai/openclaw-workspace/memory/cron-executions.json"
FAILURE_LOG="/Volumes/WorkData/ctbzai/openclaw-workspace/memory/cron-failures.md"
MAX_RETRIES=3
RETRY_BACKOFFS=(0 300 900)  # 0min, 5min, 15min

# 初始化日誌檔案
if [ ! -f "$CRON_LOG" ]; then
  echo '{"executions": []}' > "$CRON_LOG"
fi

# 函數：記錄執行
cron_start() {
  local task_id="$1"
  local task_name="$2"
  local timestamp=$(date -Iseconds)
  
  # 使用 Python 更新 JSON
  python3 << EOF
import json
import sys

try:
  with open('$CRON_LOG', 'r') as f:
    data = json.load(f)
except:
  data = {"executions": []}

data["executions"].append({
  "taskId": "$task_id",
  "taskName": "$task_name",
  "startedAt": "$timestamp",
  "status": "running",
  "attempt": 1,
  "retryCount": 0
})

with open('$CRON_LOG', 'w') as f:
  json.dump(data, f, indent=2)
EOF
  
  echo "📋 Cron 任務開始: $task_name (ID: $task_id)"
}

# 函數：記錄成功
cron_success() {
  local task_id="$1"
  local timestamp=$(date -Iseconds)
  
  python3 << EOF
import json

try:
  with open('$CRON_LOG', 'r') as f:
    data = json.load(f)
  
  for exec in data["executions"]:
    if exec["taskId"] == "$task_id" and exec["status"] == "running":
      exec["status"] = "success"
      exec["completedAt"] = "$timestamp"
      break
  
  with open('$CRON_LOG', 'w') as f:
    json.dump(data, f, indent=2)
except Exception as e:
  print(f"Error: {e}")
EOF
  
  echo "✅ Cron 任務成功: $task_id"
}

# 函數：記錄失敗並排程重試
cron_fail() {
  local task_id="$1"
  local error_msg="$2"
  local timestamp=$(date -Iseconds)
  
  python3 << EOF
import json

try:
  with open('$CRON_LOG', 'r') as f:
    data = json.load(f)
  
  for exec in data["executions"]:
    if exec["taskId"] == "$task_id" and exec["status"] in ["running", "retrying"]:
      exec["status"] = "failed"
      exec["failedAt"] = "$timestamp"
      exec["error"] = """$error_msg"""
      exec["retryCount"] = exec.get("retryCount", 0) + 1
      
      if exec["retryCount"] < $MAX_RETRIES:
        exec["nextRetry"] = "$timestamp"
        exec["shouldRetry"] = True
      else:
        exec["shouldRetry"] = False
      break
  
  with open('$CRON_LOG', 'w') as f:
    json.dump(data, f, indent=2)
except Exception as e:
  print(f"Error: {e}")
EOF
  
  # 寫入失敗日誌
  cat >> "$FAILURE_LOG" << EOF

### [CRON FAILED] $task_id
- **時間**: $timestamp
- **錯誤**: $error_msg
- **狀態**: 等待重試

EOF
  
  echo "❌ Cron 任務失敗: $task_id"
  echo "📝 錯誤已記錄到: $FAILURE_LOG"
}

# 主命令處理
case "$1" in
  start)
    cron_start "$2" "$3"
    ;;
  success)
    cron_success "$2"
    ;;
  fail)
    cron_fail "$2" "$3"
    ;;
  list)
    cat "$CRON_LOG" | python3 -m json.tool
    ;;
  *)
    echo "用法: $0 {start|success|fail|list} [task_id] [task_name|error_msg]"
    echo ""
    echo "示例:"
    echo "  $0 start daily-news '每日新聞'"
    echo "  $0 success daily-news"
    echo "  $0 fail daily-news 'API timeout'"
    ;;
esac
