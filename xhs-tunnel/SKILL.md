---
name: xhs-tunnel
description: 利用 Cloudflare Tunnel 将本地 Web 开发服务器映射到临时公网 URL，用于移动端预览与测试。Use when the user asks for a temporary public preview link, mobile-device testing, or external access to a local web app.
---

# xhs-tunnel

## 描述
利用 Cloudflare Tunnel 将本地 Web 开发服务器映射到临时公网 URL，用于移动端预览与测试。

## 用法
```bash
python3 ~/.openclaw/skills/shared/xhs-tunnel/scripts/run_tunnel.py --port 5176
```

## 功能
- 自动检测并启动 Cloudflare Tunnel
- 输出供外部访问的 `trycloudflare.com` URL
- 监控隧道状态，防止无故中断

## 触发场景
- 当用户询问“生成预览链接”、“手机预览”、“公网访问”时触发。
