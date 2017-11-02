'''
Alex Peters - fftSoundVisualizer
Requires numpy, scipy, tkinter, pygame to be installed
To run, specify the file location of a wav file in sys.argv[1]
i.e.:
    python3 fftSoundVisualizer.py audio/intro.wav
'''

from scipy.io import wavfile
from scipy.fftpack import fft
import numpy, sys
import math, pygame, time
from tkinter import *

def getFFT(filename):
    ''' Get FFT function takes a .wav filename and a framerate
        and returns an array of frequency values at the
        specified framerate per second. 
    '''
    try:
        rate, data = wavfile.read(filename)
    except:
        sys.exit('***ERROR: Could not read input. Check format of audio file, and try again.')

    data = numpy.abs(fft(data)) 

    try: 
        if not len(data[0]) == 2:
            sys.exit('***ERROR: Input.wav must be stereo.')
    except:
        sys.exit('***ERROR: Input .wav must be stereo.')   
   
    return (rate, data)

def playMusicWithPygameMixer(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

class VisualizerData(object):
    ''' Creates an object that holds all the info needed to be used by a sound visualizer. 
        Can easily be extended to accomplish this task.
    ''' 
    def __init__(self, filename, framerate, sensitivity, dimensions):
        ''' Requires non-optional filename, framerate, sensitivity, and dimensions tuple '''
        # instance-specific variables
        self._filename = filename
        self._framerate = framerate
        self._sensitivity = 1500 // sensitivity
        self._dimensions = dimensions
        self._width = dimensions[0] ; self._height = dimensions[1]
        self._rate, self._freqArray = getFFT(filename)
        self._freqArrayLength = len(self._freqArray)

        # default variable values
        self._frequency = 0
        self._black = (0, 0, 0)
        self._white = (255, 255, 255)            

class CircleVisualizerTkinter(VisualizerData):
    ''' Extends VisualizerData class to create a functioning visualizer with Tkinter '''
    def __init__(self, filename, framerate=60, sensitivity=3, dimensions=(200, 200), dual=True):
        ''' Requires non-optional filename and optional framerate, sensitivity, and dimensions tuple '''
        VisualizerData.__init__(self, filename, framerate, sensitivity, dimensions)
        self._initializeDisplay()
        self._dual = dual
        self._centerX = self._width // 2 ; self._centerY = self._height // 2
        self._quarterTwoX = self._centerX // 2
        self._quarterTwoY = self._centerY // 2
        self._quarterThreeX = self._quarterTwoX + self._centerX
        self._quarterThreeY = self._quarterTwoY + self._centerY

        if dual: self._y1 = self._quarterThreeY ; self._y2 = self._quarterTwoY
        else: self._y1 = self._centerY

        self._msToWait = 1000//self._framerate

    def _initializeDisplay(self):
        self._window = Tk()
        self._window.title('Circle Visualizer: ' + self._filename)
        self._window.resizable(False, False)
        self._canvas = Canvas(self._window, width=self._width, height=self._height)
        self._canvas.pack()
    
    def _updateWindow(self):
        end = time.time()
        elapsed = end - self._start
        
        if elapsed * self._rate < self._freqArrayLength:
            radius1 = self._freqArray[int(elapsed * self._rate)][0] / self._sensitivity
            if self._dual:
                radius2 = self._freqArray[int(elapsed * self._rate)][1] / self._sensitivity

            self._wipeScreen()
            self._drawCircle(self._centerX, self._y1, radius1, 'black')
            if self._dual:
                self._drawCircle(self._centerX, self._y2, radius2, 'black')

            self._canvas.after(self._msToWait, self._updateWindow)
        else:
            print('Total time elapsed (s):', elapsed)
            self._window.destroy()
            sys.exit()

    def play(self):
        ''' Once object is initialized, play() starts the visualizer gui '''
        self._start = time.time()
        playMusicWithPygameMixer(self._filename)
        self._updateWindow()
        self._window.mainloop()   

    def _wipeScreen(self):
        self._canvas.delete(ALL)

    def _fillBackground(self):
        self._canvas.create_rectangle(0, 0, self._width, self._height, fill='black')
    
    def _drawCircle(self, x, y, radius, color='white'):
        self._canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        CircleVisualizerTkinter(filename, framerate=60, dimensions=(500, 700), dual=True).play()
    else:
        print('***ERROR: Did not find an audio file location in cli parameters.')

if __name__ == '__main__':
    main()
