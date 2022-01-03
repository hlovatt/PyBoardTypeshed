"""
Copies the Micropython typesheds into the given directory (defaults to current directory).
"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "7.3.16"  # Version set by https://github.com/hlovatt/tag2ver

# Have to supress inspection for missing `scandir` in `os` because Micropython's `os` doesn't have `scandir`.
# Problem is that PyCharm picks up Micropython's `os.pyi` in preference to CPython version because both
# script, `micropython-typesheds`, and `os.pyi` in same directory (top directory).
# noinspection PyUnresolvedReferences
from os import scandir
from pathlib import Path
from shutil import copy2
from sys import argv
from typing import Final


def main():
    last_arg_as_path: Final = Path(argv[-1])
    destination_dir: Final = last_arg_as_path if last_arg_as_path.is_dir() else Path.cwd()  # Default to cwd.
    source_dir: Final = "https://github.com/hlovatt/PyBoardTypeshed"
    source_files: Final = (
        f.path for f in scandir(source_dir) if f.is_file() and f.name.endswith(".pyi")
    )
    for source_file in source_files:
        print(source_file)
        # copy2(source_file, destination_dir)


if __name__ == "__main__":
    main()
