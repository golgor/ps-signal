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
                signal._id = signal._id + "-filtered"
                return None
            else:
                new_signal = deepcopy(signal)
                new_signal._id = signal._id + "-filtered"
                return self._filter_fn(new_signal, cutoff, cutoff_upper)
        else:
            print("Can't apply filter to object"
                  "that is not instances of Signal()")


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
    print(signal.frequency_hz)
    print(f"Cutoff: {cutoff}")
    print(f"Cutoff_upper: {cutoff_upper}")
    normalized_cutoff = [cutoff / nyq for cutoff in (cutoff, cutoff_upper)]
    print(f"Norm_Cutoff: {normalized_cutoff[0]}")
    print(f"Norm_Cutoff_upper: {normalized_cutoff[1]}")
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
