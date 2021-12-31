"""
Not part of the typesheds project, i.e. not in git.

Used for updating latest pyi files into my IntelliJ MicroPython fork (always there).
"""

__version__ = "7.3.9"  # Version set by https://github.com/hlovatt/tag2ver

from os import listdir
from shutil import copyfile
from typing import Iterable


def copy(files: Iterable[str], *, into: str) -> None:
    to_start = (
        "/Users/lov080/Library/Mobile Documents/com~apple~CloudDocs/Python/intellij-micropython/typehints/"
        + into
        + "/"
    )
    for file in files:
        to = to_start + file
        copyfile(file, to)


def copy_remaining_into_stdlib(*excluding: str):
    remaining = filter(lambda n: n not in excluding and n.endswith(".pyi"), listdir())
    copy(remaining, into="stdlib")


def copy_all_pyi_files_into_plugin():
    esp8266 = ["esp.pyi", "esp32.pyi"]
    copy(esp8266, into="esp8266")
    pyboard = ["lcd160cr.pyi", "pyb.pyi", "stm.pyi"]
    copy(pyboard, into="pyboard")
    micropython = [
        "bluetooth.pyi",
        "btree.pyi",
        "cryptolib.pyi",
        "framebuf.pyi",
        "machine.pyi",
        "micropython.pyi",
        "neopixel.pyi",
        "network.pyi",
        "ubluetooth.pyi",
        "ucryptolib.pyi",
        "uctypes.pyi",
    ]
    copy(micropython, into="micropython")
    copy_remaining_into_stdlib(*esp8266, *pyboard, *micropython)


def main():
    copy_all_pyi_files_into_plugin()


if __name__ == "__main__":
    main()
