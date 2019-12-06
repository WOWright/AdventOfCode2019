# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
### Imports and Input Read-In
import math as math
with open('Advent2019_Day1_Input.txt', 'r') as f:
    modules = f.read().splitlines()

### Part 1
total = 0    
for m in modules:
    total = total+ math.floor(int(m)/3) - 2

print(f'Total Fuel Requirement: {total}')

### Part 2
recalc_total = 0

def fuel_calc(mass):
    return max(math.floor(mass/3) - 2,0)

for m in modules:
    mod_total = 0
    fuel_req = 12
    new_mass = int(m)
    while fuel_req > 0:
        fuel_req = fuel_calc(new_mass)
        mod_total = mod_total + fuel_req
        new_mass = fuel_req
    recalc_total = recalc_total + mod_total

print(f'Total Fuel Requirement: {recalc_total}')