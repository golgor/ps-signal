from ps_signal.signal_processing import PsSignal
import ps_signal.cli as cli


def main():
    args = cli.parser.parse_args()

    start_interval = args.i[0] if args.i else None
    length_intervall = args.i[1] if args.i else None
    title = args.t if args.t else None

    input_signal = PsSignal(
        filename=args.file,
        id="signal3",
        start_ms=start_interval,
        length_ms=length_intervall,
    )

    if args.lp:
        # Perform low pass filtering
        input_signal.apply_filter(cutoff=args.lp, order=5, type="low")

    if args.hp:
        # Perform highpass filtering
        input_signal.apply_filter(cutoff=args.hp, order=5, type="high")

    if args.bs:
        input_signal.apply_filter(cutoff=args.bs, order=5, type="stop")

    if args.fft:
        input_signal.plot_fft(
            ylim=[0, 5e5],
            title=title
        )
    else:
        input_signal.plot(
            title=title
        )


if __name__ == "__main__":
    main()
