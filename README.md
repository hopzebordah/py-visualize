# py-visualize
a python program to visualize the frequency of the sound of a WAVE file

# IMPORTANT
this programs depends on python3 and the following python modules:
  numpy   - to handle values returned from scipy
  scipy   - for fast fourier transform function to convert to frequency domain
  pygame  - to play audio because playing wav files in python is a pain and pygame makes it easy
  tkinter - for graphics

this program expects to find a WAVE file in sys.argv[1], so to execute from the command line, 
I would use something like this:

  python3 fftSoundVisualizerStereo.py audio/song.wav
  
where fftSoundVisualizer is the script and audio is a local directory that contains some stereo wav file.

