"""
WiPy specific features.

Descriptions taken from:
https://raw.githubusercontent.com/micropython/micropython/master/docs/library/wipy.rst.
*************************************

.. module:: wipy
   :synopsis: WiPy specific features

The ``wipy`` module contains functions to control specific features of the
WiPy, such as the heartbeat LED.
"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "7.5.3"  # Version set by https://github.com/hlovatt/tag2ver

from typing import overload
@overload
def heartbeat(enable: bool, /) -> None:
    """
   Get or set the state (enabled or disabled) of the heartbeat LED. Accepts and
   returns boolean values (``True`` or ``False``).
   """

@overload
def heartbeat() -> bool:
    """
   Get or set the state (enabled or disabled) of the heartbeat LED. Accepts and
   returns boolean values (``True`` or ``False``).
   """
