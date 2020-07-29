import pandas as pd
from .signal import Signal


__all__ = ['SubSignal']


class SubSignal(Signal):
    # Redefine the init function as it should now load data from a
    # file, but create subsets of already imported data
    def __init__(self, id: str):
        super().__init__(id)

    def load_data(self, signal, start_ms=None, end_ms=None):
        if isinstance(signal, Signal):
            if start_ms or end_ms:
                self._data = get_slice(signal, start_ms, end_ms)
            else:
                self._data = signal.data
        else:
            return NotImplemented


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
