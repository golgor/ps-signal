"""Module that contains various functions to perform an FFT
on a Signal.
"""
from scipy.fft import fft, fftfreq
import numpy as np


class FFT:
    """Class for explicit naming of x and y axes of the FFT.
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        """X-axis of the FFT. Contains the frequency span from the fft."""
        return self._x

    @property
    def y(self):
        """Y-axis of the FFT. Contains the amplitude data from the fft."""
        return self._y


def perform_fft_on_signal(signal):
    """Function to perform a FFT on a Signal. Using scipy.fft and scipy.fftfreq.

    Args:
        signal (Signal): The Signal object that should be analyzed.

    Returns:
        FFT: returns an object of class FFT that contain the data from the fft.
    """
    fft_y = fft(np.array(signal.data['acc']))
    fft_x = fftfreq(len(fft_y), signal.period)

    return get_positive_part_of_fft(fft_x, fft_y)


def get_positive_part_of_fft(x: np.ndarray, y: np.ndarray) -> FFT:
    """A FFT is normally centered around 0, we are though only interested
    in the positive part. The fft-function in scipy returns an array
    with the negative part in the first half, and positive in the second half.
    Thus we slice the array and only returns the positive part.

    The FFT also gives the amplitude in polar coordinates. By using
    abs() we find the real amplitude.

    Args:
        x (np.ndarray): The positive part of the x-axis.
        y (np.ndarray): The positive part of the y-axis.

    Returns:
        FFT: returns an object of class FFT that contain the data from the fft.
    """
    return FFT(x[: len(x) // 2] / 1000, abs(y[: len(y) // 2]))
