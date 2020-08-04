import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

__all__ = ['plot_data']


def plotting_dispatch(fn):
    registry = dict()
    registry['default'] = fn

    def register(style):
        def inner(fn):
            registry[style] = fn
            return fn
        return inner

    def decorator(style, *args, **kwargs):
        fn = registry.get(style, registry['default'])
        return fn(*args, **kwargs)

    decorator.register = register
    return decorator


@plotting_dispatch
def plot_data(signal, **kwargs):
    print("Choose a style!")


@plot_data.register("time_series")
def plot_time_series(*, signal, **kwargs):
    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html
    fig = plt.figure(figsize=(14, 10))

    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.axes.html
    ax = plt.axes(
        xlabel="Time (ms)",
        ylabel="Amplitude",
        title=f"Time series\nApplied filters: {signal.filter_string}"
    )
    fig.suptitle(signal.id)
    plt.plot(signal.data.time, signal.data.acc, figure=fig, axes=ax)

    plt.savefig(f"{signal.output_filename}.png")
    plt.close()


@plot_data.register("fft")
def plot_fft(*, signal, **kwargs):
    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html
    fig = plt.figure(figsize=(14, 10))

    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.axes.html
    ax = plt.axes(
        xlabel="Frequency",
        ylabel="Amplitude",
        title=f"FFT\nApplied filters: {signal.filter_string}",
        xlim=(0, 2_000),
        ylim=(0, 500_000)
    )
    fig.suptitle(signal.id)
    plt.plot(signal._fft.x, signal._fft.y, figure=fig, axes=ax)

    plt.savefig(f"{signal.output_filename}-fft.png")
    plt.close()
