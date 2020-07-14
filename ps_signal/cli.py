import argparse


welcome = "Python script for performing FFT and plotting \
           .csv data aquired from a Picoscope."

file_help = "Path to the file containting the data in .csv format."
interval_help = "The interval in the data you want to analyze."
fft_help = "Apply fft on the signal."
lowpass_help = "Apply low pass filter to the signal. Effectively removing \
                frequencies that is higher than the cutoff. Cutoff \
                given in Hz."
highpass_help = "Apply high pass filter to the signal. Effectively \
                 removing frequencies that is lower than the cutoff. \
                 Cutoff given in Hz."
bandstop_help = "Apply band stop filter to the signal. Effectively removing \
                 frequencies that is between the specified frequencies. \
                 Cutoff given in Hz."
output_help = "Folder for output. Note: Not a file but a folder as this \
               script will output several files."
title_help = "Title that will be applied to the plot."
version_help = "Shows the current version of this package."

parser = argparse.ArgumentParser(
    description=welcome,
    prog="ps_signal"
)
parser.add_argument(
    "file",
    metavar="file",
    help=file_help
)
parser.add_argument(
    "-i",
    metavar=("lower", "upper"),
    nargs=2,
    required=False,
    type=int,
    help=interval_help,
)
parser.add_argument(
    "-fft",
    action="store_true",
    required=False,
    help=fft_help
)
parser.add_argument(
    "-lp",
    metavar="cutoff",
    required=False,
    type=float,
    help=lowpass_help
)
parser.add_argument(
    "-hp",
    metavar="cutoff",
    required=False,
    type=float,
    help=highpass_help
)
parser.add_argument(
    "-bs",
    metavar=("lower", "upper"),
    nargs=2,
    required=False,
    type=float,
    help=bandstop_help,
)
parser.add_argument(
    "-o",
    metavar="dir",
    required=False,
    type=int,
    help=output_help
)

parser.add_argument(
    "-t",
    metavar="title",
    required=False,
    type=str,
    help=title_help
)

parser.add_argument(
    "--version",
    action="store_true",
    required=False,
    help=version_help
)

# For testing purposes during development only.
if __name__ == "__main__":
    args = parser.parse_args()
    print(args.file)
