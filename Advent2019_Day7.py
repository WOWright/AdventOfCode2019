# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 09:58:18 2019

@author: CoryJR
"""

with open('Advent2019_Day7_Input.txt', 'r') as f:
    orig_list = [int(c) for c in f.read().split(',')]
    
#with open('Example_Day7.txt', 'r') as f:
#    orig_list = [int(c) for c in f.read().split(',')]

### Part 1
def recur_call(cmd_list, num_recur, cmd_idx):
    if num_recur >= 1:
        return cmd_list[cmd_idx]
    else:
        return cmd_list[recur_call(cmd_list, num_recur+1,cmd_idx)]
    
class Intcode_Computer:
    def __init__(self, data_in):
        self.ops = {1:self.op_1, 2:self.op_2, 3:self.op_3, 4:self.op_4, 
                    5: self.op_5, 6: self.op_6, 7: self.op_7, 8: self.op_8}
        self.cmd_idx = 0
        self.curr_output = None
        self.input = []
        self.update_input(data_in)
        self.in_idx = 0
        self.thrown_pause = False
        self.done = False
        
        
    def op_1(self, program, modes):
        
        n1,n2 = self.get_params(program, modes)
        pos = program[self.cmd_idx+3]
        program[pos] = n1+n2
        self.cmd_idx = self.cmd_idx + 4
        
    
    def op_2(self, program, modes):
        
        n1,n2 = self.get_params(program, modes)
        pos = program[self.cmd_idx+3]
        program[pos] = n1*n2
        self.cmd_idx = self.cmd_idx + 4
    
    def op_3(self, program, modes):

        pos = recur_call(program, int(1), self.cmd_idx+1) #Always positional?
        program[pos] = self.input[self.in_idx]
        self.in_idx = self.in_idx+ 1
        self.cmd_idx = self.cmd_idx+2
    
    def op_4(self, program, modes):

        new_out = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        self.cmd_idx = self.cmd_idx+2
        self.curr_output = new_out
        self.thrown_pause = True
    
    def op_5(self, program, modes):
        
        n1,n2 = self.get_params(program, modes)
        if n1:
            self.cmd_idx = n2
        else:
            self.cmd_idx = self.cmd_idx+3
    
    def op_6(self, program, modes):
        
        n1,n2 = self.get_params(program, modes)
        if not(n1):
            self.cmd_idx = n2
        else:
            self.cmd_idx = self.cmd_idx+3
    
    def op_7(self, program, modes):
        
        n1,n2 = self.get_params(program, modes)
        pos = program[self.cmd_idx+3]
        if n1 < n2:
            program[pos] = 1
        else:
            program[pos] = 0
        self.cmd_idx = self.cmd_idx + 4
    
    def op_8(self, program, modes):
        
        n1,n2 = self.get_params(program, modes)
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
        while curr_cmd != 99 and not self.thrown_pause:
            M, O = self.mode_check(curr_cmd)
            self.ops[int(O)](code_list, M)
            curr_cmd = code_list[self.cmd_idx]
        if curr_cmd == 99:
            self.done = True
        self.thrown_pause = False
    
    def get_params(self,program, modes):
        n1 = recur_call(program, int(modes[-1]), self.cmd_idx+1)
        n2 = recur_call(program, int(modes[-2]), self.cmd_idx+2)
        return n1, n2
    
    def update_input(self, data_in):
        try:
            iter(data_in)
            self.input.extend(data_in)
        except TypeError as te:
            self.input.append(data_in)

    def reset(self):
        self.cmd_idx = 0
        self.input = []
        self.in_idx = 0



from itertools import permutations
best_signal = 0
for A1, A2, A3, A4, A5 in permutations(range(5)):
    Amp1 = Intcode_Computer([A1, 0])
    Amp1.run_program(orig_list.copy())
    
    Amp2 = Intcode_Computer([A2, Amp1.curr_output])
    Amp2.run_program(orig_list.copy())
    
    Amp3 = Intcode_Computer([A3, Amp2.curr_output])
    Amp3.run_program(orig_list.copy())
    
    Amp4 = Intcode_Computer([A4, Amp3.curr_output])
    Amp4.run_program(orig_list.copy())
    
    Amp5 = Intcode_Computer([A5, Amp4.curr_output])
    Amp5.run_program(orig_list.copy())
    
    best_signal = max(best_signal, Amp5.curr_output)
    
print(f'Best I can do, pal: {best_signal}')

##Part 2
best_signal = 0

for phases in permutations(range(5,10)):
    driving_input = 0
    #Instantiations
    mem_bank = [orig_list.copy() for i in range(5)]
    Amplifiers = [Intcode_Computer([phases[i]]) for i in range(5)]
    
    while not all([device.done for device in Amplifiers]):
        for i,amp in enumerate(Amplifiers):
            if i == 0:
                amp.update_input(driving_input)
                amp.run_program(mem_bank[i])
            else:
                amp.update_input(Amplifiers[i-1].curr_output)
                amp.run_program(mem_bank[i])
        
        driving_input = Amplifiers[-1].curr_output
#        print(driving_input)

    best_signal = max(best_signal, Amplifiers[-1].curr_output)
#139629729
print(f"We're at {best_signal}, Captain, and we cannae take no more!")