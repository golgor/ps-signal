import pandas as pd
from .signal import Signal
import matplotlib.pyplot as plt


__all__ = ['SubSignal']


class SubSignal(Signal):
    # Redefine the init function as it should now load data from a
    # file, but create subsets of already imported data
    def __init__(self, id: str):
        self._id = id
        self._data = None

    def load_signal(self, signal, start_ms=None, end_ms=None):
        if isinstance(signal, Signal):
            self._data = get_slice(signal, start_ms, end_ms)
        else:
            return NotImplemented

    def plot(self):
        if self._data is not None:
            plt.plot(self._data['time'], self._data['acc'])
            plt.savefig("test.png")
        else:
            raise ValueError(
                f"No signal has been loaded for SubSignal {self._id}"
            )


def get_slice(signal: Signal, start_ms: int = None, end_ms: int = None) -> pd.DataFrame:
    """Helper function that will return a slice of a Signal. Intended to
    be used to isolate a SubSignal from a Signal.

    :param signal: Signal containing data to be sliced.
    :type signal: Signal
    :param start_ms: Where to start slicing the data in ms. Defaults to None.
    :type start_ms: int, optional
    :param end_ms: Where to stop slicing the data in ms. Defaults to None.
    :type end_ms: int, optional
    :return: returns a slice of the data in Signal as a DataFrame.
    :rtype: pd.DataFrame
    """
    if start_ms is None:
        start_ms = 0

    if end_ms is None:
        end_ms = len(signal.data)

    start_sample_count = round((start_ms / 1000) * signal.frequency_hz)
    end_sample_count = round((end_ms / 1000) * signal.frequency_hz)
    return signal.data.iloc[
        start_sample_count: end_sample_count
    ]
