# Problem 1 - Without using any Python’s functions for solving quadratic equations, develop a Python program, which solves quadratic equations:

#%% where 𝑎, 𝑏 and 𝑐 are real numbers.

a = 23.17
b = -10.0
c = -5.0

#%% Your code here
import math
import cmath
#find discriminant
dis = (b ** 2) - (4 * a * c)

#a = 0 catch
if a == 0:
    positive = (-c / b)
    negative = math.nan
#when it is positive, we get two real solutions
elif dis > 0:
    positive = ((-b + math.sqrt(abs(dis))) / (2 * a))
    negative = ((-b - math.sqrt(abs(dis))) / (2 * a))
#when it is zero we get just ONE solution
elif dis == 0:
    positive = -b / (2 * a)
    negative = math.nan
else:
    positive = (-b + cmath.sqrt(dis)) / (2 * a)
    negative = (-b - cmath.sqrt(dis)) / (2 * a)

#%%

x1 = positive
x2 = negative
print('The equation has', abs(sum([cmath.isnan(positive),cmath.isnan(negative )]) - 2),'solution(s):')
print('x1 = ', x1)
print('x2 = ', x2)