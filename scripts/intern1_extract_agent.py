#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 14:07:51 2025

@author: nanditareddy
"""

from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.react.base import ReActAgent
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader 
from PyPDF2 import PdfReader
import os
llm = Ollama(model="llama3", request_timeout=120) 



# reader = PdfReader("invoice-samples/wordpress-sample.pdf")
# text = ""
# for i in range(len(reader.pages)):
#     page = reader.pages[i]
#     text += page.extract_text()


def validate_response(response: str) -> str:
    # You could customize this for specific validation goals
    prompt = f"Evaluate the following string for whether it is a valid date:\n\n{response}\n\nGive a brief critique and end with 'Valid' or 'Invalid'."
    return llm.complete(prompt).text.strip()

validate_tool = FunctionTool.from_defaults(fn=validate_response)

agent = ReActAgent.from_tools(
    tools=[validate_tool],
    llm=llm,
    verbose=True,
    system_prompt="You are a validator agent. Use your tool to evaluate responses for correctness and clarity."
)
# system_prompt="You are a validator agent. Use your tool to evaluate responses for correctness and clarity."

extracted_data = "05-15-2018"
expected_format = "MM-DD-YYYY"
response = f"Is {extracted_data} a valid date in the document?"
#f"Is {extracted_data} a valid date in the document and does it match the date format of {expected_format}?"
result = agent.chat(response)
print(result)

