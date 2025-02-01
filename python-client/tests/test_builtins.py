import pytest

import arakawa as ar

from .builtins import demo
from .parser import TagsRecorderParser


@pytest.fixture
def parser():
    return TagsRecorderParser()


def test_stringify(parser: TagsRecorderParser):
    report = ar.Report(demo())
    html = report.stringify()

    parser.feed(html)
    assert parser.is_valid()
