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


# def plot_fft(self, filename: str = None, title: str = None,
#                 xlim: list = [10, 1200], ylim: list = None) -> None:
#     """Performs an FFT of the signal, creates a plot and saves it to disk.

#     :param filename: The wanted prefix of the output file. If not specified
#         the filename prefix will be the same as the id of the signal.
#         Defaults to None
#     :type filename: str, optional
#     :param title: The wanted title of the plot, defaults to None
#     :type title: str optional
#     :param xlim: A list of integers indicating the wanted range on the
#         x-axis. Left limit is set to 10 as to hide the fundamental
#         frequency, which usually is not of interest and skews the graph.
#         Defaults to [10, 1200]
#     :type xlim: list, optional
#     :param ylim: A list of integer indicating the wanted range on
#         the y-axis. If no value is given, the plot will autoscale.
#         Defaults to None
#     :type ylim: list, optional
#     """
#     file_string = self._get_filename(filename)

#     if not title:
#         title = "Not set"

#     plt.figure(figsize=(14, 10))

#     # Applying actual FFT on the signal.
#     self._apply_fft()

#     # Find the length of the signal. Best to do here, and not during
#     # data import as data might be dropped.
#     n = len(self.acceleration)

#     # Using slicing as fft results are both positive and negative.
#     # We are only interested in positive. Both fft and fftfreq
#     # store positive data in first half of array and negative data
#     # data in the second half. Thus we only plot the first
#     # half of each. Division by 1000 to get KHz instad of Hz.
#     plt.plot(
#         self._fft_x[: n // 2] / 1000,
#         abs(self._fft_y[: n // 2])
#     )
#     plt.xlabel("Frequency (KHz)")
#     plt.ylabel("Amplitude")
#     plt.title(f"{title}")
#     plt.autoscale(enable=True, axis="y", tight=True)
#     plt.xlim(xlim)

#     if ylim:
#         plt.ylim(ylim)

#     plt.savefig(f"{file_string}-fft.png")
#     plt.close()
