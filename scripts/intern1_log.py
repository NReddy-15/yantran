#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 12:53:54 2025

@author: nanditareddy
"""

import csv 
from pathlib import Path
from llama_index.llms.ollama import Ollama
import pandas as pd

llm = Ollama(model="llama3", request_timeout=180) 

selected_file = 'sample-extraction.csv'
current_dir = Path(__file__).parent
file_path = current_dir.parent / 'results' / selected_file

# with open(file_path, 'r') as file:
#     reader = csv.reader(file)
    
#     for row in reader:
#         print(row)
        
df = pd.read_csv(file_path)
print(df)

dateColumns = df[['Date', 'Date Validity']]
print(dateColumns)

log_text = "Checking field: Date \n"
for i in range(len(dateColumns)):
    log_text += dateColumns['Date'][i] + " " + dateColumns['Date Validity'][i] + "\n"
log_text += "\n\n" 
log_path = current_dir.parent / 'results' / 'logger-test.txt'
with open(log_path, "w") as file:
    file.write(log_text)
