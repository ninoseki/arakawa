"""
Arakawa helper functions to improve the Arakawa UX in IPython notebooks
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from arakawa.utils import display_msg

from .environment import get_environment
from .exceptions import BlocksNotFoundError, NotebookParityError

if TYPE_CHECKING:
    from arakawa.blocks import BaseBlock


def output_cell_to_block(cell: dict, ipython_output_cache: dict) -> BaseBlock | None:
    """Convert a IPython notebook output cell to An Arakawa Block"""
    from arakawa.blocks import wrap_block

    # Get the output object from the IPython output cache
    cell_output_object = ipython_output_cache.get(cell["execution_count"], None)

    # If there's no corresponding output object, skip
    if cell_output_object is not None:
        with suppress(Exception):
            return wrap_block(cell_output_object)

    return None


def check_notebook_cache_parity(
    notebook_json: dict, ipython_input_cache: list
) -> tuple[bool, list[int]]:
    """Check that the IPython output cache is in sync with the saved notebook"""
    is_dirty = False
    dirty_cells: list[int] = []

    # inline !bang commands (get_ipython().system), %line magics, and %%cell magics are not cached
    # exclude these from conversion
    ignored_cell_functions = [
        "get_ipython().system",
        "get_ipython().run_line_magic",
        "get_ipython().run_cell_magic",
    ]

    # broad check: check the execution count is the same
    execution_counts = [
        cell.get("execution_count", 0) or 0 for cell in notebook_json["cells"]
    ]

    latest_cell_execution_count = max(execution_counts, default=0)

    # -2 to account for zero-based indexing and the invoking cell not being saved
    latest_cache_execution_count = len(ipython_input_cache) - 2
    if latest_cache_execution_count != latest_cell_execution_count:
        is_dirty = True
        return is_dirty, dirty_cells

    # narrow check: check the cell source is the same for executed cells
    for cell in notebook_json["cells"]:
        cell_execution_count = cell.get("execution_count", None)
        if (
            cell["cell_type"] == "code"
            and cell_execution_count
            and cell_execution_count < len(ipython_input_cache)
        ):
            input_cache_source = ipython_input_cache[cell_execution_count].strip()

            # skip and mark cells containing ignored functions
            if any(
                ignored_function in input_cache_source
                for ignored_function in ignored_cell_functions
            ):
                cell["contains_ignored_functions"] = True
            # dirty because input has changed between execution and save.
            elif "".join(cell["source"]).strip() != input_cache_source:
                is_dirty = True
                dirty_cells.append(cell_execution_count)

    return is_dirty, dirty_cells


def cells_to_blocks(
    opt_out: bool = True, show_code: bool = False, show_markdown: bool = True
) -> list[BaseBlock]:
    """Convert IPython notebook cells to a list of Arakawa Blocks

    Recognized cell tags:
        - `ar-exclude` - Exclude this cell (when opt_out=True)
        - `ar-include` - Include this cell (when opt_out=False)
        - `ar-show-code` - Show the input code for this cell
        - `ar-show-markdown` - Show the markdown for this cell

    ..note:: IPython output caching must be enabled for this function to work. It is enabled by default.
    """
    environment = get_environment()
    if not environment.is_notebook_environment:
        raise ValueError("This function can only be used in a notebook environment")

    ip = environment.get_ipython()
    user_ns = ip.user_ns
    ipython_output_cache = user_ns["_oh"]
    ipython_input_cache = user_ns["_ih"]

    notebook_json = environment.get_notebook_json()
    # TODO: debug message for Colab, remove after testing

    notebook_is_dirty, dirty_cells = check_notebook_cache_parity(
        notebook_json, ipython_input_cache
    )

    if notebook_is_dirty:
        notebook_parity_message = "Please ensure all cells in the notebook have been executed and saved before running the conversion."

        if dirty_cells:
            notebook_parity_message += f"""

The following cells have not been executed and saved: {", ".join(map(str, dirty_cells))}"""

        raise NotebookParityError(notebook_parity_message)

    blocks = []

    for cell in notebook_json["cells"]:
        tags = cell["metadata"].get("tags", [])

        if (opt_out and "ar-exclude" not in tags) or (
            not opt_out and "ar-include" in tags
        ):
            if (cell["cell_type"] == "markdown" and cell.get("source")) and (
                show_markdown or "ar-show-markdown" in tags
            ):
                from arakawa.blocks.text import Text

                markdown_block: BaseBlock = Text("".join(cell["source"]))
                blocks.append(markdown_block)
            elif cell["cell_type"] == "code" and not cell.get(
                "contains_ignored_functions", False
            ):
                if "ar-show-code" in tags or show_code:
                    from arakawa.blocks.text import Code

                    code_block: BaseBlock = Code("".join(cell["source"]))
                    blocks.append(code_block)

                output_block = output_cell_to_block(cell, ipython_output_cache)

                if output_block:
                    blocks.append(output_block)
                elif "ar-include" in tags:
                    display_msg(
                        f"Cell output of type {type(ipython_output_cache.get(cell['execution_count']))} not supported. Skipping.",
                    )

    if not blocks:
        raise BlocksNotFoundError("No blocks found.")

    display_msg("Notebook converted to blocks.")

    return blocks
