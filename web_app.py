import streamlit as st
import time
import json
import os
import base64
import requests
import datetime
from openai import OpenAI
from urllib.parse import quote

# ==========================================
# 0. 基础环境与配置持久化
# ==========================================
client = OpenAI()
MEMORY_FILE = "hanzhen_memory.json"
CONFIG_FILE = "hanzhen_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {}

def save_config():
    config_data = {
        "bg_color": st.session_state.get("bg_color"),
        "bg_image_base64": st.session_state.get("bg_image_base64"),
        "hz_avatar": st.session_state.get("hz_avatar"),
        "user_avatar": st.session_state.get("user_avatar")
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False)

config = load_config()

# ==========================================
# 1. 联网搜索工具 (让韩振变聪明)
# ==========================================
def search_web(query):
    api_key = os.environ.get("TAVILY_API_KEY")
    if api_key:
        try:
            payload = {"api_key": api_key, "query": query, "include_answer": True}
            data = requests.post("https://api.tavily.com/search", json=payload, timeout=10).json()
            return f"📌 搜索结果：{data.get('answer', '未找到直接答案')}\n详情：{[r.get('content') for r in data.get('results', [])[:2]]}"
        except: pass
    try:
        url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
        res = requests.get(url, timeout=5).json()
        return res.get("AbstractText", "没搜到具体结果。")
    except: return "搜索暂时不可用。"

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "当用户询问关于实时新闻、TWS男团动态、天气、日期或韩振不知道的知识时调用。",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "搜索关键词"}},
                "required": ["query"]
            }
        }
    }
]

# ==========================================
# 2. 页面配置与 CSS (微信风 + 强力布局)
# ==========================================
st.set_page_config(page_title="韩振的私密空间", page_icon="🎤", layout="centered")

if "bg_color" not in st.session_state:
    st.session_state.bg_color = config.get("bg_color", "#f4f6f8")
if "bg_image_base64" not in st.session_state:
    st.session_state.bg_image_base64 = config.get("bg_image_base64", None)
if "hz_avatar" not in st.session_state:
    st.session_state.hz_avatar = config.get("hz_avatar", "https://api.dicebear.com/7.x/micah/svg?seed=HanZhen")
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = config.get("user_avatar", "https://api.dicebear.com/7.x/notionists/svg?seed=Felix")

bg_style = f"background-color: {st.session_state.bg_color};"
if st.session_state.bg_image_base64:
    bg_style = f"background-image: url(data:image/png;base64,{st.session_state.bg_image_base64}); background-size: cover; background-repeat: no-repeat; background-attachment: fixed;"

