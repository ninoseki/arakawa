import argparse
import packaging.version


def main(version: str):
    """convert semver to PyPI version"""
    parsed = packaging.version.parse(version)
    print(parsed)  # noqa: T201


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert semver to PyPI version")
    parser.add_argument("version", type=str, help="Version string to convert")
    args = parser.parse_args()

    version: str = str(args.version)

    main(version)
