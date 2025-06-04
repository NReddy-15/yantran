#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 12:53:54 2025

@author: nanditareddy
"""

import csv 
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


selected_file = 'sample-extraction.csv'
current_dir = Path(__file__).parent
file_path = current_dir.parent / 'results' / selected_file
        
df = pd.read_csv(file_path)
dateColumns = df[['Date', 'Date Validity']]

status = ['Valid', 'Invalid']
status_counts = [0, 0]

log_text = "Checking field: Date \n"
for i in range(len(dateColumns)):
    log_text += dateColumns['Date'][i] + " " + dateColumns['Date Validity'][i] + "\n"
    if dateColumns['Date Validity'][i] == "Valid":
        status_counts[0] += 1
    else:
        status_counts[1] += 1
log_text += "\n\n" 
log_path = current_dir.parent / 'results' / 'logger-test.txt'
with open(log_path, "w") as file:
    file.write(log_text)

png_file_path = current_dir.parent / 'results' / 'status_plot.png'
plt.bar(status, status_counts)
plt.title('Valid vs Invalid Field Counts')
plt.xlabel('Status')
plt.ylabel('Count')
plt.savefig(png_file_path)
plt.show()
