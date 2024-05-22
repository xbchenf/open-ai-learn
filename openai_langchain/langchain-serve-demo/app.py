#!/usr/bin/env python
from fastapi import FastAPI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from langserve import add_routes

##FastAPI是一个基于Python的Web框架，用于构建高性能、可扩展的API。它提供了一种简单、直观的方式来定义API端点，以及处理HTTP请求和响应。
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)
# 接口1
add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

## 接口2
system_message_prompt = SystemMessagePromptTemplate.from_template("""
    You are a helpful assistant that translates {input_language} to {output_language}.
""")
human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

add_routes(
    app,
    chat_prompt | ChatOpenAI(),
    path="/translate",
)

if __name__ == "__main__":
    import uvicorn
    ## Python的web服务器
    uvicorn.run(app, host="localhost", port=9999)