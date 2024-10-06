from __future__ import annotations

import packaging.version
import semver

from arakawa.exceptions import ARError


def convert2semver(v: str) -> semver.Version:
    """Converts a PyPI version into a semver version"""
    ver = packaging.version.parse(v)

    prerelease: str = ""
    if ver.pre:
        pep440_prerelease_prefix, number = ver.pre

        if pep440_prerelease_prefix == "a":
            prerelease = "alpha"
        elif pep440_prerelease_prefix == "b":
            prerelease = "beta"
        else:
            raise ARError("Unsupported pre-release prefix", pep440_prerelease_prefix)

        if number > 0:
            prerelease += f".{number}"

    return semver.Version(*ver.release, prerelease=prerelease, build=ver.dev)
