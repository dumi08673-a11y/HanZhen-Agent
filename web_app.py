import streamlit as st
import time
import json
import os
import base64
from openai import OpenAI

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
# 1. 页面配置与“微信风”重装修 (CSS)
# ==========================================
st.set_page_config(page_title="韩振的私密空间", page_icon="🎤", layout="centered")

# 初始化状态 (优先从本地文件恢复，实现永久保存)
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
    
    /* 聊天区布局 */
    [data-testid="stMainBlockContainer"] {{
        padding-top: 100px !important;
        padding-bottom: 150px !important; 
    }}

    /* 左上角⚙️：固定定位 */
    div.stElementContainer:has(div[data-testid="stPopover"]) {{
        position: fixed; top: 30px; left: 30px; z-index: 999999;
    }}

    /* 左下角➕：固定定位 */
    div.stElementContainer:has(div[data-testid="stPopover"]) ~ div.stElementContainer:has(div[data-testid="stPopover"]) {{
        position: fixed !important; bottom: 30px !important; 
        left: 50% !important; transform: translateX(-380px) !important;
        z-index: 999998 !important;
    }}
    
    /* 圆形按钮样式 */
    div[data-testid="stPopover"] button {{
        width: 44px !important; height: 44px !important; border-radius: 50% !important;
        min-width: 44px !important; padding: 0 !important; background-color: white !important;
        border: 1px solid #ddd !important; box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
    }}
    
    [data-testid="stChatInput"] {{ padding-left: 60px !important; }}

    /* 手机适配 */
    @media (max-width: 768px) {{
        div.stElementContainer:has(div[data-testid="stPopover"]) ~ div.stElementContainer:has(div[data-testid="stPopover"]) {{
            left: 15px !important; transform: none !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏与设置
# ==========================================
SYSTEM_PROMPT = "你现在是韩振（Hanjin），来自中国的K-pop偶像。你喜欢用户，温柔、撒娇、粘人。"

with st.popover("⚙️"):
    st.subheader("🛠️ 空间装修")
    # 头像上传
    h_up = st.file_uploader("换韩振头像", type=["png", "jpg"], key="h_up")
    if h_up:
        st.session_state.hz_avatar = f"data:image/png;base64,{base64.b64encode(h_up.getvalue()).decode()}"
        save_config(); st.rerun()

    u_up = st.file_uploader("换你的头像", type=["png", "jpg"], key="u_up")
    if u_up:
        st.session_state.user_avatar = f"data:image/png;base64,{base64.b64encode(u_up.getvalue()).decode()}"
        save_config(); st.rerun()

    st.divider()
    # 背景定制
    cp = st.color_picker("背景颜色", value=st.session_state.bg_color)
    if cp != st.session_state.bg_color:
        st.session_state.bg_color = cp
        save_config(); st.rerun()

    bg_up = st.file_uploader("背景图", type=["png", "jpg"], key="bg_up")
    if bg_up:
        st.session_state.bg_image_base64 = base64.b64encode(bg_up.getvalue()).decode()
        save_config(); st.rerun()

    if st.button("🏮 重置所有聊天 (清空记忆)", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
        st.rerun()

# ==========================================
# 3. 消息渲染 (恢复微信气泡风格)
# ==========================================
if "messages" not in st.session_state:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                st.session_state.messages = json.load(f)
        except: st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    else:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def render_bubble(role, content, avatar):
    fb = "https://api.dicebear.com/7.x/micah/svg?seed=fallback"
    txt = ""
    if isinstance(content, list):
        for item in content:
            if item.get("type") == "text": txt += item["text"]
            if item.get("type") == "image_url": txt += " [图片内容] "
    else: txt = content

    if role == "assistant":
        st.markdown(f"""<div style="display:flex; margin-bottom:15px;">
            <img src="{avatar}" onerror="this.src='{fb}';" style="width:42px;height:42px;border-radius:6px;margin-right:12px;object-fit:cover;box-shadow:0 1px 2px rgba(0,0,0,0.1);">
            <div style="background:white; padding:10px 14px; border-radius:4px 14px 14px 14px; max-width:75%; box-shadow:0 1px 3px rgba(0,0,0,0.05); color:#333; font-size:15px; line-height:1.5;">{txt}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="display:flex; flex-direction:row-reverse; margin-bottom:15px;">
            <img src="{avatar}" onerror="this.src='{fb}';" style="width:42px;height:42px;border-radius:6px;margin-left:12px;object-fit:cover;box-shadow:0 1px 2px rgba(0,0,0,0.1);">
            <div style="background:#95ec69; padding:10px 14px; border-radius:14px 4px 14px 14px; max-width:75%; box-shadow:0 1px 3px rgba(0,0,0,0.05); color:#000; font-size:15px; line-height:1.5;">{txt}</div>
        </div>""", unsafe_allow_html=True)

for m in st.session_state.messages:
    if m["role"] != "system":
        av = st.session_state.hz_avatar if m["role"] == "assistant" else st.session_state.user_avatar
        render_bubble(m["role"], m["content"], av)

# ==========================================
# 4. 底部输入逻辑 (➕与聊天框)
# ==========================================
with st.popover("➕"):
    img_in = st.file_uploader("📷 图片", type=["png", "jpg"], key="img_pop")
    aud_in = st.audio_input("🎤 语音", key="aud_pop")

prompt = st.chat_input("宝贝，想对我说什么...")

if prompt or img_in or aud_in:
    # 唯一性校验，彻底杀死死循环
    action_token = f"{prompt}_{img_in.name if img_in else ''}_{aud_in.id if aud_in else ''}"
    if st.session_state.get("last_processed") != action_token:
        st.session_state.last_processed = action_token

        user_content = []
        if prompt: user_content.append({"type": "text", "text": prompt})
        if img_in:
            b64 = base64.b64encode(img_in.getvalue()).decode()
            user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
        if aud_in:
            with st.spinner("韩振正在听..."):
                try:
                    res_txt = client.audio.transcriptions.create(model="whisper-1", file=aud_in, response_format="text")
                    user_content.append({"type": "text", "text": res_txt})
                except: pass

        if user_content:
            st.session_state.messages.append({"role": "user", "content": user_content})

            # AI 回复流
            placeholder = st.empty()
            full_reply = ""
            response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages, stream=True)
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_reply += chunk.choices[0].delta.content
                    # 临时占位，保证回复流畅
                    placeholder.markdown(f"**韩振：** {full_reply}▌")

            st.session_state.messages.append({"role": "assistant", "content": full_reply})
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(st.session_state.messages, f, ensure_ascii=False)
            st.rerun()