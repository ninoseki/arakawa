from __future__ import annotations

import importlib.resources as ir
import json
from abc import ABC
from copy import copy
from os import path as osp
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import humps
from jinja2 import Environment, FileSystemLoader, Template, pass_context
from jinja2.utils import htmlsafe_json_dumps
from markupsafe import Markup

from arakawa import blocks as b
from arakawa.common import timestamp
from arakawa.exceptions import InvalidReportError
from arakawa.types import HTML, NPath
from arakawa.utils import display_msg, open_in_browser
from arakawa.view import PreProcess

from .types import BaseProcessor, Formatting


@pass_context
def include_raw(ctx, name) -> Markup:
    """Normal jinja2 {% include %} doesn't escape {{...}} which appear in React's source code"""
    env = ctx.environment
    # Escape </script> to prevent 3rd party JS terminating the local app bundle.
    # Note there's an extra "\" because it needs to be escaped at both the python and JS level
    src = env.loader.get_source(env, name)[0].replace("</script>", r"<\\/script>")
    return Markup(src)


class PreProcessView(BaseProcessor):
    """Optimization to improve the layout of the view using the Block-API"""

    def __init__(self, *, is_finalized: bool = True) -> None:
        self.is_finalized = is_finalized
        super().__init__()

    def __call__(self, _: Any) -> None:
        # AST checks
        if len(self.s.blocks.blocks) == 0:
            raise InvalidReportError(
                "Empty blocks object - must contain at least one block"
            )

        # convert Page -> Select + Group
        v = copy(self.s.blocks)
        if all(isinstance(blk, b.Page) for blk in v.blocks):
            # convert to top-level Select
            v.blocks = [
                b.Select(
                    blocks=[
                        b.Group(blocks=p.blocks, label=p.title, name=p.name)
                        for p in cast(list[b.Page], v.blocks)
                    ],
                    type=b.SelectType.TABS,
                )
            ]

        # Block-API visitors
        pp = PreProcess(is_finalized=self.is_finalized)
        v.accept(pp)
        v1 = pp.root
        # v1 = copy(v)

        # update the processor state
        self.s.blocks = v1

        return


class ConvertPydantic(BaseProcessor):
    def __init__(self, *, pretty_print: bool = False, fragment: bool = False) -> None:
        self.pretty_print: bool = pretty_print
        self.fragment: bool = fragment
        super().__init__()

    def __call__(self, _: Any):
        from arakawa.view.pydantic_visitor import PydanticBuilder

        builder_state = PydanticBuilder(store=self.s.store)
        self.s.blocks.accept(builder_state)
        view = builder_state.get_root(self.fragment)
        self.s.view_json = humps.camelize(
            view.model_dump(mode="json", by_alias=True, exclude_none=True)
        )
        return view


###############################################################################
# HTML Exporting Processors
class BaseExportHTML(BaseProcessor, ABC):
    """Provides shared logic for writing an app to local disk"""

    # Type is `ir.abc.Traversable` which extends `Path`,
    # but the former isn't compatible with `shutil`
    template_dir: Path = cast(Path, ir.files("arakawa.resources.html_templates"))
    template: Template

    template_name: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        template_loader = FileSystemLoader(cls.template_dir)
        template_env = Environment(loader=template_loader)
        template_env.globals["include_raw"] = include_raw
        cls.template = template_env.get_template(cls.template_name)

    def get_cdn(self) -> str:
        from arakawa import settings

        return settings.AR_CDN_BASE

    def _write_html_template(
        self,
        name: str,
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
        standalone: bool = False,
    ) -> tuple[str, str]:
        """Internal method to write the ViewXML and assets into a HTML container and associated files"""
        name = name or "app"
        formatting = formatting or Formatting()

        report_id: str = uuid4().hex

        # TODO - split this out?
        vs = self.s
        if vs:
            assets = vs.store.as_dict() or {}
            view_json = vs.view_json
        else:
            assets = {}
            view_json = {}

        app_data = {"viewJson": view_json, "assets": assets}
        html = self.template.render(
            # Escape JS multi-line strings
            app_data=htmlsafe_json_dumps({"data": {"result": app_data}}),
            report_width_class=formatting.width.to_css(),
            report_name=name,
            report_date=timestamp(),
            css_header=formatting.to_css(),
            is_light_prose=json.dumps(formatting.light_prose),
            events=True,
            report_id=report_id,
            cdn_base=cdn_base or self.get_cdn(),
            standalone=standalone,
        )

        return html, report_id


class ExportHTMLInlineAssets(BaseExportHTML):
    """
    Export a view into a single HTML file containing:
    - View XML - embedded
    - Assets - embedded as b64 data-uris
    """

    template_name = "local_template.html.j2"

    def __init__(
        self,
        path: str,
        open: bool = False,
        name: str = "app",
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
        standalone: bool = False,
    ):
        self.path = path
        self.open = open
        self.name = name
        self.formatting = formatting
        self.cdn_base = cdn_base
        self.standalone = standalone

    def __call__(self, _: Any) -> str:
        html, report_id = self._write_html_template(
            name=self.name,
            formatting=self.formatting,
            cdn_base=self.cdn_base,
            standalone=self.standalone,
        )

        Path(self.path).write_text(html, encoding="utf-8")

        display_msg(f"App saved to ./{self.path}")

        if self.open:
            path_uri = f"file://{osp.realpath(osp.expanduser(self.path))}"
            open_in_browser(path_uri)

        return report_id


class ExportHTMLFileAssets(BaseExportHTML):
    """
    Export a view into a single HTML file on disk, containing
    - View XML - embedded
    - Assets - referenced as remote resources
    """

    template_name = "local_template.html.j2"

    def __init__(
        self,
        app_dir: Path,
        name: str = "app",
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
        standalone: bool = False,
    ):
        self.app_dir = app_dir
        self.name = name
        self.formatting = formatting
        self.cdn_base = cdn_base
        self.standalone = standalone

    def __call__(self, _: NPath | None = None) -> Path:
        html, _ = self._write_html_template(
            name=self.name,
            formatting=self.formatting,
            cdn_base=self.cdn_base,
            standalone=self.standalone,
        )

        index_path = self.app_dir / "index.html"
        index_path.write_text(html, encoding="utf-8")
        display_msg(f"Built app in {self.app_dir}")
        return self.app_dir


class ExportHTMLStringInlineAssets(BaseExportHTML):
    """
    Export the View as an in-memory string representing a resizable HTML fragment, containing
    - View XML - embedded
    - Assets - embedded as b64 data-uris
    """

    template_name = "ipython_template.html.j2"

    def __init__(
        self,
        name: str = "Stringified App",
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
        standalone: bool = False,
    ):
        self.name = name
        self.formatting = formatting
        self.cdn_base = cdn_base
        self.standalone = standalone

    def __call__(self, _: Any) -> HTML:
        html, _ = self._write_html_template(
            name=self.name,
            formatting=self.formatting,
            cdn_base=self.cdn_base,
            standalone=self.standalone,
        )
        return HTML(html)


class ExportHTMLStringInlineNonResizableAssets(ExportHTMLStringInlineAssets):
    """
    Export the View as an in-memory string representing a non-resizable HTML fragment, containing
    - View XML - embedded
    - Assets - embedded as b64 data-uris
    """

    template_name = "local_template.html.j2"
