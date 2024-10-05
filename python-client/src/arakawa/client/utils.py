import string
import sys
from typing import Any

from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger


def get_logger():
    logger = _Logger(
        core=_Core(),
        exception=None,
        depth=0,
        record=False,
        lazy=False,
        colors=False,
        raw=False,
        capture=True,
        patchers=[],
        extra={},
    )
    logger.add(sys.stderr, level="WARNING")
    return logger


log = get_logger()

_have_setup_logging: bool = False


def enable_logging():
    """Enable logging for debug purposes"""
    global _have_setup_logging

    log.remove(0)
    log.add(sys.stderr, level="DEBUG")

    _have_setup_logging = True


def print_debug_info():
    """Print useful debugging information"""
    fields = {}

    # Known dependencies
    import numpy as np
    import pandas as pd
    import pyarrow as pa

    fields["pandas_version"] = pd.__version__
    fields["numpy_version"] = np.__version__
    fields["pyarrow_version"] = pa.__version__

    for _k, _v in fields.items():
        pass


################################################################################
# Output
def open_in_browser(url: str):
    """Open the given URL in the user's browser"""
    from arakawa.ipython.environment import get_environment

    environment = get_environment()

    # TODO - this is a bit of a hack, but works for now. JupyterLab (Codespaces) doesn't support webbrowser.open.
    if (
        environment.is_notebook_environment
        and not environment.can_open_links_from_python
    ):
        ip = environment.get_ipython()
        ip.run_cell_magic("javascript", "", f'window.open("{url}", "_blank")')
    else:
        import webbrowser

        webbrowser.open(url, new=1)


class MarkdownFormatter(string.Formatter):
    """Support {:l} and {:cmd} format fields"""

    in_jupyter: bool

    def __init__(self, in_jupyter: bool):
        self.in_jupyter = in_jupyter
        super().__init__()

    def format_field(self, value: Any, format_spec: str) -> Any:
        if format_spec.endswith("l"):
            if self.in_jupyter:
                value = f"<a href='{value}' target='_blank'>here</a>"
            else:
                value = f"at {value}"
            format_spec = format_spec[:-1]
        elif format_spec.endswith("cmd"):
            value = f"!{value}" if self.in_jupyter else value
            format_spec = format_spec[:-3]
        return super().format_field(value, format_spec)


def display_msg(text: str, **params: str):
    from arakawa.ipython.environment import get_environment

    environment = get_environment()

    msg = MarkdownFormatter(environment.is_notebook_environment).format(text, **params)
    if environment.is_notebook_environment:
        from IPython.display import Markdown, display

        display(Markdown(msg))
    else:
        print(msg)  # noqa: T201
