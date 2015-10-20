# history class

import config
import crypt
import math

history_features = []
# history_features_str = []


# initialize the history file
def init():
    global history_features
    history_features = [['$$$' for j in xrange(config.max_features)] for i in xrange(config.history_size)]  # pad '$$$' as initial features
    save()


# save the history file to disk
def save():
    global history_features
    features_str = to_string(history_features)
    features_str_cypher = crypt.encrypt(features_str, config.h_pwd)  # encrypt history features before write to disk
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
    if len(history_message) != config.history_file_len:  # wrong length
        if __debug__: print 'a'
        return False
    history_features_str = history_message.split(';')
    global history_features
    if len(history_features_str) == 6:  # verify if there are 5 groups of features
        for i in xrange(5):
            if len(history_features_str[i].split(',')) != config.max_features:
                return False
        pad_str = '0' * len(history_features_str[5])  # length of padded part
        if history_features_str[5] == pad_str:  # check if redundant part is string of '0'
            history_features = from_string(history_message)  # extract history features
            return True
        else:   # decryption failed
            if __debug__: print 'b'
            return False
    else:   # decryption failed
        if __debug__:
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
    if not _any:    # still in init stage
        return None, None
    mu = float(sum) / cnt
    sum = 0
    for f in feature:
        if isinstance(f, int):
            sum += (f - mu) * (f - mu)
    if cnt > 1:
        sigma = math.sqrt(sum / cnt)
    else:
        sigma = 0
    return sigma, mu


# add new feature to history
def add_feature(feature):
    if len(feature) < config.max_features:
        feature.extend(['$$$' for i in xrange(config.max_features - len(feature))])  # pad features to max_features
    global history_features
    if history_features:
        history_features.append(feature)
        history_features = history_features[1:]  # remove the oldest group of features
        stat = []
        for i in xrange(config.max_features):
            stat.append(cal_sigma_mu([history_features[j][i] for j in xrange(config.history_size)]))  # calculate new sigma & mu
        save()
        if not __debug__:
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
    features_string += '0' * (config.history_file_len - len(features_string))  # pad features_string to fixed size
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
            if feature_str[j] == '$$$':  # padded part
                feature.append('$$$')
            else:
                try:
                    feature.append(int(feature_str[j]))
                except ValueError:
                    if __debug__:
                        f = open('error.txt', 'w')
                        f.write(features_str)
                        f.write('\n')
                        f.write(features_str_arr[i])
                        f.write('\n')
                        f.write(feature_str[j])
                        f.write('\n')
                        f.close()
                    raise
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
