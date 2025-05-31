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
from pathlib import Path
import re

llm = Ollama(model="llama3", request_timeout=120) 

selected_file = 'wordpress-sample.pdf'
current_dir = Path(__file__).parent
file_path = current_dir.parent / 'invoices' / selected_file


reader = PdfReader(file_path)
text = ""
for i in range(len(reader.pages)):
    page = reader.pages[i]
    text += page.extract_text()

extracted_inv_num = re.findall("INV-\d+", text)
extracted_date = re.match(r"\d{4}-\d{2}-\d{2}", text)
expected_format = "MM-DD-YYYY"
extracted_date = "05-28-2005"
print(extracted_inv_num)

log_text = "Validating file: " + selected_file + "\n"

def validate_response(response: str) -> str:
    prompt = f"You are a validator agent. Use your tool to ensure that in the following text, the date follows the format '{expected_format}': {response}."
    return llm.complete(prompt).text.strip()
validate_tool = FunctionTool.from_defaults(fn=validate_response)

agent = ReActAgent.from_tools(
    tools=[validate_tool],
    llm=llm,
    verbose=True,
    system_prompt=f"You are a validator agent. Check whether the date follows the format '{expected_format}'."
)

if extracted_date:
    response = f"Is {extracted_date} a valid date in the document and does it match the date format of {expected_format}?"
    result = agent.chat(response)
else:
    result = "Date not found, may not be in correct format\n"
print(result)
log_text += result + "\n"
if len(extracted_inv_num) == 1:
    num_result = f"Invoice number found: {extracted_inv_num[0]}\n"
else:
    num_result = "Invoice number not found, may not be in correct format\n"
print(num_result)
log_text += num_result + "\n\n"

log_path = current_dir.parent / 'results' / 'validation-log.txt'
with open(log_path, "a") as file:
    file.write(log_text)



