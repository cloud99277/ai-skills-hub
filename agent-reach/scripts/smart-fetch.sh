#!/usr/bin/env bash
# smart-fetch.sh — 智能网页抓取（纯免费方案）
#
# 用法：smart-fetch.sh <URL> [--raw]
# 输出：抓取到的 Markdown 内容（stdout）
# 退出码：0=成功  1=所有方式都失败
#
# 策略：
#   1. 默认用 Jina Reader（免费，输出 Markdown）
#   2. 检查返回质量（长度、是否为空、是否全是 JS/HTML 垃圾）
#   3. 质量不合格 → fallback 到直接 curl + 浏览器 UA
#   4. --raw → 跳过 Jina，直接用 curl 抓取原始 HTML
#
# 依赖：curl（必须）

set -euo pipefail

URL="${1:-}"
MODE="${2:-}"

if [[ -z "$URL" ]]; then
    echo "用法: smart-fetch.sh <URL> [--raw]" >&2
    exit 1
fi

# === 质量检查 ===
check_quality() {
    local content="$1"
    local char_count="${#content}"

    # 空内容或太短
    if [[ $char_count -lt 100 ]]; then
        echo "too_short"
        return
    fi

    # HTML 标签密度检查
    local tag_count
    tag_count=$(echo "$content" | grep -oP '<[a-zA-Z]' 2>/dev/null | wc -l | tr -d '[:space:]')
    tag_count=${tag_count:-0}
    local line_count
    line_count=$(echo "$content" | wc -l | tr -d '[:space:]')
    line_count=${line_count:-0}

    if [[ $line_count -gt 0 ]] && [[ $tag_count -gt $((line_count / 2)) ]] && [[ $tag_count -gt 20 ]]; then
        echo "html_heavy"
        return
    fi

    # JS 代码残留检查
    local js_markers
    js_markers=$(echo "$content" | grep -cE '(function\s*\(|var\s+|const\s+|let\s+|=>\s*\{|window\.|document\.)' || true)
    if [[ $js_markers -gt 10 ]]; then
        echo "js_heavy"
        return
    fi

    echo "ok"
}

# === Jina Reader（Markdown 输出） ===
fetch_jina() {
    local url="$1"
    curl -sL --max-time 15 "https://r.jina.ai/${url}" 2>/dev/null || true
}

# === 直接 curl + 浏览器 UA（fallback） ===
fetch_raw() {
    local url="$1"
    curl -sL --max-time 15 \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
        -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
        "$url" 2>/dev/null || true
}

# === 主流程 ===

# --raw 模式
if [[ "$MODE" == "--raw" ]]; then
    echo "[smart-fetch] 直接 curl: $URL" >&2
    result=$(fetch_raw "$URL")
    if [[ -n "$result" ]]; then
        echo "$result"
        exit 0
    fi
    echo "[smart-fetch] curl 失败" >&2
    exit 1
fi

# 默认：Jina → 质量检查 → 可能 fallback 到 curl
echo "[smart-fetch] 尝试 Jina Reader: $URL" >&2
jina_result=$(fetch_jina "$URL")
quality=$(check_quality "$jina_result")

if [[ "$quality" == "ok" ]]; then
    echo "[smart-fetch] Jina Reader 成功 (${#jina_result} 字符)" >&2
    echo "$jina_result"
    exit 0
fi

# Jina 质量不合格，fallback 到直接 curl
echo "[smart-fetch] Jina 质量不合格: $quality，fallback 到直接 curl..." >&2
raw_result=$(fetch_raw "$URL")

if [[ -n "$raw_result" ]] && [[ ${#raw_result} -gt ${#jina_result} ]]; then
    echo "[smart-fetch] curl fallback 成功 (${#raw_result} 字符，原始 HTML)" >&2
    echo "$raw_result"
    exit 0
fi

# 返回较好的那个
if [[ -n "$jina_result" ]]; then
    echo "[smart-fetch] 返回 Jina 结果 (${#jina_result} 字符)" >&2
    echo "$jina_result"
    exit 0
fi

if [[ -n "$raw_result" ]]; then
    echo "[smart-fetch] 返回 curl 结果 (${#raw_result} 字符)" >&2
    echo "$raw_result"
    exit 0
fi

echo "[smart-fetch] 所有方式都失败: $URL" >&2
exit 1
