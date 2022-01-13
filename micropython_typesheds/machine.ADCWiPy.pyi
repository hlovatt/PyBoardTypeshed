"""
class ADCWiPy -- analog to digital conversion.

Descriptions taken from:
https://raw.githubusercontent.com/micropython/micropython/master/docs/library/machine.ADCWiPy.rst.
=============================================

.. note::

    This class is a non-standard ADC implementation for the WiPy.
    It is available simply as ``machine.ADC`` on the WiPy but is named in the
    documentation below as ``machine.ADCWiPy`` to distinguish it from the
    more general :ref:`machine.ADC <machine.ADC>` class.
"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "7.5.3"  # Version set by https://github.com/hlovatt/tag2ver

from typing import overload

class ADC:
    """
   Usage::
   
      import machine
   
      adc = machine.ADC()             # create an ADC object
      apin = adc.channel(pin='GP3')   # create an analog pin on GP3
      val = apin()                    # read an analog value
   """

    def __init__(self, id: int = 0, /, *, bits: int = 12):
        """
      Create an ADC object associated with the given pin.
      This allows you to then read analog values on that pin.
      For more info check the `pinout and alternate functions
      table. <https://raw.githubusercontent.com/wipy/wipy/master/docs/PinOUT.png>`_
      
      .. warning::
      
         ADC pin input range is 0-1.4V (being 1.8V the absolute maximum that it
         can withstand). When GP2, GP3, GP4 or GP5 are remapped to the
         ADC block, 1.8 V is the maximum. If these pins are used in digital mode,
         then the maximum allowed input is 3.6V.
      """
    @overload
    def channel(self, id: int, /) -> ADCChannel:
        """
      Create an analog pin. If only channel ID is given, the correct pin will
      be selected. Alternatively, only the pin can be passed and the correct
      channel will be selected. Examples::
      
         # all of these are equivalent and enable ADC channel 1 on GP3
         apin = adc.channel(1)
         apin = adc.channel(pin='GP3')
         apin = adc.channel(id=1, pin='GP3')
      """
    @overload
    def channel(self, /, *, pin: str) -> ADCChannel:
        """
      Create an analog pin. If only channel ID is given, the correct pin will
      be selected. Alternatively, only the pin can be passed and the correct
      channel will be selected. Examples::
      
         # all of these are equivalent and enable ADC channel 1 on GP3
         apin = adc.channel(1)
         apin = adc.channel(pin='GP3')
         apin = adc.channel(id=1, pin='GP3')
      """
    @overload
    def channel(self, id: int, /, *, pin: str) -> ADCChannel:
        """
      Create an analog pin. If only channel ID is given, the correct pin will
      be selected. Alternatively, only the pin can be passed and the correct
      channel will be selected. Examples::
      
         # all of these are equivalent and enable ADC channel 1 on GP3
         apin = adc.channel(1)
         apin = adc.channel(pin='GP3')
         apin = adc.channel(id=1, pin='GP3')
      """
    def init(self) -> None:
        """
      Enable the ADC block.
      """
    def deinit(self) -> None:
        """
      Disable the ADC block.
      """

class ADCChannel:
    """
   class ADCChannel --- read analog values from internal or external sources
   =========================================================================
   
   ADC channels can be connected to internal points of the MCU or to GPIO pins.
   ADC channels are created using the ADC.channel method.
   """

    def __call__(self) -> int:
        """
      Fast method to read the channel value.
      """
    def value(self) -> int:
        """
      Read the channel value.
      """
    def init(self) -> None:
        """
      Re-init (and effectively enable) the ADC channel.
      """
    def deinit(self) -> None:
        """
      Disable the ADC channel.
      """
