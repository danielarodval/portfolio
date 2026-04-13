"""
Lagrange Error Theorem, or Taylor's Remainder Theorem 

"""
import math
import numpy as np

def get_m(x, err):
    m = 0
    while (math.fabs(x) ** (2*m+1)/(math.factorial(2*m+1))) > err:
        m += 1
    return m

#Approach 2
def approx_cos(x, err):
    m0 = get_m(x, err)
    s = float(0)
    for k in range(0, m0 + 1, 1):
        s += (-1)**k * x **(2*k)/ math.factorial(2*k)
    return s

def f(x, allowed_err):
    x_range = np.arange(1, 2, 0.05) #creating range of values
    for values in x_range :#looping through range to print table of values
        print("cos(%.2f) with 0.003 = %.10f approximately" %(values,approx_cos(values, 0.003)))

    value_of_cos = approx_cos(x, allowed_err)#singular call for the user requested input
    return"\n cos(%.2f) = %.10f approximately" %(x, value_of_cos)


# Running the actual program
x = 1.5
allowed_error = .04 #add check that err > 0

print(f(float(x),float(allowed_error)))