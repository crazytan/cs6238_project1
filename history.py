# history class

import config
import crypt


history_features = []
history_features_str = []


# initialize the history file
def init():
    history_file = open('history.dat', 'w+')
    for i in xrange(config.history_size):
        features = []
        for j in xrange(config.max_features):
            features.append(None)
        features_string = to_string(features)
        history_file.writeline(features_string)
    history_file.close()


# save the history file to disk
def save():
    global history_features
    features_str = to_string(history_features)
    history_file = open('history.dat', 'w')
    history_file.write(features_str)
    history_file.close()


# read the history file from disk
def read():
    history_file = open('history.dat', 'r')
    history_file_content = history_file.read()
    history_file.close()
    return history_file_content


# try to decrypt the history file using the password
def decrypt(history_cypher, h_pwd_):
    history_message = crypt.decrypt(history_cypher, h_pwd_)
    global history_features_str
    history_features_str = history_message.split(';')
    total_len = 0
    for i in xrange(len(history_features_str)):
        total_len += len(history_features_str[i])
    if total_len != (config.feature_length + 1) * config.max_features * config.history_size:  # wrong length
        return 0
    if len(history_features_str) == 5:  # no padding
        global history_features
        history_features = from_string(history_features_str)
        return 1
    else:
        if len(history_features_str) == 6:
            len_of_last = len(history_features_str[5])  # length of padded part
            pad_str = '0' * len_of_last
            if history_features_str[5] == pad_str:
                history_features_str = history_features_str[:5]  # remove padded '0'
                global history_features
                history_features = from_string(history_features_str)
                return 1
            else:
                return 0
        else:
            return 0


# add new feature to history
def add_feature(feature):
    global history_features
    history_features.append(feature)
    history_features = history_features[:5]


# int to string
def to_string(features):
    features_string = ''
    for i in xrange(len(features)):
        for j in xrange(len(features[i])):
            features_string += str(features[i][j]) + ','
        features_string = features_string[:-1] + ';'
    # pad features_string to fixed size
    print len(features_string)
    if len(features_string) < (config.feature_length + 1) * config.max_features * config.history_size:
        features_string += '0' * ((config.feature_length + 1) * config.max_features * config.history_size - len(features_string))
    return features_string


# string to int
def from_string(features_str):
    features = []
    features_str_arr = features_str.split(';')
    for i in xrange(len(features_str_arr)):
        feature_str = features_str_arr[i].split(',')
        feature = []
        for j in xrange(len(feature_str)):
            feature.append(int(feature_str[j]))
        features.append(feature)
    return features


# test
if __name__ == "__main__":
    test_features = [[1, 2, 3], [3, 4, 5], [4, 5, 6]]
    test_features_str = to_string(test_features)
    # print test_features_str
    # print len(test_features_str)
    features_from_str = from_string(test_features_str)
    print features_from_str
