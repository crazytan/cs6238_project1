# history class

import config

m = 64  # maximum password length


# initialize the history file
def init():
    history_file = open('history.dat', 'w+')
    for i in xrange(config.history_size):
        features = []
        for j in xrange(config.max_features):
            features.append(None)
        features_string = to_string(features)
        history_file.writeline(features_string)


# save the history file to disk
def save():
    pass


# read the history file from disk
def read():
    pass


# try to decrypt the history file using the password
def decrypt(h_pwd_):
    pass


# add new feature to history
def add_feature(feature):
    pass


def to_string(features):
    features_string = ''
    for i in xrange(len(features)):
        features_string += str(features[i]) + ','
    features_string += ';'
    return features_string
