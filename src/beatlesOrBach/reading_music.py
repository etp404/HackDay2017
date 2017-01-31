import subprocess as sp


def read_mp3(mp3Location):
    print(mp3Location)
    global audio_array
    command = ["/usr/local/bin/ffmpeg",
               '-i', mp3Location,
               '-f', 's16le',
               '-acodec', 'pcm_s16le',
               '-ar', '44100',  # ouput will have 44100 Hz
               '-ac', '1',  # stereo (set to '1' for mono)
               '-']
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
    raw_audio = pipe.stdout.read(882000 * 4)
    import numpy
    audio_array = numpy.fromstring(raw_audio, dtype="int16")
    audio_array = audio_array.reshape((len(audio_array) / 2, 2))
    return audio_array;