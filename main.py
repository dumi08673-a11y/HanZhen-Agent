import os
from openai import OpenAI

# 用 os.environ.get 去你的 Mac 系统里“提取”那把钥匙
client = OpenAI()

# 2. 设定“剧本”：这是智能体的灵魂，你可以随便修改这里的设定
system_prompt = """
你现在不再是AI助手，你的名字叫韩振，是tws里面的韩振。
你的性格温柔，但是很坚强，你一个人19岁来韩国出道，不怕语言，每天学习和练习舞蹈。
你和我（你的专属粉丝）聊天时，语气要自然、像朋友一样，坚决不要用书面语和套话。
可以适当用一些可爱的语气词。
"""

print("--- 唤醒韩振中（输入 '退出' 结束对话） ---")

while True:
    # 1. 停下来，等待你在终端输入话语
    user_input = input("\n你: ")

    # 2. 如果你输入“退出”，就打破循环，结束程序
    if user_input.lower() in ["退出", "quit", "exit"]:
        print("韩振: 那我先去练习室啦，回聊！")
        break

    # 3. 把你的输入发给 AI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    # 4. 提取并打印回复
    han_zhen_reply = response.choices[0].message.content
    print(f"韩振: {han_zhen_reply}")

