#%% Problem 2 - Using sympy package for symbolic computations, evaluate the following indefinite integral:
from sympy import *

init_printing()

x = Symbol('x')

result = integrate(pow(exp(1),x) * sin(3 * x) ,x)

result = (integrate(exp(1),x))

#%% The output should be represented as LaTeX expression ready to copy/paste in a LaTeX document.

print(latex(result))