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
    global table
    table = []  # clear the table
    for i in xrange(config.max_features):
        x_0 = crypt.p(mpz((i + 1) << 1), config.r)  # calculate x0, x1 and y0, y1
        x_1 = crypt.p(mpz(((i + 1) << 1) + 1), config.r)
        y_0 = gmpy2.add(poly.calculate(x_0), crypt.g(mpz((i + 1) << 1), config.r ^ pwd))  # use r xor pwd as the key
        y_1 = gmpy2.add(poly.calculate(x_1), crypt.g(mpz(((i + 1) << 1) + 1), config.r ^ pwd))
        if reader.if_init():
            table.append((y_0, y_1))  # if in initialization phase, add correct value
        else:
            if stat[i][0] is None:
                table.append((y_0, y_1))  # if no statistic information is derived
            elif (stat[i][1] + stat[i][0] * config.k) < config.ti:  # if fast
                rand_value = gmpy2.t_mod(config.generate_rand(), config.q)
                table.append((y_0, rand_value))
            elif (stat[i][1] - stat[i][0] * config.k) > config.ti:  # if slow
                rand_value = gmpy2.t_mod(config.generate_rand(), config.q)
                table.append((rand_value, y_1))
            else:
                table.append((y_0, y_1))


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
    while len(coordinates) < config.max_features:  # append more coordinates for interpolation
        i += 1
        x = crypt.p(mpz(i << 1), config.r)
        y = gmpy2.sub(table[i - 1][0], crypt.g(mpz(i << 1), config.r ^ pwd))
        coordinates.append((x, y))
    return coordinates


# extract the coordinate at specified index
def extract_at(pwd, features, index):
    index += 1
    pwd = mpz(crypt.get_bit_str_from_byte(pwd), base=2)
    if features[index - 1] > config.ti:  # pick the other column of the table
        x = crypt.p(mpz(index << 1), config.r)
        y = gmpy2.sub(table[index - 1][0], crypt.g(mpz(index << 1), config.r ^ pwd))
        return x, y
    else:
        x = crypt.p(mpz((index << 1) + 1), config.r)
        y = gmpy2.sub(table[index - 1][1], crypt.g(mpz((index << 1) + 1), config.r ^ pwd))
        return x, y

if __name__ == "__main__":
    # demonstrate the instruction table set up is correct
    config.init_random()
    config.generate_prime()
    config.generate_r()
    config.generate_h_pwd()
    poly.generate_poly()
    mock_pwd = "CorrectPassword"
    generate(mock_pwd, None)
    coordinates = extract(mock_pwd, [0])
    assert poly.get_h_pwd(coordinates) == config.h_pwd, "table initialization error!"
