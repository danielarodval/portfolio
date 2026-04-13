# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 21:03:20 2023

@author: danma
"""
2
#%% Problem 1 Design a function
n = int(-237)

def GetDigitsNo(n):
    return len(str(abs(n)))
    
print(GetDigitsNo(n))