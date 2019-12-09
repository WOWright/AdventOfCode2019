# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 13:31:31 2019

@author: CoryJR
"""

#Password conditions
# 6 digit number in given range
#Contains adjacent repeated digit
#Digits increase Left to Right

password_range = range(156218, 652527+1)

def get_digit(number, n):
    return number // 10**n % 10

repeats = set()
for poss_pw in password_range:
    for i in range(5):
        if get_digit(poss_pw,i) == get_digit(poss_pw,i+1):
            repeats.add(poss_pw)
            break

badnums = set()
for rep_num in repeats:
    for i in range(5):
        if get_digit(rep_num,i) < get_digit(rep_num,i+1):
            badnums.add(rep_num)
            break
        
all_poss = repeats - badnums

print(f'Number of possible passwords: {len(all_poss)}')

#Part 2
keepers = set()
for num in all_poss:
    num_str = str(num)
    digits = set(num_str)
    for d in digits:
        C = num_str.count(d)
        if C == 2:
            keepers.add(num)
            break

print(f'Number of possible passwords: {len(keepers)}')