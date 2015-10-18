# Project 1 for CS6238
# Implements password hardening as described in the paper
# Authors:
#   Jia Tan, tanjia@gatech.edu
#   Zenong Lu, kardlu@gatech.edu


import login_reader as reader
import instruction_table as table
import polynomial as poly
import config
import history

# initialization procedure
def initialize():
    config.init_random()
    config.simple = False
    config.debug = False
    config.generate_prime()
    config.generate_h_pwd()
    poly.generate_poly()
    if config.debug:
        pwd = reader.init("input.txt")
    else:
        pwd = reader.init(raw_input("enter the input file: "))
    table.generate(pwd, None)
    history.init()


# Simple error correction
def correction(pwd, feature):
    coordinates = table.extract(pwd, feature)
    for i in xrange(len(feature)):
        tmp_x = coordinates[i][0]
        tmp_y = coordinates[i][1]
        coordinates[i] = table.extract_at(pwd, feature, i)
        h_pwd_ = poly.get_h_pwd(coordinates)
        if history.decrypt(h_pwd_):
            return True
        coordinates[i][0] = tmp_x
        coordinates[i][1] = tmp_y
    return False


# update the history file and instruction table after successful login
def update(pwd, feature):
    config.generate_h_pwd()
    stat = history.add_feature(feature)
    config.generate_r()
    poly.generate_poly()
    table.generate(pwd, stat)


def main():
    initialize()
    while reader.has_next():
        pwd, feature = reader.next_login()
        h_pwd_ = poly.get_h_pwd(table.extract(pwd, feature))
        if history.decrypt(h_pwd_):
            print 1
            update(pwd, feature)
        else:
            if correction(pwd, feature):
                print 1
                update(pwd, feature)
            else:
                print 0


if __name__ == "__main__":
    main()
