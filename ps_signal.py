import ps_signal.signal_processing as sp
import ps_signal.cli as cli


if __name__ == "__main__":
    args = cli.parser.parse_args()

    input_signal = sp.ps_signal(
        filename=args.file,
        id="signal3",
        start_ms=(start_intervall := (args.i[0] if args.i else None)),
        length_ms=(length_intervall := (args.i[1] if args.i else None)),
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
            title=(title := (args.t if args.t else None))
        )
    else:
        input_signal.plot(
            title=(title := (args.t if args.t else None))
        )
