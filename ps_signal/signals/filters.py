"""Module that contains the class Filter and instantiate four
Filter objects for the following filter types:

* Lowpass - lowpass_filter
* Highpass - highpass_filter
* Bandstop - bandstop_filter
* Bandpass - bandpass_filter
"""
from .signal import Signal
from scipy.signal import filtfilt, butter
from copy import deepcopy


class Filter:
    """A callable class that applies filtering to a Signal.

    Args:
        filter_fn (function): A function to use when applying the filter.
        filter_type (str): A string used to identify the filter type
            when printing out information about the object.
    """
    def __init__(self, filter_fn, filter_type):
        self._filter_fn = filter_fn
        self._filter_type = filter_type
        self._cutoff = None
        self._cutoff_upper = None

    def __call__(self, signal: Signal, cutoff: float,
                 cutoff_upper: float = None, inplace=False) -> Signal:
        """Making a filter object callable. This method applies a filter.

        Args:
            signal (Signal): A Signal object to which a filter will be applied.
            cutoff (float): The wanted cutoff frequency of
                the filter.
            cutoff_upper (float, optional): In case of bandstop
                or bandpass filters, the upper cutoff frequency is needed.
                Defaults to None.
            inplace (bool, optional): If the signal filtering should be made
                inplace, i.e. replacing the Signal object or creating a new
                Signal object. Defaults to False.

        Returns:
            Signal: Returns a filtered Signal.
        """
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

    def __repr__(self):
        """For printing out information about the Filter object."""
        if not self._cutoff_upper:
            return f"{self._filter_type}_{self._cutoff:.3g}"
        else:

            return (f"{self._filter_type}"
                    "_("
                    f"{self._cutoff:.3g}"
                    "-"
                    f"{self._cutoff_upper:.3g}"
                    ")")


def _apply_low_pass_filter(signal: Signal, cutoff: float,
                           cutoff_upper: float = None) -> Signal:
    """Function for performing low pass filtering on a signal.
    Intended to be passed as a filtering function when
    instantiating a Filter object.

    Args:
        signal (Signal): A Signal object to which a filter will be applied.
        cutoff (float): The wanted cutoff frequency of the filter.
        cutoff_upper (float, optional): This parameter is not used for low
            pass filtering. It is here due to compability reasons with other
            filtering functions. Defaults to None.

    Returns:
        Signal: A Signal object with an applied filter.
    """
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


def _apply_high_pass_filter(signal: Signal, cutoff: float,
                            cutoff_upper: float = None) -> Signal:
    """Function for performing high pass filtering on a signal.
    Intended to be passed as a filtering function when
    instantiating a Filter object.

    Args:
        signal (Signal): A Signal object to which a filter will be applied.
        cutoff (float): The wanted cutoff frequency of the filter.
        cutoff_upper (float, optional): This parameter is not used for high
            pass filtering. It is here due to compability reasons with other
            filtering functions. Defaults to None.

    Returns:
        Signal: A Signal object with an applied filter.
    """
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


def _apply_band_pass_filter(signal: Signal, cutoff: float,
                            cutoff_upper: float = None) -> Signal:
    """Function for performing band pass filtering on a signal. Everything
    but the frequencies in between cutoff and cutoff_upper will be filtered
    out.

    Intended to be passed as a filtering function when
    instantiating a Filter object.

    Args:
        signal (Signal): A Signal object to which a filter will be applied.
        cutoff (float): The wanted cutoff frequency of the filter.
            Where to start filtering.
        cutoff_upper (float, optional): The upper cutoff frequency.
            Where to stop filtering. Defaults to None.

    Returns:
        Signal: A Signal object with an applied filter.
    """
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


def _apply_band_stop_filter(signal: Signal, cutoff: float,
                            cutoff_upper: float = None) -> Signal:
    """Function for performing band stop filtering on a signal. All
    frequencies in between cutoff and cutoff_upper will be filtered out.

    Intended to be passed as a filtering function when
    instantiating a Filter object.

    Args:
        signal (Signal): A Signal object to which a filter will be applied.
        cutoff (float): The wanted cutoff frequency of the filter.
            Where to start filtering.
        cutoff_upper (float, optional): The upper cutoff frequency.
            Where to stop filtering. Defaults to None.

    Returns:
        Signal: A Signal object with an applied filter.
    """
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


lowpass_filter = Filter(_apply_low_pass_filter, "lowpass")
highpass_filter = Filter(_apply_high_pass_filter, "highpass")
bandpass_filter = Filter(_apply_band_pass_filter, "bandpass")
bandstop_filter = Filter(_apply_band_stop_filter, "bandstop")
