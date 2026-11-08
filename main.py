from fastapi import FastAPI
from pydantic import BaseModel
from llm import chat, client
from fastapi.openapi.docs import get_swagger_ui_html
from kb import collection


# 创建FastAPI实例
app = FastAPI(title="Chat API")

# 定义请求体格式（Pydantic）
class ChatReq(BaseModel):
    question: str


# 创建对话请求 路由接口
@app.post("/chat")
def chat_api(req: ChatReq):     # 接收前端传过来的 JSON，并自动用ChatReq 模型进行解析和校验
    answer = chat(req.question)    # 调用AI大模型函数，传入问题，得到回复
    return {"answer": answer}

# 向 向量库collection集合提交查询请求
@app.get("/search")
def search_api(q: str, k: int=2):
    result = collection.query(
        query_texts = [q],
        n_results = k
    )
    return {"query": q, "matched": result["documents"][0]}

# 创建对话请求
# RAG 实现，用户提问后先去私有知识库（collect）中去检索语义最相近的几条资料，后把资料连同用户问题一起传给大模型，让他根据资料去回答
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

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )