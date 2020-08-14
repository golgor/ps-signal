"""Module that is the entry point from the interaces to invoke the CLI.
"""
from . import cli_conf
from ... import signals
from ...signals import data
from ...signals import filters


def run_cli():
    """Function that is the entry point into the CLI package. This is the
    function that will invoke and execute the CLI. It uses :mod:`.cli_conf`
    for configuration of the CLI.
    """
    # Singleton instances of the different kinds of filters.
    lowpass_filter = filters.lowpass()
    highpass_filter = filters.highpass()
    bandpass_filter = filters.bandpass()
    bandstop_filter = filters.bandstop()

    args = cli_conf.parse_args()

    # Instantiate a Data object and load data from a file.
    # The data object is assigned a file loader function by default.
    input_data = data.Data()
    input_data.load(args.file)

    # If the user wants just a part of the data, slice it. Else use all.
    if args.i:
        input_data_slice = data.slice_data(
            input_data,
            start_ms=args.i[0],
            end_ms=args.i[1]
        )
        input_signal = signals.Signal(
            id="Signal_1",
            input_data=input_data_slice
        )
    else:
        input_signal = signals.Signal(id="Signal_1", input_data=input_data)

    if args.lp:
        lowpass_filter(
            input_signal,
            cutoff=args.lp,
            inplace=True
        )

    if args.hp:
        highpass_filter(
            input_signal,
            cutoff=args.hp,
            inplace=True
        )

    if args.bp:
        bandpass_filter(
            input_signal,
            cutoff=args.bp[0],
            cutoff_upper=args.bp[1],
            inplace=True
        )

    if args.bs:
        bandstop_filter(
            input_signal,
            cutoff=args.bs[0],
            cutoff_upper=args.bs[1],
            inplace=True
        )

    if args.fft:
        input_signal.calc_fft()
        input_signal.plot_fft()
    else:
        input_signal.plot_signal()
