from .signal import Signal


__all__ = ['SubSignal']


class SubSignal(Signal):
    # Redefine the init function as it should now load data from a
    # file, but create subsets of already imported data
    def __init__(self, signal, interval):
        if isinstance(signal, Signal):
            # Create a subset of the signal using split_signal()
            pass
        else:
            return NotImplemented
