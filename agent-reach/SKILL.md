---
name: agent-reach
description: >
  Give your AI agent eyes to see the entire internet (15+ platforms).
  Search and read Twitter/X, Reddit, YouTube, GitHub, Bilibili, 小红书, 抖音, 微博,
  微信公众号, LinkedIn, V2EX, RSS, Exa web search, and any web page.
  Use when the user asks to search or read any of these platforms, shares a URL,
  searches the web, or researches a topic.
  Triggers: "搜推特", "搜小红书", "看视频", "搜一下", "上网搜", "帮我查", "全网搜索",
  "search twitter", "read tweet", "youtube transcript", "search reddit",
  "read this link", "看这个链接", "B站", "bilibili", "抖音视频",
  "微信文章", "公众号", "LinkedIn", "GitHub issue", "RSS", "微博",
  "V2EX", "v2ex", "看主题", "技术社区",
  "search online", "web search", "find information", "research",
  "帮我配", "configure", "帮我安装".
io:
  input:
    - type: text
      description: URL、搜索关键词、平台名 + 操作指令
  output:
    - type: text
      description: 平台内容（Markdown 格式）或搜索结果列表
---

# Agent Reach — 全平台搜索与阅读

> 让 AI Agent 像真人一样访问互联网 15+ 平台。

## Skill 路由（互斥边界）

| 场景 | 用哪个 skill |
|------|-------------|
| 用户分享了一个 URL，或让你"搜一下" / "看一下" | **→ agent-reach** |
| "这个领域有什么开源方案？对比一下" | → `deep-research`（会调用 agent-reach 做 Phase 2 搜索） |
| "市场有多大？投资人怎么看？" | → `market-research`（会调用 agent-reach 获取数据） |
| "有没有现成的库可以用？" | → `search-first` |
| "上传到 GitHub" | → `upload-to-github` |

## 协作接口（被其他 skill 调用时）

### 被 `deep-research` 调用

`deep-research` Phase 2（搜索阶段）应调用 agent-reach 进行多平台搜索：

```
调用方式：deep-research Phase 2 直接使用下方各渠道的命令
输入：搜索关键词 + 目标平台列表
输出：各平台的搜索结果（Markdown 格式）
```

**推荐调研搜索组合**：

| 调研需求 | 推荐渠道组合 |
|---------|-------------|
| 开源项目/技术选型 | GitHub（`gh search repos`）+ Web（Jina Reader）+ Exa 语义搜索 |
| 中文社区口碑 | V2EX + 小红书 + 微博 + 微信公众号 |
| 英文社区讨论 | Reddit + Twitter/X + YouTube |
| 全面技术调研 | 以上全部 + RSS 订阅 |

### 被 `market-research` 调用

市场调研需要获取竞品信息、用户评价、行业讨论时，调用 agent-reach 对应渠道。

### 被 `search-first` 调用

快速查找现有工具/库时，调用 GitHub 渠道（`gh search repos` / `gh search code`）。

---

## 渠道能力矩阵

> 运行 `agent-reach doctor` 查看当前各渠道实际状态。

| 渠道 | Tier | 后端工具 | 搜索 | 阅读 | 需要认证 |
|------|------|---------|------|------|---------|
| Web（任意网页） | 0 | Jina Reader + curl fallback | — | ✅ | 否 |
| GitHub | 0 | gh CLI | ✅ | ✅ | 建议 |
| YouTube | 0 | yt-dlp | ✅ | ✅（字幕） | 否 |
| B站 | 0 | yt-dlp | — | ✅（字幕） | 否 |
| V2EX | 0 | 公开 API | ✅（节点浏览） | ✅ | 否 |
| RSS | 0 | feedparser | — | ✅ | 否 |
| Exa 语义搜索 | 0 | mcporter + Exa MCP | ✅ | — | 免费 |
| Twitter/X | 1 | xreach-cli | ✅ | ✅ | 否 |
| Reddit | 1 | 公开 JSON API | ✅ | ✅ | 否（可能需代理） |
| 微博 | 1 | mcporter + mcp-server-weibo | ✅ | ✅ | 否 |
| 小宇宙播客 | 1 | Groq Whisper | — | ✅（转文字） | 免费 Key |
| 小红书 | 2 | mcporter + xiaohongshu-mcp | ✅ | ✅ | Cookie |
| 抖音 | 2 | mcporter + douyin-mcp-server | — | ✅ | 否 |
| LinkedIn | 2 | mcporter + linkedin-mcp | ✅ | ✅ | 需配置 |
| 微信公众号 | 2 | miku_ai + Camoufox | ✅ | ✅ | 否 |

**Tier 说明**：0 = 装好即用｜1 = 需安装免费工具｜2 = 需额外配置

---

## ⚠️ Workspace Rules

**永远不要在 agent workspace 里创建文件。** 临时输出用 `/tmp/`，持久数据用 `~/.agent-reach/`。

---

## 各渠道调用指南

### Web — 任意网页

**推荐：smart-fetch（自动 fallback，纯免费）**：
```bash
~/.ai-skills/agent-reach/scripts/smart-fetch.sh "URL"
```

smart-fetch 策略：
1. 先用 Jina Reader 抓取（免费，输出 Markdown）
2. 自动检查返回质量（内容长度、HTML 标签密度、JS 代码残留）
3. 质量不合格 → fallback 到直接 curl（浏览器 UA）
4. 返回质量更好的结果

**直接 curl 模式**（跳过 Jina，获取原始 HTML）：
```bash
~/.ai-skills/agent-reach/scripts/smart-fetch.sh "URL" --raw
```

