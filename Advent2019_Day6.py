# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:55:45 2019

@author: CoryJR
"""

with open('Advent2019_Day6_Input.txt', 'r') as f:
    orbits = f.read().splitlines()
    
#with open('Example_Day6.txt', 'r') as f:
#    orbits = f.read().splitlines()
    
all_bodies = {'COM':[]}
for spin in orbits:
    ctr, sat = spin.split(')')
    if sat in all_bodies:
        all_bodies[sat].append(ctr)
    else:
        all_bodies[sat] = [ctr]
    
orbit_count = {'COM': 0}
for bod in all_bodies:
    curr_check = bod
    orbit_count[bod] = 0
    while curr_check != 'COM':
        orbit_count[bod] += 1
        curr_check = all_bodies[curr_check][0]    
        
print(f'Total Orbits: {sum(orbit_count.values())}')

#Part 2
orbit_path = {'YOU':[], 'SAN':[]}
for poi in orbit_path:
    curr_loc = all_bodies[poi][0]
    while curr_loc != 'COM':
        orbit_path[poi].append(curr_loc)
        curr_loc = all_bodies[curr_loc][0]

my_set = set(orbit_path['YOU'])
santa_set = set(orbit_path['SAN'])

transfers = my_set.union(santa_set) - my_set.intersection(santa_set)

print(f'Total Transfers: {len(transfers)}')