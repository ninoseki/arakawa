import os

os.environ["AR_TEST_ENV"] = "true"

import pytest

from arakawa import ARMode, set_ar_mode


@pytest.fixture(autouse=True)
def dp_setup():
    set_ar_mode(ARMode.SCRIPT)
