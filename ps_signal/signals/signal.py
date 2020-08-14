"""Module for the Signal class.
"""
from . import fft
from . import plot


__all__ = ["Signal"]


class Signal:
    """Class that handles the data, called a Signal.

    A signal is an amount of data with a specified duration that can be either
    all of the data or parts of it. I.e. it is possible to derive several
    signals from one and the same data source if there is an interest to
    analyze small intervalls separately.

    Args:
        id (str): An id used to identify the signal. By default the id will
            be used as the output filename.
        input_data (Data): Input data is of the class Data.
    """
    def __init__(self, id: str, input_data):
        self._id = id
        self._data = input_data.data
        self._sample_size = input_data.size
        self._memory_usage_mb = input_data.memory_usage_mb
        self._frequency_hz = input_data.frequency_hz
        self._period = input_data.period
        self._total_time = self._sample_size * self._period

        self._applied_filters = []
        self._output_filename = str(self._id)
        self._fft = None

    def __repr__(self) -> str:
        """Used to print out information about the signal.

        Returns:
            str: Returns a string with parameters of the signal such as id,
            frequency, size and memory usage.
        """
        return (
            f"{self._id.center(50, '=')}"
            f"Memory usage: {self._memory_usage_mb}MB\n"
            f"Sampling frequency: {self._frequency_hz}Hz\n"
            f"Sampling period: {self._period}s\n"
            f"Number of samples: {self._sample_size}\n"
            f"Total time: {self._total_time}s"
        )

    def calc_fft(self):
        """Method to perform a FFT analysis on a signal.
        Memoized so it only performs it if it is not already done.
        The FFT result is stored in an internal variable, can be plotted
        using :func:`plot_fft`.
        """
        if not self._fft:
            self._fft = fft.perform_fft_on_signal(self)

    def plot_signal(self):
        """Method that plots the signal as is. Can be used to find
        certain intervals of interest or limiting the amount of data
        to decrease computational time. Using the time_series style of
        the plotter dispatcher :func:`ps_signal.signals.plot.plot_data`.
        """
        try:
            plot.plot_data(
                signal=self,
                style='time_series'
            )
        except AttributeError as error:
            print(error)
        except Exception as error:
            print(error)

    def plot_fft(self):
        """Method that plots the FFT data of the signal. Assumes a FFT is
        done before this function is called. Using the fft style of
        the plotter dispatcher :func:`ps_signal.signals.plot.plot_data`.
        Appends "-fft" to the output file to distinguish from the time
        series output.
        """
        try:
            plot.plot_data(
                signal=self,
                style='fft'
            )
        except AttributeError as error:
            print(error)
            print("Likely caused by not running calc_fft first!")
        except Exception as error:
            print(error)

    def _add_filter(self, filter):
        """Method to add a filter to the internal filter list.
        This is used to keep track of what filters are applied to the signal.
        The different applied filters will be added to the output filename.

        Args:
            filter (Filter): An object of Filter class to add.
        """
        self._applied_filters.append(filter)

    @property
    def id(self):
        """The id of the signal. Will be used when printing out
        information about the signal object as well as be present
        in the output filename."""
        return self._id

    @property
    def data(self):
        """The data of the signal stored as a Pandas.DataFrame."""
        return self._data

    @property
    def frequency_hz(self):
        """The calculated sampling frequency."""
        return self._frequency_hz

    @property
    def period(self):
        """The calculated period, i.e. the inverse
        of the sampling frequency."""
        return self._period

    @property
    def size(self):
        """The row count of the imported data."""
        return self._sample_size

    @property
    def memory_usage_mb(self) -> int:
        """The memory used by the imported data.
        Calculated to show total size in megabytes."""
        return self._memory_usage_mb

    @property
    def output_filename(self) -> str:
        """The output filename, which is the id concatenated with
        the applied filters."""
        if self.filter_string:
            return self._output_filename + "-" + self.filter_string
        return self._output_filename

    @property
    def filter_string(self):
        """Method that generates a string for each and every filter
        that is applied joins them all together and returns a concatenated
        string with all filters applied."""
        if self._applied_filters:
            filter_str = [repr(filter) for filter in self._applied_filters]
            return "-".join(filter_str)
        else:
            return ""
