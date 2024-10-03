from __future__ import annotations

import importlib.resources as ir
import json
from abc import ABC
from copy import copy
from itertools import count
from os import path as osp
from pathlib import Path
from typing import Any, BinaryIO, cast
from uuid import uuid4

from jinja2 import Environment, FileSystemLoader, Template, pass_context
from jinja2.utils import htmlsafe_json_dumps
from lxml import etree
from markupsafe import Markup

from arakawa import blocks as b
from arakawa.client.utils import display_msg, log, open_in_browser
from arakawa.common import HTML, NPath, timestamp, validate_view_doc
from arakawa.common.viewxml_utils import ElementT, local_view_resources
from arakawa.exceptions import InvalidReportError
from arakawa.view import PreProcess, XMLBuilder

from .file_store import FileEntry
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


class ConvertXML(BaseProcessor):
    """Convert the View AST into an XML fragment"""

    local_post_xslt = etree.parse(str(local_view_resources / "local_post_process.xslt"))
    local_post_transform = etree.XSLT(local_post_xslt)

    def __init__(self, *, pretty_print: bool = False, fragment: bool = False) -> None:
        self.pretty_print: bool = pretty_print
        self.fragment: bool = fragment
        super().__init__()

    def __call__(self, _: Any) -> ElementT:
        initial_doc = self.convert_xml()
        transformed_doc = self.post_transforms(initial_doc)

        # convert to string
        view_xml_str: str = etree.tounicode(
            transformed_doc, pretty_print=self.pretty_print
        )
        # s1 = dc.replace(s, view_xml=view_xml_str)
        self.s.view_xml = view_xml_str

        log.debug(etree.tounicode(transformed_doc, pretty_print=True))

        # return the doc for further processing (xml str stored in state)
        return transformed_doc

    def convert_xml(self) -> ElementT:
        # create initial state
        builder_state = XMLBuilder(store=self.s.store)
        self.s.blocks.accept(builder_state)
        return builder_state.get_root(self.fragment)

    def post_transforms(self, view_doc: ElementT) -> ElementT:
        # TODO - post-xml transformations, essentially xslt / lxml-based DOM operations
        # post_process via xslt
        processed_view_doc: ElementT = self.local_post_transform(view_doc)

        # TODO - custom lxml-based transforms go here...

        # validate post all transformations
        validate_view_doc(xml_doc=processed_view_doc)
        return processed_view_doc


class PreUploadProcessor(BaseProcessor):
    def __call__(self, doc: ElementT) -> tuple[str, list[BinaryIO]]:
        """
        pre-upload pass of the XML doc so can be uploaded to DPCloud
        modifies the document based on the FileStore
        """

        # NOTE - this currently relies on all assets existing linearly in document order
        # in the asset store - if we move to a cas we will need to update the algorithm here
        # replace ref -> attachment in view
        # all blocks with a ref
        refs: list[ElementT] = doc.xpath("/View//*[@src][starts-with(@src, 'ref://')]")
        for idx, ref, f_entry in zip(count(0), refs, self.s.store.files):
            ref: ElementT
            f_entry: FileEntry
            _hash: str = ref.get("src").split("://")[1]
            ref.set("src", f"attachment://{idx}")
            assert _hash == f_entry.hash  # sanity check

        self.s.view_xml = etree.tounicode(doc)
        return (self.s.view_xml, self.s.store.file_list)


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
        from arakawa import __version__

        return f"https://cdn.jsdelivr.net/npm/arakawa@{__version__}/dist"

    def _write_html_template(
        self,
        name: str,
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
    ) -> tuple[str, str]:
        """Internal method to write the ViewXML and assets into a HTML container and associated files"""
        name = name or "app"
        formatting = formatting or Formatting()

        report_id: str = uuid4().hex

        # TODO - split this out?
        vs = self.s
        if vs:
            assets = vs.store.as_dict() or {}
            view_xml = vs.view_xml
        else:
            assets = {}
            view_xml = ""

        app_data = {"view_xml": view_xml, "assets": assets}
        html = self.template.render(
            # Escape JS multi-line strings
            app_data=htmlsafe_json_dumps(app_data),
            report_width_class=formatting.width.to_css(),
            report_name=name,
            report_date=timestamp(),
            css_header=formatting.to_css(),
            is_light_prose=json.dumps(formatting.light_prose),
            events=False,
            report_id=report_id,
            cdn_base=cdn_base or self.get_cdn(),
        )

        return html, report_id


class ExportBaseHTMLOnly(BaseExportHTML):
    """Export the base view used to render an App, containing no ViewXML nor Assets"""

    # TODO (JB) - Create base HTML-only template
    template_name = "local_template.html"

    def __init__(
        self,
        debug: bool,
        formatting: Formatting | None = None,
    ):
        self.debug = debug
        self.formatting = formatting

    def generate_chrome(self) -> HTML:
        # TODO - this is a bit hacky
        self.s = None
        html, _ = self._write_html_template(
            "app",
            formatting=self.formatting,
        )
        return HTML(html)

    def get_cdn(self) -> str:
        return "/web-static" if self.debug else super().get_cdn()

    def __call__(self, _: Any) -> None:
        return None


class ExportHTMLInlineAssets(BaseExportHTML):
    """
    Export a view into a single HTML file containing:
    - View XML - embedded
    - Assets - embedded as b64 data-uris
    """

    template_name = "local_template.html"

    def __init__(
        self,
        path: str,
        open: bool = False,
        name: str = "app",
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
    ):
        self.path = path
        self.open = open
        self.name = name
        self.formatting = formatting
        self.cdn_base = cdn_base

    def __call__(self, _: Any) -> str:
        html, report_id = self._write_html_template(
            name=self.name,
            formatting=self.formatting,
            cdn_base=self.cdn_base,
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

    template_name = "local_template.html"

    def __init__(
        self,
        app_dir: Path,
        name: str = "app",
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
    ):
        self.app_dir = app_dir
        self.name = name
        self.formatting = formatting
        self.cdn_base = cdn_base

    def __call__(self, dest: NPath | None = None) -> Path:
        html, _ = self._write_html_template(
            name=self.name,
            formatting=self.formatting,
            cdn_base=self.cdn_base,
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

    template_name = "ipython_template.html"

    def __init__(
        self,
        name: str = "Stringified App",
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
    ):
        self.name = name
        self.formatting = formatting
        self.cdn_base = cdn_base

    def __call__(self, _: Any) -> HTML:
        html, _ = self._write_html_template(
            name=self.name, formatting=self.formatting, cdn_base=self.cdn_base
        )
        return HTML(html)
