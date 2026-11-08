# 项目名称
AI Chat

## 项目简介
基于 FastAPI + Chroma 向量库 + DeepSeek 构建的 AI 应用服务，集成两大核心能力：

- **RAG 知识库问答**：文档切片向量化入库、语义检索 top-k、检索增强生成（Retrieval-Augmented Generation），支持基于企业私有资料的准确问答与可溯源，通过 system prompt 抑制幻觉
- **Agent 工具调用（Function Calling）**：大模型根据工具描述自行决策是否调用外部函数，已实现时间查询、数学计算两个示例工具，返回调用链可溯源

采用 OpenAI 兼容协议（base_url 可切换），实现模型无关架构；Pydantic 做接口入参校验，.env 管理 API Key，.gitignore 排除敏感配置。

## 功能特性
实现的接口：

| 请求方法  |  URL路径 | 处理函数  |  功能 |  技术 |
|---|---|---|---|---|
| POST  |  /chat    |  chat_api  | 裸模型对话  |  LLM API |
|  GET |  /search | search_api  | 向量语义检索| Embedding + 向量库  |
| POST   | /ask  | ask   |RAG知识库问答 |  检索增强生成 |
|  POST      |    /agent   |  agent     |   工具调用      |  Function Calling / Agent |

支持私有知识库构建   
私有知识库语义检索     
从私有知识库中语义检索资料传入大语言模型（DeekSeek）实现准确问答并反馈答复依据原文   
大模型根据工具description自行决定是否调用工具   
支持get_current_time(获取时间)、calculate（数学计算）两个实例工具  
返回tool_used列表，可溯源本次调用了哪些工具
自动生成可交互文档

## 项目结构
kb.py        --- 知识库创建             
llm.py       --- 大模型对话配置             
main.py      --- RAG知识库问答          


## 接口文档链接
http://127.0.0.1:8000/docs

## 环境要求
Python 3.12             
FastAPI（Web框架）         
ChromaDb（向量库）       
OpenAI

## 快速开始
pip install -r requirements.txt                                                     
uvicorn main:app --reload