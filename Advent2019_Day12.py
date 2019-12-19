# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:46:35 2019

@author: CoryJR
"""

with open('Advent2019_Day12_Input.txt', 'r') as f:
    field = f.read().splitlines()

#with open('Example_Day12.txt', 'r') as f:
#    field = f.read().splitlines()
    
class Moon():
    def __init__(self, position, velocity = None):
        self.position = position
        if velocity is None:
            self.velocity = [0,0,0]
        else:
            self.velocity = velocity
        self.total_energy = self.energy()
        
    def apply_gravity(self, companion):
        for idx, coord in enumerate(self.position):
            other = companion.position[idx]
            if coord > other:
                self.velocity[idx]+=-1
                companion.velocity[idx]+=1
            elif other > coord:
                self.velocity[idx]+=1
                companion.velocity[idx]+=-1            
    
    def energy(self):
        potential = sum(abs(x) for x in self.position)
        kinetic = sum(abs(v) for v in self.velocity)
        
        return potential * kinetic
    
    def update(self):
        self.position = [x+v for x,v in zip(self.position, self.velocity)]
        self.total_energy = self.energy()
        
import re
from itertools import combinations

pattern = '-?\d+'
satellites = []
for pos in field:
    locale = [int(num) for num in re.findall(pattern, pos)]
    satellites.append(Moon(locale))

for t in range(1000):    
    for M1,M2 in combinations(satellites,2):
        M1.apply_gravity(M2)
        
    for s in satellites:
        s.update()

sys_energy = sum(s.total_energy for s in satellites)
print(f'System Energy: {sys_energy}')

#Part 2
    