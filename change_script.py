#!/usr/bin/env python
# -*- coding: utf8 -*-


import re
import glob



def change_script(html_file_path):
    old_script = ""
    with open(html_file_path, mode="r", newline="", encoding="utf-8_sig") as f:
        old_script = f.read()
        old_script = old_script.replace("\r\n", "\n").replace("\r", "\n")
    if '3.4.1' in old_script:
        print(html_file_path)

for file in glob.glob("**/*.html", recursive=True):
    change_script(file)
print("Finished.")
