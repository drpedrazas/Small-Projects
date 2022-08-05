import sys, os
import time, random
import wave, argparse, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt

Notes = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}

def writeWAVE(fname, data):
    file = wave.open(fname, 'wb')
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE','noncompressed'))
    file.writeframes(data)
    file.close()

def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    buf = deque([random.random() - 0.5 for i in range(N)])
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()
    samples = np.array(samples*32767, 'int16')
    return samples.tobytes()

class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.notes = {}

    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + ' not dound!')
    def playRandom(self):
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()

def main():
    parser = argparse.ArgumentParser(description= "Música con Karplus")
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    args = parser.parse_args()
    nplayer = NotePlayer()
    print('creating notes...')
    for name, freq in list(Notes.items()):
        fileName = name + '.wav'
        if os.path.exists(fileName):
            data = generateNote(freq)
            print('creating'+fileName+'...')
            writeWAVE(fileName, data)
        else:
            print('fileName already created. skipping...')
        nplayer.add(name+'.wav')
        if args.play:
            while True:
                try:
                    nplayer.playRandom()
                    rest = np.random.choice([1,2,4,8], 1, p=[0.15,0.7,0.1,0.05])
                    time.spleep(0.25*rest[0])
                except KeyboardInterrupt:
                    exit()
        if args.piano:
            while True:
                for event in pygame.event.get():
                    if(event.type == pygame.KEYUP):
                        print("key pressed")
                        nplayer.playRandom()
                        time.sleep(0.5)

#We generate notes
gnotes = {i : generateNote(j) for i, j in Notes.items()}
#We put them together
exp = np.append([], [j for i,j in gnotes.items()])
#We create a new file
writeWAVE('test',exp)
#let's make som music with the fibonacci numbers
fibonacci = [1,1]
while len(fibonacci) < 50:
    fibonacci.append(fibonacci[-2]+fibonacci[-1])
notes_places = [i for i,j in Notes.items()]
song_sheet0 = [notes_places[i % len(notes_places)] for i in fibonacci]
print(song_sheet0)
song_sheet = [Notes[notes_places[i % len(notes_places)]] for i in fibonacci]
song_data = np.append([],[generateNote(i) for i in song_sheet])
writeWAVE('fib', song_data)
