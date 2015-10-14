# instruction table class

import config
import crypt
import polynomial as poly

# instruction table variable
table = []


# generate the instruction table based on current polynomial
def generate(pwd):
    config.r = config.generate_rand()
    for i in xrange(config.max_features):
        x_0 = crypt.p(i * 2, config.r)
        x_1 = crypt.p(i * 2 + 1, config.r)
        y_0 = poly.calculate(x_0) # TODO
        y_1 = poly.calculate(x_1) # TODO
        global table
        table.append((y_0, y_1))


# extract the coordinates based on the current features
def extract(pwd, feature):
    pass
