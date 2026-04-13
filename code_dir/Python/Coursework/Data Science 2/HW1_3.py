#%% Problem 3 - For a given positive integer number N, print all prime numbers between 1 and N (including N if it is prime itself).

N = 25
print("Prime numbers between 1 and 25 are")

#%% How to check if a number M is prime or not? Start with developing a program checking if a number is prime or not.
temp = 0
i = 1
#doing it with loops
while temp < N:
    j = 1
    ct = 0
    while j <= i :
        if i % j == 0:
            ct = ct + 1
        j = j + 1
    if ct == 2:
        if i <= N:
            print(i)
        temp = temp + 1
    i = i + 1