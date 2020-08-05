"""Module that contains functions for plotting.
"""
from functools import wraps
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)


def _plotting_dispatch(fn):
    """Dispatch decorator used to dispatch function calls to other
    functions depending on the wanted "style". Using .register to add
    functions into the dispatch list with a specified "style".

    Examples:

        .. code-block::

            @_plotting_dispatch
            def plot_data(signal, **kwargs):
                print("Default!")

            @plot_data.register("time_series"):
                print("Dispatched to 'time_series!'")

            @plot_data.register("fft"):
                print("Dispatched to 'fft!'")

    Args:
        fn (function): The function to be "decorated". The function will
            not get decorated, but will be returned as is. It will though
            be added as the default option in case a call is not dispatched
            to another function.

    Returns:
        function: Return the function as is, register it as a default
        function for dispatching.
    """
    registry = dict()
    registry['default'] = fn

    def register(style):
        def inner(fn):
            registry[style] = fn
            return fn
        return inner

    @wraps(fn)
    def decorator(style, *args, **kwargs):
        fn = registry.get(style, registry['default'])
        return fn(*args, **kwargs)

    decorator.register = register
    return decorator


@_plotting_dispatch
def plot_data(signal, **kwargs):
    """The function that will be used as a dispatcher. The intention
    is that this function body never is executed.

    Args:
        signal (Signal): The Signal object to be plotted.

    Note:

        As this function is decorated, it has to be added manually in
        ps_signal.signals.rst

        .. code-block::

            .. automodule:: ps_signal.signals.plot
                :members: plot_data, _plot_time_series, _plot_fft
                :undoc-members:
                :show-inheritance:

    """
    pass


@plot_data.register("time_series")
def _plot_time_series(*, signal, **kwargs):
    """This function is registered as a plotting function
    for the time series-"style".

    x- and y-labels are applied to fit a time-series.

    The plotting is made in this way, i.e. separated generation of figure
    and axes, to make it easier to customize the plotting for the future
    using the **kwargs** argument.

    Args:
        signal (Signal): The Signal object to be plotted.

    Note:

        As this function is decorated, it has to be added manually in
        ps_signal.signals.rst

        .. code-block::

            .. automodule:: ps_signal.signals.plot
                :members: plot_data, _plot_time_series, _plot_fft
                :undoc-members:
                :show-inheritance:

    """
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
def _plot_fft(*, signal, **kwargs):
    """This function is registered as a plotting function
    for the fft-"style".

    This function will thus plot the given FFT of a Signal object.
    It applies certain x- and y-axis limitations that is commonly used
    as well as x- and y-labels that are fits a FFT plot.

    * X-axis is limited between 0 and 2000KHz, i.e. 2MHz.
    * Y-axis is limited between 0 and 500K.

    The plotting is made in this way, i.e. separated generation of figure
    and axes, to make it easier to customize the plotting for the future
    using the **kwargs** argument.

    Args:
        signal (Signal): The Signal object to be plotted.

    Note:

        As this function is decorated, it has to be added manually in
        ps_signal.signals.rst

        .. code-block::

            .. automodule:: ps_signal.signals.plot
                :members: plot_data, _plot_time_series, , _plot_fft
                :undoc-members:
                :show-inheritance:

    """
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