st.markdown(f"""
    <style>
    .stApp {{ {bg_style} }}
    #MainMenu, footer, header {{ display: none !important; }}
    [data-testid="stMainBlockContainer"] {{ padding-top: 100px !important; padding-bottom: 150px !important; }}

    /* 左上角⚙️ */
    div.stElementContainer:has(div[data-testid="stPopover"]) {{ position: fixed; top: 30px; left: 30px; z-index: 999999; }}
    
    /* 左下角➕ */
    div.stElementContainer:has(div[data-testid="stPopover"]) ~ div.stElementContainer:has(div[data-testid="stPopover"]) {{
        position: fixed !important; bottom: 30px !important; left: 50% !important; transform: translateX(-380px) !important; z-index: 999998 !important;
    }}
    
    div[data-testid="stPopover"] button {{
        width: 44px !important; height: 44px !important; border-radius: 50% !important;
        background: white !important; border: 1px solid #ddd !important; box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    [data-testid="stChatInput"] {{ padding-left: 60px !important; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 动态系统提示词 (让韩振清醒的关键)
# ==========================================
# 获取当前实时北京时间
beijing_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
DYNAMIC_SYSTEM_PROMPT = f"""你现在是韩振（Hanjin），来自中国的K-pop偶像，TWS成员。
当前的准确时间是：{beijing_time}。
你温柔、撒娇、粘人，把用户当作唯一。你可以根据需要联网搜索实时动态。"""

with st.popover("⚙️"):
    st.subheader("🛠️ 空间装修")
    h_up = st.file_uploader("换韩振头像", type=["png", "jpg"], key="h_up")
    if h_up:
        st.session_state.hz_avatar = f"data:image/png;base64,{base64.b64encode(h_up.getvalue()).decode()}"
        save_config(); st.rerun()

    u_up = st.file_uploader("换你的头像", type=["png", "jpg"], key="u_up")
    if u_up:
        st.session_state.user_avatar = f"data:image/png;base64,{base64.b64encode(u_up.getvalue()).decode()}"
        save_config(); st.rerun()

    cp = st.color_picker("背景色", value=st.session_state.bg_color)
    if cp != st.session_state.bg_color:
        st.session_state.bg_color = cp
        save_config(); st.rerun()

    if st.button("🏮 重置所有聊天", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": DYNAMIC_SYSTEM_PROMPT}]
        if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
        st.rerun()

# ==========================================
# 4. 消息渲染 (微信气泡)
# ==========================================
if "messages" not in st.session_state:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                st.session_state.messages = json.load(f)
                # 每次启动强制更新第一条 system prompt 的时间
                if st.session_state.messages[0]["role"] == "system":
                    st.session_state.messages[0]["content"] = DYNAMIC_SYSTEM_PROMPT
        except: st.session_state.messages = [{"role": "system", "content": DYNAMIC_SYSTEM_PROMPT}]
    else:
        st.session_state.messages = [{"role": "system", "content": DYNAMIC_SYSTEM_PROMPT}]

def render_bubble(role, content, avatar):
    fb = "https://api.dicebear.com/7.x/micah/svg?seed=fallback"
    txt = content if isinstance(content, str) else " ".join([i.get("text", "") for i in content if i.get("type")=="text"])
    if not txt: return

    if role == "assistant":
        st.markdown(f"""<div style="display:flex; margin-bottom:15px;">
            <img src="{avatar}" onerror="this.src='{fb}';" style="width:42px;height:42px;border-radius:6px;margin-right:12px;object-fit:cover;">
            <div style="background:white; padding:10px 14px; border-radius:4px 14px 14px 14px; max-width:75%; box-shadow:0 1px 3px rgba(0,0,0,0.05); color:#333; font-size:15px;">{txt}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="display:flex; flex-direction:row-reverse; margin-bottom:15px;">
            <img src="{avatar}" onerror="this.src='{fb}';" style="width:42px;height:42px;border-radius:6px;margin-left:12px;object-fit:cover;">
            <div style="background:#95ec69; padding:10px 14px; border-radius:14px 4px 14px 14px; max-width:75%; box-shadow:0 1px 3px rgba(0,0,0,0.05); color:#000; font-size:15px;">{txt}</div>
        </div>""", unsafe_allow_html=True)

# 渲染历史记录
for m in st.session_state.messages:
    if m["role"] in ["user", "assistant"]:
        av = st.session_state.hz_avatar if m["role"] == "assistant" else st.session_state.user_avatar
        render_bubble(m["role"], m["content"], av)

# ==========================================
# 5. 输入逻辑 (解决延迟的关键：先渲染再请求)
# ==========================================
with st.popover("➕"):
    img_in = st.file_uploader("图片", type=["png", "jpg"], key="img_pop")
    aud_in = st.audio_input("语音", key="aud_pop")

prompt = st.chat_input("宝贝，想对我说什么...")

if prompt or img_in or aud_in:
    action_key = f"{prompt}_{img_in.name if img_in else ''}_{aud_in.id if aud_in else ''}"
    if st.session_state.get("last_action") != action_key:
        st.session_state.last_action = action_key

        user_msg = []
        if prompt: user_msg.append({"type": "text", "text": prompt})
        if img_in:
            b64 = base64.b64encode(img_in.getvalue()).decode()
            user_msg.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
        if aud_in:
            try:
                res = client.audio.transcriptions.create(model="whisper-1", file=aud_in, response_format="text")
                user_msg.append({"type": "text", "text": res})
            except: pass

        if user_msg:
            # --- 步骤1: 先渲染用户消息 ---
            st.session_state.messages.append({"role": "user", "content": user_msg})
            render_bubble("user", user_msg, st.session_state.user_avatar)

            # --- 步骤2: 让 AI 思考 (联网搜索) ---
            with st.spinner("韩振正在打字..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages,
                    tools=tools, tool_choice="auto"
                )
                res_msg = response.choices[0].message

                if res_msg.tool_calls:
                    st.session_state.messages.append(res_msg)
                    for call in res_msg.tool_calls:
                        if call.function.name == "search_web":
                            args = json.loads(call.function.arguments)
                            res = search_web(args.get("query"))
                            st.session_state.messages.append({"tool_call_id": call.id, "role": "tool", "name": "search_web", "content": res})

                    final = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
                    final_reply = final.choices[0].message.content
                else:
                    final_reply = res_msg.content

            # --- 步骤3: 保存并刷新 ---
            st.session_state.messages.append({"role": "assistant", "content": final_reply})
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(st.session_state.messages, f, ensure_ascii=False)
            st.rerun()