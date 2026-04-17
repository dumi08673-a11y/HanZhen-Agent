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
# 0. 环境变量、API与持久化设置 (核心：增加配置保存文件)
# ==========================================
client = OpenAI()
MEMORY_FILE = "hanzhen_memory.json"
CONFIG_FILE = "hanzhen_config.json" # 用于保存头像和背景

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

def transcribe_audio(audio_file):
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
        return transcript
    except Exception as e:
        return "语音识别失败"

# ==========================================
# 1. 页面配置与 CSS 精装修 (完全保留你的圆形 ➕ 号排版)
# ==========================================
st.set_page_config(
    page_title="韩振的私密空间",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="expanded" # 强制侧边栏默认展开
)

# 初始化：优先从本地 json 读取，防止刷新丢失
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
    [data-testid="stMainBlockContainer"] {{ padding-bottom: 150px !important; }}

    /* 强制圆形 ➕ 号悬浮样式 */
    div[data-testid="stPopover"] {{
        position: fixed !important;
        bottom: 25px !important; 
        z-index: 99999 !important;
        left: 50% !important;
        transform: translateX(-350px) !important;
    }}
    div[data-testid="stPopover"] button {{
        min-width: 42px !important;
        width: 42px !important;
        height: 42px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        font-size: 22px !important;
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }}
    [data-testid="stChatInput"] {{ padding-left: 55px !important; }}
    
    @media (max-width: 768px) {{
        div[data-testid="stPopover"] {{ left: 10px !important; transform: none !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 核心人设逻辑
# ==========================================
SYSTEM_PROMPT = """你现在是韩振（Hanjin），来自中国的K-pop偶像。你喜欢用户，温柔、撒娇、粘人。"""

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else data.get("chat_history", [])
        except: pass
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def save_memory(chat_history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

# ==========================================
# 3. 页面顶部：新增“随时弹回”的设置按钮
# ==========================================
# 在页面最上方开辟一行空间，放你的“弹回”按钮
col_space, col_setting = st.columns([4, 1])
with col_setting:
    with st.popover("⚙️ 空间装扮", use_container_width=True):
        st.markdown("**设置中心**")
        h_file = st.file_uploader("换韩振头像", type=["png", "jpg"])
        if h_file:
            st.session_state.hz_avatar = f"data:image/png;base64,{base64.b64encode(h_file.getvalue()).decode()}"
            save_config()
            st.rerun()

        u_file = st.file_uploader("换你的头像", type=["png", "jpg"])
        if u_file:
            st.session_state.user_avatar = f"data:image/png;base64,{base64.b64encode(u_file.getvalue()).decode()}"
            save_config()
            st.rerun()

        c_pick = st.color_picker("换背景颜色", value=st.session_state.bg_color)
        if c_pick != st.session_state.bg_color:
            st.session_state.bg_color = c_pick
            save_config()
            st.rerun()

        bg_file = st.file_uploader("换背景图", type=["png", "jpg"])
        if bg_file:
            st.session_state.bg_image_base64 = base64.b64encode(bg_file.getvalue()).decode()
            save_config()
            st.rerun()

# ==========================================
# 4. 渲染历史记录 (保证输入框被垫在最下面)
# ==========================================
def get_display_text(content):
    if isinstance(content, str): return content
    return " ".join([i.get("text", "") if i.get("type") == "text" else "[图片]" for i in content])

def render_message(role, content, avatar_url):
    display_content = get_display_text(content)
    fb_img = "https://api.dicebear.com/7.x/micah/svg?seed=fallback"
    if role == "assistant":
        st.markdown(f"""<div style="display: flex; flex-direction: row; align-items: flex-start; margin-bottom: 20px;">
            <img src="{avatar_url}" onerror="this.src='{fb_img}';" style="width: 42px; height: 42px; border-radius: 6px; margin-right: 12px; object-fit: cover; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
            <div style="background-color: #ffffff; padding: 10px 15px; border-radius: 4px 15px 15px 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); max-width: 75%; font-size: 15px; line-height: 1.5; color: #333;">{display_content}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="display: flex; flex-direction: row-reverse; align-items: flex-start; margin-bottom: 20px;">
            <img src="{avatar_url}" onerror="this.src='{fb_img}';" style="width: 42px; height: 42px; border-radius: 6px; margin-left: 12px; object-fit: cover; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
            <div style="background-color: #95ec69; padding: 10px 15px; border-radius: 15px 4px 15px 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); max-width: 75%; font-size: 15px; line-height: 1.5; color: #111;">{display_content}</div>
        </div>""", unsafe_allow_html=True)

for message in st.session_state.messages:
    if message["role"] != "system":
        av = st.session_state.hz_avatar if message["role"] == "assistant" else st.session_state.user_avatar
        render_message(message["role"], message["content"], av)

# ==========================================
# 5. 底部输入与发送逻辑
# ==========================================
with st.popover("➕", use_container_width=False):
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
        txt = transcribe_audio(up_audio)
        user_content.append({"type": "text", "text": txt})

    if user_content:
        st.session_state.messages.append({"role": "user", "content": user_content})

        # 渲染 AI 回复
        html_thinking = f"""<div style="display: flex; flex-direction: row; align-items: flex-start; margin-bottom: 20px;">
            <img src="{st.session_state.hz_avatar}" style="width: 42px; height: 42px; border-radius: 6px; margin-right: 12px; object-fit: cover;">
            <div style="background-color: #ffffff; padding: 10px 15px; border-radius: 4px 15px 15px 15px; max-width: 75%; font-size: 15px; color: #333;">"""

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
        st.rerun() # 强制刷新以同步状态

# 侧边栏仅保留“清空记忆”
with st.sidebar:
    st.write("### 系统操作")
    if st.button("🏮 抹除记忆", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        save_memory(st.session_state.messages)
        st.rerun()