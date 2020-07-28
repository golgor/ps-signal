# import ps_signal.signal_processing as sp
# import ps_signal.cli as cli


from . import validators
from . import signals
from .interfaces import cli


def main():
    cli.process_args()
    # for k in dict(globals()).keys():
    #     print(k)

    # print("\nFor ps_signal")
    # for k in signal.__dict__.keys():
    #     print(k)

    # print("\nFor common")
    # for k in ps_signal.signal.__dict__.keys():
    #     print(k)

    # signal.fft.perform_fft_on_signal()
    # signal.filter.apply_low_pass_filter()
    # validators.file.is_picoscope_file()


if __name__ == "__main__":
    main()
