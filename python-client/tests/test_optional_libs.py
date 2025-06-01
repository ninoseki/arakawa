import itertools

import pytest
import tomlkit
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from pyproject_metadata import StandardMetadata

from arakawa import optional_libs


def get_specifiers() -> set[str]:
    def is_specifier(name: str):
        return name.endswith("_V_SPECIFIER")

    return {name for name in dir(optional_libs) if is_specifier(name)}


def get_specifier_by_name(name: str) -> SpecifierSet:
    return getattr(optional_libs, name)


@pytest.fixture(params=get_specifiers())
def name_and_specifier(request: pytest.FixtureRequest) -> tuple[str, SpecifierSet]:
    specifier = get_specifier_by_name(request.param)
    name = str(request.param).lower().removesuffix("_v_specifier")
    return name, specifier


@pytest.fixture(scope="session")
def pyproject_metadata():
    with open("pyproject.toml") as f:
        parsed = tomlkit.parse(f.read())

    return StandardMetadata.from_pyproject(parsed)


@pytest.fixture(scope="session")
def requirements(pyproject_metadata: StandardMetadata) -> set[Requirement]:
    return set(
        itertools.chain.from_iterable(pyproject_metadata.optional_dependencies.values())
    )


def test_validate_optional_libs_specifier_sets(
    name_and_specifier: tuple[str, Requirement], requirements: set[Requirement]
):
    name, specifier_set = name_and_specifier

    def eq(req: Requirement):
        return req.name == name and req.specifier == specifier_set

    assert any(eq(req) for req in requirements)
