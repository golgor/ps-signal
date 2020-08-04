from . import fft
from . import plot


__all__ = ["Signal"]


class Signal:
    def __init__(self, id: str, input_data):
        self._id = id
        self._data = input_data.data
        self._sample_size = input_data.size
        self._memory_usage_mb = input_data.memory_usage_mb
        self._frequency_hz = input_data.frequency_hz
        self._period = input_data.period
        self._total_time = self._sample_size * self._period

        self._applied_filters = list()
        self._output_filename = str(self._id)
        self._fft = None

    def __repr__(self) -> str:
        return (
            f"{self._id.center(50, '=')}"
            f"Memory usage: {self._memory_usage_mb}MB\n"
            f"Sampling frequency: {self._frequency_hz}Hz\n"
            f"Sampling period: {self._period}s\n"
            f"Number of samples: {self._sample_size}\n"
            f"Total time: {self._total_time}s"
        )

    def calc_fft(self):
        if not self._fft:
            self._fft = fft.perform_fft_on_signal(self)

    def plot_signal(self):
        try:
            plot.plot_data(
                signal=self,
                style='time_series'
            )
        except AttributeError as error:
            print(error)
        except Exception as error:
            print(error)

    def plot_fft(self):
        try:
            plot.plot_data(
                signal=self,
                style='fft'
            )
        except AttributeError as error:
            print(error)
            print("Likely caused by not running calc_fft first!")
        except Exception as error:
            print(error)

    def _add_filter(self, filter):
        self._applied_filters.append(filter)

    @property
    def id(self):
        return self._id

    @property
    def filename(self):
        return self._filename

    @property
    def data(self):
        return self._data

    @property
    def frequency_hz(self):
        return self._frequency_hz

    @property
    def period(self):
        return self._period

    @property
    def size(self):
        return self._sample_size

    @property
    def memory_usage_mb(self) -> int:
        return self._memory_usage_mb

    @property
    def output_filename(self) -> str:
        if self.filter_string:
            return self._output_filename + "-" + self.filter_string
        return self._output_filename

    @property
    def filter_string(self):
        if self._applied_filters:
            filter_str = [repr(filter) for filter in self._applied_filters]
            return "-".join(filter_str)
        else:
            return ""
