from . import cli_conf
from ... import signals

__all__ = ['run_cli']


def run_cli():
    args = cli_conf.parse_args()

    input_signal = signals.Signal(id="Signal_1")
    input_signal.load_data(filename=args.file)

    if args.i:
        start_interval = args.i[0]
        end_intervall = args.i[1]

        subsignal_1 = signals.SubSignal(id="Subsignal_1")
        subsignal_1.load_data(
            input_signal,
            start_ms=start_interval,
            end_ms=end_intervall
        )
        input_signal = subsignal_1

    if args.lp:
        signals.lowpass_filter(
            input_signal,
            cutoff=args.lp,
            inplace=True
        )

    if args.hp:
        signals.highpass_filter(
            input_signal,
            cutoff=args.hp,
            inplace=True
        )

    if args.bs:
        signals.bandstop_filter(
            input_signal,
            cutoff=args.bs[0],
            cutoff_upper=args.bs[1],
            inplace=True
        )

    if args.bp:
        signals.bandpass_filter(
            input_signal,
            cutoff=args.bs[0],
            cutoff_upper=args.bs[1],
            inplace=True
        )

    if args.fft:
        input_signal.plot_fft()
    else:
        input_signal.plot()
