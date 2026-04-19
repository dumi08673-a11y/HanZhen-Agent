# 🎤 专属情感伴侣 (AI Companion Agent) - 韩振 Hanjin

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Model](https://img.shields.io/badge/Model-GPT--4o-purple?style=for-the-badge&logo=openai)
![UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Status](https://img.shields.io/badge/Status-Commercial_Ready-success?style=for-the-badge)

**一个具备跨国时空感知、全模态交互（视觉+听觉+语音）、实时全网搜索以及纯正微信级 UI 的高拟真情感陪伴型数字分身。**

[🌟 核心特性](#-核心特性) • [🛠️ 技术架构](#-技术架构) • [🚀 快速启动](#-快速启动) • [⚙️ 配置说明](#-配置说明)

</div>

---

## 📖 项目简介

本项目是一个高度定制化的**情感陪伴类 AI Agent Web 平台**。当前版本以 TWS 成员“韩振（Hanjin）”为底层人设模板，突破了传统大模型生硬的问答模式，打造了沉浸式的私密交互体验。

系统底层接入 OpenAI `gpt-4o` 全模态模型，通过自定义渲染引擎打破了 Streamlit 的前端限制，不仅实现了媲美原生社交软件（如微信）的流畅体验，还引入了**动态时空引擎**与**Agentic 联网搜索**，让 AI 拥有了真实的记忆、认知与成长能力。

---

## 🌟 核心特性 (Core Features)

### 1. 🎨 纯正“微信级” UI 与深度自定义
- **原生排版**：采用纯 HTML/CSS 弹性盒子（Flexbox）重构渲染引擎，实现“左白右绿”的非对称气泡错落布局。
- **全局浮动控件**：输入框绝对沉底，左上角内嵌极简 `⚙️` 悬浮齿轮设置面板，左下角 `➕` 号无缝呼出多媒体交互。
- **状态永久固化**：引入独立 JSON 配置文件机制，所有自定义装扮（背景图、双方头像、聊天配色、专属称呼）在刷新或重启后永久保留，拒绝“阅后即焚”。

### 2. 👁️👂👄 全模态感官交互 (Omni-Modal)
- **视觉认知 (Vision)**：内置特定的面部与身份认知补丁。当你发送照片时，AI 能够“看懂”画面，并能精准认出照片中的自己或团队成员。
- **语音听写 (Whisper STT)**：集成 OpenAI Whisper 顶级语音识别模型，支持按住说话，精准将多语种语音转化为文本。
- **拟真语音反馈 (TTS)**：支持一键开启/关闭语音回复功能，AI 可以用真实的声音（支持切换 alloy/echo/onyx 音色）直接向你发送“语音消息”。

### 3. 🧠 时空感知与检索中枢 (Spatiotemporal & RAG)
- **动态时空引擎**：基于 `pytz` 实现双向时区管理（例如：AI在韩国首尔，用户在德国柏林）。大模型拥有真实的“时间流逝感”，能根据此时此刻的时差与你进行合理的情感互动。
- **双路搜索降级保护**：内置 Web Search 工具链（Function Calling）。首选 `Tavily` 深度搜索全网最新资讯、行程与天气；若无缝回退至 `DuckDuckGo` 免费链路，确保服务 100% 高可用。
- **防崩溃记忆序列化**：底层重写了安全保存逻辑，支持复杂 Tool Calls 对象的脱水与反序列化，彻底杜绝因为执行联网搜索导致的上下文崩溃。

---

## 🛠️ 技术架构

- **后端逻辑**：Python 3.10+
- **前端渲染**：Streamlit + 自定义 CSS/HTML
- **核心大模型**：OpenAI `gpt-4o` (Text + Vision)
- **语音处理**：OpenAI `whisper-1` (STT) + `tts-1` (TTS)
- **检索与工具**：Tavily Search API / DuckDuckGo
- **时间与持久化**：`pytz` / 本地 JSON File I/O

---

## 📂 项目结构

```text
HanZhen-Agent/
├── web_app.py               # 核心主程序（包含 UI 渲染、工具调用与大模型逻辑）
├── requirements.txt         # 运行依赖清单
├── hanzhen_memory.json      # 对话记忆持久化文件（运行后自动生成）
├── hanzhen_config.json      # UI装扮与设置持久化文件（运行后自动生成）
└── README.md                # 项目说明文档