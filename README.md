# HanZhen-Agent: AI K-pop Idol Chat Assistant

**An AI chat assistant of a K-pop idol featuring long-term memory, real-time search, and emotional interaction capabilities.**

[Quick Start](https://www.google.com/search?q=%23quick-start) • [Features](https://www.google.com/search?q=%23features) • [Configuration](https://www.google.com/search?q=%23configuration) • [FAQ](https://www.google.com/search?q=%23faq)

---

## 📖 Project Introduction

**HanZhen-Agent** is an AI chatbot based on OpenAI GPT-4o-mini, simulating Hanjin—a K-pop idol from the six-member boy group TWS (Twenty Four Seven With Us) under Pledis Entertainment.

The project utilizes a **Smart Memory Management System** and a **Streaming Conversation Engine**, allowing the AI to remember your chat history, understand your emotions, and search for the latest information in real-time, just like a real person.

### 🎯 Core Concepts

* **Authentic Companionship**: Brings warmth to every conversation through long-term memory and emotion recognition.
* **Real-Time Responsiveness**: Integrates professional search APIs to fetch the latest performances, news, and more.
* **Extensibility**: Clean, modular code that is easy to modify for different personas or to add new features.

---

## ✨ Core Features

### 🧠 Smart Memory System (RAG)

```
Past Conversations ──> Smart Integration ──> Condensed Summary ──> Current Context

```

* **Auto-Memory**: Every conversation is automatically persisted to `hanzhen_memory.json`.
* **Incremental Integration**: Automatically triggers a summarization algorithm when messages exceed 80.
* **Sliding Window**: Always retains the latest 40 messages to ensure contextual coherence.
* **Conflict Avoidance**: Prevents AI "schizophrenia" by requiring the deletion of old memory files when persona settings are changed.

### 🌐 Real-Time Web Search

| Feature | DuckDuckGo | Tavily API |
| --- | --- | --- |
| Wiki Knowledge | ✅ | ✅ |
| Real-Time News | ❌ | ✅ |
| Fansign Info | ❌ | ✅ |
| Free Quota | Unlimited | 1000 requests/month |
| Recommendation | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**Auto-Downgrade Mechanism**: Automatically falls back to DuckDuckGo if Tavily is unavailable.

### 💬 Streaming Conversation Experience

* **Typewriter Effect**: Simulates human typing speed (0.03s delay per character).
* **Tool Calling**: Supports function calls like time queries and web searches.
* **Secondary Response**: Automatically makes a secondary API call after tool execution to provide a complete, well-rounded response.

### 💖 Emotional Interaction

* **Detailed Persona**: Gentle, friendly, slightly tsundere, and caring.
* **Rich Modal Particles**: Frequently uses Chinese conversational particles to sound natural and lively.
* **Emotion Perception**: Recognizes user emotions (e.g., exhaustion, joy) and responds accordingly.

### 👤 Precise Identity Setting

```
Name: Hanjin (韩振)            Birth: Jan 5, 2006
Hometown: Xinxiang, Henan      Identity: TWS Member (The only Chinese member)
Debut: 2024                    Position: Sub-vocalist, Visual

```

---

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* OpenAI API Key
* Internet Connection

### Installation Steps

1. **Clone the Project**
```bash

```



cd /Users/xuyiling/IdeaProjects/HanZhen-Agent

```

2.  **Install Dependencies**
    ```bash
pip install requests openai

```

3. **Set OpenAI API Key**
```bash

```



export OPENAI_API_KEY="sk-..."

```

4.  **(Optional) Enable Tavily Search**
    ```bash
export TAVILY_API_KEY="tvly-..."

```

5. **Run the Application**
```bash

```



python3 main.py

```

### First Run


```

--- Waking up Hanjin ---

You: Hello!
Hanjin: Hey, hello there! How are you doing today?

You: Are you tired lately?
Hanjin: [Cares for you in a considerate way]

You: Goodnight
Hanjin: Go to bed early then, don't overwork yourself. Come find me anytime.
[Program saves memory and exits]

```

---

## 📚 Features

### 1. Long-Term Memory

Hanjin can remember everything you've said (up to the last 20 conversational turns).

```python
# Memory Example
User: "I've been learning Korean recently."
... (Several conversations later) ...
User: "How do you think my Korean is doing?"
Hanjin: "You can do it! You mentioned before that you were studying Korean, I'm sure you'll make great progress!"

```

### 2. Real-Time Information Query

```bash
User: What time is it now?
Hanjin: It is currently 2024-04-15 14:30:22.

User: Does TWS have any performances recently?
Hanjin: [Replies with the latest performance info after searching the web]

```

### 3. Emotional Interaction

```bash
User: You are so handsome!
Hanjin: [Shyly changes the subject, but is secretly thrilled]

User: I am so exhausted lately.
Hanjin: [Expresses caring concern and reminds you to rest well]

```

### 4. Supported Exit Commands

* Exit / Goodbye / Bye / Goodnight / Talk later
* Going to sleep / Going to shower / Going to eat / Going to play

---

## ⚙️ Configuration Guide

### Modifying Hanjin's Persona

Edit the `system_prompt` variable in `main.py`:

```python
system_prompt = """You are now Hanjin...
【Basic Info】
...
【Personality Traits】
...
"""

```

**You MUST delete the old memory file** after making changes:

```bash
rm hanzhen_memory.json

```

### Enabling Tavily Real-Time Search

#### Step 1: Register an Account

Visit [https://tavily.com](https://tavily.com) and click Sign Up.

#### Step 2: Get API Key

After logging in, go to the Dashboard and copy your API Key (Format: `tvly-...`).

#### Step 3: Set Environment Variable

```bash
export TAVILY_API_KEY="your_api_key_here"
python3 main.py

```

#### FAQ

**Q: Is the free Tavily quota enough?**
A: Yes! You get 1,000 free requests per month, averaging about 33 searches a day.

**Q: What happens if I don't set the API Key?**
A: It will automatically downgrade to the free DuckDuckGo API, which is mostly limited to Wiki knowledge searches.

---

## 🏗️ Architecture Design

### System Flowchart

```
User Input
   ↓
Append to Chat History
   ↓
Check if Memory Integration is needed
(Triggered when history > 80 messages)
   ↓
Call OpenAI API with Tools
   ↓
Decision: Is a tool call required?
   ├─ Yes → Execute Tool → Get Result → Secondary API Call
   └─ No → Return Response Directly
   ↓
Streaming Output (Typewriter effect)
   ↓
Save to Memory File

```

### Memory Integration Logic

```python
Messages ≤ 50    →  Retain all
Messages 50-80   →  Retain latest 40
Messages > 80    →  Trigger integration
                    System Prompt + Past Summary + Latest 40 messages

```

### File Structure

```
HanZhen-Agent/
├── main.py                  # Main script (344 lines)
├── hanzhen_memory.json      # Memory data (auto-generated)
├── README.md                # Project documentation (this file)
└── SETUP_COMPLETE.md        # Quick Start Guide

```

---

## 🛠️ API Description

### Supported Tools

#### 1. `get_current_time()`

Fetches the current system time.

```python
# Internal call
result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Output: "2024-04-15 14:30:22"

```

#### 2. `search_web(query)`

Searches for information on the web.

```python
# Priority Rules
1. If TAVILY_API_KEY is set → Use Tavily API
2. Otherwise → Use DuckDuckGo API

```

**Tavily API Parameters**:

* `query`: The search term.
* `include_answer`: Whether to include an AI-generated answer.
* `max_results`: Maximum number of results to return (Default: 5).

---

## 📖 Usage Examples

### Example 1: Chat and Memory

```bash
User: I am Xiaoming, from Beijing.
Hanjin: Oh, hello Xiaoming! From Beijing, huh~

... (Several conversations later) ...

User: Do you still remember my name?
Hanjin: Of course I do! You're Xiaoming, the Xiaoming from Beijing~

```

### Example 2: Searching for the Latest Info

```bash
User: Does TWS have any activities recently?
Hanjin: [Calls search_web tool]
        [Retrieves search results]
        Replies with the latest performance information based on the results.

```

### Example 3: Emotion Recognition

```bash
User: I've been working so hard lately, I really can't take it anymore.
Hanjin: [Recognizes the exhausted emotion]
        Don't push yourself too hard! Make sure to eat well and don't stay up late.
        Just treat me as a friend, come talk to me whenever you need to~

```

---

## 🐛 Frequently Asked Questions (FAQ)

### Q: Getting "ModuleNotFoundError: No module named 'requests'" on startup.

**A**: Run `pip install requests` to install the required dependency.

### Q: Why does Hanjin give wrong info after starting up (like saying he's from Korea)?

**A**: The old `hanzhen_memory.json` contains outdated information. Delete it and restart:

```bash
rm hanzhen_memory.json
python3 main.py

```

### Q: Why can't the search function find the latest news?

**A**: You are using the free DuckDuckGo API, which is primarily limited to Wiki articles. You need to upgrade to Tavily:

```bash
export TAVILY_API_KEY="your_key"

```

### Q: Can I change Hanjin's name/personality?

**A**: Yes! Edit `system_prompt` in `main.py`, and delete `hanzhen_memory.json` after making the changes:

```bash
# Edit main.py
nano main.py

# Delete old memory
rm hanzhen_memory.json

# Restart
python3 main.py

```

### Q: How do I share memories between different computers?

**A**: Copy `hanzhen_memory.json` to the project directory on the other computer:

```bash
# Save memory on Computer A
# Copy hanzhen_memory.json
scp hanzhen_memory.json user@Computer_B:/path/to/project/

```

### Q: Is the memory saved permanently?

**A**: Yes. Unless you manually delete `hanzhen_memory.json`, all conversations will be saved.

### Q: Can one memory file be used by multiple users simultaneously?

**A**: Not recommended. Concurrent modifications will cause conflicts. It is advised to create a separate file for each user:

```bash
# User A's memory
hanzhen_memory_userA.json

# User B's memory
hanzhen_memory_userB.json

```

---

## 🔄 Deep Dive: How It Works

### Memory Integration Algorithm

Triggered when conversational messages exceed 80:

1. **Extract**: Extracts key information from the user's historical messages.
```python

```



user_messages = [msg for msg in old_msgs if msg["role"] == "user"]

```

2.  **Generate Summary**: Transforms insights into first-person notes.
    ```python
summary = f"【Past Memory Summary】Topics the fan discussed with me include: ... etc."

```

3. **Replace**: Replaces the full history with the summary + the latest 40 messages.
```python

```



integrated_history = [system_msg, summary_msg] + recent_msgs

```

4.  **Benefits**:
    *   ✅ Reduces API call costs
    *   ✅ Speeds up response times
    *   ✅ Retains crucial information
    *   ✅ Prevents context "overload"

### Streaming Conversation Flow

```python
for chunk in response:  # Receive streaming data chunks one by one
    if chunk.choices[0].delta.tool_calls:
        # This is a tool call request
        execute_tool()
    elif chunk.choices[0].delta.content:
        # This is actual response text
        print(char, end="")
        time.sleep(0.03)  # Simulate typing speed

```

---

## 📊 Performance Metrics

| Metric | Value |
| --- | --- |
| Typical Response Latency | 1-3 seconds |
| Streaming Typing Speed | 30 chars/second |
| Max History Messages | 80+ (Auto-integration) |
| Memory File Size | < 100KB (Typically) |
| Tavily API Free Quota | 1000 requests/month |

---

## 🔐 Privacy and Security

* ✅ Chat records are ONLY saved locally in `hanzhen_memory.json`.
* ✅ No server, no cloud storage.
* ✅ Chat content is never uploaded to third parties (except for the OpenAI API call).
* ⚠️ Please manage your API Keys securely and do NOT commit them to Git.

---

## 🚀 Future Roadmap

* [ ] Support independent memory management for multiple users
* [ ] Voice conversation support (TTS/STT)
* [ ] Integrate more search engines
* [ ] Image generation features (DALL-E)
* [ ] Discord/QQ bot integration
* [ ] More detailed personality traits and background lore
* [ ] Web UI interface
* [ ] Database storage (Replacing JSON)

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

### How to Contribute

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

If you have any questions or suggestions, please feel free to open an Issue.

---

## 🙏 Acknowledgements

* Thanks to OpenAI for providing the powerful GPT-4o-mini model.
* Thanks to Tavily for the real-time search API.
* Thanks to all TWS fans for the inspiration and support.

---

**Enjoy your conversations with Hanjin!** 💫

Made with ❤️ for K-pop fans
