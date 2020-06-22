import sys
import xlrd
from scipy.fft import fft, fftfreq
from scipy import signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

fs = 0

def calc_fft(fs, data):
    n = len(data)
    yf = fft(np.array(data))
    xf = fftfreq(len(yf), 1/fs)
    return xf, yf, n


def _create_butter_lowpass(cutoff, fs, order=2):
    nyq = 0.5 * fs
    normalized_cutoff = cutoff / nyq
    b, a = signal.butter(order, normalized_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = _create_butter_lowpass(cutoff, fs, order)
    y = signal.filtfilt(b, a, data)
    return y


def import_data(file):
    data = pd.read_csv(file, sep=";", decimal=",",skiprows=[0, 2])
    data.columns = ["time", "acc"]
    return data


class ps_signal():
    def __init__(self, filename, id, start=0, length=None):
        try:
            self._data = pd.read_csv(filename, sep=";", decimal=",",skiprows=[0, 2])
            self._data.columns = ["time", "acc"]

            self._data.drop(self._data.index[list(range(0, start))], inplace=True)
            
            if length:
                self._data.drop(self._data.index[list(range(length, len(self._data)))], inplace=True)

            self._t = round((self._data.time.iloc[1]- self._data.time.iloc[0]) / 1000, 12)
            self._fs = int(round(1 / self._t))
            self._n = len(self._data)
            self._fft = None
            self.raw_x = self._data.acc
            self.time = self._data.time
            self.id = str(id)
            self.fft_y_filt = None
            self.fft_y = None

        # Error if the file was not found.
        except FileNotFoundError as error:
            sys.exit(error)

        # Errors such as the excel sheet was not found.
        except xlrd.biffh.XLRDError as error:
            sys.exit(error)

        # Catching all other errors, whatever they might be.
        except Exception as error:
            sys.exit(error)


    def plot(self, filename=False, title="No title set", filtered=None):
        if not filename:
            filename = self.id
        
        plt.close()

        if filtered:
            plt.plot(self.time, self.filt_x)
            plt.xlabel("Time (ms)")
            plt.ylabel("Amplitude")
            plt.title(f"{title}-filtered")
            plt.savefig(f"{filename}-filt.png")
        else:
            plt.plot(self.time, self.raw_x)
            plt.xlabel("Time (ms)")
            plt.ylabel("Amplitude")
            plt.title(title)
            plt.savefig(f"{filename}.png")
        plt.close()


    def _apply_fft(self, filtered=False):
        n = len(self._data.acc)
        if filtered:
            self.fft_y_filt = fft(np.array(self.filt_x))
            self.fft_x_filt = fftfreq(len(self.fft_y_filt), 1/self._fs)
        else:
            self.fft_y = fft(np.array(self.raw_x))
            self.fft_x = fftfreq(len(self.fft_y), 1/self._fs)


    def plot_fft(self, filename=None, title="No title set", filtered=False, ylim=None):
        if not filename:
            filename = self.id
        
        plt.close()

        if filtered:
            if not self.fft_y_filt:
                self._apply_fft(filtered=True)
            
            plt.plot(self.fft_x_filt[:self._n // 2] / 1000, abs(self.fft_y_filt[:self._n // 2]))
            plt.title(f"{title}-filtered")
        else:
            if not self.fft_y:
                self._apply_fft(filtered=False)
            plt.plot(self.fft_x[:self._n // 2] / 1000, abs(self.fft_y[:self._n // 2]))
            plt.title(title)
        
        plt.xlabel("Frequency (KHz)")
        plt.ylabel("Amplitude")
        plt.title(title)
        plt.autoscale(enable=True, axis="y", tight=True)
        plt.xlim([10, 1200])

        if ylim:
            plt.ylim(ylim)

        plt.savefig(f"{filename}-fft.png")
        plt.close()

    def apply_filter(self, cutoff, order=5, type="low"):
        nyq = 0.5 * self._fs
        normalized_cutoff = cutoff / nyq
        b, a = signal.butter(order, normalized_cutoff, btype=type, analog=False)
        self.filt_x = signal.filtfilt(b, a, self._data.acc)
