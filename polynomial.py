# polynomial module

import config

# coefficient list for representing the polynomial
c = []


# randomly generate a polynomial of degree m-1
def generate_poly():
    global c
    c.append(config.h_pwd)   # first coefficient is the hardened password
    for i in xrange(config.max_features):
        tmp = config.generate_rand()
        c.append(tmp % config.q)


# calculate the hardened password using interpolation
def calculate(coordinates):
    pass
