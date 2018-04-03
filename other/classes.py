# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 17:38:33 2018

@author: catalinayepes
"""
import pandas as pd

class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

class Repl_Cost():
    repl_cost_file = 'Replacement_cost_v3.xlsx'

    dwl_to_bdg = pd.read_excel(repl_cost_file, sheetname='dwl_to_bdg', index_col= 0)
    dwl_area = pd.read_excel(repl_cost_file, sheetname='dwl_area', index_col= 0)
    repl_cost = pd.read_excel(repl_cost_file, sheetname='dwl_repl_cost', index_col= 0)

    def __init__(self, repl_cost_file):
        self.repl_cost_file = repl_cost_file    # instance variable unique to each instance

