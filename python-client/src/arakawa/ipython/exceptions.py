from arakawa.utils import display_msg


class NotebookError(Exception):
    """Exception raised when a Notebook to Arakawa conversion fails."""

    def _render_traceback_(self):
        display_msg(
            f"""**Conversion failed**

{self!s}"""
        )


class NotebookParityError(NotebookError):
    """Exception raised when IPython output cache is not in sync with the saved notebook"""


class BlocksNotFoundError(NotebookError):
    """Exception raised when no blocks are found during conversion"""
