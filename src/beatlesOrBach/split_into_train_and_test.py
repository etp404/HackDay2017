import random

f = open('sample_band_data.csv', 'r')
test = open('sample_band_data_test.csv', 'w')
train = open('sample_band_data_train.csv', 'w')
untouched = open('sample_band_data_untouched.csv', 'w')

f.readline()

for line in f:
    random_random = random.random()
    if random_random <0.05:
        test.write(line)
    elif random_random < 0.1:
        untouched.write(line)
    else:
        train.write(line)