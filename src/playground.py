from reading_music import read_mp3

mp3Location = 'http://cdn-preview-d.deezer.com/stream/dbe5bb0dd6ab92c7bd96f67e336b56f9-3.mp3'


audio_array = read_mp3(mp3Location)

import pygame
pygame.init()
pygame.mixer.init(44100, -16, 1) # 44100 Hz, 16bit, 2 channels
sound = pygame.sndarray.make_sound( audio_array )
sound.play()

print("playing")
