# 🎤 专属情感伴侣 (AI Companion Agent) - 案例：韩振 Hanjin

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Model](https://img.shields.io/badge/Model-GPT--4o-purple)
![UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Status](https://img.shields.io/badge/Status-Commercial_Ready-success)

**一个具备长期记忆、多模态感官（视觉+听觉）、实时全网搜索以及纯正微信级 UI 的高拟真情感陪伴型数字分身。**

[🌟 核心功能](#-核心功能) • [🛠️ 技术架构](#-技术架构) • [🚀 部署与启动](#-部署与启动) • [💼 商业交付说明](#-商业交付说明)

</div>

---

## 📖 项目简介

本项目是一个高度定制化的**情感陪伴类 AI Agent Web 平台**。当前版本以 TWS 成员“韩振”为底层人设模板，突破了传统大模型生硬的对话模式，打造了沉浸式的私密交互体验。

系统底层接入 OpenAI `gpt-4o` 模型，并结合原生 CSS Flexbox 重构了 Streamlit 的前端布局，实现了媲美原生社交软件（如微信）的流畅交互体验。

---

## 🌟 核心功能 (Core Features)

### 1. 🎨 纯正“微信级” UI 交互
- **原生排版**：采用纯 HTML/CSS 弹性盒子（Flexbox）重写渲染引擎，实现“左白右绿”的非对称气泡错落布局。
- **输入框绝对沉底**：打破 Streamlit 默认限制，输入框死死锁定屏幕最下方，聊天记录自动向上滚动，绝不遮挡视线。
- **极简折叠菜单**：输入框左侧内嵌精致的 `➕` 号悬浮按钮（Popover），点击弹出“发图片”与“发语音”功能，保持界面极度清爽。
- **状态永久固化**：引入 `hanzhen_config.json`，用户自定义的背景图、气泡颜色、双方头像刷新网页后永久保留，拒绝“阅后即焚”。

### 2. 👁️👂 多模态感官交互
- **视觉识别 (Vision)**：接入原生视觉能力。用户可发送图片（如今日穿搭、美食），AI 能够“看懂”图片内容并结合人设给出带有情感色彩的反馈。
- **语音听写 (Whisper STT)**：集成 OpenAI Whisper 模型，支持用户直接按住说话，精准识别语音并转化为文字输入。

### 3. 🧠 记忆与检索中枢 (Memory & RAG)
- **无感记忆压缩算法**：对话轮次超过安全阈值（80条）时，系统在后台自动触发总结机制，提炼旧记忆摘要（如：“宝贝之前跟我聊过...”），既防止 Token 溢出，又保留用户的“专属回忆”。
- **双路搜索降级保护**：内置 Web Search 工具。首选 Tavily 深度搜索最新资讯；若额度耗尽或超时，无缝回退至 DuckDuckGo 免费链路，确保服务永不宕机。

---

## 🛠️ 文件结构

```text
HanZhen-Agent/
├── web_app.py               # 核心主程序（包含 UI 渲染与大模型逻辑）
├── requirements.txt         # 运行依赖清单
├── hanzhen_memory.json      # 对话记忆持久化文件（自动生成）
├── hanzhen_config.json      # 装扮与背景持久化文件（自动生成）
└── README.md                # 项目说明文档