**手动调用 Jina**：
```bash
curl -s "https://r.jina.ai/URL"
```

> 全部免费，无需 API Key。

### Web Search — Exa 语义搜索

```bash
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'
mcporter call 'exa.get_code_context_exa(query: "code question", tokensNum: 3000)'
```

### GitHub (gh CLI)

```bash
gh search repos "query" --sort stars --limit 10
gh repo view owner/repo
gh search code "query" --language python
gh issue list -R owner/repo --state open
gh issue view 123 -R owner/repo
```

### Twitter/X (xreach)

```bash
xreach search "query" -n 10 --json          # 搜索
xreach tweet URL_OR_ID --json                # 读推文（支持 /status/ 和 /article/）
xreach tweets @username -n 20 --json         # 用户时间线
xreach thread URL_OR_ID --json               # 完整 thread
```

### YouTube (yt-dlp)

```bash
yt-dlp --dump-json "URL"                     # 视频元数据
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"
                                             # 下载字幕，然后读 .vtt 文件
yt-dlp --dump-json "ytsearch5:query"         # 搜索
```

### Bilibili (yt-dlp)

```bash
yt-dlp --dump-json "https://www.bilibili.com/video/BVxxx"
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --convert-subs vtt --skip-download -o "/tmp/%(id)s" "URL"
```

> 服务器 IP 可能 412。用 `--cookies-from-browser chrome` 或配代理。

### Reddit

```bash
curl -s "https://www.reddit.com/r/SUBREDDIT/hot.json?limit=10" -H "User-Agent: agent-reach/1.0"
curl -s "https://www.reddit.com/search.json?q=QUERY&limit=10" -H "User-Agent: agent-reach/1.0"
```

> 服务器 IP 可能 403。通过 Exa 搜索替代，或配代理。

### 小红书 / XiaoHongShu (mcporter)

```bash
mcporter call 'xiaohongshu.search_feeds(keyword: "query")'
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy")'
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy", load_all_comments: true)'
```

> 需要登录 Cookie。用 Cookie-Editor 导入。

### 抖音 / Douyin (mcporter)

```bash
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxx/")'
mcporter call 'douyin.get_douyin_download_link(share_link: "https://v.douyin.com/xxx/")'
```

### 微信公众号 / WeChat Articles

**搜索**（miku_ai）：
```python
python3 -c "
import asyncio
from miku_ai import get_wexin_article
async def s():
    for a in await get_wexin_article('query', 5):
        print(f'{a[\"title\"]} | {a[\"url\"]}')
asyncio.run(s())
"
```

**阅读**（Camoufox — 绕过微信反 Bot）：
```bash
cd ~/.agent-reach/tools/wechat-article-for-ai && python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

> 微信文章不能用 Jina Reader 或 curl 读取，必须用 Camoufox。

### LinkedIn (mcporter)

```bash
mcporter call 'linkedin.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'
mcporter call 'linkedin.search_people(keyword: "AI engineer", limit: 10)'
```

Fallback: `curl -s "https://r.jina.ai/https://linkedin.com/in/username"`

### V2EX (公开 API)

```bash
# 热门主题
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# 节点主题（node_name 如 python、tech、jobs、qna）
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"

# 主题详情
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"

# 主题回复
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"

# 用户信息
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

Python 调用示例：

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# 热门帖子
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} 回复) {t['url']}")

# 指定节点
node_topics = ch.get_node_topics("python", limit=5)

# 帖子详情 + 回复
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])
for r in topic["replies"]:
    print(f"  {r['author']}: {r['content'][:80]}")

# 用户信息
user = ch.get_user("Livid")
print(user["username"], user["bio"], user["github"])
```

> 无需认证。V2EX 节点名见 https://www.v2ex.com/planes

### 微博 (mcporter)

```bash
mcporter call 'weibo.search(keyword: "query", count: 10)'
mcporter call 'weibo.get_hot_search()'
```

> 需要 mcporter + mcp-server-weibo。

### 小宇宙播客

```bash
# 下载音频后用 Groq Whisper 转文字
~/.ai-skills/agent-reach/scripts/transcribe_xiaoyuzhou.sh "EPISODE_URL"
```

> 需要 Groq API Key（免费）。配置：`agent-reach configure groq-key gsk_xxxxx`

### RSS

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

---

## 诊断与排障

```bash
agent-reach doctor              # 查看所有渠道状态
agent-reach setup                # 交互式配置更多渠道
agent-reach check-update         # 检查新版本
agent-reach watch                # 快速健康检查（适合定时任务）
```

- **某渠道不工作？** → 运行 `agent-reach doctor` 看状态和修复指引
- **Twitter 失败？** → 确保 `npm install -g undici`，配代理：`agent-reach configure proxy URL`
- **用户说"帮我配 XXX"？** → 获取安装指南：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md，用户只需提供 Cookie，其余由 Agent 完成

---

## Skill 协作关系

```
agent-reach（多平台搜索与阅读）
  │
  ├─ 被调用 ←── deep-research Phase 2     （技术调研的搜索引擎）
  ├─ 被调用 ←── market-research           （市场调研的数据源）
  ├─ 被调用 ←── search-first              （快速查找的 GitHub 搜索）
  ├─ 互补   ↔── baoyu-url-to-markdown     （agent-reach 做 URL 路由，baoyu 做深度转换）
  └─ 互补   ↔── translate                 （agent-reach 获取外文内容，translate 翻译）
```

**互斥关系**：
- `agent-reach` ↔ `upload-to-github`：读 GitHub vs 写 GitHub
