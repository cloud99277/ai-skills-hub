#!/bin/bash
# 读取 Claude 历史对话记录
# 用法: ./history.sh [数量]

COUNT=${1:-10}
HISTORY_FILE="$HOME/.claude/history.jsonl"

if [ ! -f "$HISTORY_FILE" ]; then
    echo "历史记录文件不存在: $HISTORY_FILE"
    exit 1
fi

echo "========== 最近 $COUNT 条对话 =========="
echo ""

# 倒序读取最后 N 行，解析 display 字段
tail -n "$COUNT" "$HISTORY_FILE" | while IFS= read -r line; do
    # 提取 display 字段的值（JSON 解析）
    display=$(echo "$line" | grep -o '"display":"[^"]*"' | head -1 | sed 's/"display":"//;s/"$//')
    if [ -n "$display" ]; then
        echo "> $display"
    fi
done

echo ""
echo "========================================="
