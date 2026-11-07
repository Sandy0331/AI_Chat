import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()     # 从 .env 读 key,并加载到项目环境变量中

# 配置客户端
client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com" # DeepSeek 兼容 OpenAI 协议
)

# 定义大模型对话函数（裸模型对话）
def chat(question: str) ->str:
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
        {"role": "system", "content": "你是一个乐于助人的助手，回答简洁"},
        {"role": "user", "content": question}
        ],
        temperature=0.7)
    return resp.choices[0].message.content
