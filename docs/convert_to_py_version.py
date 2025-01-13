import typer
import packaging.version


def main(version: str):
    """convert semver to PyPI version"""
    parsed = packaging.version.parse(version)
    print(parsed)  # noqa: T201


if __name__ == "__main__":
    typer.run(main)
