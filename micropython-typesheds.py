"""
Copies the Micropython typesheds into the given directory (defaults to current directory).
"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "7.3.19"  # Version set by https://github.com/hlovatt/tag2ver

from argparse import ArgumentParser
from io import BytesIO

# noinspection PyUnresolvedReferences
from os import scandir  # Not in Micropython `os`, hence suppression for CPython use.
from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory
from typing import Final
from urllib.request import urlopen
from zipfile import ZipFile


def main():
    parse_args: Final = ArgumentParser(
        description="Copy Micropython typesheds (a.k.a.: interface stubs, `pyi` files, and type hints) into given directory (directory must exist)"
    )
    parse_args.add_argument(
        "-V",
        "--version",
        help="show program's version number and exit",
        action="version",
        version="%(prog)s " + __version__,
    )
    parse_args.add_argument(
        "directory",
        help="directory (which must exist) into which typesheds are copied into",
    )
    args: Final = parse_args.parse_args()
    destination_dir: Final = Path(args.directory)
    if not destination_dir.is_dir():
        raise NotADirectoryError(
            f"Given destination directory, `{destination_dir}`, is not an existing directory!"
        )

    with urlopen(
        "https://github.com/hlovatt/PyBoardTypeshed/archive/master.zip"
    ) as http_response:
        with ZipFile(BytesIO(http_response.read())) as zipfile:
            typesheds: Final = [f for f in zipfile.namelist() if f.endswith(".pyi")]
            with TemporaryDirectory() as temp_top_level:
                zipfile.extractall(path=temp_top_level, members=typesheds)
                temp_typeshed_level = (
                    Path(temp_top_level)
                    / "PyBoardTypeshed-master"
                    / "micropython-typesheds"
                )
                for file in scandir(temp_typeshed_level):
                    copy2(file, destination_dir)


if __name__ == "__main__":
    main()
