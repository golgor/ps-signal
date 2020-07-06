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
    """[summary]
    """

    def __init__(self, filename, id, start_ms=None, length_ms=None):
        """[summary]

        Args:
            filename ([type]): [description]
            id ([type]): [description]
            start (int, optional): [description]. Defaults to 0.
            length ([type], optional): [description]. Defaults to None.
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
        self.fft_y_filt = None
        self.fft_y = None
        self.filt_x = None
        self._applied_filters = {}

    def _drop_data(self, start_ms, length_ms):
        """[summary]

        Args:
            start_ms ([type]): [description]
            length_ms ([type]): [description]
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
        """[summary]

        Args:
            filename (bool, optional): [description]. Defaults to False.
            title (str, optional): [description]. Defaults to "No title set".
            filtered ([type], optional): [description]. Defaults to None.
        """
        file_string = self._get_filename(filename)

        plt.figure(figsize=(14, 10))

        plt.plot(self.time, self.acc)
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.title(f"{title}")
        plt.savefig(f"{file_string}.png")
        plt.close()

    # Doing to actual FFT on the signal.
    def _apply_fft(self):
        """[summary]
        """
        self.fft_y = fft(np.array(self.acc))
        self.fft_x = fftfreq(len(self.fft_y), 1 / self._fs)

    def plot_fft(self, filename=None, title=None, ylim=None):
        """[summary]

        Args:
            filename ([type], optional): [description]. Defaults to None.
            title (str, optional): [description]. Defaults to "No title set".
            ylim ([type], optional): [description]. Defaults to None.
        """

        file_string = self._get_filename(filename)

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
        plt.xlim([10, 1200])

        if ylim:
            plt.ylim(ylim)

        plt.savefig(f"{file_string}-fft.png")
        plt.close()

    def apply_filter(self, cutoff, order=5, type="low"):
        """[summary]

        Args:
            cutoff ([type]): [description]
            order (int, optional): [description]. Defaults to 5.
            type (str, optional): [description]. Defaults to "low".
        """
        nyq = 0.5 * self._fs

        if not type == "band":
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

        self._applied_filters[type] = cutoff

        self.acc = signal.filtfilt(b, a, self.acc)

    def _get_filter_string(self, sep):
        """[summary]

        Args:
            sep ([type]): [description]

        Returns:
            [type]: [description]
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

    def _get_filename(self, filename):
        """[summary]

        Args:
            filename ([type]): [description]

        Returns:
            [type]: [description]
        """
        # If no filename is provided, use the id of the signal.
        if not filename:
            filename = self.id

        filter_list = self._get_filter_string("-")
        return "_".join([filename, *filter_list])
