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
    config.generate_prime()
    config.generate_h_pwd()
    poly.generate_poly()
    if __debug__:
        pwd = reader.init("input.txt")
    else:
        pwd = reader.init(raw_input("enter the input file: "))
    table.generate(pwd, None)
    history.init()


# Simple error correction
def correction(pwd, feature):
    coordinates = table.extract(pwd, feature)
    for i in xrange(len(feature)):
        tmp = coordinates[i]  # save the original coordinate
        coordinates[i] = table.extract_at(pwd, feature, i)  # extract the other entry from table
        h_pwd_ = poly.get_h_pwd(coordinates)
        if history.decrypt(h_pwd_):
            return True
        coordinates[i] = tmp  # restore the original coordinate
    return False


# update the history file and instruction table after successful login
def update(pwd, feature):
    config.generate_h_pwd()  # generate the new h_pwd
    stat = history.add_feature(feature)  # add the new feature to history file and save it
    poly.generate_poly()  # generate the new polynomial
    table.generate(pwd, stat)  # generate the new table


def main():
    initialize()
    while reader.has_next():  # if there is still login attempts to process
        pwd, feature = reader.next_login()
        h_pwd_ = poly.get_h_pwd(table.extract(pwd, feature))  # use the coordinates extracted from table to get h_pwd
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
