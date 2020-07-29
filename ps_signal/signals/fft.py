from collections import namedtuple
from scipy.fft import fft, fftfreq
import numpy as np


FFT = namedtuple('FFT', 'x, y')


def perform_fft_on_signal(signal):
    fft_y = fft(np.array(signal.data['acc']))
    fft_x = fftfreq(len(fft_y), signal.period)

    return get_positive_part_of_fft(fft_x, fft_y)


def get_positive_part_of_fft(x, y):
    """A FFT normally is centered around 0, we are though only interested
    in the positive part. The fft-function in scipy returns an array
    with the negative part in the first half, and positive in the second half.
    Thus we slice the array and only returns the positive part.

    The FFT also represents the amplitude in polar coordinates. By using
    abs() we find the real amplitude.

    :param x: X-component of the data.
    :type x: np.ndarray
    :param y: Y-component of the data.
    :type y: np.ndarray
    :return: returns a tuple with the sliced x and y components.
    :rtype: tuple(np.ndarray, np.ndarray)
    """
    return FFT(x[: len(x) // 2] / 1000, abs(y[: len(y) // 2]))
