# helper module for reading login file

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


# if there is still any login to process
def has_next():
    return current < len(attempts)


# return the next login attempt
def next_login():
    global current
    current += 1
    return attempts[current - 1]
