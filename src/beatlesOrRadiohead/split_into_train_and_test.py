import random

f = open('sample_band_data_2.csv', 'r')
test = open('sample_band_data_test.csv', 'w')
train = open('sample_band_data_train.csv', 'w')

f.readline()

for line in f:
    if random.random()<0.05:
        test.write(line)
    else:
        train.write(line)