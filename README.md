# Picoscope Signal Analyzer
Module used to import .csv files made form a pico scope and analyse the data.

## How to install
Currently no install needed, simply download and follow steps below.

## How to use
This is a script using a Command Line Interface (CLI). Run the script by invoking:

```
$ python py_signal
```

### Mandatory arguments
* file - The path to a file containing data that have been exported to a .csv from the software Picoscope. The file have to be in the following format:

```
Time;Channel A
(ms);(mV)

-200,00015929;-0,21362960
-200,00004729;-0,73854790
```

### Optional argument
* -h, --help - Showing a help message with all the available arguments.
* -i lower upper - Set an interval in the x-axis (time). This can be used to isolate parts of a signal that is of interest.
* -fff - Used to invoke running a FFT on the given signal.
* -lp cutoff - Applying a low pass filter on the signal. Can be used to remove high frequency disturbances.
* -hp cutoff - Applying a high pass filter on the singal. Can be used to remove low frequency disturbances.
* -bs lower upper - Applying a band stop filter on the signal. Can be used to remove disturbances that is defined by a band in the frequency spectrum.
* -o - Can be used to set an alternative output folder.

# Data files
This module will work with .csv files as exported from PicoScope 6.14.x.

### Other
Using pipreqs to generate requirements.txt
