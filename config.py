# parameter configuration

import gmpy2
import random

# size of history file
history_size = 5

# maximum number of distinguishing features
max_features = 127

k = 2

ti = 10

# hardened password
h_pwd = 0


# instance of Random class
rand = None


# initiate rand
def init_random():
    global rand
    rand = random.Random()
    rand.seed()


# generate a q_size bit long random integer
def generate_rand():
    return rand.getrandbits(q_size)


# randomly generate a hardened password
def generate_h_pwd():
    global h_pwd
    h_pwd = generate_rand()
    while h_pwd >= q:
        h_pwd = generate_rand()


# prime
q = 0


# prime size
q_size = 160


# randomly generate a 160 bit prime
def generate_prime():
    global q
    q = generate_rand()
    while not gmpy2.is_prime(q):
        q = generate_rand()
