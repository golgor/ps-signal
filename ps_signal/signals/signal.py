import pandas as pd
import sys
import xlrd
import matplotlib.pyplot as plt
from . import fft

__all__ = ["Signal"]


class Signal:
    def __init__(self, id: str):
        self._id = id
        self._data = None

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

    def fft(self):
        print(f"Performing FFT on {self._id}")
        self._fft = fft.perform_fft_on_signal(self)
        self.plot_fft()

    def plot(self):
        if self._data is not None:
            plt.plot(self._data['time'], self._data['acc'])
            plt.savefig(f"{self._id}.png")
            plt.close()
        else:
            raise ValueError(
                f"No data is loaded for {self._id}"
            )

    def plot_fft(self):
        plt.figure(figsize=(14, 10))
        plt.plot(self._fft.x, self._fft.y)
        plt.autoscale(enable=True, axis="y", tight=True)
        plt.ylim([0, 500000])
        plt.xlim([0, 2000])
        plt.savefig(f"{self._id}-fft.png")
        plt.close()

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
