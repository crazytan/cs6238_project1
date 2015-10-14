# polynomial module

import config

# coefficient list for representing the polynomial
c = []


# randomly generate a polynomial of degree m-1
def generate_poly():
    global c
    c = [config.h_pwd]   # first coefficient is the hardened password
    for i in xrange(config.max_features - 1):
        tmp = config.generate_rand()
        c.append(tmp % config.q)


# calculate the hardened password using interpolation
def get_h_pwd(coordinates):
    pass


# calculate the value of the polynomial at a point x
def calculate(x):
    ans = 0
    for c_i in c:
        ans = ans * x + c_i
        ans = ans % config.q
    return ans
