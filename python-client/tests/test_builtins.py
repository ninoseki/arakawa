from html.parser import HTMLParser

import pytest

import arakawa as ar

from .builtins import demo


@pytest.fixture
def parser():
    return HTMLParser()


def test_stringify(parser: HTMLParser):
    report = ar.Report(demo())
    html = report.stringify()
    assert parser.feed(html) is None
