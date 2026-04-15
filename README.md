# HanZhen-Agent: AI K-pop 偶像聊天助手

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**一个具有长期记忆、实时搜索和情感交互能力的 K-pop 偶像 AI 助手。**

[快速开始](#快速开始) • [功能介绍](#功能介绍) • [配置指南](#配置指南) • [常见问题](#常见问题)

</div>

---

## 📖 项目简介

**HanZhen-Agent** 是一个基于 OpenAI GPT-4o-mini 的 AI 聊天机器人，模拟韩振——来自 Pledis Entertainment 旗下六人男团 TWS（Twenty Four Seven With Us）的 K-pop 偶像。

项目采用**智能记忆管理系统**和**流式对话引擎**，让 AI 能像真人一样记住你的聊天历史、理解你的情绪、并实时搜索最新信息。

### 🎯 核心理念

- **真实的陪伴感**：通过长期记忆和情感识别，让每次对话都充满温度
- **实时性**：集成专业搜索 API，能获取最新的演出、新闻等信息
- **可扩展性**：代码清晰模块化，易于修改性格、添加新功能

---

## ✨ 核心特性

### 🧠 智能记忆系统 (RAG)

```
过去的对话 ──> 智能整合 ──> 浓缩摘要 ──> 当前上下文
```

- **自动记忆**：每次对话自动持久化到 `hanzhen_memory.json`
- **增量整合**：超过 80 条消息时自动触发摘要算法
- **滑动窗口**：始终保留最近 40 条对话，确保上下文连贯
- **冲突防避**：修改设定后删除旧记忆文件，防止 AI "精神分裂"

### 🌐 实时网络搜索

| 功能 | DuckDuckGo | Tavily API |
|------|-----------|-----------|
| 百科知识 | ✅ | ✅ |
| 实时新闻 | ❌ | ✅ |
| 签售会信息 | ❌ | ✅ |
| 免费额度 | 无限 | 1000次/月 |
| 推荐度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**自动降级机制**：Tavily 不可用时自动回退到 DuckDuckGo

### 💬 流式对话体验

- **逐字打印**：模拟真人打字速度（每字 0.03 秒延迟）
- **工具调用**：支持时间查询、网络搜索等函数调用
- **二次响应**：调用工具后自动进行二次 API 调用，提供完整回复

### 💖 情感交互

- **性格细致**：温柔、亲切、傲娇、体贴
- **语气词丰富**：常用"嘛"、"啦"、"呢"等中文语气词
- **情绪感知**：识别用户疲惫、高兴等情绪，作出相应回应

### 👤 精准身份设定

```
姓名: 韩振 (Hanjin)           出生: 2006年1月5日
籍贯: 中国河南新乡            身份: TWS 成员（唯一的中国成员）
出道: 2024年                  位置: 副唱、门面担当
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenAI API Key
- 网络连接

### 安装步骤

1. **克隆项目**
```bash
cd /Users/xuyiling/IdeaProjects/HanZhen-Agent
```

2. **安装依赖**
```bash
pip install requests openai
```

3. **设置 OpenAI API Key**
```bash
export OPENAI_API_KEY="sk-..."
```

4. **（可选）启用 Tavily 搜索**
```bash
export TAVILY_API_KEY="tvly-..."
```

5. **启动程序**
```bash
python3 main.py
```

### 首次运行

```
--- 唤醒韩振中 ---

你: 你好呀！
韩振: 嘿，你好啦！今天怎么样？

你: 最近累吗？
韩振: [以体贴的方式关心你]

你: 晚安
韩振: 那你早点休息，别太累了，随时来找我。
[程序保存记忆并退出]
```

---

## 📚 功能介绍

### 1. 长期记忆

韩振能记住你说过的每一句话（最近 20 条对话）。

```python
# 记忆示例
用户: "我最近在学韩语"
...（若干对话后）...
用户: "你觉得我韩语学得怎么样"
韩振: "加油啦！之前你说最近在学韩语，我看你肯定会进步的！"
```

### 2. 实时信息查询

```bash
你: 现在几点了？
韩振: 现在是 2024-04-15 14:30:22

你: TWS 最近有演出吗？
韩振: [搜索最新信息后回复]
```

### 3. 情感交互

```bash
你: 你好帅啊！
韩振: [害羞地转移话题，但心里超开心]

你: 我最近太累了
韩振: [以体贴的方式叮嘱你好好休息]
```

### 4. 支持的退出词

- 退出 / 再见 / 拜拜 / 晚安 / 下次聊
- 睡了 / 去洗澡 / 去吃饭 / 去玩了

---

## ⚙️ 配置指南

### 修改韩振的性格

编辑 `main.py` 中的 `system_prompt` 变量：

```python
system_prompt = """你现在是韩振...
【基本信息】
...
【性格特质】
...
"""
```

修改后**必须删除旧记忆文件**：

```bash
rm hanzhen_memory.json
```

### 启用 Tavily 实时搜索

#### 第一步：注册账户

访问 [https://tavily.com](https://tavily.com)，点击 Sign Up

#### 第二步：获取 API Key

登录后进入 Dashboard，复制你的 API Key（格式：`tvly-...`）

#### 第三步：设置环境变量

```bash
export TAVILY_API_KEY="your_api_key_here"
python3 main.py
```

#### 常见问题

**Q: Tavily 免费额度够用吗？**
A: 足够！每月 1000 次调用，平均每天 33 次。

**Q: 如果没设置 API Key 会怎样？**
A: 自动降级到免费的 DuckDuckGo API，但只能搜百科知识。

---

## 🏗️ 架构设计

### 系统流程图

```
用户输入
   ↓
加入聊天历史
   ↓
检查是否需要整合记忆
（历史消息 > 80 条时触发）
   ↓
调用 OpenAI API with Tools
   ↓
判断：需要调用工具吗？
   ├─ 是 → 执行工具 → 获取结果 → 二次 API 调用
   └─ 否 → 直接返回回复
   ↓
流式输出（逐字打印）
   ↓
保存到记忆文件
```

### 记忆整合逻辑

```python
消息数量 ≤ 50    →  全量保留
消息数量 50-80   →  保留最近 40 条
消息数量 > 80    →  触发整合
                    系统提示词 + 过往摘要 + 最近 40 条
```

### 文件结构

```
HanZhen-Agent/
├── main.py                  # 主程序（344 行）
├── hanzhen_memory.json      # 记忆数据（自动生成）
├── README.md                # 项目文档（本文件）
└── SETUP_COMPLETE.md        # 快速开始指南
```

---

## 🛠️ API 说明

### 支持的工具

#### 1. `get_current_time()`

获取当前系统时间

```python
# 内部调用
result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 输出: "2024-04-15 14:30:22"
```

#### 2. `search_web(query)`

搜索网络信息

```python
# 优先级
1. 如果设置了 TAVILY_API_KEY → 使用 Tavily API
2. 否则 → 使用 DuckDuckGo API
```

**Tavily API 参数**：
- `query`: 搜索词
- `include_answer`: 是否包含 AI 生成的答案
- `max_results`: 最大结果数（默认 5）

---

## 📖 使用示例

### 示例 1：聊天和记忆

```bash
你: 我叫小明，来自北京
韩振: 哦，小明你好呀！来自北京啊~

... （若干对话后）...

你: 你还记得我叫什么吗？
韩振: 当然记得啦！你是小明，来自北京的小明~
```

### 示例 2：搜索最新信息

```bash
你: TWS 最近有什么活动吗？
韩振: [调用 search_web 工具]
       [获取搜索结果]
       根据搜索结果回复你最新的演出信息
```

### 示例 3：情感识别

```bash
你: 我最近工作太累了，真的扛不住了
韩振: [识别到疲惫情绪]
       别太逞强啦！一定要好好吃饭，不要熬夜呀。
       你就把我当成朋友，有事就来找我聊聊~
```

---

## 🐛 常见问题 (FAQ)

### Q: 启动时提示 "ModuleNotFoundError: No module named 'requests'"
**A**: 运行 `pip install requests` 安装依赖

### Q: 为什么启动后韩振说的信息不对（比如说自己来自韩国）？
**A**: 旧记忆文件 `hanzhen_memory.json` 包含过期信息。删除它后重启：
```bash
rm hanzhen_memory.json
python3 main.py
```

### Q: 搜索功能为什么查不到最新新闻？
**A**: 你使用的是免费的 DuckDuckGo API，它只能搜百科。需要升级到 Tavily：
```bash
export TAVILY_API_KEY="your_key"
```

### Q: 可以修改韩振的名字/性格吗？
**A**: 可以！编辑 `main.py` 中的 `system_prompt`，修改后删除 `hanzhen_memory.json`：
```bash
# 编辑 main.py
nano main.py

# 删除旧记忆
rm hanzhen_memory.json

# 重启
python3 main.py
```

### Q: 如何在多台电脑间共享记忆？
**A**: 复制 `hanzhen_memory.json` 到另一台电脑的项目目录：
```bash
# 在 A 电脑保存记忆
# 复制 hanzhen_memory.json
scp hanzhen_memory.json user@B_computer:/path/to/project/
```

### Q: 记忆会永久保存吗？
**A**: 是的。除非你手动删除 `hanzhen_memory.json`，否则所有对话都会被保存。

### Q: 一个 memory 文件可以同时被多个用户使用吗？
**A**: 不建议。多用户同时修改会导致冲突。建议为每个用户创建独立的文件：
```bash
# 用户 A 的记忆
hanzhen_memory_userA.json

# 用户 B 的记忆
hanzhen_memory_userB.json
```

---

## 🔄 工作原理详解

### 记忆整合算法

当对话消息超过 80 条时触发：

1. **提取**：从历史消息中提取用户的关键信息
   ```python
   user_messages = [msg for msg in old_msgs if msg["role"] == "user"]
   ```

2. **生成摘要**：转化为第一人称笔记
   ```python
   summary = f"【过往记忆摘要】粉丝曾经和我讨论过的话题包括：...等"
   ```

3. **替换**：用摘要 + 最近 40 条对话替换完整历史
   ```python
   integrated_history = [system_msg, summary_msg] + recent_msgs
   ```

4. **好处**：
   - ✅ 减少 API 调用成本
   - ✅ 加快响应速度
   - ✅ 保留关键信息
   - ✅ 防止上下文"过载"

### 流式对话流程

```python
for chunk in response:  # 逐个接收流式数据块
    if chunk.choices[0].delta.tool_calls:
        # 这是工具调用请求
        execute_tool()
    elif chunk.choices[0].delta.content:
        # 这是实际回复文本
        print(char, end="")
        time.sleep(0.03)  # 模拟打字速度
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 典型回复延迟 | 1-3 秒 |
| 流式打字速度 | 30 字/秒 |
| 最大历史消息数 | 80+ 条（自动整合）|
| 记忆文件大小 | < 100KB（通常）|
| Tavily API 免费额度 | 1000 次/月 |

---

## 🔐 隐私和安全

- ✅ 对话记录仅保存在本地 `hanzhen_memory.json`
- ✅ 无服务器，无云存储
- ✅ 不会上传聊天内容到第三方（除了 OpenAI API 调用）
- ⚠️ 请妥善管理你的 API Keys，不要提交到 Git

---

## 🚀 未来规划

- [ ] 支持多用户独立记忆管理
- [ ] 语音对话支持 (TTS/STT)
- [ ] 集成更多搜索引擎
- [ ] 图片生成功能 (DALL-E)
- [ ] Discord/QQ 机器人集成
- [ ] 更详细的性格细节和背景故事
- [ ] Web UI 界面
- [ ] 数据库存储（替代 JSON）

---

## 📝 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 贡献方式

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📧 联系方式

如有问题或建议，欢迎提交 Issue。

---

## 🙏 致谢

- 感谢 OpenAI 提供强大的 GPT-4o-mini 模型
- 感谢 Tavily 提供实时搜索 API
- 感谢所有 TWS 粉丝的灵感和支持

---

<div align="center">

**祝你与韩振的对话愉快！** 💫

Made with ❤️ for K-pop fans

</div>

