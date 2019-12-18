# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:05:42 2019

@author: CoryJR
"""

with open('Advent2019_Day10_Input.txt', 'r') as f:
    field = f.read().splitlines()
    
#with open('Example_Day10.txt', 'r') as f:
#    field = f.read().splitlines()
    
## Part 1
from math import sqrt
#Create list of asteroid coordinates
coord_list = []
for i, ast in enumerate(field):
    for j, a in enumerate(ast):
        if a == '#':
            coord_list.append((j,i))


class Asteroid():
    def __init__(self, coords):
        self.locale = coords
        self.headings = {}
        self.distances = {}
        self.visible = set()
        
    def ranging(self, otherasteroid):
        if otherasteroid.locale not in self.headings:
            dX = self.locale[0] - otherasteroid.locale[0]
            dY = self.locale[1] - otherasteroid.locale[1]
            D = sqrt(dX**2 + dY**2)
            #Rounding to 10 digits to deal with floating point errors
            self.headings[otherasteroid.locale] = (round(dX/D,10), round(dY/D,10))
            otherasteroid.headings[self.locale] = (-round(dX/D,10), -round(dY/D,10))
            
            self.distances[otherasteroid.locale] = D
            otherasteroid.distances[self.locale] = D
            
    def find_visibles(self):
        unique_vecs = list(set(i for i in self.headings.values()))
        for v in unique_vecs:
            aligned = [k for k,x in self.headings.items() if x==v]
            if len(aligned) > 1:
                dists = [self.distances[place] for place in aligned]
                lowest_dist = dists.index(min(dists))
                self.visible.add(aligned[lowest_dist])
            else:
                self.visible.add(aligned[0])


ast_field = [Asteroid(c) for c in coord_list]
best = 0
for rock in ast_field:
    others = [r for r in ast_field if r.locale != rock.locale]
    for station in others:
        rock.ranging(station)
    rock.find_visibles()
    best = max(len(rock.visible), best)
    
print(f'Maximum Visible: {best}')

##### Original Part 1 Solution ######
#It works, but it takes a very long time for the actual puzzle input


#from itertools import permutations
#from numpy import cross, dot
#from numpy.linalg import norm
#
#def view_block(A1, A2, A3):
#    V1 = [A1[0] - A2[0], A1[1] - A2[1]]
#    V2 = [A1[0] - A3[0], A1[1] - A3[1]]
#    
#    if cross(V1, V2) == 0 and not dot(V1, V2) < 0:
#        #check to see which asteroid is closer, return the blocked asteroid
#        if norm(V1) > norm(V2):
#            return A2
#        else:
#            return A3
#    else:
#        return False
#
#visibilities = {el:set([c for c in coord_list if c != el]) for el in coord_list}
#
#for A1, A2, A3 in permutations(coord_list, 3):
#    #Check to see if asteroids are aligned. If they are, return the asteroid
#    #that is blocked from A1's view
#    blocked = view_block(A1, A2, A3)
#    if blocked:
#        visibilities[A1].discard(blocked)
#
#most_vis = max([len(v) for v in visibilities.values()])
#print(f'Most visibilities: {most_vis}')

## Part 2
from numpy import dot,arccos,pi

for sky_pebble in ast_field:
    if len(sky_pebble.visible) == best:
        bestroid = sky_pebble
        
destruction = {}
galactic_north = (0,1)
for potato in bestroid.visible:
    vec = bestroid.headings[potato]
    ang = arccos(dot(galactic_north, vec))
    if potato[0] < bestroid.locale[0]:
        destruction[potato] = 2*pi - ang
    else:
        destruction[potato] = ang    


vapor_order = [k for k,v in sorted(destruction.items(), key=lambda item: item[1])]
chicken_dinner = vapor_order[199]
print(f'ID Code: {chicken_dinner[0]*100+chicken_dinner[1]}')