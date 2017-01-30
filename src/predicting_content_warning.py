import mxnet as mx
import numpy
from numpy import ndarray

from reading_music import read_mp3

train = open('training_data.csv', 'r')
trainLabels=[]
trainMp3Content = ndarray((10,1000))
i=0
while i<10:
    line = train.readline()
    lineSplit = line.split(",")
    trainLabels.append(1 if lineSplit[2] == 'True' else 0)
    musicUrl = lineSplit[3][:-1]
    music = read_mp3(musicUrl)
    musicNPArray = numpy.asarray(music[0:1000, 1])
    musicToAppend = musicNPArray.transpose()
    trainMp3Content[i,:] = musicToAppend
    i += 1


test = open('test_data.csv', 'r')
testLabels=[]
testMp3Content = ndarray((10,1000))
i=0
while i<10:
    line = test.readline()
    lineSplit = line.split(",")
    testLabels.append(1 if lineSplit[2] == 'True' else 0)
    musicUrl = lineSplit[3][:-1]
    music = read_mp3(musicUrl)
    musicNPArray = numpy.asarray(music[0:1000, 1])
    musicToAppend = musicNPArray.transpose()
    trainMp3Content[i,:] = musicToAppend
    i += 1

batch_size = 3;
trainLabelsArray = numpy.asarray(trainLabels)
train_iter = mx.io.NDArrayIter(trainMp3Content, trainLabelsArray, batch_size, shuffle=True)
test_iter = mx.io.NDArrayIter(testMp3Content, numpy.asarray(testLabels), batch_size, shuffle=True)



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
