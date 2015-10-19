# polynomial module

import config
import gmpy2
from gmpy2 import mpz

# coefficient list for representing the polynomial
c = []


# randomly generate a polynomial of degree m-1
def generate_poly():
    global c
    c = [config.h_pwd]   # first coefficient is the hardened password
    for i in xrange(config.max_features - 1):
        tmp = config.generate_rand()
        c.append(gmpy2.t_mod(tmp, config.q))


# calculate the Lagrange coefficient for interpolation
def get_lambda_i(x, i):
    lambda_i = mpz(1)
    for j in xrange(len(x)):
        if i != j:
            if x[i] == x[j] and config.debug:
                print x
                print i
                print j
                print config.q
            tmp = gmpy2.invert(gmpy2.sub(x[j], x[i]), config.q)
            tmp = gmpy2.t_mod(gmpy2.mul(x[j], tmp), config.q)
            lambda_i = gmpy2.t_mod(gmpy2.mul(lambda_i, tmp), config.q)
    return lambda_i


# calculate the hardened password using interpolation
def get_h_pwd(coordinates):
    x = map(lambda x: x[0], coordinates)  # extract the x and y coordinates
    y = map(lambda x: x[1], coordinates)
    h_pwd_ = mpz()
    for i in xrange(config.max_features):
        h_pwd_ = gmpy2.add(h_pwd_, gmpy2.t_mod(gmpy2.mul(y[i], get_lambda_i(x, i)), config.q))
    h_pwd_ = gmpy2.t_mod(h_pwd_, config.q)
    return h_pwd_


# calculate the value of the polynomial at a point x
def calculate(x):
    ans = mpz()
    for c_i in c[::-1]:
        ans = gmpy2.t_mod(gmpy2.add(gmpy2.mul(ans, x), c_i), config.q)
    return ans

if __name__ == "__main__":
    # test for calculate
    config.init_random()
    config.generate_prime()
    global c
    c = [mpz(20), mpz(1), mpz(2)]
    print calculate(mpz(2))

    # test for generate_poly() and get_h_pwd
    config.generate_h_pwd()
    config.max_features = 127
    print "h_pwd: ", config.h_pwd
    generate_poly()
    coordinates = [(i, calculate(i)) for i in [mpz(j+1) for j in range(config.max_features)]]
    print "h_pwd_: ", get_h_pwd(coordinates)
