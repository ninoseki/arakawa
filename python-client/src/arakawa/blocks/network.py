from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

import humps
from pydantic import Field

from arakawa import optional_libs as opt
from arakawa.exceptions import ARError

from .base import DataBlock
from .mixins import OptionalLabelMixin, OptionalNameMinx

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


class LayoutSettings(TypedDict, total=False):
    adjust_sizes: bool | None
    barnes_hut_optimize: bool | None
    barnes_hut_theta: int | float | None
    edge_weight_influence: int | float | None
    gravity: int | float | None
    lin_log_mode: bool | None
    outbound_attraction_distribution: bool | None
    scaling_ratio: int | float | None
    slow_down: int | float | None
    strong_gravity_mode: bool | None


class Sigma(OptionalNameMinx, OptionalLabelMixin, DataBlock):
    _tag = "Sigma"

    data: dict[str, Any] = Field(...)
    width: int = Field(...)
    height: int = Field(...)
    layout_settings: LayoutSettings = Field(...)

    def __init__(
        self,
        data: dict[str, Any],
        width: int = 960,
        height: int = 540,
        layout_settings: LayoutSettings | None = None,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            data: A Sigma/Graphology graph data to attach
            width: A width of the graph
            height: A height of the graph
            layout_settings: see https://www.npmjs.com/package/graphology-layout-forceatlas2#settings (optional, each key should be snake_cased)
            name: A unique name for the block to reference when adding text or embedding (optional)
            label: A label used when displaying the block (optional)
        """
        super().__init__(
            data=data,
            layout_settings=humps.camelize(layout_settings or {}),
            name=name,
            label=label,
            width=width,
            height=height,
        )


def network_graph_to_sigma(G: opt.NXGraph, layout_function: Callable[[Any], Any]):  # noqa: N803
    data = {
        "options": {
            "type": "directed" if G.is_directed() else "undirected",
            "multi": bool(G.is_multigraph()),
            "allowSelfLoops": True,
        },
        "attributes": G.graph,
        "nodes": [
            {"key": node_id, "attributes": attributes}
            for node_id, attributes in dict(G.nodes(data=True)).items()
        ],
        "edges": [
            {"key": idx, "source": src, "target": tar, "attributes": attr}
            for idx, (src, tar, attr) in enumerate(list(G.edges(data=True)))
        ],
    }
    absence_of_layout_info = False
    for node_data in data["nodes"]:
        if "x" not in node_data["attributes"] or "y" not in node_data["attributes"]:
            absence_of_layout_info = True
            break

    if absence_of_layout_info:
        layout = layout_function(G)
        for node_data in data["nodes"]:
            node_data["attributes"]["x"] = layout[node_data["key"]][0]
            node_data["attributes"]["y"] = layout[node_data["key"]][1]

    return data


class NetworkX(Sigma):
    """
    The NetworkX block allows you to embed an NetworkX graph (rendered by Sigma.js) into your app.
    """

    def __init__(
        self,
        graph: opt.NXGraph,
        width: int = 960,
        height: int = 540,
        layout_settings: LayoutSettings | None = None,
        layout_function: Callable[[opt.NXGraph], Any] | None = None,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            graph: An NetworkX graph to attach
            width: A width of the graph
            height: A height of the graph
            layout_settings: see https://www.npmjs.com/package/graphology-layout-forceatlas2#settings (optional, each key should be snake_cased)
            layout_function: A layout function. Defaults to spring_layout.
            name: A unique name for the block to reference when adding text or embedding (optional)
            label: A label used when displaying the block (optional)
        """
        if not opt.HAVE_NETWORKX:
            raise ARError(
                "NetworkX is not installed. Please install networkx to use this block."
            )

        super().__init__(
            data=network_graph_to_sigma(
                graph, layout_function=layout_function or opt.networkx.spring_layout
            ),
            layout_settings=layout_settings,
            name=name,
            label=label,
            height=height,
            width=width,
        )
