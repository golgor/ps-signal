import ps_signal.signal_processing as sp
import ps_signal.cli as cli


def run_fft():
    DATAFILE1 = "20200612-0001-upp-ner-cylinder-avfettad.csv"
    # DATAFILE2 = "20200612-0001-avfettad-cyliner-islag-i-topplock.csv"

    # data = sp.import_data(DATAFILE1)

    # Sampling time calculated as difference between two samples.
    # Times 1000 to convert from KHz to Hz (Time was in ms)

    signal1 = sp.ps_signal(
        DATAFILE1,
        "signal1",
        start=1350000,
        length=1070000
    )

    signal2 = sp.ps_signal(
        DATAFILE1,
        "signal2",
        start=2420000,
        length=1030000
    )

    signal3 = sp.ps_signal(
        DATAFILE1,
        "signal3",
        start=3450000,
        length=1150000
    )

    signal1.apply_filter(3e5)
    signal1.plot_fft(
        filename="s1-fft-pre-filt",
        title="s1-pre-filt"
    )
    signal1.plot_fft(
        filename="s1-fft-post-filt",
        title="s1-post-filt",
        filtered=True
    )
    signal1.plot(
        filename="s1-pre-filt",
        title="Signal 1 unfiltered"
    )
    signal1.plot(
        filename="s1-post-filt",
        title="Signal 1 filtered",
        filtered=True
    )

    signal2.apply_filter(3e5)
    signal2.plot_fft(
        filename="s2-fft-pre-filt",
        title="s2-pre-filt",
        ylim=[0, 1e5]
    )
    signal2.plot_fft(
        filename="s2-fft-post-filt",
        title="s2-post-filt",
        filtered=True, ylim=[0, 5e4]
    )
    signal2.plot(
        filename="s2-pre-filt",
        title="Signal 2 unfiltered"
    )
    signal2.plot(
        filename="s2-post-filt",
        title="Signal 2 filtered",
        filtered=True
    )


if __name__ == "__main__":
    args = cli.parser.parse_args()

    input_signal = sp.ps_signal(
        args.file,
        "signal3",
        start_ms=(start_intervall := (args.i[0] if args.i else None)),
        length_ms=(length_intervall := (args.i[1] if args.i else None)),
    )

    if args.lp:
        # Perform low pass filtering
        input_signal.apply_filter(cutoff=args.lp, order=5, type="low")

    if args.hp:
        # Perform highpass filtering
        input_signal.apply_filter(cutoff=args.hp, order=5, type="high")

    # print(args.bs)
    input_signal.plot(
        filtered=bool(args.lp) or bool(args.hp)
    )

"""
x1, y1, n1 = sp.calc_fft(fs, data1.acc)
x2, y2, n2 = sp.calc_fft(fs, data2.acc)
x3, y3, n3 = sp.calc_fft(fs, data3.acc)

fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(35, 14))

axes[0, 0].set_title("Ner FFT")
axes[0, 0].plot(x1[:n1//2] / 1000, abs(y1[:n1//2]), color='C0')
axes[0, 0].set_xlabel("Frequency (KHz)")
axes[0, 0].set_ylabel("Amplitude")
axes[0, 0].set_xlim([-50, 1200])

axes[0, 1].set_title("Towards Cylinder Head")
axes[0, 1].plot(data1.time + 50, data1.acc)
axes[0, 1].set_xlabel("Time (ms)")
axes[0, 1].set_ylabel("Amplitude")
axes[0, 1].set_xlim([-10, 130])
axes[0, 1].set_ylim([-40,40])

axes[0, 2].set_title("Lågpassfiltrerad på 300KHz")
axes[0, 2].plot(data1.time, data1_filt)
axes[0, 2].set_xlabel("Time (ms)")
axes[0, 2].set_ylabel("Amplitude")

axes[1, 0].set_title("Störningar FFT")
axes[1, 0].plot(x2[:n2//2] / 1000, abs(y2[:n2//2]), color='C0')
axes[1, 0].set_xlabel("Frequency (KHz)")
axes[1, 0].set_ylabel("Amplitude")
axes[1, 0].set_xlim([-50, 1200])

axes[1, 1].set_title("Störning")
axes[1, 1].plot(data2.time, data2.acc)
axes[1, 1].set_xlabel("Time (ms)")
axes[1, 1].set_ylabel("Amplitude")

axes[1, 2].set_title("Lågpassfiltrerad på  300KHz")
axes[1, 2].plot(data2.time, data2_filt)
axes[1, 2].set_xlabel("Time (ms)")
axes[1, 2].set_ylabel("Amplitude")

axes[2, 0].set_title("Upp FFT")
axes[2, 0].plot(x3[:n2//2] / 1000, abs(y3[:n2//2]), color='C0')
axes[2, 0].set_xlabel("Frequency (KHz)")
axes[2, 0].set_ylabel("Amplitude")
axes[2, 0].set_xlim([-50, 1200])

axes[2, 1].set_title("Towards Crank Case")
axes[2, 1].plot(data3.time - 190, data3.acc)
axes[2, 1].set_xlabel("Time (ms)")
axes[2, 1].set_ylabel("Amplitude")
axes[2, 1].set_xlim([-10, 130])
axes[2, 1].set_ylim([-40,40])

axes[2, 2].set_title("Lågpassfiltrerad 300KHz")
axes[2, 2].plot(data3.time, data3_filt)
axes[2, 2].set_xlabel("Time (ms)")
axes[2, 2].set_ylabel("Amplitude")

plt.tight_layout()
plt.savefig("FFT Plots.png")
"""
