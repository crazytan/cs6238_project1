# history class

import config
import crypt
import math

history_features = []
# history_features_str = []


# initialize the history file
def init():
    global history_features
    history_features = [['$$$' for j in xrange(config.max_features)] for i in xrange(config.history_size)]
    save()


# save the history file to disk
def save():
    global history_features
    features_str = to_string(history_features)
    features_str_cypher = crypt.encrypt(features_str, config.h_pwd)
    with open('history.dat', 'w') as file:
        file.write(features_str_cypher)


# read the history file from disk
def read():
    with open('history.dat', 'r') as file:
        history_file_content = file.read()
    return history_file_content


# try to decrypt the history file using the password
def decrypt(h_pwd_):
    history_message = crypt.decrypt(read(), h_pwd_)
    if len(history_message) != (config.feature_length + 1) * config.max_features * config.history_size + config.redundancy_len:  # wrong length
        if config.debug: print 'a'
        return False
    # global history_features_str
    history_features_str = history_message.split(';')
    global history_features
    if len(history_features_str) == 6:
        len_of_last = len(history_features_str[5])  # length of padded part
        pad_str = '0' * len_of_last
        if history_features_str[5] == pad_str:
            # history_features_str = history_features_str[:5]  # remove padded '0'
            history_features = from_string(history_message)
            return True
        else:
            if config.debug: print 'b'
            return False
    else:
        if config.debug:
            print 'c'
            print len(history_features_str)
        return False


# calculate mean and standard deviation for a feature
def cal_sigma_mu(feature):
    sum = 0
    cnt = 0
    _any = False
    for f in feature:
        if isinstance(f, int):
            sum += f
            cnt += 1
            _any = True
    if not _any:
        return None, None
    # if cnt < 5:
    #     return None, None
    mu = float(sum) / cnt
    sum = 0
    for f in feature:
        if isinstance(f, int):
            sum += (f - mu) * (f - mu)
    sigma = math.sqrt(sum / cnt)
    return sigma, mu


# add new feature to history
def add_feature(feature):
    if len(feature) < config.max_features:
        feature.extend(['$$$' for i in xrange(config.max_features - len(feature))])
    global history_features
    if history_features:
        history_features.append(feature)
        history_features = history_features[1:]
        stat = []
        for i in xrange(config.max_features):
            stat.append(cal_sigma_mu([history_features[j][i] for j in xrange(config.history_size)]))
        save()
        if not config.debug:
            history_features = [] # erase the data in memory
        return stat
    else:
        raise ValueError("history not decrypted yet!")


# serialize the feature history
def to_string(features):
    features_string = ''
    for i in xrange(len(features)):
        for j in xrange(len(features[i])):
            features_string += str(features[i][j]) + ','
        features_string = features_string[:-1] + ';'
    # pad features_string to fixed size
    features_string += '0' * ((config.feature_length + 1) * config.max_features * config.history_size - len(features_string) + config.redundancy_len)
    # if len(features_string) < (config.feature_length + 1) * config.max_features * config.history_size:
    #     features_string += '0' * ((config.feature_length + 1) * config.max_features * config.history_size - len(features_string))
    return features_string


# deserialize the feature history
def from_string(features_str):
    features = []
    features_str_arr = features_str.split(';')
    features_str_arr = features_str_arr[:5]
    for i in xrange(len(features_str_arr)):
        feature_str = features_str_arr[i].split(',')
        feature = []
        for j in xrange(len(feature_str)):
            if feature_str[j] == '$$$':
                feature.append('$$$')
            else:
                feature.append(int(feature_str[j]))
        features.append(feature)
    return features


if __name__ == "__main__":
    config.init_random()
    config.generate_r()
    config.generate_prime()
    config.max_features = 10

    # test init()
    init()
    print decrypt(config.h_pwd)

    # test add_feature()
    test_feature = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print "statistics: ", add_feature(test_feature)
    print "history features: ", history_features
    print decrypt(config.h_pwd)
    print "statistics: ", add_feature(test_feature[::-1])
    print "history features: ", history_features
    print decrypt(config.h_pwd)
