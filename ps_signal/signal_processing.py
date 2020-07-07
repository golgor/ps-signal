import sys
import xlrd
from scipy.fft import fft, fftfreq
from scipy import signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(color_codes=True)


class ps_signal:
    """
    Class for importing and analysing signals.

    The signals needs to be imported from a .csv file that is exported
    from the Picoscope software. Several different kind of analyses is
    possible, such as applying filters and performing a FFT.

    Output files will be generated in a .png-format depending on the
    parameters given for each method in this class.
    """

    def __init__(self, filename, id, start_ms=None, length_ms=None):
        """
        Initialization function for the class ps_signal. This function
        reads in the .csv file using pandas.read_csv, clean the data and
        calculate some signal specific parameters such as sampling frequency.

        Args
        ----
        filename : str
                The name of the file to read from. Current working directory
                is assumed.
        id : str
                A string identifier of the signal. This is used to generate
                filenames of output files.
        start : int, optional
                Where to start the analysis of the signal. Data below this
                point is effectively cut out and not analysed at all.
                Value is given in milliseconds. Defaults to 0.
        length : int, optional
                Where to end the analysis of the signal. This is specified
                as the length from the defined start, see above. If not
                specified, length is assumed to be "the rest of the signal".
        """
        try:
            # Formatting of file is separated by ";" and decimals using ","
            # First two rows are headers.
            self._data = pd.read_csv(filename, sep=";", decimal=",",
                                     skiprows=[0, 2])

        # Error if the file was not found.
        except (FileNotFoundError, xlrd.biffh.XLRDError, Exception) as error:
            sys.exit(error)

        # Shift data so it begins from 0 in case
        # data was saved before trigger.
        self._data.columns = ["time", "acc"]
        self.acc = self._data.acc
        self.time = self._data.time - self._data.time.iloc[0]

        # Takes the difference between the first two data
        # points and calculates the time difference.
        # This assumed as the time step and used to calculate
        # sampling frequency and period used for fft.
        # Division by 1000 as data is normally stored in ms
        # instead of seconds. Rounded two the 12th decimal. 8928571
        self._t = round((self.time.iloc[1] - self.time.iloc[0]) / 1000, 12)
        self._fs = int(round(1 / self._t))

        self._drop_data(start_ms, length_ms)

        self._n = len(self._data)
        self.id = str(id)
        self.fft_y = None
        self.filt_x = None
        self._applied_filters = {}

    def _drop_data(self, start_ms, length_ms):
        """
        Internal function used to drop data from the pandas dataframe.
        This is used to isolate certain parts of the signal. I.e. If
        only a small part of the full signal is of interest, this
        function is used to keep only the data of interest.

        Args
        ----
        start_ms : int
                Where the signal of interest starts. Given in ms.
        length_ms : int
                The length of the signal in milliseconds. Given in ms.
        """
        if start_ms:
            # Convert from shift in ms as input from cli
            # to number of samples as the data is stored.
            start = round(start_ms * self._fs / 1000)

            # If start is specified, remove n numbers of rows
            # starting from the beginning.
            self._data.drop(self._data.index[list(range(0, start))],
                            inplace=True)

        if length_ms:
            # Convert from shift in ms as input from cli
            # to number of samples as the data is stored.
            length = round(length_ms * self._fs / 1000)

            # If length is specified, drop everything after
            # length is reached. Used together with "start"
            # to specify a interval.
            self._data.drop(
                self._data.index[list(range(length, len(self._data)))],
                inplace=True
            )

    def plot(self, filename=None, title=None):
        """
        Plotting the imported signal and saves it to disk.

        Args
        ----
        filename : str
                The wanted filename of the output file. If not specified
                the filename prefix will be the same as the id of the signal.
        title : str
                The wanted title of the plot. Defaults to "No title set".
        """
        file_string = self._get_filename(filename)

        if not title:
            title = "Not set"

        plt.figure(figsize=(14, 10))

        plt.plot(self.time, self.acc)
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.title(f"{title}")
        plt.savefig(f"{file_string}.png")
        plt.close()

    # Doing to actual FFT on the signal.
    def _apply_fft(self):
        """
        Internal function to apply the actual FFT on the signal.
        """
        self.fft_y = fft(np.array(self.acc))
        self.fft_x = fftfreq(len(self.fft_y), 1 / self._fs)

    def plot_fft(self, filename=None, title=None, xlim=[10, 1200], ylim=None):
        """
        Performs an FFT of the signal, creates a plot and saves it to disk.

        Args
        ----
        filename : str, optional
                The wanted prefix of the output file. If not specified
                the filename prefix will be the same as the id of the
                signal.
        title : str, optional
                The wanted title of the plot. Defaults to "No title set".
        xlim : [int, int], optional
                A list of integer indicating the wanted range on the x-axis.
                Defaults to 10, 1200. Left limit is set to 10 as to hide the
                fundamental frequency, which usually is not of interest and
                skews the graph.
        ylim : [int, int], optional
                A list of integer indicating the wanted range on the y-axis.
                Defaults to None, which means autoscaling.
        """

        file_string = self._get_filename(filename)

        if not title:
            title = "Not set"

        plt.figure(figsize=(14, 10))

        # Applying actual FFT on the signal.
        self._apply_fft()

        # Using slicing as fft results are both positive and negative.
        # We are only interested in positive. Both fft and fftfreq
        # store positive data in first half of array and negative data
        # data in the second half. Thus we only plot the first
        # half of each. Division by 1000 to get KHz instad of Hz.
        plt.plot(
            self.fft_x[: self._n // 2] / 1000,
            abs(self.fft_y[: self._n // 2])
        )
        plt.xlabel("Frequency (KHz)")
        plt.ylabel("Amplitude")
        plt.title(f"{title}")
        plt.autoscale(enable=True, axis="y", tight=True)
        plt.xlim(xlim)

        if ylim:
            plt.ylim(ylim)

        plt.savefig(f"{file_string}-fft.png")
        plt.close()

    def apply_filter(self, cutoff, order=5, type="low"):
        """
        Apply a filter to the imported signal.

        This function is used to apply four different filters to
        to the signal:
        * Lowpass filter
        * Highpass filter
        * Bandstop filter
        * Bandpass filter by using lowpass- and highpass filter simultaneously

        Args
        ----
        cutoff : float, int or list
                The cutoff frequency for the chosen filter.
                For lowpass- and highpass filters this is a integer
                or float. For bandpass filter this is a list with two
                elements, where both elements are int or float type.
        order : int, optional
                What order of filter to apply, defaults to 5.
        type : str, optional
                What type of filter to apply to the signal:
                low = Low pass
                high = High pass
                stop = Bandstop
                Defaults to "low".
        """
        nyq = 0.5 * self._fs

        # Normalize the filter around the Nyqvist frequency.
        if not type == "stop":
            normalized_cutoff = cutoff / nyq
        else:
            normalized_cutoff = list()
            normalized_cutoff.append(cutoff[0] / nyq)
            normalized_cutoff.append(cutoff[1] / nyq)

        b, a = signal.butter(
            order,
            normalized_cutoff,
            btype=type,
            analog=False
        )

        # Adding the currently applied filter to a dict.
        # Dict is later used for filename generation.
        self._applied_filters[type] = cutoff

        self.acc = signal.filtfilt(b, a, self.acc)

    def _get_filter_string(self, sep):
        """
        Internal function to the get a string of all applied filters.

        Args
        ----
        sep : str
                The type of seperator to use for the string representation.

        Returns
        -------
        filter_list: [str]
                A list of strings representing all the applied filters.
        """
        filters = self._applied_filters

        # Create string containing upper and lower for bandstop filter.
        # This is needed as it is send as a list and not as a single value.
        # Using int() to create integer from float, otherwise it will add
        # decimals to outputted hertz, but lowest  quantization is 1Hz.
        if "band" in filters:
            filters["band"] = "-".join(
                [
                    str(int(filters["band"][0])),
                    str(int(filters["band"][1]))
                ]
            )
        # Casting to int() to remove the decimal from Hz saved in filename.
        if "low" in filters:
            filters["low"] = int(filters["low"])
        if "high" in filters:
            filters["high"] = int(filters["high"])

        # Add all filters from the applied filters dict to a list.
        # If None, do not add, otherwise stringify filter type
        # and filter frequency with "sep" in betwen.
        filter_list = [
            sep.join([str(filt_type), str(filt_cutoff)])
            for filt_type, filt_cutoff in filters.items()
            if filters is not None
        ]
        return filter_list

    def _get_filename(self, filename=None):
        """
        Internal function for generating the filename that the output
        file will be saved with.

        Args
        ----
        filename : str, optional
                The wanted prefix of the output file. If not specified
                the filename prefix will be the same as the id of the
                signal.

        Returns
        -------
        ret: str
                A string containing the prefix and all the applied filters.
        """
        # If no filename is provided, use the id of the signal.
        if not filename:
            filename = self.id

        filter_list = self._get_filter_string("-")
        ret = "_".join([filename, *filter_list])

        return ret
