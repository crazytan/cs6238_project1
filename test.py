import random

f = open('test.in', 'w')
pwd = 'password'
random.seed()

for i in xrange(100):
    f.write(pwd)
    f.write('\n')
    tmp = []
    for j in xrange(20):
        tmp.append(str(random.randrange(-5,15)))
    f.write(','.join(tmp))
    f.write('\n')

f.close()
