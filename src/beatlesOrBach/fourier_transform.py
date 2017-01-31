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
    fourier_transform_result = fourier_transform(read_mp3(input)[:, 0])
    return fourier_transform_result

def transformData(inputDataFileName, transformedDataFileName):
    inputDataFile = open(inputDataFileName, 'r')
    outputDataFile = open(transformedDataFileName, 'w')

    global csv_writer, totalNumber, i, line, lineSplit, musicUrl, transformedMusic, lineToWrite
    csv_writer = csv.writer(outputDataFile)
    totalNumber = sum(1 for row in inputDataFile)
    inputDataFile.seek(0)
    i = 0
    for line in inputDataFile:
        lineSplit = line.split(",")
        print("Transforming line " + str(i) + " of " + str(totalNumber))
        musicUrl = lineSplit[2][:-1]
        transformedMusic = read_and_transformMp3(musicUrl)
        lineToWrite = numpy.insert(transformedMusic, 0, lineSplit[1])
        csv_writer.writerow(lineToWrite)
        i += 1
    outputDataFile.close()
    inputDataFile.close()



transformData('sample_band_data_train.csv', 'transformed_sample_band_data_train.csv')
transformData('sample_band_data_untouched.csv', 'transformed_sample_band_data_untouched.csv')
transformData('sample_band_data_test.csv', 'transformed_sample_band_data_testn.csv')
