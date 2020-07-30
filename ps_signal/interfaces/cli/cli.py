from . import cli_conf
from ... import signals

__all__ = ['run_cli']


def run_cli():
    args = cli_conf.parse_args()

    input_signal = signals.Signal(id="Signal1")
    input_signal.load_data(filename=args.file)
    print(input_signal)

    input_signal.plot()
    input_signal.fft()

    signals.bandstop_filter(input_signal, 250_000, 500_000, inplace=True)

    input_signal.plot()
    input_signal.fft()

    # title = args.t if args.t else None

    if args.i:
        start_interval = args.i[0]
        end_intervall = args.i[1]

        subsignal_1 = signals.SubSignal(id="Subsignal_1")
        subsignal_1.load_data(
            input_signal,
            start_ms=start_interval,
            end_ms=end_intervall
        )
        print(subsignal_1)
        subsignal_1.plot()
        subsignal_1.fft()

    # if args.lp:
    #     # Perform low pass filtering
    #     input_signal.apply_filter(cutoff=args.lp, order=5, type="low")

    # if args.hp:
    #     # Perform highpass filtering
    #     input_signal.apply_filter(cutoff=args.hp, order=5, type="high")

    # if args.bs:
    #     input_signal.apply_filter(cutoff=args.bs, order=5, type="stop")

    # if args.fft:
    #     input_signal.plot_fft(
    #         ylim=[0, 5e5],
    #         title=title
    #     )
    # else:
    #     input_signal.plot(
    #         title=title
    #     )
