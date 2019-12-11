# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 09:58:18 2019

@author: CoryJR
"""

with open('Advent2019_Day7_Input.txt', 'r') as f:
    codes = [int(c) for c in f.read().split(',')]
    
orig_list = codes.copy()
### Part 1
from Advent2019_Day5 import Intcode_Computer, recur_call 