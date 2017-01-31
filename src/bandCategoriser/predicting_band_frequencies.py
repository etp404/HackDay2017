import csv

import mxnet as mx
import numpy
from numpy import ndarray

artistMap = {}
artistsToClassify = csv.reader(open("artists.csv"))
for artist in artistsToClassify:
    artistMap[float(artist[1])] = artist[2]

csv_reader_test = csv.reader(open('transformed_sample_band_data_train.csv', 'r'))
trainLabels=[]
spectrumSize = 338688
trainMp3Content = ndarray((0, spectrumSize))
i=0
for row in csv_reader_test:
    trainLabels.append(float(row[0]))
    trainAsarray = numpy.asarray(row[1:], float)
    trainNormalisedArray= numpy.divide(trainAsarray, max(trainAsarray))

    if (trainNormalisedArray.shape != (spectrumSize,)):
        print "Weirdly shaped item: " + str(trainNormalisedArray.shape)
        continue
    trainNormalisedArray = trainNormalisedArray.reshape(1, spectrumSize)
    trainMp3Content = numpy.append(trainMp3Content, trainNormalisedArray, 0)

print ("training data read in")
csv_reader_train = csv.reader(open('transformed_sample_band_data_test.csv', 'r'))
testLabels=[]
testMp3Content = ndarray((0, spectrumSize))
i=0
for row in csv_reader_train:
    testLabels.append(float(row[0]))
    testAsarray = numpy.asarray(row[1:], float)
    testNormalisedArray= numpy.divide(testAsarray, max(testAsarray))
    if (testNormalisedArray.shape != (spectrumSize,)):
        print "Weirdly shaped item: " +str(testNormalisedArray.shape)
        continue
    testNormalisedArray = testNormalisedArray.reshape(1, spectrumSize)
    testMp3Content = numpy.append(testMp3Content, testNormalisedArray, 0)


print "Chance validation level: " + str(1-sum(testLabels)/len(testLabels) )

batch_size = 3;
trainLabelsArray = numpy.asarray(trainLabels)
train_iter = mx.io.NDArrayIter(trainMp3Content, trainLabelsArray, batch_size, shuffle=True)

testLabelsArray = numpy.asarray(testLabels)
test_iter = mx.io.NDArrayIter(testMp3Content, testLabelsArray, batch_size, shuffle=True)

# Create a place holder variable for the input data
data = mx.sym.Variable('data')
# Flatten the data from 4-D shape (batch_size, num_channel, width, height)
# into 2-D (batch_size, num_channel*width*height)
data = mx.sym.Flatten(data=data)

# The first fully-connected layer
fc1  = mx.sym.FullyConnected(data=data, name='fc1', num_hidden=128)
# Apply relu to the output of the first fully-connnected layer
act1 = mx.sym.Activation(data=fc1, name='relu1', act_type="relu")

# The second fully-connected layer and the according activation function
fc2  = mx.sym.FullyConnected(data=act1, name='fc2', num_hidden = 64)
act2 = mx.sym.Activation(data=fc2, name='relu2', act_type="relu")
#
# The thrid fully-connected layer, note that the hidden size should be 10, which is the number of unique digits
fc3  = mx.sym.FullyConnected(data=act2, name='fc3', num_hidden=2)
# The softmax and loss layer
mlp  = mx.sym.SoftmaxOutput(data=fc3, name='softmax')
#
# # We visualize the network structure with output size (the batch_size is ignored.)
# shape = {"data" : (batch_size, 1, 28, 28)}
# mx.viz.plot_network(symbol=mlp, shape=shape)
#
# # Output may vary
import logging
logging.getLogger().setLevel(logging.DEBUG)
#
model = mx.model.FeedForward(
    symbol = mlp,       # network structure
    num_epoch = 10,     # number of data passes for training
    learning_rate = 0.1 # learning rate of SGD
)
model.fit(
    X=train_iter,       # training data
    eval_data=test_iter, # validation data
    batch_end_callback = mx.callback.Speedometer(batch_size, 200) # output progress for each 200 data batches
)


print ("untouched data read in")
csv_reader_untouched = csv.reader(open('transformed_sample_band_data_untouched.csv', 'r'))
untouchedLabels=[]
untouchedMp3Content = ndarray((0, spectrumSize))
i=0
for row in csv_reader_untouched:
    untouchedLabels.append(float(row[0]))
    untouchedAsarray = numpy.asarray(row[1:], float)
    untouchedNormalisedArray= numpy.divide(untouchedAsarray, max(untouchedAsarray))
    if (untouchedNormalisedArray.shape != (spectrumSize,)):
        print "Weirdly shaped item: " + str(untouchedNormalisedArray.shape)
        continue
    untouchedNormalisedArray = untouchedNormalisedArray.reshape(1, spectrumSize)
    untouchedMp3Content = numpy.append(untouchedMp3Content, untouchedNormalisedArray, 0)

untouchedLabelsArray = numpy.asarray(untouchedLabels)
untouched_iter = mx.io.NDArrayIter(untouchedMp3Content, untouchedLabelsArray, batch_size, shuffle=True)
print "Final score is  " + str(model.score(untouched_iter))

prob = model.predict(untouchedMp3Content)
j=0
while j<len(prob):
    result = numpy.argmax(prob[j])
    verdict = "SUCCESS"  if result == untouchedLabels[j] else "FAIL"
    actual = artistMap[untouchedLabels[j]]
    predicted = artistMap[result]
    print ("{}: Actual: {}. Predicted : {}".format(verdict, actual, predicted))
    j+=1