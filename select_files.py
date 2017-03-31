# -*- coding: utf-8 -*-
"""
Select files inside a folder

@catalinayepes
"""

import os

def select_files(folder=".", start="", end="", contain=""):
    files = []
    for file_name in os.listdir(folder):
        if file_name.startswith(start):
            if file_name.endswith(end):
                if file_name.find(contain) != -1:
                    files.append(file_name)
    if len(files) == 1:
        return files[0]
    else:
        assert len(files) != 0, '\nNo files selected\n'
        return files