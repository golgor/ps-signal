import pandas as pd
import sys
import xlrd

__all__ = ['Signal']


class Signal:
    def __init__(self, filename):
        self._filename = filename
        self._data = load_data(filename)
        self._frequency = calculate_sampling_frequency(self._data)
        self._period = int(round(1 / self._frequency))

    @property
    def filename(self):
        return self._filename

    @property
    def data(self):
        return self._data

    @property
    def frequency(self):
        return self._frequency

    @property
    def period(self):
        return self._period


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
        data = pd.read_csv(filename, sep=";", decimal=",",
                           skiprows=[0, 2])

    except (FileNotFoundError, xlrd.biffh.XLRDError, Exception) as error:
        sys.exit(error)
    else:
        data.columns = ["time", "acc"]
        return data


def calculate_sampling_frequency():
    pass


def split_signal(signal: Signal, start: int, end: int) -> pd.DataFrame:
    """Funktion för att isolera ett subset ur den grundläggande signalen.
    Input är ett Signal-objekt och ett intervall givet i ms. Output är ett
    nytt signalobjekt men med annorlunda sample i.
    """
    pass


def signal_helper():
    print("Signal_helper!")
