import os, time
from openai import OpenAI
from dotenv import load_dotenv
from kb import collection


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



"""
    SSE流式响应大模型对话
"""
def stream_chat(prompt: str):
    # 向量库检索
    results = collection.query(query_texts=[prompt], n_results=2)
    context = "\n".join(results["documents"][0])

    # 把资料和问题拼进prompt
    stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system",
                 "content": "你是公司助手。只能按照下面的参考资料回答；如果参考资料里没有相关信息，就回答‘资料中未提及"},
                {"role": "user",
                 "content": f"参考资料：\n{context}\n\n问题：{prompt}"}
            ],
            stream=True        # 关键：打开流式
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content    # 逐块取增量文本内容
        if delta:                                 # 必须判空，不然可能为None，或空或报错
            yield delta                           # 取一个往前端推一个

