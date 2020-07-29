from . import signal


__all__ = ['apply_low_pass_filter']


# TODO: Create a filter class


def apply_low_pass_filter():
    """ Applying a low pass filter on a Signal objekt"""
    test = signal.Signal()
    print("Testing in applying low pass filter")
    print(test.a)
    pass


def apply_high_pass_filter():
    """ Applying a high pass filter on a Signal objekt"""
    pass


def apply_band_pass_filter():
    """ Applying a band pass filter on a Signal objekt"""
    pass


def apply_band_stop_filter():
    """ Applying a band stop filter on a Signal objekt"""
    pass
