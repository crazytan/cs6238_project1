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


def initialize():
    config.init_random()
    config.generate_prime()
    config.generate_h_pwd()
    poly.generate_poly()
    pwd = reader.init(raw_input())
    table.generate(pwd)
    history.init()


# Simple error correction
def correction(pwd, feature):
    coordinates = table.extract(pwd, feature)
    for i in xrange(len(feature)):
        coordinates_ = coordinates
        coordinates_[i] = table.extract_at(pwd, feature, i)
        h_pwd_ = poly.get_h_pwd(coordinates_)
        if history.decrypt(h_pwd_):
            history.add_feature(feature)
            return 1
        else:
            if i == len(feature) - 1:
                return 0


def main():
    initialize()
    while reader.has_next():
        pwd, feature = reader.next_login()
        h_pwd_ = poly.get_h_pwd(table.extract(pwd, feature))
        if history.decrypt(h_pwd_):
            print 1
            history.add_feature(feature)
        else:
            if correction():
                print 1
            else:
                print 0


if __name__ == "__main__":
    main()
