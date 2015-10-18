# instruction table class

import config
import crypt
import polynomial as poly
import login_reader as reader
import gmpy2
from gmpy2 import mpz

# instruction table variable
table = []


# generate the instruction table based on current polynomial
def generate(pwd, stat):
    config.generate_r()
    pwd = mpz(crypt.get_bit_str_from_byte(pwd), base=2)
    for i in xrange(config.max_features):
        x_0 = crypt.p(mpz((i + 1) << 1), config.r)
        x_1 = crypt.p(mpz(((i + 1) << 1) + 1), config.r)
        y_0 = gmpy2.add(poly.calculate(x_0), crypt.g(mpz((i + 1) << 1), config.r ^ pwd))
        y_1 = gmpy2.add(poly.calculate(x_1), crypt.g(mpz(((i + 1) << 1) + 1), config.r ^ pwd))
        global table
        if reader.if_init():
            table.append((y_0, y_1))
        else:
            for j in xrange(len(stat)):
                if stat[j][0] is None:
                    table.append((y_0, y_1))
                elif (stat[j][1] + stat[j][0] * config.k) < config.ti:
                    rand_value = gmpy2.t_mod(config.generate_rand(), config.q)
                    table.append((y_0, rand_value))
                elif (stat[j][1] - stat[j][0] * config.k) > config.ti:
                    rand_value = gmpy2.t_mod(config.generate_rand(), config.q)
                    table.append((rand_value, y_1))
            if len(stat) < config.max_features:
                table.extend([(y_0, y_1) for j in xrange(config.max_features - len(stat))])


# extract the coordinates based on the current features
def extract(pwd, features):
    coordinates = []
    i = 0
    pwd = mpz(crypt.get_bit_str_from_byte(pwd), base=2)
    for feature in features:
        i += 1
        if feature < config.ti:
            x = crypt.p(mpz(i << 1), config.r)
            y = gmpy2.sub(table[i - 1][0], crypt.g(mpz(i << 1), config.r ^ pwd))
            coordinates.append((x, y))
        else:
            x = crypt.p(mpz((i << 1) + 1), config.r)
            y = gmpy2.sub(table[i - 1][1], crypt.g(mpz((i << 1) + 1), config.r ^ pwd))
            coordinates.append((x, y))
    while len(coordinates) < config.max_features:
        i += 1
        x = crypt.p(mpz(i << 1), config.r)
        y = gmpy2.sub(table[i - 1][0], crypt.g(mpz(i << 1), config.r ^ pwd))
        coordinates.append((x, y))
    return coordinates


# extract the coordinate at specified index
def extract_at(pwd, features, index):
    coordinate = []
    # index += 1
    pwd = mpz(crypt.get_bit_str_from_byte(pwd), base=2)
    if features[index] > config.ti:
        x = crypt.p(mpz(index << 1), config.r)
        y = gmpy2.sub(table[index - 1][0], crypt.g(mpz(index << 1), config.r ^ pwd))
        coordinate.append(x)
        coordinate.append(y)
    else:
        x = crypt.p(mpz((index << 1) + 1), config.r)
        y = gmpy2.sub(table[index - 1][1], crypt.g(mpz((index << 1) + 1), config.r ^ pwd))
        coordinate.append(x)
        coordinate.append(y)
    return coordinate
