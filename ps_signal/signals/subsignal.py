"""Module for the class SubSignal. Used to create subsets of Signal.

.. deprecated:: 0.1.6
    Use :class:`Data` and :func:`slice_data` instead.
"""
import pandas as pd
from .signal import Signal


class SubSignal(Signal):
    """Deprecated class.
    """
    def __init__(self, id: str):
        super().__init__(id)

    def load_data(self, signal, start_ms=None, end_ms=None):
        if isinstance(signal, Signal):
            if start_ms or end_ms:
                self._data = _get_slice(signal, start_ms, end_ms)
            else:
                self._data = signal.data
            # Calculate various properties for the signal.
            # Most things are constant, but for example signal length
            # is changed, which would corrupt the fft.
            super()._prepare_signal(remove_offset=False)
        else:
            return NotImplemented


def _get_slice(signal: Signal, start_ms: int = None,
               end_ms: int = None) -> pd.DataFrame:
    """Deprecated helper function.
    """
    if start_ms is None:
        start_ms = 0

    if end_ms is None:
        end_ms = len(signal.data)

    start_sample_count = round((start_ms / 1000) * signal.frequency_hz)
    end_sample_count = round((end_ms / 1000) * signal.frequency_hz)

    # Creating a subset of a COPY of the DataFrame. Important to make a copy
    # and not assignment with '=' as assignment '=' can result in only
    # creating a reference rather than a fresh copy. I.e. risk of modifying
    # the original when the "copy" is modified.
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    return signal.data.copy().iloc[
        start_sample_count: end_sample_count
    ]
