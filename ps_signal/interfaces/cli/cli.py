from . import cli_conf
from ...signals.signal import Signal
from ...signals.subsignal import SubSignal


__all__ = ['run_cli']


def run_cli():
    args = cli_conf.parse_args()

    input_signal = Signal(id="Signal1")
    input_signal.load_data(filename=args.file)

    # title = args.t if args.t else None

    if args.i:
        start_interval = args.i[0]
        end_intervall = args.i[1]

        subsignal_1 = SubSignal(id="Subsignal_1")
        subsignal_1.load_data(
            input_signal,
            start_ms=start_interval,
            end_ms=end_intervall
        )
        subsignal_1.plot()

    # input_signal = sp.PsSignal(
    #     filename=args.file,
    #     id="signal3",
    #     start_ms=start_interval,
    #     length_ms=length_intervall,
    # )

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
