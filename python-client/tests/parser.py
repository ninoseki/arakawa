from html.parser import HTMLParser
from typing import Any


class TagsRecorderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.start_tags: list[Any] = []
        self.end_tags: list[Any] = []

    def _has_any_tags(self):
        return len(self.start_tags) > 0

    def _has_same_number_of_tags(self):
        return len(self.start_tags) == len(self.end_tags)

    def is_valid(self):
        return self._has_any_tags() and self._has_same_number_of_tags()

    def handle_starttag(self, tag: Any, _: Any):
        self.start_tags.append(tag)

    def handle_endtag(self, tag: Any):
        self.end_tags.append(tag)
