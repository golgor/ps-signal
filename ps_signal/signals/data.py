import pandas as pd
import sys
import xlrd
import copy
from time import perf_counter

__all__ = ["Data", "slice_data"]


def picoscope_data_loader(filename: str) -> pd.DataFrame:
    """Loading the data from a file. Custom file loader
    made for loading files exported from picoscope as a .csv

    :param filename: [description]
    :type filename: str
    :return: [description]
    :rtype: pd.Dataframe
    """
    # Formatting of file is separated by ";" and decimals using ","
    # First two rows are headers.
    try:
        start = perf_counter()
        data = pd.read_csv(filename, sep=";", decimal=",", skiprows=[0, 2])
        print(f"Total time for file import: {perf_counter()-start}")
    except (FileNotFoundError, xlrd.biffh.XLRDError, Exception) as error:
        sys.exit(error)
    else:
        data.columns = ["time", "acc"]
        return data


class Data:
    def __init__(self, loader=picoscope_data_loader) -> None:
        self._loader = loader
        self._data = None
        self._trigger_offset = None

    def load(self, data_path, remove_offset: bool = True):
        try:
            self._data = self._loader(data_path)
        except Exception as error:
            print(error)

        self._size = len(self._data)
        self._frequency_hz = calculate_sampling_frequency(self._data)
        self._period = 1 / self._frequency_hz
        self._memory_usage = self._data.memory_usage(index=True, deep=True)

        # With for example pre-trigger, the data starts from for example
        # -200ms. By substracting with the first value, the offset is removed.
        if remove_offset:
            self._trigger_offset = self._data.time.iloc[0]
            self._data.time -= self._data.time.iloc[0]

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._size

    @property
    def frequency_hz(self):
        return self._frequency_hz

    @property
    def period(self):
        return self._period

    @property
    def memory_usage(self):
        return self._memory_usage

    @property
    def memory_usage_mb(self) -> int:
        memory_mb = round(sum(self._memory_usage / 1000 ** 2), 3)
        return int(memory_mb)

    @property
    def memory_usage_kb(self) -> int:
        memory_kb = round(sum(self._memory_usage / 1000), 3)
        return int(memory_kb)


def slice_data(data: Data, start_ms: int = None, end_ms: int = None) -> Data:
    """Function that takes a Data object and slice the data into a subset.
    Can be used if there is an interest only for a small part of the data.

    :param data: A Data object
    :type data: Data
    :param start_ms: Where to start slicing in ms, defaults to None
    :type start_ms: int, optional
    :param end_ms: Where to stop slicing in ms, defaults to None
    :type end_ms: int, optional
    :return: Returns a data object that is a subset of the input
    :rtype: Data
    """
    if start_ms is None:
        start_ms = 0

    if end_ms is None:
        end_ms = data.size

    start_sample_count = round((start_ms / 1000) * data.frequency_hz)
    end_sample_count = round((end_ms / 1000) * data.frequency_hz)

    # Creating a copy to make sure there is two separate data sets,
    # i.e. not two object with references to the same data.
    # Using iloc from Pandas DataFrame object to slice the data.
    new_copy = copy.deepcopy(data)
    new_copy._data = new_copy.data.iloc[start_sample_count: end_sample_count]

    return new_copy


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
