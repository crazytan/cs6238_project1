# instruction table class

import config
import crypt
import polynomial as poly
import login_reader as reader
import gmpy2

# instruction table variable
table = []


# generate the instruction table based on current polynomial
def generate(pwd, feature, stat):
    config.generate_r()
    for i in xrange(config.max_features):
        x_0 = crypt.p((i + 1) << 1, config.r)
        x_1 = crypt.p((i + 1) << 1 + 1, config.r)
        y_0 = gmpy2.add(poly.calculate(x_0), crypt.g((i + 1) << 1, config.r ^ pwd))
        y_1 = gmpy2.add(poly.calculate(x_1), crypt.g((i + 1) << 1 + 1, config.r ^ pwd))
        global table
        if reader.if_init():
            table.append((y_0, y_1))
        else:
            pass  # TODO


# extract the coordinates based on the current features
def extract(pwd, features):
    coordinates = []
    i = 0
    for feature in features:
        i += 1
        if feature < config.ti:
            x = crypt.p(i << 1, config.r)
            y = gmpy2.sub(table[i - 1][0], crypt.g(i << 1, config.r ^ pwd))
            coordinates.append((x, y))
        else:
            x = crypt.p(i << 1 + 1, config.r)
            y = gmpy2.sub(table[i - 1][1], crypt.g(i << 1 + 1, config.r ^ pwd))
            coordinates.append((x, y))
    while len(coordinates) < config.max_features:
        i += 1
        x = crypt.p(i << 1, config.r)
        y = gmpy2.sub(table[i - 1][0], crypt.g(i << 1, config.r ^ pwd))
        coordinates.append((x, y))
    return coordinates


# extract the coordinate at specified index
def extract_at(pwd, features, index):
    coordinate = []
    index += 1
    if features[index] > config.ti:
        x = crypt.p(index << 1, config.r)
        y = gmpy2.sub(table[index - 1][0], crypt.g(index << 1, config.r ^ pwd))
        coordinate.append(x)
        coordinate.append(y)
    else:
        x = crypt.p(index << 1 + 1, config.r)
        y = gmpy2.sub(table[index - 1][1], crypt.g(index << 1 + 1, config.r ^ pwd))
        coordinate.append(x)
        coordinate.append(y)
    return coordinate
