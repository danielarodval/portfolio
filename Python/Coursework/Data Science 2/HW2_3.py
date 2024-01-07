# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 21:31:46 2023

@author: danma
"""

#%% Problem 3 - Develop a program that asks a user about the name of a data file you want to process. The file must be in text format and should have positive and negative integers in every line. This is an example of such file:

def SumPositiveIntegers(file_name):
    sum = 0
    try:
        with open(file_name) as f:
            data = f.readlines()
        for i in range(5):
            if '-' in data[i] :
                pass
            else :
                sum = sum + int(data[i])
        print("For the file above, the sum is equal to", sum)
    except:
        print('No such a file found!')
    return 0

file_name = input('Enter a file name: ')
SumPositiveIntegers(file_name)