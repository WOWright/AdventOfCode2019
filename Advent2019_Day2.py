# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:08:00 2019

@author: CoryJR
"""

### Imports and Input Read-In
import numpy as np


with open('Advent2019_Day2_Input.txt', 'r') as f:
    codes = [int(c) for c in f.read().split(',')]

codes[1] = 12
codes[2] = 2

orig_list = codes.copy()
### Part 1


ops = {1:sum, 2:np.prod}
def intcoder(code_list, operations):
    cmd_idx = range(0,len(code_list),4)
    for cmd in cmd_idx:
        
        run_func = code_list[cmd]
        n1 = code_list[code_list[cmd+1]]
        n2 = code_list[code_list[cmd+2]]
        pos = code_list[cmd+3]
        
        if run_func==99:
            return code_list[0]
        else:
            code_list[pos] = ops[run_func]([n1,n2])
        
print(f'Position 0: {intcoder(codes,ops)}')

### Part 2
from itertools import product

for noun, verb in product(range(0,100),range(0,100)):
    trial_code = orig_list.copy()
    trial_code[1] = noun
    trial_code[2] = verb
    val = intcoder(trial_code, ops)
    if val == 19690720:
        break
print(f'Basic Checksum: {100*noun + verb}')