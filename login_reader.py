# helper module for reading login file

from gmpy2 import mpz
import config

# list for all login attempts
attempts = []

# next login attempt to process
current = 0


# read the input file and store the login information in global variables
def init(input_file):
    with open(input_file, 'r') as login:
        lines = login.readlines()
        for i in range(len(lines) / 2):
            pwd = lines[i * 2].strip()
            feature = map(lambda x: int(x), lines[i * 2 + 1].strip().split(','))
            global attempts
            attempts.append((pwd, feature))
    return attempts[0][0]


# if there is still any login to process
def has_next():
    return current < len(attempts)


# return the next login attempt
def next_login():
    global current
    current += 1
    return attempts[current - 1]


# return if still in initialization stage
def if_init():
    return current < config.history_size

if __name__ == "__main__":
    assert "CorrectPassword" == init("input.txt"), "init pwd error!"
    i = 0
    while has_next():
        i += 1
        if i <= 5:
            assert if_init(), "initialization message error!"
        else:
            assert not if_init(), "initialization message error!"
        pwd, feature = next_login()
        assert type(pwd) == str
        assert type(feature) == list
