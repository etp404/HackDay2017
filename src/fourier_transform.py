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

# drawTransform(read_and_transformMp3("/Users/Matt/Downloads/DTMF-3.mp3"));
# drawTransform(read_and_transformMp3("/Users/Matt/Downloads/mp3tones/440Hz-5sec.mp3"));
# drawTransform(read_and_transformMp3("http://cdn-preview-9.deezer.com/stream/907bfbaed6eef6ccc70ce3dcbec4e86f-5.mp3"));

testDataFile = open('test_data.csv', 'r')
transformedMusicFile = open('transformed_test_data.csv', 'w')
csv_writer = csv.writer(transformedMusicFile)
totalNumber = sum(1 for row in testDataFile)
testDataFile.seek(0)
i = 0;
# for line in testDataFile:
#     lineSplit = line.split(",")
#     print "Transforming test line " + str(i) + " of " + str(totalNumber)
#     year = lineSplit[1]
#     label = 1 if lineSplit[2] == 'True' else 0
#     musicUrl = lineSplit[3][:-1]
#     transformedMusic = read_and_transformMp3(musicUrl)
#     lineToWrite = numpy.insert(transformedMusic, 0, label)
#     lineToWrite = numpy.insert(lineToWrite, 0, year)
#     csv_writer.writerow(lineToWrite)
#     i+=1;
# transformedMusicFile.close()
# testDataFile.close()


trainDataFile = open('training_data.csv', 'r')
transformedMusicFile = open('transformed_training_data.csv', 'wa')
csv_writer = csv.writer(transformedMusicFile)
totalNumber = sum(1 for row in trainDataFile)
trainDataFile.seek(0)
i=0
for line in trainDataFile:
    while i<5627:
        i+=1
        continue
    lineSplit = line.split(",")
    print "Transforming training line " + str(i) + " of " + str(totalNumber)
    year = lineSplit[1]
    label = 1 if lineSplit[2] == 'True' else 0
    musicUrl = lineSplit[3][:-1]
    try:
        transformedMusic = read_and_transformMp3(musicUrl)
        lineToWrite = numpy.insert(transformedMusic, 0, label)
        lineToWrite = numpy.insert(lineToWrite, 0, year)
        csv_writer.writerow(lineToWrite)
        i+=1
    except ValueError:
        continue

transformedMusicFile.close()
trainDataFile.close()
