from arakawa.blocks.controls import ControlBlock


class TestControlBlock(ControlBlock):
    _tag = "Dummy"


def test_name():
    block = TestControlBlock(name="foo")
    dumped = block.model_dump(by_alias=True, exclude_none=True)
    # should have both name and id
    assert dumped == {"name": "foo", "id": "foo", "_tag": "Dummy"}
