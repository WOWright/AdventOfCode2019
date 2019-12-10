# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:55:45 2019

@author: CoryJR
"""

with open('Advent2019_Day6_Input.txt', 'r') as f:
    orbits = f.read().splitlines()
    
class OrbitalBody(object):
    def __init__(self, parent, name):
        self.direct = parent # Single object
        self.indirect = []
        self.child = []  # Array of objects
        self.name = name

all_bodies = [OrbitalBody(parent=None, name='COM')]
for spin in orbits:
    ctr, sat = spin.split(')')       
#    for x in all_bodies:
#        if x.name == sat:
#            x.direct = ctr
#            break
#        else:
#            all_bodies.append(OrbitalBody(parent=ctr, name = sat))