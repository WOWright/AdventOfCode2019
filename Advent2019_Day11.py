# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:54:23 2019

@author: CoryJR
"""

with open('Advent2019_Day11_Input.txt', 'r') as f:
    orig_list = [int(c) for c in f.read().split(',')]
    
class Intcode_Computer:
    def __init__(self, data_in):
        
        #Dict of computer operations
        self.ops = {1:self.add, 2:self.mult, 3:self.read_in, 4:self.out, 
                    5: self.true_jump, 6: self.false_jump, 7: self.lt, 8: self.eq,
                    9: self.update_relBase, 99:self.endprog}
        #Number of operands expected by each operation
        self.n_operands = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1, 99:0}
        
        self.cmd_idx = 0
        self.output = None
        self.input = []
        self.update_input(data_in)
        self.in_idx = 0
        self.paused = False
        self.done = False
        self.rel_base = 0
        self.feedback = False
        
        
    def add(self, modes):
        operands = self.read_vals(modes[:-1])
        operands.extend(self.write_vals(modes[-1], starter=2))
        self.update_program(operands[2], self.run_prog)
        self.run_prog[operands[2]] = operands[0] + operands[1]    
    
    def mult(self, modes):
        operands = self.read_vals(modes[:-1])
        operands.extend(self.write_vals(modes[-1], starter=2))
        self.update_program(operands[2], self.run_prog)
        self.run_prog[operands[2]] = operands[0] * operands[1]
    
    def read_in(self, modes):
        operands = self.write_vals(modes)
        self.update_program(operands[0], self.run_prog)
        self.run_prog[operands[0]] = self.input[self.in_idx]
        self.in_idx = self.in_idx+ 1
    
    def out(self, modes):
        operands = self.read_vals(modes)
        self.output = operands[0]
#        print(f'Output: {self.output}')
        if self.feedback:
            self.paused = True #for feedback mode only
    
    def true_jump(self, modes):
        operands = self.read_vals(modes)
        if operands[0]:
            self.cmd_idx = operands[1]
        else:
            self.cmd_idx = self.cmd_idx+len(operands)+1
    
    def false_jump(self, modes):
        operands = self.read_vals(modes)
        if not(operands[0]):
            self.cmd_idx = operands[1]
        else:
            self.cmd_idx = self.cmd_idx+len(operands)+1
    
    def lt(self, modes):
        operands = self.read_vals(modes[:-1])
        operands.extend(self.write_vals(modes[-1], starter=2))
        self.update_program(operands[2], self.run_prog)
        if operands[0] < operands[1]:
            self.run_prog[operands[2]] = 1
        else:
             self.run_prog[operands[2]] = 0
    
    def eq(self, modes):
        operands = self.read_vals(modes[:-1])
        operands.extend(self.write_vals(modes[-1], starter=2))
        self.update_program(operands[2], self.run_prog)
        if operands[0] == operands[1]:
            self.run_prog[operands[2]] = 1
        else:
            self.run_prog[operands[2]] = 0
        
    def endprog(self, modes):
        self.done = True
    
    def update_relBase(self, modes):
        operands = self.read_vals(modes)
        self.rel_base += operands[0]
        
    def mode_check(self, curr_cmd):
        cmd_str = str(curr_cmd)
        modes, op = cmd_str[:-2], cmd_str[-2:]
        op = int(op)
        num_ops = self.n_operands[op]
        padded_modes = ('0'*(num_ops-len(modes)) + modes)[::-1] #Reverse the string of leading zeros
        return padded_modes, op

        
    def get_operands(self, fetches, modes, starter=0):
     
        operands = []
        for i,m in enumerate(modes):
            new_o = fetches[m](self.cmd_idx+i+starter+1, self.run_prog)
            operands.append(new_o)
        return operands
    
    def read_vals(self, modes):
        #'0' - Use as pointer
        #'1' - Use as value
        #'2' - Add to relative base         
        fetches = {'0':lambda idx,cmd: self.basic_grab(self.basic_grab(idx,cmd), cmd),
           '1':lambda idx,cmd: self.basic_grab(idx, cmd),
           '2':lambda idx,cmd: self.basic_grab(self.basic_grab(idx,cmd) + self.rel_base, cmd)}
        
        return self.get_operands(fetches, modes)
            
    
    def write_vals(self, modes, starter=0):
        fetches = {'0':lambda idx,cmd: self.basic_grab(idx,cmd),
           '2':lambda idx,cmd: self.basic_grab(idx,cmd) + self.rel_base}
        return self.get_operands(fetches, modes, starter)
    
    def run_program(self):               
        while not (self.paused or self.done):
            instruction = self.run_prog[self.cmd_idx]
            modes, cmd = self.mode_check(instruction)
            self.ops[cmd](modes)
            if not(cmd==5 or cmd==6):
                self.cmd_idx += self.n_operands[cmd]+1
            
        self.paused = False

    def new_program(self, program):
        self.orig_prog = program.copy()
        self.run_prog = self.orig_prog.copy() 
        
    def update_input(self, data_in):
        try:
            iter(data_in)
            self.input.extend(data_in)
        except TypeError as te:
            self.input.append(data_in)
    
    def update_program(self, pointer, full_prog):
        if pointer >= len(full_prog):
            full_prog.extend([0 for i in range(pointer+1-len(full_prog))])
            
    def basic_grab(self, idx, cmd):
        self.update_program(idx, cmd)
        return cmd[idx]
    
## Part 1
robot = Intcode_Computer([0])
robot.feedback = True

hull = {}
current_position = [0, 0]
heading = [1,0]
robot.new_program(orig_list.copy())
painted = set()
left = [1,0]
while not robot.done:
#    painted.add(tuple(current_position))
    robot.run_program()
    #First output is paint color
    hull[tuple(current_position)] = robot.output
    robot.run_program()        
    if robot.output==0:
        heading = [heading[1], -heading[0]]
    else:
        heading = [-heading[1], heading[0]]
    current_position = [c+h for c,h in zip(current_position, heading)]
    if tuple(current_position) in hull.keys():
        robot.update_input(hull[tuple(current_position)])
    else:
        robot.update_input(0)
    
print(f'Painted panels: {len(hull)}')

##Part 2

#Copy and paste of part 1, with initial input changed
robot = Intcode_Computer([1])
robot.feedback = True

hull = {}
current_position = [0, 0]
heading = [1,0]
robot.new_program(orig_list.copy())
painted = set()
left = [1,0]
while not robot.done:
#    painted.add(tuple(current_position))
    robot.run_program()
    #First output is paint color
    hull[tuple(current_position)] = robot.output
    robot.run_program()        
    if robot.output==0:
        heading = [heading[1], -heading[0]]
    else:
        heading = [-heading[1], heading[0]]
    current_position = [c+h for c,h in zip(current_position, heading)]
    if tuple(current_position) in hull.keys():
        robot.update_input(hull[tuple(current_position)])
    else:
        robot.update_input(0)

#Actual new stuff        
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

panels = []

for coord in hull.keys():
    if hull[coord] == 1:
        rect = Rectangle((coord[1], coord[0]), 1, 1)
        panels.append(rect)
    
pc = PatchCollection(panels, facecolor='black', edgecolor='None')

fig, ax = plt.subplots()
ax.add_collection(pc)
ax.autoscale_view() #because add_collection and add_patch don't do this for reasons
ax.axis('equal') #Keep the text from being stretched weird
plt.show()













