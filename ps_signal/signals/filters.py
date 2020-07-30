from .signal import Signal
from scipy.signal import filtfilt, butter
from copy import deepcopy


__all__ = [
    'lowpass_filter',
    'highpass_filter',
    'bandpass_filter',
    'bandstop_filter'
]


class Filter:
    def __init__(self, filter_fn, filter_type):
        self._filter_fn = filter_fn
        self._filter_type = filter_type
        self._cutoff = None
        self._cutoff_upper = None

    def __call__(self, signal, cutoff, cutoff_upper=None, inplace=False):
        if isinstance(signal, Signal):
            self._cutoff = cutoff
            self._cutoff_upper = cutoff_upper

            if inplace:
                self._filter_fn(signal, cutoff, cutoff_upper)
                signal._add_filter(self)
                return None
            else:
                new_signal = deepcopy(signal)
                signal._add_filter(self)
                return self._filter_fn(new_signal, cutoff, cutoff_upper)
        else:
            print("Can't apply filter to object"
                  "that is not instances of Signal()")

    def __str__(self):
        return "Tjosan"

    def __repr__(self):
        if not self._cutoff_upper:
            return f"{self._filter_type}_{self._cutoff:.3g}"
        else:

            return (f"{self._filter_type}"
                    "_("
                    f"{self._cutoff:.3g}"
                    "-"
                    f"{self._cutoff_upper:.3g}"
                    ")")


def apply_low_pass_filter(signal, cutoff, cutoff_upper=None):
    nyq = 0.5 * signal.frequency_hz
    normalized_cutoff = cutoff / nyq
    b, a = butter(
        5,
        normalized_cutoff,
        btype="low",
        analog=False
    )
    signal._data.acc = filtfilt(b, a, signal.data.acc)
    return signal


def apply_high_pass_filter(signal, cutoff, cutoff_upper=None):
    nyq = 0.5 * signal.frequency_hz
    normalized_cutoff = cutoff / nyq
    b, a = butter(
        5,
        normalized_cutoff,
        btype="high",
        analog=False
    )
    signal._data.acc = filtfilt(b, a, signal.data.acc)
    return signal


def apply_band_pass_filter(signal, cutoff, cutoff_upper=None):
    nyq = 0.5 * signal.frequency_hz
    normalized_cutoff = [cutoff / nyq for cutoff in (cutoff, cutoff_upper)]
    b, a = butter(
        5,
        normalized_cutoff,
        btype="bandpass",
        analog=False
    )
    signal._data.acc = filtfilt(b, a, signal.data.acc)
    return signal


def apply_band_stop_filter(signal, cutoff, cutoff_upper=None):
    nyq = 0.5 * signal.frequency_hz
    normalized_cutoff = [cutoff / nyq for cutoff in (cutoff, cutoff_upper)]
    b, a = butter(
        5,
        normalized_cutoff,
        btype="bandstop",
        analog=False
    )
    signal._data.acc = filtfilt(b, a, signal.data.acc)
    return signal


lowpass_filter = Filter(apply_low_pass_filter, "lowpass")
highpass_filter = Filter(apply_high_pass_filter, "highpass")
bandpass_filter = Filter(apply_band_pass_filter, "bandpass")
bandstop_filter = Filter(apply_band_stop_filter, "bandstop")
