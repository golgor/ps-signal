import sys
import xlrd
from scipy.fft import fft, fftfreq
from scipy import signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union

sns.set(color_codes=True)


class PsSignal:
    """Class for importing and analysing signals.

    The signals needs to be imported from a .csv file that is exported
    from the Picoscope software. Several different kind of analyses is
    possible, such as applying filters and performing a FFT.

    Output files will be generated in a .png-format depending on the
    parameters given for each method in this class.
    """
    def __init__(self, filename: str, id: str,
                 start_ms: Union[int, float] = None,
                 length_ms: Union[int, float] = None) -> None:
        """Initialization function for the class ps_signal.

        This function reads in the .csv file using pandas.read_csv,
        clean the data and calculate some signal specific parameters
        such as sampling frequency.

        :param filename: The name of the file to read from.
            Current working directory is assumed.
        :type filename: str
        :param id: A string identifier of the signal. This is used
            to generate filenames of output files.
        :type id: str
        :param start_ms: Where to start the analysis of the signal.
            Data below this point is effectively cut out and not
            analysed at all. Value is given in milliseconds.
            Defaults to None
        :type start_ms: Union[int, float], optional
        :param length_ms: Where to end the analysis of the signal.
            This is specified as the length from the defined start,
            see above. If not specified, length is assumed to be
            "the rest of the signal". Defaults to None
        :type length_ms: Union[int, float], optional
        """
        try:
            # Formatting of file is separated by ";" and decimals using ","
            # First two rows are headers.
            self._data = pd.read_csv(filename, sep=";", decimal=",",
                                     skiprows=[0, 2])

            self._data.columns = ["time", "acc"]

        # Error if the file was not found.
        except (FileNotFoundError, xlrd.biffh.XLRDError, Exception) as error:
            sys.exit(error)

        # Data from the import is assigned to another variable
        # as the self._acceleration might be modified with filters. This
        # allows us to always have the source signal available.
        self._acceleration = self._data.acc

        # Time is adjusted so first sample is at 0 ms. This might
        # not be the case if the trigger point is changed during
        # the measurements. Makes it easier to understand.
        self._time = self._data.time - self._data.time.iloc[0]

        # The period is calculated based on the time difference in time between
        # the first two samples of the imported data. Divided by 1000 as by
        # default, the time stamp from Picoscopes are given in ms.
        # Rounded to avoid floating point errors.
        self._period = round(
            (self._time.iloc[1] - self._time.iloc[0]) / 1000, 12
        )

        # this function calculates it based on
        # the inverse of the period. Rounded to integer as the
        # smallest quantization of frequency is Hz.
        self._sampling_frequency = int(round(1 / self.period))

        # Drop data according to input from CLI
        self._drop_data(start_ms, length_ms)

        self._id = str(id)
        self._fft_y = None
        self._fft_x = None
        self._applied_filters = {}

    @property
    def time(self):
        """Public getter for the time vector.

        :return: Returns the time vector as a Pandas Series object.
        :rtype: pandas.core.series.Series
        """
        return self._time

    @property
    def acceleration(self):
        """Public getter for the acceleration vector.

        :return: Returns the acceleration vector as a Pandas Series object.
        :rtype: pandas.core.series.Series
        """
        return self._acceleration

    @property
    def period(self):
        """Public getter for the period of the signal.

        :return: Will return the period in seconds.
        :rtype: numpy.float64
        """
        return self._period

    @property
    def sampling_frequency(self):
        """Public getter for the sampling frequency of the signal.

        :return: Returns the samplings frequency in Hz.
        :rtype: int
        """
        return self._sampling_frequency

    def _drop_data(self, start_ms: Union[int, float] = None,
                   length_ms: Union[int, float] = None) -> None:
        """Internal function used to drop data from the pandas dataframe.

        This is used to isolate certain parts of the signal. I.e. If
        only a small part of the full signal is of interest, this
        function is used to keep only the data of interest.

        :param start_ms: Where the signal of interest starts. Given in ms.
            Defaults to None
        :type start_ms: Union[int, float], optional
        :param length_ms: The length of the signal in milliseconds.
            Given in ms. Defaults to None
        :type length_ms: Union[int, float], optional
        """
        if start_ms:
            # Convert from shift in ms as input from cli
            # to number of samples as the data is stored.
            start = round(start_ms * self._sampling_frequency / 1000)

            # If start is specified, remove n numbers of rows
            # starting from the beginning.
            self._time.drop(
                self._time.index[list(range(0, start))],
                inplace=True
            )

            self.acceleration.drop(
                self.acceleration.index[list(range(0, start))],
                inplace=True
            )

        if length_ms:
            # Convert from shift in ms as input from cli
            # to number of samples as the data is stored.
            length = round(length_ms * self._sampling_frequency / 1000)

            # If length is specified, drop everything after
            # length is reached. Used together with "start"
            # to specify a interval.
            self._time.drop(
                self._time.index[list(range(length, len(self._time)))],
                inplace=True
            )

            self.acceleration.drop(
                self.acceleration.index[
                    list(range(length, len(self.acceleration)))
                ],
                inplace=True
            )

    def plot(self, filename: str = None, title: str = None) -> None:
        """Plotting the imported signal and saves it to disk.

        :param filename: The wanted prefix of the output file.
            If not specified the filename prefix will be the same
            as the id of the signal. Defaults to None
        :type filename: str, optional
        :param title: The wanted title of the plot. If not set, title will
            be set to "No title set". Defaults to None
        :type title: str, optional
        """
        file_string = self._get_filename(filename)

        if not title:
            title = "Not set"

        plt.figure(figsize=(14, 10))
        plt.plot(self._time, self.acceleration)
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.title(f"{title}")
        plt.savefig(f"{file_string}.png")
        plt.close()

    # Doing to actual FFT on the signal.
    def _apply_fft(self) -> None:
        """
        Internal function to apply the actual FFT on the signal.
        """
        self._fft_y = fft(np.array(self.acceleration))
        self._fft_x = fftfreq(len(self._fft_y), 1 / self._sampling_frequency)

    def plot_fft(self, filename: str = None, title: str = None,
                 xlim: list = [10, 1200], ylim: list = None) -> None:
        """Performs an FFT of the signal, creates a plot and saves it to disk.

        :param filename: The wanted prefix of the output file. If not specified
            the filename prefix will be the same as the id of the signal.
            Defaults to None
        :type filename: str, optional
        :param title: The wanted title of the plot, defaults to None
        :type title: str optional
        :param xlim: A list of integers indicating the wanted range on the
            x-axis. Left limit is set to 10 as to hide the fundamental
            frequency, which usually is not of interest and skews the graph.
            Defaults to [10, 1200]
        :type xlim: list, optional
        :param ylim: A list of integer indicating the wanted range on
            the y-axis. If no value is given, the plot will autoscale.
            Defaults to None
        :type ylim: list, optional
        """
        file_string = self._get_filename(filename)

        if not title:
            title = "Not set"

        plt.figure(figsize=(14, 10))

        # Applying actual FFT on the signal.
        self._apply_fft()

        # Find the length of the signal. Best to do here, and not during
        # data import as data might be dropped.
        n = len(self.acceleration)

        # Using slicing as fft results are both positive and negative.
        # We are only interested in positive. Both fft and fftfreq
        # store positive data in first half of array and negative data
        # data in the second half. Thus we only plot the first
        # half of each. Division by 1000 to get KHz instad of Hz.
        plt.plot(
            self._fft_x[: n // 2] / 1000,
            abs(self._fft_y[: n // 2])
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

    def apply_filter(self, cutoff: Union[int, list], order: int = 5,
                     type: str = "low") -> None:
        """Apply a filter to the imported signal.

        This function is used to apply four different filters to
        to the signal:
        * Lowpass filter
        * Highpass filter
        * Bandstop filter
        * Bandpass filter by using lowpass- and highpass filter simultaneously.

        :param cutoff: The cutoff frequency for the chosen filter.
            For lowpass- and highpass filters this is a integer or float.
            For bandpass filter this is a list with two elements, where
            both elements are int or float type.
        :type cutoff: float, int, list
        :param order: What order of filter to apply, defaults to 5
        :type order: int, optional
        :param type: What type of filter to apply to the signal.
            low = Low pass
            high = High pass
            stop = Bandstop
            defaults to "low"
        :type type: str, optional
        """
        nyq = 0.5 * self._sampling_frequency

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
        self._acceleration = signal.filtfilt(b, a, self._acceleration)

    def _get_filter_string(self, sep: str) -> list:
        """Internal function to the get a string of all applied filters.

        :param sep: The type of seperator to use for the
            string representation.
        :type sep: str
        :return: A list of strings representing all the applied filters.
        :rtype: list
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

    def _get_filename(self, filename: str = None) -> str:
        """Internal function for generating the filename that the output
        file will be saved with.

        :param filename: The desired prefix of the output file,
            defaults to None
        :type filename: string, optional
        :return: Returns a concatenated string with the chosen filters.
        :rtype: string
        """
        # If no filename is provided, use the id of the signal.
        if not filename:
            filename = self._id

        filter_list = self._get_filter_string("-")
        ret = "_".join([filename, *filter_list])

        return ret
