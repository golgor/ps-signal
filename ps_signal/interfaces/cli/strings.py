welcome = "Python script for performing FFT and plotting \
           .csv data aquired from a Picoscope."

file = "Path to the file containting the data in .csv format."
interval = "The interval in the data you want to analyze."
fft = "Apply fft on the signal."
lowpass = "Apply low pass filter to the signal. Effectively removing \
                frequencies that is higher than the cutoff. Cutoff \
                given in Hz."
highpass = "Apply high pass filter to the signal. Effectively \
                 removing frequencies that is lower than the cutoff. \
                 Cutoff given in Hz."
bandstop = "Apply band stop filter to the signal. Effectively removing \
                 frequencies that is between the specified frequencies. \
                 Cutoff given in Hz."
bandpass = "Apply band pass filter to the signal. Effectively removing \
                 all frequencies that is not between the specified \
                 frequencies. Cutoff given in Hz."
output = "Folder for output. Note: Not a file but a folder as this \
               script will output several files."
title = "Title that will be applied to the plot."
version = "Shows the current version of this package."
