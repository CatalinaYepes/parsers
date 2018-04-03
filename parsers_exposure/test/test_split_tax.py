# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 13:56:37 2017

@author: catalinayepes
"""

from parsers_exposure.functions import split_tax

name = u'80% MUR/H:1,3\n20% MUR+ADO/H:1,2'
print split_tax(name)


name = u'\n30% MUR/H:1,3\n60% MUR+ADO/H:1,2\n'
print split_tax(name)