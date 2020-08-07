"""Package that contains the different options for how the user can interact
with the package, such as CLI or GUI. Each option should be implemented as a
subpackage with a function run_<option> to invoke it.

Examples:

    * :func:`cli.run_cli()` - Function that is used to invoke the CLI from
      the __main__.py.

    * :func:`gui.run_gui()` - Function that is used to invoke the GUI from
      the __main__.py

"""
from .cli import *
from .gui import *
