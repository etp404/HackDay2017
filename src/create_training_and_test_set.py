import random

f = open('sample_data.csv', 'r')
test = open('test_data.csv', 'w')
train = open('training_data.csv', 'w')

f.readline()

for line in f:
    if random.random()<0.05:
        test.write(line)
    else:
        train.write(line)
