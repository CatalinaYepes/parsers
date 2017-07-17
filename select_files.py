# -*- coding: utf-8 -*-
"""
Select files inside a folder

@catalinayepes
"""

import os

def select_files(folder=".", start="", end="", contain=""):
    '''Function to select files inside a folder
        
        :folder: folder name, by default current one

        :start: select the files that start with a given string

        :end: select the files that end with a given string

        :contain: select the files that contain a given string

        Returns a list_names of files if more than one
    '''
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