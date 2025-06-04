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
import datetime

llm = Ollama(model="llama3", request_timeout=180) 

selected_file = 'wordpress-sample.pdf'
current_dir = Path(__file__).parent
file_path = current_dir.parent / 'invoices' / selected_file


reader = PdfReader(file_path)
text = ""
for i in range(len(reader.pages)):
    page = reader.pages[i]
    text += page.extract_text()

#extracted_inv_num = re.findall("INV-\d+", text)
#extracted_date = re.match(r"\d{4}-\d{2}-\d{2}", text)
# date_format = "MM-DD-YYYY"
# inv_format = r"INV-\d+"
#extracted_date = "05-28-2005"
#extracted_dates = ["31-07-2003", "05-28-2005", "04/05/2006", "January 25, 2021", "4 April 2016", "08-17-2012"]
# print(extracted_inv_num)

log_text = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + "\nValidating file: " + selected_file + "\n"

def search_response(response: str) -> str:
    prompt = f"You are a search agent. Find the invoice number and invoice date in the following text: {response}."
    return llm.complete(prompt).text.strip()
search_tool = FunctionTool.from_defaults(fn=search_response)
# f"You are a validator agent. Use your tool to ensure that in the following text, the date follows the format '{expected_format}': {response}."
# def validate_response(response: str) -> str:
#     prompt = f"You are a validator agent. Find the invoice number and invoice date in the following text: {response}."
#     return llm.complete(prompt).text.strip()
# validate_tool = FunctionTool.from_defaults(fn=validate_response)

def id_valid_format(s: str) -> str:
    pattern = r"INV-\d+"
    if re.search(pattern, s):
        return f"✅ '{s}' is in the correct format."
    else:
        return f"❌ '{s}' is not in the correct format."
id_check_tool = FunctionTool.from_defaults(fn=id_valid_format)

def date_valid_format(s: str) -> str:
    try:
       # Try to parse the string into a date
       datetime.strptime(s, "%d/%m/%Y")
       return f"✅ '{s}' is a valid date in DD-MM-YYYY format."
    except ValueError:
       return f"❌ '{s}' is not a valid date in DD-MM-YYYY format."
date_check_tool = FunctionTool.from_defaults(fn=date_valid_format)

searchAgent = ReActAgent.from_tools(
    tools=[search_tool],
    llm=llm,
    verbose=True,
    system_prompt="You are a search agent. Use your tool to find the invoice number and invoice date in the text. Format your response as the two fields separated by a comma.",
    max_steps=3
)
validateAgent = ReActAgent.from_tools(
    tools=[id_check_tool, date_check_tool],
    llm=llm,
    verbose=True,
    system_prompt="You are a validator agent. Use your tool to check whether in the following text, the fields follow the expected format. In the case of a date format, M represents month, D represents day and Y represents year. Label each field as valid or invalid format.",
    max_steps=3
)

response = f"Find the invoice number and invoice date in the following text: {text}."
agent_resp = searchAgent.chat(response)
print(agent_resp)
result = str(agent_resp)
log_text += result + "\n"

#result = "The invoice number is: INV-3337 And the invoice date is: January 25, 2016"
inv_res = "INV-3337"

# validate_request = f"Check that in the following text, the invoice number follows format {inv_format} and the invoice date follows format {date_format}: {result}. Label each field as valid or invalid format."
validate_request = f"Can you check if the following fields are in the right format?: {result}"
valid_resp = validateAgent.chat(validate_request)
print(valid_resp)
# log_text += str(valid_resp) + "\n\n"
# if len(extracted_inv_num) == 1:
#     num_result = f"Invoice number found: {extracted_inv_num[0]}\n"
# else:
#     num_result = "Invoice number not found, may not be in correct format\n"
# print(num_result)
# log_text += num_result + "\n\n"

# log_path = current_dir.parent / 'results' / 'validation-log.txt'
# with open(log_path, "a") as file:
#     file.write(log_text)



