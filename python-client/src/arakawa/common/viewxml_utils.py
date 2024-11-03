from __future__ import annotations

import dataclasses as dc
import importlib.resources as ir
import json
import math
import re
from collections.abc import Sized
from numbers import Number
from typing import Any

from loguru import logger as log
from lxml import etree
from lxml.etree import DocumentInvalid
from lxml.etree import _Element as ElementT
from micawber import ProviderException, bootstrap_basic, bootstrap_noembed, cache

from arakawa.exceptions import ARError

from .ar_types import HTML, SSDict

local_view_resources = ir.files("arakawa.resources.view_resources")
rng_validator = etree.RelaxNG(file=str(local_view_resources / "full_schema.rng"))

ViewXML = str


def load_doc(x: str) -> ElementT:
    parser = etree.XMLParser(
        strip_cdata=False, recover=True, remove_blank_text=True, remove_comments=True
    )
    return etree.fromstring(x, parser=parser)


def is_valid_id(id: str) -> bool:
    """(cached) regex to check for a xsd:ID name"""
    return re.fullmatch(r"^[a-zA-Z_][\w.-]*$", id) is not None


def validate_view_doc(
    xml_str: str | None = None,
    xml_doc: ElementT | None = None,
    quiet: bool = False,
) -> bool:
    """Validate the model against the schema, throws an etree.DocumentInvalid if not"""
    assert xml_str or (xml_doc is not None)

    if xml_str:
        xml_doc = etree.fromstring(xml_str)

    try:
        rng_validator.assertValid(xml_doc)
        return True
    except DocumentInvalid:
        if not quiet:
            xml_str = xml_str if xml_str else etree.tostring(xml_doc, pretty_print=True)
            log.error(
                f"Error validating report document:\n\n{xml_str}\n{rng_validator.error_log}\n"
            )
        raise


def conv_attrib(v: Any) -> str | None:
    """
    Convert a value to a str for use as an ElementBuilder attribute
    - also handles None to a string for optional field values
    """
    # TODO - use a proper serialisation framework here / lxml features
    if v is None:
        return v
    if isinstance(v, Sized) and len(v) == 0:
        return None
    if isinstance(v, str):
        return v
    if isinstance(v, Number) and not isinstance(v, bool):
        if math.isinf(v) and v > 0:
            return "INF"
        if math.isinf(v) and v < 0:
            return "-INF"
        if math.isnan(v):
            return "NaN"
        return str(v)
    return json.dumps(v)


def mk_attribs(**attribs: Any) -> SSDict:
    """convert attributes, dropping None and empty values"""
    return {
        str(k): v1 for (k, v) in attribs.items() if (v1 := conv_attrib(v)) is not None
    }


#####################################################################
# Embed Asset Helpers
providers = bootstrap_basic(cache=cache.Cache())


@dc.dataclass(frozen=True)
class Embedded:
    html: HTML
    title: str
    provider: str


def get_embed_url(url: str, width: int = 960, height: int = 540) -> Embedded:
    """Return html for an embeddable URL"""
    try:
        r = providers.request(url, maxwidth=width, maxheight=height)
    except ProviderException:
        # add NoEmbed to the list and try again
        try:
            log.debug("Initializing NoEmbed OEmbed provider")
            bootstrap_noembed(registry=providers)
            r = providers.request(url, maxwidth=width, maxheight=height)
        except ProviderException as e:
            raise ARError(
                f"No embed provider found for URL '{url}' - is there an active internet connection?"
            ) from e

    return Embedded(
        html=r["html"],
        title=r.get("title", "Title"),
        provider=r.get("provider_name", "Embedding"),
    )
