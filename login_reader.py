# helper class for reading login file

# list for all login attempts
attempts = []

# next login attempt to process
current = 0


def init(input_file):
    # read the input file and store the login information in global variables
    with open(input_file, 'r') as login:
        lines = login.readlines()
        for i in range(len(lines) / 2):
            pwd = lines[i * 2].strip()
            feature = map(lambda x: int(x), lines[i * 2 + 1].strip().split(','))
            global attempts
            attempts.append((pwd, feature))


def has_next():
    # if there is still any login to process
    return current < len(attempts)


def next_login():
    # return the next login attempt
    global current
    current += 1
    return attempts[current - 1]
