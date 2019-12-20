# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:46:35 2019

@author: CoryJR
"""

#with open('Advent2019_Day12_Input.txt', 'r') as f:
#    field = f.read().splitlines()

with open('Example_Day12.txt', 'r') as f:
    field = f.read().splitlines()

from operator import sub, add
from numpy import sign
    
class Moon():
    def __init__(self, position, velocity = None):
        self.start = position
        self.position = position
        if velocity is None:
            self.velocity = [0,0,0]
        else:
            self.velocity = velocity
        self.total_energy = self.energy()
        self.delta_v = None
        self.period = None
        
    def apply_gravity(self, companions):
        
        dif = [list(map(sub,x.position,self.position)) for x in companions]
        sgn = [list(map(sign,x)) for x in dif]
        self.delta_v = [sum(i) for i in zip(*sgn)]
    
    def energy(self):
        potential = sum(abs(x) for x in self.position)
        kinetic = sum(abs(v) for v in self.velocity)
        
        return potential * kinetic
    
    def update(self):
        self.velocity = list(map(add,self.velocity, self.delta_v))        
        self.position = list(map(add,self.velocity, self.position))
        self.total_energy = self.energy()

        
import re

pattern = '-?\d+'
satellites = []
for pos in field:
    locale = [int(num) for num in re.findall(pattern, pos)]
    satellites.append(Moon(locale))

for t in range(10):
        
    for s in satellites:
        s.apply_gravity([o for o in satellites if o != s])
        
    for s in satellites:
        s.update()

sys_energy = sum(s.total_energy for s in satellites)
print(f'System Energy: {sys_energy}')


def info_dump(lunar):
    for l in lunar:
        print(l.position, l.velocity)
#Part 2

pattern = '-?\d+'
satellites = []
steps = 0

for pos in field:
    locale = [int(num) for num in re.findall(pattern, pos)]
    satellites.append(Moon(locale))

from math import gcd

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

#From subreddit 'help'
    #Get period of velocity of each axis of each moon
    #First time axis returns to zero is 1/2 the period
    #My own guesswork
    #Use the LCM of the 3 axis periods to get period of moon
    #Use LCM of 4 moon periods to get system period
    #Profit???