# import ps_signal.signal_processing as sp
# import ps_signal.cli as cli


from . import interfaces


def print_globals():
    for k in dict(globals()).keys():
        print(k)


def print_namespace(namespace):
    for k in namespace.__dict__.keys():
        print(k)


def main():
    interfaces.run_cli()

    # print("\nGlobals")
    # print_globals()

    # print("\ninterfaces")
    # print_namespace(interfaces)

    # signal.fft.perform_fft_on_signal()
    # signal.filter.apply_low_pass_filter()
    # validators.file.is_picoscope_file()


if __name__ == "__main__":
    main()
