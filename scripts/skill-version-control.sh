#!/bin/bash
# skill-version-control.sh
# Skill 版本控制管理

SKILLS_DIR="/Volumes/WorkData/ctbzai/openclaw-workspace/skills"
VERSIONS_DIR="$SKILLS_DIR/.versions"

# 創建版本目錄
mkdir -p "$VERSIONS_DIR"

# 函數：備份當前 Skill
backup_skill() {
  local skill_name="$1"
  local skill_path="$SKILLS_DIR/$skill_name"
  
  if [ ! -d "$skill_path" ]; then
    echo "❌ Skill 不存在: $skill_name"
    return 1
  fi
  
  local version=$(date +%Y%m%d_%H%M%S)
  local backup_path="$VERSIONS_DIR/$skill_name/$version"
  
  mkdir -p "$backup_path"
  cp -r "$skill_path"/* "$backup_path/"
  
  # 記錄版本資訊
  cat > "$backup_path/.version-info.json" << EOF
{
  "version": "$version",
  "backedUpAt": "$(date -Iseconds)",
  "skillName": "$skill_name"
}
EOF
  
  echo "✅ 已備份: $skill_name → v$version"
  echo "   位置: $backup_path"
}

# 函數：列出所有版本
list_versions() {
  local skill_name="$1"
  
  if [ -z "$skill_name" ]; then
    echo "📋 所有 Skill 的版本:"
    ls -1 "$VERSIONS_DIR" 2>/dev/null | while read skill; do
      echo ""
      echo "🔧 $skill:"
      ls -1 "$VERSIONS_DIR/$skill" 2>/dev/null | sort -r | head -5 | while read ver; do
        echo "   - $ver"
      done
    done
  else
    echo "📋 $skill_name 的版本歷史:"
    ls -1 "$VERSIONS_DIR/$skill_name" 2>/dev/null | sort -r | while read ver; do
      local info_file="$VERSIONS_DIR/$skill_name/$ver/.version-info.json"
      local date_str=$(echo "$ver" | sed 's/_/ /')
      echo "   - $date_str"
    done
  fi
}

# 函數：還原到指定版本
restore_version() {
  local skill_name="$1"
  local version="$2"
  
  local backup_path="$VERSIONS_DIR/$skill_name/$version"
  local skill_path="$SKILLS_DIR/$skill_name"
  
  if [ ! -d "$backup_path" ]; then
    echo "❌ 版本不存在: $version"
    return 1
  fi
  
  # 先備份當前版本
  backup_skill "$skill_name"
  
  # 還原
  rm -rf "$skill_path"
  cp -r "$backup_path" "$skill_path"
  rm -f "$skill_path/.version-info.json"
  
  echo "✅ 已還原: $skill_name → $version"
}

# 函數：創建 CHANGELOG
create_changelog() {
  local skill_name="$1"
  local skill_path="$SKILLS_DIR/$skill_name"
  local changelog="$skill_path/CHANGELOG.md"
  
  if [ ! -f "$changelog" ]; then
    cat > "$changelog" << 'EOF'
# Changelog

所有版本的變更記錄。

## [Unreleased]

### Added
- 

### Changed
- 

### Fixed
- 

## 版本歷史

EOF
    echo "✅ 已創建 CHANGELOG.md"
  else
    echo "ℹ️ CHANGELOG.md 已存在"
  fi
}

# 主命令處理
case "$1" in
  backup)
    backup_skill "$2"
    ;;
  list)
    list_versions "$2"
    ;;
  restore)
    restore_version "$2" "$3"
    ;;
  changelog)
    create_changelog "$2"
    ;;
  *)
    echo "🔧 Skill 版本控制工具"
    echo ""
    echo "用法:"
    echo "  $0 backup <skill-name>       - 備份當前 Skill"
    echo "  $0 list [skill-name]          - 列出版本歷史"
    echo "  $0 restore <skill> <version> - 還原到指定版本"
    echo "  $0 changelog <skill-name>    - 創建 CHANGELOG"
    echo ""
    echo "示例:"
    echo "  $0 backup minimax-multimodal"
    echo "  $0 list minimax-multimodal"
    echo "  $0 restore minimax-multimodal 20260401_120000"
    ;;
esac
