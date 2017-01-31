import numpy
import scipy.fftpack
import matplotlib.pyplot as plt
from scipy.signal import decimate
import csv

from reading_music import read_mp3


def drawTransform(signal):
    fig, ax = plt.subplots()
    ax.plot(signal)
    plt.show()

def fourier_transform(input):
    pureTransform = scipy.fftpack.fft(input)
    transform = abs(pureTransform)[:len(pureTransform) // 2]
    decimated = decimate(transform, 10)
    decimated = decimate(decimated, 10)
    return decimated


def read_and_transformMp3(input):
    return fourier_transform(read_mp3(input)[:,0])

testDataFile = open('sample_band_data_test.csv', 'r')
transformedMusicFile = open('transformed_sample_band_data_test.csv', 'w')
csv_writer = csv.writer(transformedMusicFile)
totalNumber = sum(1 for row in testDataFile)
testDataFile.seek(0)
i = 0;
for line in testDataFile:
    lineSplit = line.split(",")
    print "Transforming test line " + str(i) + " of " + str(totalNumber)
    if lineSplit[1] == 'The Beatles':
        label = 1
    elif lineSplit[1] == 'Radiohead':
        label = 0
    else:
        continue
    musicUrl = lineSplit[2][:-1]
    transformedMusic = read_and_transformMp3(musicUrl)
    lineToWrite = numpy.insert(transformedMusic, 0, label)
    csv_writer.writerow(lineToWrite)
    i+=1;
transformedMusicFile.close()
testDataFile.close()


trainDataFile = open('sample_band_data_train.csv', 'r')
transformedMusicFile = open('transformed_sample_band_data_train.csv', 'w')
csv_writer = csv.writer(transformedMusicFile)
totalNumber = sum(1 for row in trainDataFile)
trainDataFile.seek(0)
i=0
for line in trainDataFile:
    lineSplit = line.split(",")
    print "Transforming training line " + str(i) + " of " + str(totalNumber)
    if lineSplit[1] == 'The Beatles':
        label = 1
    elif lineSplit[1] == 'Radiohead':
        label = 0
    else :
        continue
    musicUrl = lineSplit[2][:-1]
    transformedMusic = read_and_transformMp3(musicUrl)
    lineToWrite = numpy.insert(transformedMusic, 0, label)
    csv_writer.writerow(lineToWrite)
    i+=1
transformedMusicFile.close()
trainDataFile.close()
