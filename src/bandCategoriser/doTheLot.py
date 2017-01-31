import os

os.system("python data_collection.py")
os.system("python split_into_train_and_test.py")
os.system("python fourier_transform.py")
os.system("python predicting_band_frequencies.py")
