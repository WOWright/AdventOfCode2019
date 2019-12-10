# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 14:57:23 2019

@author: CoryJR
"""

with open('Advent2019_Day5_Input.txt', 'r') as f:
    codes = [int(c) for c in f.read().split(',')]
    
#with open('Example_Day5.txt', 'r') as f:
#    codes = [int(c) for c in f.read().split(',')]
    
#with open('Advent2019_Day2_Input.txt', 'r') as f:
#    codes = [int(c) for c in f.read().split(',')]
#
#codes[1] = 12
#codes[2] = 2
    
orig_list = codes.copy()
### Part 1
def recur_call(cmd_list, num_recur, cmd_idx):
    if num_recur >= 1:
        return cmd_list[cmd_idx]
    else:
        return cmd_list[recur_call(cmd_list, num_recur+1,cmd_idx)]
    
class Intcode_Computer:
    def __init__(self):
        self.ops = {1:self.op_1, 2:self.op_2, 3:self.op_3, 4:self.op_4, 
                    5: self.op_5, 6: self.op_6, 7: self.op_7, 8: self.op_8}
        self.cmd_idx = 0
        self.curr_output = None
        self.curr_input = 1
        
    def op_1(self, program, modes):
        
        n1 = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        n2 = recur_call(program, int(modes[-2]), self.cmd_idx+2)
        pos = program[self.cmd_idx+3]
        program[pos] = n1+n2
        self.cmd_idx = self.cmd_idx + 4
        
    
    def op_2(self, program, modes):
        
        n1 = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        n2 = recur_call(program, int(modes[-2]), self.cmd_idx+2)
        pos = program[self.cmd_idx+3]
        program[pos] = n1*n2
        self.cmd_idx = self.cmd_idx + 4
    
    def op_3(self, program, modes):
#        pos = program[self.cmd_idx+1]
        pos = recur_call(program, int(1), self.cmd_idx+1) #Always positional?
        program[pos] = self.curr_input
        self.cmd_idx = self.cmd_idx+2
    
    def op_4(self, program, modes):
#        pos = program[self.cmd_idx+1]
        new_out = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        self.cmd_idx = self.cmd_idx+2
        self.curr_output = new_out
    
    def op_5(self, program, modes):
        n1 = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        n2 = recur_call(program, int(modes[-2]), self.cmd_idx+2)
        if n1:
            self.cmd_idx = n2
        else:
            self.cmd_idx = self.cmd_idx+3
    
    def op_6(self, program, modes):
        n1 = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        n2 = recur_call(program, int(modes[-2]), self.cmd_idx+2)
        if not(n1):
            self.cmd_idx = n2
        else:
            self.cmd_idx = self.cmd_idx+3
    
    def op_7(self, program, modes):
        n1 = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        n2 = recur_call(program, int(modes[-2]), self.cmd_idx+2)
        pos = program[self.cmd_idx+3]
        if n1 < n2:
            program[pos] = 1
        else:
            program[pos] = 0
        self.cmd_idx = self.cmd_idx + 4
    
    def op_8(self, program, modes):
        n1 = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        n2 = recur_call(program, int(modes[-2]), self.cmd_idx+2)
        pos = program[self.cmd_idx+3]
        if n1 == n2:
            program[pos] = 1
        else:
            program[pos] = 0
        self.cmd_idx = self.cmd_idx + 4
    
    def mode_check(self, curr_cmd):
        cmd_str = str(curr_cmd)
        modes, op = cmd_str[:-2], cmd_str[-2:]
        leading_zeros = 3-len(modes)
        return '0'*leading_zeros+modes, op
    
    def run_program(self, code_list):
        curr_cmd = code_list[self.cmd_idx]
        while curr_cmd != 99:
            M, O = self.mode_check(curr_cmd)
#            print(M,O)
            self.ops[int(O)](code_list, M)
            curr_cmd = code_list[self.cmd_idx]
        self.reset()
    
    def reset(self):
        self.cmd_idx = 0

#day2_IC = Intcode_Computer()
#day2_IC.run_program(codes)
#3931283 - correct answer for day 2, part 1

day5_IC = Intcode_Computer()
day5_IC.curr_input = 5
day5_IC.run_program(codes)

print(f'Result: {day5_IC.curr_output}')
#Part 2
"""Opcode 5 is jump-if-true: if the first parameter is non-zero, 
it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing."""

"""Opcode 6 is jump-if-false: if the first parameter is zero, 
it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing."""

"""Opcode 7 is less than: if the first parameter is less than the second parameter, 
t stores 1 in the position given by the third parameter. Otherwise, it stores 0."""

"""Opcode 8 is equals: if the first parameter is equal to the second parameter, 
it stores 1 in the position given by the third parameter. Otherwise, it stores 0."""