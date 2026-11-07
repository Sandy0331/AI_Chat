# 项目名称
AI Chat

## 项目简介
基于 FastAPI + Chroma向量库 + DeepSeek 构建的RAG知识库问答系统：                                                        
文档切片向量化入库、语义检索top-k、检索增强生成，支持基于企业私有资料的准确问答与可溯源。

## 功能特性
实现的接口：

| 请求方法  |  URL路径 | 处理函数  |  功能 |
|---|---|---|---|
| POST  |  /chat    |  chat_api  | 创建大模型对话请求  |
|  GET |  /search | search_api  | 从私有知识库中语义检索|
| POST   | /ask  | ask   | 创建支持从私有知识库中语义检索的大模型对话请求  |

支持私有知识库构建   
私有知识库语义检索     
从私有知识库中语义检索资料传入大语言模型（DeekSeek）实现准确问答并反馈答复依据原文
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