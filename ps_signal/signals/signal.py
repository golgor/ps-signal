import pandas as pd
import sys
import xlrd
from . import fft
from . import plot


__all__ = ["Signal"]


# TODO: Have one class for Signal and one class for "Data".
# Data is the imported data using pd.csv reader.
# Every object of Signal is initiated with an instance
# of Data class such as self._data = Data(args, kwargs).
# This would be using a "factory"-design pattern?
# Data changes (intervals), everything else is the same
# for different signals methods for FFT and filters.
# Creating data class with importing a file for data
# Can have methods for returning a subset of data.
# Also file loader can be a class, so it is easier to
# add additional file types. Instantiate a Dataclass by
# using a FileLoader instance.
class Signal:
    def __init__(self, id: str):
        self._id = id
        self._data = None
        self._applied_filters = list()
        self._output_filename = str(self._id)
        self._fft = None

    def load_data(self, filename: str):
        self._filename = filename
        self._data = load_data(filename)
        self._prepare_signal()

    def _prepare_signal(self, remove_offset: bool = True):
        if remove_offset:
            self._data = remove_trigger_offset(self._data)

        self._frequency_hz = calculate_sampling_frequency(self._data)
        self._period = 1 / self._frequency_hz
        self._sample_size = len(self._data)
        self._sample_time = self._sample_size * self._period
        self._memory_usage = self._data.memory_usage(index=True, deep=True)

    def __repr__(self) -> str:
        return (
            f"{self._id.center(50, '=')}"
            f"Memory usage: {self.memory_usage_mb}MB\n"
            f"Sampling frequency: {self._frequency_hz}Hz\n"
            f"Sampling period: {self._period}s\n"
            f"Number of samples: {self._sample_size}\n"
            f"Total time: {self._sample_time}s"
        )

    def calc_fft(self):
        if not self._fft:
            self._fft = fft.perform_fft_on_signal(self)

    def plot_signal(self):
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
        self._applied_filters.append(filter)

    @property
    def id(self):
        return self._id

    @property
    def filename(self):
        return self._filename

    @property
    def data(self):
        return self._data

    @property
    def frequency_hz(self):
        return self._frequency_hz

    @property
    def period(self):
        return self._period

    @property
    def size(self):
        return self._sample_size

    @property
    def memory_usage_mb(self) -> int:
        memory_mb = round(sum(self._memory_usage / 1000 ** 2), 3)
        return int(memory_mb)

    @property
    def memory_usage_kb(self) -> int:
        memory_kb = round(sum(self._memory_usage / 1000), 3)
        return int(memory_kb)

    @property
    def output_filename(self) -> str:
        if self.filter_string:
            return self._output_filename + "-" + self.filter_string
        return self._output_filename

    @property
    def filter_string(self):
        if self._applied_filters:
            filter_str = [repr(filter) for filter in self._applied_filters]
            return "-".join(filter_str)
        else:
            return ""


def load_data(filename: str) -> pd.DataFrame:
    """Loading the data from a file

    :param filename: [description]
    :type filename: str
    :return: [description]
    :rtype: pd.Dataframe
    """
    # Formatting of file is separated by ";" and decimals using ","
    # First two rows are headers.
    try:
        data = pd.read_csv(filename, sep=";", decimal=",", skiprows=[0, 2])

    except (FileNotFoundError, xlrd.biffh.XLRDError, Exception) as error:
        sys.exit(error)
    else:
        data.columns = ["time", "acc"]
        return data


def remove_trigger_offset(data) -> pd.DataFrame:
    # With for example pre-trigger, the data starts from for example -200ms.
    # By substracting with the first value, the offset is removed.
    data.time -= data.time.iloc[0]
    return data


def calculate_sampling_frequency(data):
    # Calculate a pandas series with the difference between all elements.
    diff = data.time.diff()[1:]

    # If the standard deviation is "high", the sampling rate is not consistent.
    # Without a consistent sampling frequency, a FFT will not be accurate.
    # Maximum std is for now an arbitrary number i.e. estimated based
    # on current available data.
    if not diff.std() < 1e-6:
        print("\nInconsistent sampling frequency found. \
              FFT will not be accurate!\n")

    # Mean value of the difference is the sampling frequency.
    # Division by 1000 due to time stored in ms and not seconds.
    mean_diff = round(sum(diff) / len(diff), 9) / 1000
    return round(1 / mean_diff)
