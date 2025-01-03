from __future__ import annotations

import dataclasses
from enum import Enum
from pathlib import Path
from typing import Any, Generic, TypeVar

from arakawa.view import Blocks

from .file_store import DummyFileEntry, FileEntry, FileStore


@dataclasses.dataclass
class ViewState:
    # maybe a FileHandler interface??
    blocks: Blocks
    file_entry_klass: dataclasses.InitVar[type[FileEntry]]
    store: FileStore = dataclasses.field(init=False)
    view_json: dict[str, Any] = dataclasses.field(default_factory=dict)
    entries: dict[str, str] = dataclasses.field(default_factory=dict)
    dir_path: dataclasses.InitVar[Path | None] = None

    def __post_init__(self, file_entry_klass, dir_path):
        # TODO - should we use a lambda for file_entry_klass with dir_path captured?
        self.store = FileStore(fw_klass=file_entry_klass, assets_dir=dir_path)


P_IN = TypeVar("P_IN")
P_OUT = TypeVar("P_OUT")


class BaseProcessor(Generic[P_IN, P_OUT]):
    """Processor class that handles pipeline operations"""

    s: ViewState

    def __call__(self, x: P_IN) -> P_OUT:
        raise NotImplementedError("Implement in subclass")


# TODO - type this properly
class Pipeline(Generic[P_IN]):
    """
    A simple, programmable, eagerly-evaluated, pipeline specialized on ViewAST transformations
    similar to f :: State s => s ViewState x -> s ViewState y
    """

    # NOTE - toolz has an untyped function for this

    def __init__(self, s: ViewState, x: P_IN = None):
        self._state = s
        self._x = x

    def pipe(self, p: BaseProcessor[P_IN, P_OUT]) -> Pipeline[P_OUT]:
        p.s = self._state
        y = p.__call__(self._x)  # need to call as positional args
        self._state = p.s
        return Pipeline(self._state, y)

    @property
    def state(self) -> ViewState:
        return self._state

    @property
    def result(self) -> P_IN:
        return self._x


def mk_null_pipe(blocks: Blocks) -> Pipeline[None]:
    s = ViewState(blocks, file_entry_klass=DummyFileEntry)
    return Pipeline(s)


# Top-level API options / types
class Width(Enum):
    NARROW = "narrow"
    MEDIUM = "medium"
    FULL = "full"

    def to_css(self) -> str:
        if self == self.NARROW:
            return "max-w-3xl"
        if self == self.MEDIUM:
            return "max-w-screen-xl"
        return "max-w-full"


class TextAlignment(Enum):
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


class FontChoice(Enum):
    DEFAULT = "Inter, ui-sans-serif, system-ui"
    SANS = "ui-sans-serif, sans-serif, system-ui"
    SERIF = "ui-serif, serif, system-ui"
    MONOSPACE = "ui-monospace, monospace, system-ui"


@dataclasses.dataclass
class Formatting:
    """Configure styling and formatting"""

    bg_color: str = "#FFF"
    accent_color: str = "#4E46E5"
    font: FontChoice | str = FontChoice.DEFAULT
    text_alignment: TextAlignment = TextAlignment.LEFT
    width: Width = Width.MEDIUM
    light_prose: bool = False

    def to_css(self) -> str:
        font = self.font.value if isinstance(self.font, FontChoice) else self.font

        return f""":root {{
    --ar-accent-color: {self.accent_color};
    --ar-bg-color: {self.bg_color};
    --ar-text-align: {self.text_alignment.value};
    --ar-font-family: {font};
}}"""
