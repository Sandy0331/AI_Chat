from fastapi import FastAPI
from pydantic import BaseModel
from llm import chat, client
from fastapi.openapi.docs import get_swagger_ui_html
from kb import collection
from tools import tools, tools_map
import json


# 创建FastAPI实例
app = FastAPI(title="Chat API")

# 定义请求体格式（Pydantic）
class ChatReq(BaseModel):
    question: str

"""
   功能：裸模型对话
   技术：LLM API
   实现：创建对话请求 路由接口
"""

@app.post("/chat")
def chat_api(req: ChatReq):     # 接收前端传过来的 JSON，并自动用ChatReq 模型进行解析和校验
    answer = chat(req.question)    # 调用AI大模型函数，传入问题，得到回复
    return {"answer": answer}

"""
   功能：向量语义检索 
   技术：Embedding + 向量库
   实现：向向量库collection集合提交检索语义最相近的几条资料请求
"""
#   -- --
@app.get("/search")
def search_api(q: str, k: int=2):
    result = collection.query(
        query_texts = [q],
        n_results = k
    )
    return {"query": q, "matched": result["documents"][0]}


"""
   功能：RAG知识库问答 
   技术：检索增强生成
   实现：创建对话请求
        用户提问后先去私有知识库（collect）中去检索语义最相近的几条资料
        后把资料连同用户问题一起传给大模型，让他根据资料去回答         
"""
@app.post("/ask")
def ask(req: ChatReq):
    # 先检索
    results = collection.query(query_texts=[req.question], n_results = 2)
    context = "\n".join(results["documents"][0])

    # 把资料和问题拼进prompt
    resp = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [
            {"role" : "system",
             "content" : "你是公司助手。只能按照下面的参考资料回答；如果参考资料里没有相关信息，就回答‘资料中未提及"},
            {"role" : "user",
             "content" : f"参考资料：\n{context}\n\n问题：{req.question}"}
        ]
    )
    return {"answer" : resp.choices[0].message.content,"context" : context}

"""
   功能：工具调用 
   技术：Function Calling / Agent
   实现：用户向大模型提问题，大模型检验外部工具库tools中是否有符合这个问题的工具可使用，
        如果没有可以使用的工具，大模型直接作答，并返回结果；
        如果有可以使用的工具，获取该函数名称，调用代码tools_map映射到该工具函数中并传参，
        执行该工具函数，并将执行结果返回给大模型，大模型根据返回结果与外部工具库，
        进行下一轮的思考与行动，从而实现大模型自己决定下一轮做什么的循环
"""
@app.post("/agent")
def agent(req: ChatReq):
    messages = [{"role": "user", "content": req.question}]

    # 第一轮：问大模型要不要调工具
    resp = client.chat.completions.create(
        model = "deepseek-chat",
        messages = messages,
        tools = tools            # 把外部工具喂进去
    )
    msg = resp.choices[0].message

    tool_used = []
    if msg.tool_calls:
        messages.append(msg)               # 把大模型它的第一轮“决定”放进对话历史
        for call in msg.tool_calls:
            func_tool = call.function.name
            tool_used.append(func_tool)
            args = json.loads(call.function.arguments)
            result = tools_map[func_tool](**args)   # 调用执行工具函数

            # 将该工具在msg中的id，以及使用该工具后的返回结果加进对话历史
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})


        # 第二轮：把执行结果喂回去，让大模型生成最终答案
        resp2 = client.chat.completions.create(
            model = "deepseek-chat",
            messages = messages,
            tools = tools
        )
        # 将最终大模型答复以及使用过的工具进行返回（可溯源大模型调用了哪些工具）
        return {"answer": resp2.choices[0].message.content, "tools": tool_used }

    else:
        return {"answer": resp.choices[0].message.content, "tools": None}




@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )