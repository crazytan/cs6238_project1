# parameter configuration

from gmpy2 import mpz
import gmpy2
import random

# size of history file
history_size = 5

# maximum number of distinguishing features
max_features = 127

# maximum length of single feature
feature_length = 3

k = 2

ti = 10

r = 0


# generate r
def generate_r():
    global r
    r = mpz(generate_rand())

# hardened password
h_pwd = mpz()

# instance of Random class
rand = None


# initiate rand
def init_random():
    global rand
    rand = random.Random()
    rand.seed()


# generate a q_size bit long random integer
def generate_rand():
    return mpz(rand.getrandbits(q_size))


# randomly generate a hardened password
def generate_h_pwd():
    global h_pwd
    h_pwd = gmpy2.t_mod(generate_rand(), q)

# prime
q = mpz()

# prime size
q_size = 160


# randomly generate a 160 bit prime
def generate_prime():
    global q
    q = generate_rand()
    while not gmpy2.is_prime(q):
        q = generate_rand()
    q = mpz(q)
