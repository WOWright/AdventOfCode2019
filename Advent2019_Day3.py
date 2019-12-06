# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:47:35 2019

@author: CoryJR
"""

with open('Advent2019_Day3_Input.txt', 'r') as f:
    wires = f.read().splitlines()

#Part 1
allpoints = []

def wire_right(c_point, movement):
    return set([(c_point[0]+i, c_point[1]) for i in range(movement+1)]), (c_point[0]+movement, c_point[1])

def wire_left(c_point, movement):
    return set([(c_point[0]-i, c_point[1]) for i in range(movement+1)]), (c_point[0]-movement, c_point[1])

def wire_up(c_point, movement):
    return set([(c_point[0], c_point[1]+i) for i in range(movement+1)]), (c_point[0], c_point[1]+movement)

def wire_down(c_point, movement):
    return set([(c_point[0], c_point[1]-i) for i in range(movement+1)]), (c_point[0], c_point[1]-movement)

ops = {'R': wire_right, 'L': wire_left, 'U': wire_up, 'D': wire_down}


for i,w in enumerate(wires):
    allpoints.append(set())
    corner = (0,0)
    inst_list = wires[i].split(',')
    for cmd in inst_list:
        S, corner = ops[cmd[0].upper()](corner, int(cmd[1:]))
        allpoints[i] = allpoints[i].union(S)
        
crossings = set.intersection(*allpoints)
crossings.remove((0,0))
closest = min(crossings,key=lambda x:abs(x[0]) + abs(x[1]))

print(f'Taxicab distance: {abs(closest[0])+abs(closest[1])}')

#Part 2
