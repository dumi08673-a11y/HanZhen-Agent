import streamlit as st
import time
import json
import os
import base64
from openai import OpenAI

# ==========================================
# 0. 强力初始化与重置 (核心：解决崩溃)
# ==========================================
client = OpenAI()
MEMORY_FILE = "hanzhen_memory.json"
CONFIG_FILE = "hanzhen_config.json"

# 如果你想彻底重来，运行这一版会自动帮你清理一次
# 只要点击侧边栏的重置，文件就会被物理删除
def hard_reset():
    for f in [MEMORY_FILE, CONFIG_FILE]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass
    st.session_state.clear()
    st.rerun()

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {}

config = load_config()

# ==========================================
# 1. 极致稳固的 UI 布局
# ==========================================
st.set_page_config(page_title="韩振的私密空间", page_icon="🎤", layout="centered")

# 状态初始化
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
    
    /* 聊天区上下留白，确保不被固定按钮挡住 */
    [data-testid="stMainBlockContainer"] {{
        padding-top: 70px !important;
        padding-bottom: 120px !important; 
    }}

    /* 左上角齿轮定位 */
    .gear-container {{
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 999999;
    }}
    
    /* 左下角➕号定位 */
    .plus-container {{
        position: fixed;
        bottom: 25px;
        left: 50%;
        transform: translateX(-385px);
        z-index: 999998;
    }}

    /* 按钮样式：精致圆形 */
    div[data-testid="stPopover"] button {{
        width: 42px !important;
        height: 42px !important;
        border-radius: 50% !important;
        min-width: 42px !important;
        background-color: white !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    
    /* 输入框偏移 */
    [data-testid="stChatInput"] {{
        padding-left: 55px !important;
    }}

    @media (max-width: 768px) {{
        .plus-container {{ left: 10px; transform: none; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏与设置 (弹回功能在这里)
# ==========================================
with st.sidebar:
    st.title("⚙️ 空间管理")
    if st.button("🏮 毁灭性重置 (彻底清空一切)", use_container_width=True):
        hard_reset()

    st.divider()
    st.subheader("形象装扮")
    h_up = st.file_uploader("换韩振头像", type=["png", "jpg"], key="sidebar_h")
    u_up = st.file_uploader("换你的头像", type=["png", "jpg"], key="sidebar_u")

    if h_up:
        st.session_state.hz_avatar = f"data:image/png;base64,{base64.b64encode(h_up.getvalue()).decode()}"
        with open(CONFIG_FILE, "w") as f: json.dump({"hz_avatar": st.session_state.hz_avatar}, f)
        st.rerun()

# 这一行代码会把齿轮按钮钉在左上角
st.markdown('<div class="gear-container">', unsafe_allow_html=True)
with st.popover("⚙️"):
    st.write("### 快速设置")
    if st.button("🏮 抹除记忆"): hard_reset()
    st.color_picker("背景色", key="bg_color_input")
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. 对话渲染逻辑
# ==========================================
if "messages" not in st.session_state:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: st.session_state.messages = json.load(f)
    else:
        st.session_state.messages = [{"role": "system", "content": "你现在是韩振，可爱的偶像。"}]

for m in st.session_state.messages:
    if m["role"] != "system":
        av = st.session_state.hz_avatar if m["role"] == "assistant" else st.session_state.user_avatar
        with st.chat_message(m["role"], avatar=av):
            # 处理复杂内容
            if isinstance(m["content"], list):
                for item in m["content"]:
                    if item["type"] == "text": st.write(item["text"])
            else:
                st.write(m["content"])

# ==========================================
# 4. 输入处理 (防死循环补丁)
# ==========================================
# 左下角➕号
st.markdown('<div class="plus-container">', unsafe_allow_html=True)
with st.popover("➕"):
    img_in = st.file_uploader("图片", type=["png", "jpg"], key="plus_img")
    aud_in = st.audio_input("语音", key="plus_aud")
st.markdown('</div>', unsafe_allow_html=True)

prompt = st.chat_input("宝贝，想对我说什么...")

# 防止重复处理同一段语音或图片的 ID 检查
if prompt or img_in or aud_in:
    # 构造当前动作的唯一特征
    action_key = f"{prompt}_{img_in.name if img_in else ''}_{aud_in.id if aud_in else ''}"

    if st.session_state.get("last_processed_action") != action_key:
        st.session_state.last_processed_action = action_key

        user_content = []
        if prompt: user_content.append({"type": "text", "text": prompt})
        if img_in:
            b64 = base64.b64encode(img_in.getvalue()).decode()
            user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
        if aud_in:
            with st.spinner("听取中..."):
                try:
                    txt = client.audio.transcriptions.create(model="whisper-1", file=aud_in, response_format="text")
                    user_content.append({"type": "text", "text": txt})
                except: pass

        if user_content:
            st.session_state.messages.append({"role": "user", "content": user_content})

            # AI 回复
            with st.chat_message("assistant", avatar=st.session_state.hz_avatar):
                placeholder = st.empty()
                full_reply = ""
                response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages, stream=True)
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_reply += chunk.choices[0].delta.content
                        placeholder.markdown(full_reply)

            st.session_state.messages.append({"role": "assistant", "content": full_reply})
            with open(MEMORY_FILE, "w") as f: json.dump(st.session_state.messages, f)
            st.rerun() # 发完立刻重置，清空上传组件的状态