# Project 1 for CS6238
# Implements password hardening as described in the paper
# Author:
#   Jia Tan, tanjia@gatech.edu
#   Zenong Lu, kardlu@gatech.edu


import login_reader as reader
import instruction_table as table
import history


def initialize():
    reader.init(raw_input())
    table.init()
    history.init()


def main():
    initialize()
    while reader.has_next():
        pass


if __name__ == "__main__":
    main()
