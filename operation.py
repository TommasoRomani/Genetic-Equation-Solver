#file containing all operations that can appear in the population

import math


# sum
def sum(x1,x2):
    return x1+x2

# subtraction
def sub(x1,x2):
    return x1-x2

#multiplication
def mul(x1,x2):
    return x1*x2

# division
def div(x1,x2):
    return x1/x2

# square root
def sqrt(x1):
    return x1**0.5

# sigmoid function
def sigmoid(x1):
    return 1/(1+math.exp(-x1))