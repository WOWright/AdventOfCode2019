# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:22:36 2019

@author: CoryJR
"""

with open('Advent2019_Day8_Input.txt', 'r') as f:
    image_str = f.read()

image_enc = [int(N) for N in image_str]
AR = [25, 6]
pix_per_layer = AR[0] * AR[1]
layer_idx = range(0, len(image_enc), pix_per_layer)
image = []
for layer_start in layer_idx:
    image.append([])
    for line_start in range(6):
        slice_start = AR[0]*line_start + layer_start
        image[layer_start//pix_per_layer].append(image_enc[slice_start:slice_start+AR[0]])
#Part 1
layers = []
n_zeros = []
for layer_start in layer_idx:
    the_layer = image_enc[layer_start:layer_start+pix_per_layer]
    layers.append(the_layer)
    n_zeros.append(the_layer.count(0))

layer_min_zeros = layers[n_zeros.index(min(n_zeros))]

checksum = layer_min_zeros.count(1) * layer_min_zeros.count(2)

print(f'Required checksum: {checksum}')