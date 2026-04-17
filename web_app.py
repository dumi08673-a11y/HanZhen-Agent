import streamlit as st
import time
import datetime
import json
import os
import requests
import base64
from openai import OpenAI
from urllib.parse import quote

# ==========================================
# 0. 持久化设置与加载
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
# 1. 页面配置与 CSS 布局 (核心：左上角弹回按钮)
# ==========================================
st.set_page_config(
    page_title="韩振的私密空间",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed" # 初始缩进，靠左上角按钮呼出
)

# 初始状态加载
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
    
    /* 聊天区留白 */
    [data-testid="stMainBlockContainer"] {{ padding-bottom: 150px !important; }}

    /* === 左上角“弹回设置”按钮 CSS === */
    /* 强行把第一个 popover 移动到左上角 */
    div.stElementContainer:has(div[data-testid="stPopover"]) {{
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 999999;
    }}
    
    /* ➕号按钮 CSS：精准对齐输入框左侧 */
    div[data-testid="stChatInput"] + div div[data-testid="stPopover"],
    section[data-testid="stMain"] div[data-testid="stPopover"]:last-child {{
        position: fixed !important;
        bottom: 27px !important; 
        z-index: 99999 !important;
        left: 50% !important;
        transform: translateX(-385px) !important;
    }}
    
    /* 按钮通用圆形样式 */
    div[data-testid="stPopover"] button {{
        width: 42px !important;
        height: 42px !important;
        border-radius: 50% !important;
        min-width: 42px !important;
        padding: 0 !important;
        background-color: white !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }}
    
    [data-testid="stChatInput"] {{ padding-left: 55px !important; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 页面最上方：那个可以“弹回”的设置按钮
# ==========================================
# 这是一个特殊的 Popover，放在代码最前面，CSS 会把它挪到左上角
with st.popover("⚙️"):
    st.markdown("### 🛠️ 空间装修面板")
    st.info("在这里更换头像和背景，刷新后自动保存。")

    h_file = st.file_uploader("换韩振头像", type=["png", "jpg"])
    if h_file:
        st.session_state.hz_avatar = f"data:image/png;base64,{base64.b64encode(h_file.getvalue()).decode()}"
        save_config(); st.rerun()

    u_file = st.file_uploader("换你的头像", type=["png", "jpg"])
    if u_file:
        st.session_state.user_avatar = f"data:image/png;base64,{base64.b64encode(u_file.getvalue()).decode()}"
        save_config(); st.rerun()

    st.markdown("---")
    c_pick = st.color_picker("聊天背景颜色", value=st.session_state.bg_color)
    if c_pick != st.session_state.bg_color:
        st.session_state.bg_color = c_pick
        save_config(); st.rerun()

    bg_file = st.file_uploader("换背景图片", type=["png", "jpg"])
    if bg_file:
        st.session_state.bg_image_base64 = base64.b64encode(bg_file.getvalue()).decode()
        save_config(); st.rerun()

    if st.button("移除背景图", use_container_width=True):
        st.session_state.bg_image_base64 = None
        save_config(); st.rerun()

    st.markdown("---")
    if st.button("🏮 抹除记忆 (重新开始)", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": "你现在是韩振（Hanjin），来自中国的K-pop偶像。你喜欢用户，温柔、撒娇、粘人。"}]
        if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
        st.rerun()

# ==========================================
# 3. 聊天逻辑与消息渲染
# ==========================================
SYSTEM_PROMPT = """你现在是韩振（Hanjin），来自中国的K-pop偶像。你喜欢用户，温柔、撒娇、粘人。"""

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def save_memory(chat_history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

def render_message(role, content, avatar_url):
    fb = "https://api.dicebear.com/7.x/micah/svg?seed=fallback"
    text = ""
    if isinstance(content, list):
        for item in content:
            if item["type"] == "text": text += item["text"]
            if item["type"] == "image_url": text += " [图片内容] "
    else: text = content

    if role == "assistant":
        st.markdown(f"""<div style="display: flex; flex-direction: row; align-items: flex-start; margin-bottom: 20px;">
            <img src="{avatar_url}" onerror="this.src='{fb}';" style="width: 42px; height: 42px; border-radius: 6px; margin-right: 12px; object-fit: cover; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
            <div style="background-color: white; padding: 10px 15px; border-radius: 4px 15px 15px 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); max-width: 75%; font-size: 15px; color: #333;">{text}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="display: flex; flex-direction: row-reverse; align-items: flex-start; margin-bottom: 20px;">
            <img src="{avatar_url}" onerror="this.src='{fb}';" style="width: 42px; height: 42px; border-radius: 6px; margin-left: 12px; object-fit: cover; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
            <div style="background-color: #95ec69; padding: 10px 15px; border-radius: 15px 4px 15px 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); max-width: 75%; font-size: 15px; color: #111;">{text}</div>
        </div>""", unsafe_allow_html=True)

# 渲染对话
for message in st.session_state.messages:
    if message["role"] != "system":
        av = st.session_state.hz_avatar if message["role"] == "assistant" else st.session_state.user_avatar
        render_message(message["role"], message["content"], av)

# ==========================================
# 4. 底部输入框与 ➕ 号
# ==========================================
with st.popover("➕"):
    up_img = st.file_uploader("📷 图片", type=["png", "jpg"], label_visibility="collapsed")
    up_audio = st.audio_input("🎤 语音", label_visibility="collapsed")

prompt = st.chat_input("宝贝，对我说点什么...")

if prompt or up_img or up_audio:
    user_content = []
    if prompt: user_content.append({"type": "text", "text": prompt})
    if up_img:
        b64 = base64.b64encode(up_img.getvalue()).decode()
        user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})

    if up_audio:
        with st.spinner("韩振正在听..."):
            try:
                txt = client.audio.transcriptions.create(model="whisper-1", file=up_audio, response_format="text")
                user_content.append({"type": "text", "text": txt})
            except: pass

    if user_content:
        st.session_state.messages.append({"role": "user", "content": user_content})

        # 准备回复区
        html_thinking = f"""<div style="display: flex; flex-direction: row; align-items: flex-start; margin-bottom: 20px;">
            <img src="{st.session_state.hz_avatar}" style="width: 42px; height: 42px; border-radius: 6px; margin-right: 12px; object-fit: cover;">
            <div style="background-color: white; padding: 10px 15px; border-radius: 4px 15px 15px 15px; max-width: 75%; font-size: 15px; color: #333;">"""

        placeholder = st.empty()
        res = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages, stream=True)
        full_res = ""
        for chunk in res:
            if chunk.choices and chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                placeholder.markdown(f'{html_thinking}{full_res}▌</div></div>', unsafe_allow_html=True)

        placeholder.markdown(f'{html_thinking}{full_res}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
        save_memory(st.session_state.messages)
        st.rerun()