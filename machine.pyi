"""

functions related to the hardware

Descriptions taken from 
`https://raw.githubusercontent.com/micropython/micropython/master/docs/library/machine.rst`, etc.

====================================================

.. module:: machine
   :synopsis: functions related to the hardware

   

   The ``machine`` module contains specific functions related to the hardware
   on a particular board. Most functions in this module allow to achieve direct
   and unrestricted access to and control of hardware blocks on a system
   (like CPU, timers, buses, etc.). Used incorrectly, this can lead to
   malfunction, lockups, crashes of your board, and in extreme cases, hardware
   damage.
   
   .. _machine_callbacks:
   
   A note of callbacks used by functions and class methods of :mod:`machine` module:
   all these callbacks should be considered as executing in an interrupt context.
   This is true for both physical devices with IDs >= 0 and "virtual" devices
   with negative IDs like -1 (these "virtual" devices are still thin shims on
   top of real hardware and real hardware interrupts). See :ref:`isr_rules`.
   
"""



__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "3.6.1"  # Version set by https://github.com/hlovatt/tag2ver



from abc import abstractmethod
from typing import overload, Union, Tuple, TypeVar, Optional, NoReturn, List, Callable
from typing import Type, Sequence, runtime_checkable, Protocol, ClassVar

import pyb
from uarray import array



@runtime_checkable
class _AbstractBlockDev(Protocol):
    """
    A `Protocol` (structurally typed) with the defs needed by 
    `usb_mode` argument `msc`.
    """

    __slots__ = ()

    @abstractmethod
    def readblocks(self, blocknum: int, buf: bytes, offset: int = 0, /) -> None: ... 

    @abstractmethod
    def writeblocks(self, blocknum: int, buf: bytes, offset: int = 0, /) -> None: ...

    @abstractmethod
    def ioctl(self, op: int, arg: int) -> Optional[int]: ...




_AnyWritableBuf = TypeVar('_AnyWritableBuf', bytearray, array, memoryview)
"""
Type that allows bytearray, array, or memoryview, but only one of these and not a mixture in a single declaration.
"""




_AnyReadableBuf = TypeVar('_AnyReadableBuf', bytearray, array, memoryview, bytes)
"""
Type that allows bytearray, array, memoryview, or bytes, 
but only one of these and not a mixture in a single declaration.
"""



def reset() -> NoReturn:
   """
   Resets the device in a manner similar to pushing the external RESET
   button.
   """

def soft_reset() -> NoReturn:
   """
   Performs a soft reset of the interpreter, deleting all Python objects and
   resetting the Python heap.  It tries to retain the method by which the user
   is connected to the MicroPython REPL (eg serial, USB, Wifi).
   """

def reset_cause() -> int:
   """
   Get the reset cause. See :ref:`constants <machine_constants>` for the possible return values.
   """

def disable_irq() -> bool:
   """
   Disable interrupt requests.
   Returns the previous IRQ state which should be considered an opaque value.
   This return value should be passed to the `enable_irq()` function to restore
   interrupts to their original state, before `disable_irq()` was called.
   """

def enable_irq(state: bool = True, /) -> None:
   """
   Re-enable interrupt requests.
   The *state* parameter should be the value that was returned from the most
   recent call to the `disable_irq()` function.
   """

def freq() -> int:
   """
    Returns CPU frequency in hertz.
   """

def idle() -> None:
   """
   Gates the clock to the CPU, useful to reduce power consumption at any time during
   short or long periods. Peripherals continue working and execution resumes as soon
   as any interrupt is triggered (on many ports this includes system timer
   interrupt occurring at regular intervals on the order of millisecond).
   """

def sleep() -> None:
   """
   .. note:: This function is deprecated, use `lightsleep()` instead with no arguments.
   """

@overload
def lightsleep() -> None:
   """
   Stops execution in an attempt to enter a low power state.
   
   If *time_ms* is specified then this will be the maximum time in milliseconds that
   the sleep will last for.  Otherwise the sleep can last indefinitely.
   
   With or without a timeout, execution may resume at any time if there are events
   that require processing.  Such events, or wake sources, should be configured before
   sleeping, like `Pin` change or `RTC` timeout.
   
   The precise behaviour and power-saving capabilities of lightsleep and deepsleep is
   highly dependent on the underlying hardware, but the general properties are:
   
   * A lightsleep has full RAM and state retention.  Upon wake execution is resumed
     from the point where the sleep was requested, with all subsystems operational.
   
   * A deepsleep may not retain RAM or any other state of the system (for example
     peripherals or network interfaces).  Upon wake execution is resumed from the main
     script, similar to a hard or power-on reset. The `reset_cause()` function will
     return `machine.DEEPSLEEP` and this can be used to distinguish a deepsleep wake
     from other resets.
   """

@overload
def lightsleep(time_ms: int, /) -> None:
   """
   Stops execution in an attempt to enter a low power state.
   
   If *time_ms* is specified then this will be the maximum time in milliseconds that
   the sleep will last for.  Otherwise the sleep can last indefinitely.
   
   With or without a timeout, execution may resume at any time if there are events
   that require processing.  Such events, or wake sources, should be configured before
   sleeping, like `Pin` change or `RTC` timeout.
   
   The precise behaviour and power-saving capabilities of lightsleep and deepsleep is
   highly dependent on the underlying hardware, but the general properties are:
   
   * A lightsleep has full RAM and state retention.  Upon wake execution is resumed
     from the point where the sleep was requested, with all subsystems operational.
   
   * A deepsleep may not retain RAM or any other state of the system (for example
     peripherals or network interfaces).  Upon wake execution is resumed from the main
     script, similar to a hard or power-on reset. The `reset_cause()` function will
     return `machine.DEEPSLEEP` and this can be used to distinguish a deepsleep wake
     from other resets.
   """

@overload
def deepsleep() -> NoReturn:
   """
   Stops execution in an attempt to enter a low power state.
   
   If *time_ms* is specified then this will be the maximum time in milliseconds that
   the sleep will last for.  Otherwise the sleep can last indefinitely.
   
   With or without a timeout, execution may resume at any time if there are events
   that require processing.  Such events, or wake sources, should be configured before
   sleeping, like `Pin` change or `RTC` timeout.
   
   The precise behaviour and power-saving capabilities of lightsleep and deepsleep is
   highly dependent on the underlying hardware, but the general properties are:
   
   * A lightsleep has full RAM and state retention.  Upon wake execution is resumed
     from the point where the sleep was requested, with all subsystems operational.
   
   * A deepsleep may not retain RAM or any other state of the system (for example
     peripherals or network interfaces).  Upon wake execution is resumed from the main
     script, similar to a hard or power-on reset. The `reset_cause()` function will
     return `machine.DEEPSLEEP` and this can be used to distinguish a deepsleep wake
     from other resets.
   """

@overload
def deepsleep(time_ms: int, /) -> NoReturn:
   """
   Stops execution in an attempt to enter a low power state.
   
   If *time_ms* is specified then this will be the maximum time in milliseconds that
   the sleep will last for.  Otherwise the sleep can last indefinitely.
   
   With or without a timeout, execution may resume at any time if there are events
   that require processing.  Such events, or wake sources, should be configured before
   sleeping, like `Pin` change or `RTC` timeout.
   
   The precise behaviour and power-saving capabilities of lightsleep and deepsleep is
   highly dependent on the underlying hardware, but the general properties are:
   
   * A lightsleep has full RAM and state retention.  Upon wake execution is resumed
     from the point where the sleep was requested, with all subsystems operational.
   
   * A deepsleep may not retain RAM or any other state of the system (for example
     peripherals or network interfaces).  Upon wake execution is resumed from the main
     script, similar to a hard or power-on reset. The `reset_cause()` function will
     return `machine.DEEPSLEEP` and this can be used to distinguish a deepsleep wake
     from other resets.
   """

def wake_reason() -> int:
   """
   Get the wake reason. See :ref:`constants <machine_constants>` for the possible return values.
   
   Availability: ESP32, WiPy.
   """

def unique_id() -> bytes:
   """
   Returns a byte string with a unique identifier of a board/SoC. It will vary
   from a board/SoC instance to another, if underlying hardware allows. Length
   varies by hardware (so use substring of a full value if you expect a short
   ID). In some MicroPython ports, ID corresponds to the network MAC address.
   """

def time_pulse_us(pin: Pin, pulse_level: int, timeout_us: int = 1_000_000, /) -> int:
   """
   Time a pulse on the given *pin*, and return the duration of the pulse in
   microseconds.  The *pulse_level* argument should be 0 to time a low pulse
   or 1 to time a high pulse.
   
   If the current input value of the pin is different to *pulse_level*,
   the function first (*) waits until the pin input becomes equal to *pulse_level*,
   then (**) times the duration that the pin is equal to *pulse_level*.
   If the pin is already equal to *pulse_level* then timing starts straight away.
   
   The function will return -2 if there was timeout waiting for condition marked
   (*) above, and -1 if there was timeout during the main measurement, marked (**)
   above. The timeout is the same for both cases and given by *timeout_us* (which
   is in microseconds).
   """

def rng() -> int:
   """
   Return a 24-bit software generated random number.
   
   Availability: WiPy.
   """


IDLE: int = ...
"""
    IRQ wake values.
"""


SLEEP: int = ...
"""
    IRQ wake values.
"""


DEEPSLEEP: int = ...
"""
    IRQ wake values.
"""




PWRON_RESET: int = ...
"""
    Reset causes.
"""


HARD_RESET: int = ...
"""
    Reset causes.
"""


WDT_RESET: int = ...
"""
    Reset causes.
"""


DEEPSLEEP_RESET: int = ...
"""
    Reset causes.
"""


SOFT_RESET: int = ...
"""
    Reset causes.
"""




WLAN_WAKE: int = ...
"""
    Wake-up reasons.
"""


PIN_WAKE: int = ...
"""
    Wake-up reasons.
"""


RTC_WAKE: int = ...
"""
    Wake-up reasons.
"""



Pin: Type[pyb.Pin] = pyb.Pin

UART: Type[pyb.UART] = pyb.UART

RTC: Type[pyb.RTC] = pyb.RTC


class Signal:
   """
   The Signal class is a simple extension of the `Pin` class. Unlike Pin, which
   can be only in "absolute" 0 and 1 states, a Signal can be in "asserted"
   (on) or "deasserted" (off) states, while being inverted (active-low) or
   not. In other words, it adds logical inversion support to Pin functionality.
   While this may seem a simple addition, it is exactly what is needed to
   support wide array of simple digital devices in a way portable across
   different boards, which is one of the major MicroPython goals. Regardless
   of whether different users have an active-high or active-low LED, a normally
   open or normally closed relay - you can develop a single, nicely looking
   application which works with each of them, and capture hardware
   configuration differences in few lines in the config file of your app.
   
   Example::
   
       from machine import Pin, Signal
   
       # Suppose you have an active-high LED on pin 0
       led1_pin = Pin(0, Pin.OUT)
       # ... and active-low LED on pin 1
       led2_pin = Pin(1, Pin.OUT)
   
       # Now to light up both of them using Pin class, you'll need to set
       # them to different values
       led1_pin.value(1)
       led2_pin.value(0)
   
       # Signal class allows to abstract away active-high/active-low
       # difference
       led1 = Signal(led1_pin, invert=False)
       led2 = Signal(led2_pin, invert=True)
   
       # Now lighting up them looks the same
       led1.value(1)
       led2.value(1)
   
       # Even better:
       led1.on()
       led2.on()
   
   Following is the guide when Signal vs Pin should be used:
   
   * Use Signal: If you want to control a simple on/off (including software
     PWM!) devices like LEDs, multi-segment indicators, relays, buzzers, or
     read simple binary sensors, like normally open or normally closed buttons,
     pulled high or low, Reed switches, moisture/flame detectors, etc. etc.
     Summing up, if you have a real physical device/sensor requiring GPIO
     access, you likely should use a Signal.
   
   * Use Pin: If you implement a higher-level protocol or bus to communicate
     with more complex devices.
   
   The split between Pin and Signal come from the use cases above and the
   architecture of MicroPython: Pin offers the lowest overhead, which may
   be important when bit-banging protocols. But Signal adds additional
   flexibility on top of Pin, at the cost of minor overhead (much smaller
   than if you implemented active-high vs active-low device differences in
   Python manually!). Also, Pin is a low-level object which needs to be
   implemented for each support board, while Signal is a high-level object
   which comes for free once Pin is implemented.
   
   If in doubt, give the Signal a try! Once again, it is offered to save
   developers from the need to handle unexciting differences like active-low
   vs active-high signals, and allow other users to share and enjoy your
   application, instead of being frustrated by the fact that it doesn't
   work for them simply because their LEDs or relays are wired in a slightly
   different way.
   """



   
   @overload
   def __init__(self, pin_obj: Pin, invert: bool = False, /):
      """
      Create a Signal object. There're two ways to create it:
      
      * By wrapping existing Pin object - universal method which works for
        any board.
      * By passing required Pin parameters directly to Signal constructor,
        skipping the need to create intermediate Pin object. Available on
        many, but not all boards.
      
      The arguments are:
      
        - ``pin_obj`` is existing Pin object.
      
        - ``pin_arguments`` are the same arguments as can be passed to Pin constructor.
      
        - ``invert`` - if True, the signal will be inverted (active low).
      """

   
   @overload
   def __init__(
      self, 
      id: Union[Pin, str], 
      /, 
      mode: int = Pin.IN, 
      pull: int = Pin.PULL_NONE, 
      af: Union[str, int] = -1, 
      *, 
      invert: bool = False
   ):
      """
      Create a Signal object. There're two ways to create it:
      
      * By wrapping existing Pin object - universal method which works for
        any board.
      * By passing required Pin parameters directly to Signal constructor,
        skipping the need to create intermediate Pin object. Available on
        many, but not all boards.
      
      The arguments are:
      
        - ``pin_obj`` is existing Pin object.
      
        - ``pin_arguments`` are the same arguments as can be passed to Pin constructor.
      
        - ``invert`` - if True, the signal will be inverted (active low).
      """

   @overload
   def value(self) -> int:
      """
      This method allows to set and get the value of the signal, depending on whether
      the argument ``x`` is supplied or not.
      
      If the argument is omitted then this method gets the signal level, 1 meaning
      signal is asserted (active) and 0 - signal inactive.
      
      If the argument is supplied then this method sets the signal level. The
      argument ``x`` can be anything that converts to a boolean. If it converts
      to ``True``, the signal is active, otherwise it is inactive.
      
      Correspondence between signal being active and actual logic level on the
      underlying pin depends on whether signal is inverted (active-low) or not.
      For non-inverted signal, active status corresponds to logical 1, inactive -
      to logical 0. For inverted/active-low signal, active status corresponds
      to logical 0, while inactive - to logical 1.
      """

   @overload
   def value(self, x: int) -> None:
      """
      This method allows to set and get the value of the signal, depending on whether
      the argument ``x`` is supplied or not.
      
      If the argument is omitted then this method gets the signal level, 1 meaning
      signal is asserted (active) and 0 - signal inactive.
      
      If the argument is supplied then this method sets the signal level. The
      argument ``x`` can be anything that converts to a boolean. If it converts
      to ``True``, the signal is active, otherwise it is inactive.
      
      Correspondence between signal being active and actual logic level on the
      underlying pin depends on whether signal is inverted (active-low) or not.
      For non-inverted signal, active status corresponds to logical 1, inactive -
      to logical 0. For inverted/active-low signal, active status corresponds
      to logical 0, while inactive - to logical 1.
      """

   def on(self) -> None:
      """
      Activate signal.
      """

   def off(self) -> None:
      """
      Deactivate signal.
      """


class ADC:
   """
   The ADC class provides an interface to analog-to-digital convertors, and
   represents a single endpoint that can sample a continuous voltage and
   convert it to a discretised value.
   
   Example usage::
   
      import machine
   
      adc = machine.ADC(pin)   # create an ADC object acting on a pin
      val = adc.read_u16()     # read a raw analog value in the range 0-65535
   """



   def __init__(self, pin: Union[int, Pin], /):
      """
      Access the ADC associated with a source identified by *id*.  This
      *id* may be an integer (usually specifying a channel number), a
      :ref:`Pin <machine.Pin>` object, or other value supported by the
      underlying machine.
      """

   def read_u16(self) -> int:
      """
      Take an analog reading and return an integer in the range 0-65535.
      The return value represents the raw reading taken by the ADC, scaled
      such that the minimum value is 0 and the maximum value is 65535.
      """


class SPI:
   """
   SPI is a synchronous serial protocol that is driven by a master. At the
   physical level, a bus consists of 3 lines: SCK, MOSI, MISO. Multiple devices
   can share the same bus. Each device should have a separate, 4th signal,
   SS (Slave Select), to select a particular device on a bus with which
   communication takes place. Management of an SS signal should happen in
   user code (via machine.Pin class).
   
   Both hardware and software SPI implementations exist via the
   :ref:`machine.SPI <machine.SPI>` and `machine.SoftSPI` classes.  Hardware SPI uses underlying
   hardware support of the system to perform the reads/writes and is usually
   efficient and fast but may have restrictions on which pins can be used.
   Software SPI is implemented by bit-banging and can be used on any pin but
   is not as efficient.  These classes have the same methods available and
   differ primarily in the way they are constructed.
   """



   MASTER: ClassVar[int] = ...
   """
   for initialising the SPI bus to master; this is only used for the WiPy
   """




   MSB: ClassVar[int] = ...
   """
   set the first bit to be the most significant bit
   """




   LSB: ClassVar[int] = ...
   """
   set the first bit to be the least significant bit
   """




   @overload
   def __init__(self, id: int, /):
      """
      Construct an SPI object on the given bus, *id*. Values of *id* depend
      on a particular port and its hardware. Values 0, 1, etc. are commonly used
      to select hardware SPI block #0, #1, etc.
      
      With no additional parameters, the SPI object is created but not
      initialised (it has the settings from the last initialisation of
      the bus, if any).  If extra arguments are given, the bus is initialised.
      See ``init`` for parameters of initialisation.
      """

   @overload
   def __init__(
      self, 
      id: int, 
      /, 
      baudrate: int = 1_000_000, 
      *,
      polarity: int = 0, 
      phase: int = 0, 
      bits: int = 8, 
      firstbit: int = MSB, 
      sck: Optional[Pin] = None, 
      mosi: Optional[Pin] = None, 
      miso: Optional[Pin] = None, 
   ):
      """
      Construct an SPI object on the given bus, *id*. Values of *id* depend
      on a particular port and its hardware. Values 0, 1, etc. are commonly used
      to select hardware SPI block #0, #1, etc.
      
      With no additional parameters, the SPI object is created but not
      initialised (it has the settings from the last initialisation of
      the bus, if any).  If extra arguments are given, the bus is initialised.
      See ``init`` for parameters of initialisation.
      """

   @overload
   def __init__(
      self, 
      id: int, 
      /, 
      baudrate: int = 1_000_000, 
      *,
      polarity: int = 0, 
      phase: int = 0, 
      bits: int = 8, 
      firstbit: int = MSB, 
      pins: Optional[Tuple[Pin, Pin, Pin]] = None, 
   ):
      """
      Construct an SPI object on the given bus, *id*. Values of *id* depend
      on a particular port and its hardware. Values 0, 1, etc. are commonly used
      to select hardware SPI block #0, #1, etc.
      
      With no additional parameters, the SPI object is created but not
      initialised (it has the settings from the last initialisation of
      the bus, if any).  If extra arguments are given, the bus is initialised.
      See ``init`` for parameters of initialisation.
      """

   @overload
   def init(
      self, 
      baudrate: int = 1_000_000, 
      *,
      polarity: int = 0, 
      phase: int = 0, 
      bits: int = 8, 
      firstbit: int = MSB, 
      sck: Optional[Pin] = None, 
      mosi: Optional[Pin] = None, 
      miso: Optional[Pin] = None, 
   ) -> None:
      """
      Initialise the SPI bus with the given parameters:
      
        - ``baudrate`` is the SCK clock rate.
        - ``polarity`` can be 0 or 1, and is the level the idle clock line sits at.
        - ``phase`` can be 0 or 1 to sample data on the first or second clock edge
          respectively.
        - ``bits`` is the width in bits of each transfer. Only 8 is guaranteed to be supported by all hardware.
        - ``firstbit`` can be ``SPI.MSB`` or ``SPI.LSB``.
        - ``sck``, ``mosi``, ``miso`` are pins (machine.Pin) objects to use for bus signals. For most
          hardware SPI blocks (as selected by ``id`` parameter to the constructor), pins are fixed
          and cannot be changed. In some cases, hardware blocks allow 2-3 alternative pin sets for
          a hardware SPI block. Arbitrary pin assignments are possible only for a bitbanging SPI driver
          (``id`` = -1).
        - ``pins`` - WiPy port doesn't ``sck``, ``mosi``, ``miso`` arguments, and instead allows to
          specify them as a tuple of ``pins`` parameter.
      
      In the case of hardware SPI the actual clock frequency may be lower than the
      requested baudrate. This is dependant on the platform hardware. The actual
      rate may be determined by printing the SPI object.
      """

   @overload
   def init(
      self, 
      baudrate: int = 1_000_000, 
      *,
      polarity: int = 0, 
      phase: int = 0, 
      bits: int = 8, 
      firstbit: int = MSB, 
      pins: Optional[Tuple[Pin, Pin, Pin]] = None, 
   ) -> None:
      """
      Initialise the SPI bus with the given parameters:
      
        - ``baudrate`` is the SCK clock rate.
        - ``polarity`` can be 0 or 1, and is the level the idle clock line sits at.
        - ``phase`` can be 0 or 1 to sample data on the first or second clock edge
          respectively.
        - ``bits`` is the width in bits of each transfer. Only 8 is guaranteed to be supported by all hardware.
        - ``firstbit`` can be ``SPI.MSB`` or ``SPI.LSB``.
        - ``sck``, ``mosi``, ``miso`` are pins (machine.Pin) objects to use for bus signals. For most
          hardware SPI blocks (as selected by ``id`` parameter to the constructor), pins are fixed
          and cannot be changed. In some cases, hardware blocks allow 2-3 alternative pin sets for
          a hardware SPI block. Arbitrary pin assignments are possible only for a bitbanging SPI driver
          (``id`` = -1).
        - ``pins`` - WiPy port doesn't ``sck``, ``mosi``, ``miso`` arguments, and instead allows to
          specify them as a tuple of ``pins`` parameter.
      
      In the case of hardware SPI the actual clock frequency may be lower than the
      requested baudrate. This is dependant on the platform hardware. The actual
      rate may be determined by printing the SPI object.
      """

   def deinit(self) -> None:
      """
      Turn off the SPI bus.
      """

   def read(self, nbytes: int, write: int = 0x00, /) -> bytes:
      """
       Read a number of bytes specified by ``nbytes`` while continuously writing
       the single byte given by ``write``.
       Returns a ``bytes`` object with the data that was read.
      """

   def readinto(self, buf: _AnyWritableBuf, write: int = 0x00, /) -> Optional[int]:
      """
       Read into the buffer specified by ``buf`` while continuously writing the
       single byte given by ``write``.
       Returns ``None``.
       
       Note: on WiPy this function returns the number of bytes read.
      """

   def write(self, buf: _AnyReadableBuf, /) -> Optional[int]:
      """
       Write the bytes contained in ``buf``.
       Returns ``None``.
       
       Note: on WiPy this function returns the number of bytes written.
      """

   def write_readinto(self, write_buf: _AnyReadableBuf, read_buf: _AnyWritableBuf, /) -> Optional[int]:
      """
       Write the bytes from ``write_buf`` while reading into ``read_buf``.  The
       buffers can be the same or different, but both buffers must have the
       same length.
       Returns ``None``.
       
       Note: on WiPy this function returns the number of bytes written.
      """


# noinspection PyShadowingNames
class I2C:
   """
   I2C is a two-wire protocol for communicating between devices.  At the physical
   level it consists of 2 wires: SCL and SDA, the clock and data lines respectively.
   
   I2C objects are created attached to a specific bus.  They can be initialised
   when created, or initialised later on.
   
   Printing the I2C object gives you information about its configuration.
   
   Both hardware and software I2C implementations exist via the
   :ref:`machine.I2C <machine.I2C>` and `machine.SoftI2C` classes.  Hardware I2C uses
   underlying hardware support of the system to perform the reads/writes and is
   usually efficient and fast but may have restrictions on which pins can be used.
   Software I2C is implemented by bit-banging and can be used on any pin but is not
   as efficient.  These classes have the same methods available and differ primarily
   in the way they are constructed.
   
   Example usage::
   
       from machine import I2C
   
       i2c = I2C(freq=400000)          # create I2C peripheral at frequency of 400kHz
                                       # depending on the port, extra parameters may be required
                                       # to select the peripheral and/or pins to use
   
       i2c.scan()                      # scan for slaves, returning a list of 7-bit addresses
   
       i2c.writeto(42, b'123')         # write 3 bytes to slave with 7-bit address 42
       i2c.readfrom(42, 4)             # read 4 bytes from slave with 7-bit address 42
   
       i2c.readfrom_mem(42, 8, 3)      # read 3 bytes from memory of slave 42,
                                       #   starting at memory-address 8 in the slave
       i2c.writeto_mem(42, 2, b'\x10') # write 1 byte to memory of slave 42
                                       #   starting at address 2 in the slave
   """



   @overload
   def __init__(self, id: int, /, *, freq: int = 400_000):
      """
      Construct and return a new I2C object using the following parameters:
      
         - *id* identifies a particular I2C peripheral.  Allowed values for
           depend on the particular port/board
         - *scl* should be a pin object specifying the pin to use for SCL.
         - *sda* should be a pin object specifying the pin to use for SDA.
         - *freq* should be an integer which sets the maximum frequency
           for SCL.
      
      Note that some ports/boards will have default values of *scl* and *sda*
      that can be changed in this constructor.  Others will have fixed values
      of *scl* and *sda* that cannot be changed.
      """

   @overload
   def __init__(self, id: int, /, *, scl: Pin, sda: Pin, freq: int = 400_000):
      """
      Construct and return a new I2C object using the following parameters:
      
         - *id* identifies a particular I2C peripheral.  Allowed values for
           depend on the particular port/board
         - *scl* should be a pin object specifying the pin to use for SCL.
         - *sda* should be a pin object specifying the pin to use for SDA.
         - *freq* should be an integer which sets the maximum frequency
           for SCL.
      
      Note that some ports/boards will have default values of *scl* and *sda*
      that can be changed in this constructor.  Others will have fixed values
      of *scl* and *sda* that cannot be changed.
      """

   @overload
   def init(self, *, freq: int = 400_000) -> None:
      """
     Initialise the I2C bus with the given arguments:
     
        - *scl* is a pin object for the SCL line
        - *sda* is a pin object for the SDA line
        - *freq* is the SCL clock rate
      """

   @overload
   def init(self, *, scl: Pin, sda: Pin, freq: int = 400_000) -> None:
      """
     Initialise the I2C bus with the given arguments:
     
        - *scl* is a pin object for the SCL line
        - *sda* is a pin object for the SDA line
        - *freq* is the SCL clock rate
      """

   def deinit(self) -> None:
      """
      Turn off the I2C bus.
      
      Availability: WiPy.
      """

   def scan(self) -> List[int]:
      """
      Scan all I2C addresses between 0x08 and 0x77 inclusive and return a list of
      those that respond.  A device responds if it pulls the SDA line low after
      its address (including a write bit) is sent on the bus.
      """

   def start(self) -> None:
      """
      Generate a START condition on the bus (SDA transitions to low while SCL is high).
      
      
      Primitive I2C operations
      ------------------------
      
      The following methods implement the primitive I2C master bus operations and can
      be combined to make any I2C transaction.  They are provided if you need more
      control over the bus, otherwise the standard methods (see below) can be used.
      
      These methods are only available on the `machine.SoftI2C` class.
      """

   def stop(self) -> None:
      """
      Generate a STOP condition on the bus (SDA transitions to high while SCL is high).
      
      
      Primitive I2C operations
      ------------------------
      
      The following methods implement the primitive I2C master bus operations and can
      be combined to make any I2C transaction.  They are provided if you need more
      control over the bus, otherwise the standard methods (see below) can be used.
      
      These methods are only available on the `machine.SoftI2C` class.
      """

   def readinto(self, buf: _AnyWritableBuf, nack: bool = True, /) -> None:
      """
      Reads bytes from the bus and stores them into *buf*.  The number of bytes
      read is the length of *buf*.  An ACK will be sent on the bus after
      receiving all but the last byte.  After the last byte is received, if *nack*
      is true then a NACK will be sent, otherwise an ACK will be sent (and in this
      case the slave assumes more bytes are going to be read in a later call).
      
      
      Primitive I2C operations
      ------------------------
      
      The following methods implement the primitive I2C master bus operations and can
      be combined to make any I2C transaction.  They are provided if you need more
      control over the bus, otherwise the standard methods (see below) can be used.
      
      These methods are only available on the `machine.SoftI2C` class.
      """

   def write(self, buf: _AnyReadableBuf, /) -> int:
      """
      Write the bytes from *buf* to the bus.  Checks that an ACK is received
      after each byte and stops transmitting the remaining bytes if a NACK is
      received.  The function returns the number of ACKs that were received.
      
      
      Primitive I2C operations
      ------------------------
      
      The following methods implement the primitive I2C master bus operations and can
      be combined to make any I2C transaction.  They are provided if you need more
      control over the bus, otherwise the standard methods (see below) can be used.
      
      These methods are only available on the `machine.SoftI2C` class.
      """

   def readfrom(self, addr: int, nbytes: int, stop: bool = True, /) -> bytes:
      """
      Read *nbytes* from the slave specified by *addr*.
      If *stop* is true then a STOP condition is generated at the end of the transfer.
      Returns a `bytes` object with the data read.
      
      
      Standard bus operations
      -----------------------
      
      The following methods implement the standard I2C master read and write
      operations that target a given slave device.
      """

   def readfrom_into(self, addr: int, buf: _AnyWritableBuf, stop: bool = True, /) -> None:
      """
      Read into *buf* from the slave specified by *addr*.
      The number of bytes read will be the length of *buf*.
      If *stop* is true then a STOP condition is generated at the end of the transfer.
      
      The method returns ``None``.
      
      
      Standard bus operations
      -----------------------
      
      The following methods implement the standard I2C master read and write
      operations that target a given slave device.
      """

   def writeto(self, addr: int, buf: _AnyWritableBuf, stop: bool = True, /) -> int:
      """
      Write the bytes from *buf* to the slave specified by *addr*.  If a
      NACK is received following the write of a byte from *buf* then the
      remaining bytes are not sent.  If *stop* is true then a STOP condition is
      generated at the end of the transfer, even if a NACK is received.
      The function returns the number of ACKs that were received.
      
      
      Standard bus operations
      -----------------------
      
      The following methods implement the standard I2C master read and write
      operations that target a given slave device.
      """

   
   def writevto(
      self, 
      addr: int, 
      vector: Sequence[_AnyReadableBuf], 
      stop: bool = True, 
      /
   ) -> int:
      """
      Write the bytes contained in *vector* to the slave specified by *addr*.
      *vector* should be a tuple or list of objects with the buffer protocol.
      The *addr* is sent once and then the bytes from each object in *vector*
      are written out sequentially.  The objects in *vector* may be zero bytes
      in length in which case they don't contribute to the output.
      
      If a NACK is received following the write of a byte from one of the
      objects in *vector* then the remaining bytes, and any remaining objects,
      are not sent.  If *stop* is true then a STOP condition is generated at
      the end of the transfer, even if a NACK is received.  The function
      returns the number of ACKs that were received.
      
      
      Standard bus operations
      -----------------------
      
      The following methods implement the standard I2C master read and write
      operations that target a given slave device.
      """

   def readfrom_mem(self, addr: int, memaddr: int, nbytes: int, /, *, addrsize: int = 8) -> bytes:
      """
      Read *nbytes* from the slave specified by *addr* starting from the memory
      address specified by *memaddr*.
      The argument *addrsize* specifies the address size in bits.
      Returns a `bytes` object with the data read.
      
      
      Memory operations
      -----------------
      
      Some I2C devices act as a memory device (or set of registers) that can be read
      from and written to.  In this case there are two addresses associated with an
      I2C transaction: the slave address and the memory address.  The following
      methods are convenience functions to communicate with such devices.
      """

   
   def readfrom_mem_into(
      self, 
      addr: int, 
      memaddr: int, 
      buf: _AnyWritableBuf, 
      /, 
      *, 
      addrsize: int = 8
   ) -> None:
      """
      Read into *buf* from the slave specified by *addr* starting from the
      memory address specified by *memaddr*.  The number of bytes read is the
      length of *buf*.
      The argument *addrsize* specifies the address size in bits (on ESP8266
      this argument is not recognised and the address size is always 8 bits).
      
      The method returns ``None``.
      
      
      Memory operations
      -----------------
      
      Some I2C devices act as a memory device (or set of registers) that can be read
      from and written to.  In this case there are two addresses associated with an
      I2C transaction: the slave address and the memory address.  The following
      methods are convenience functions to communicate with such devices.
      """

   def writeto_mem(self, addr: int, memaddr: int, buf: _AnyReadableBuf, /, *, addrsize: int = 8) -> None:
      """
      Write *buf* to the slave specified by *addr* starting from the
      memory address specified by *memaddr*.
      The argument *addrsize* specifies the address size in bits (on ESP8266
      this argument is not recognised and the address size is always 8 bits).
      
      The method returns ``None``.
      
      Memory operations
      -----------------
      
      Some I2C devices act as a memory device (or set of registers) that can be read
      from and written to.  In this case there are two addresses associated with an
      I2C transaction: the slave address and the memory address.  The following
      methods are convenience functions to communicate with such devices.
      """


class Timer:
   """
   Hardware timers deal with timing of periods and events. Timers are perhaps
   the most flexible and heterogeneous kind of hardware in MCUs and SoCs,
   differently greatly from a model to a model. MicroPython's Timer class
   defines a baseline operation of executing a callback with a given period
   (or once after some delay), and allow specific boards to define more
   non-standard behavior (which thus won't be portable to other boards).
   
   See discussion of :ref:`important constraints <machine_callbacks>` on
   Timer callbacks.
   
   .. note::
   
       Memory can't be allocated inside irq handlers (an interrupt) and so
       exceptions raised within a handler don't give much information.  See
       :func:`micropython.alloc_emergency_exception_buf` for how to get around this
       limitation.
   
   If you are using a WiPy board please refer to :ref:`machine.TimerWiPy <machine.TimerWiPy>`
   instead of this class.
   """



   ONE_SHOT: ClassVar[int] = ...
   """
   Timer operating mode.
   """


   PERIODIC: ClassVar[int] = ...
   """
   Timer operating mode.
   """




   @overload
   def __init__(
      self, 
      id: int, 
      /
   ):
      """
      Construct a new timer object of the given id. Id of -1 constructs a
      virtual timer (if supported by a board).
      
      See ``init`` for parameters of initialisation.
      """

   @overload
   def __init__(
      self, 
      id: int, 
      /, 
      *, 
      mode: int = PERIODIC, 
      period: int = -1, 
      callback: Optional[Callable[["Timer"], None]] = None, 
   ):
      """
      Construct a new timer object of the given id. Id of -1 constructs a
      virtual timer (if supported by a board).
      
      See ``init`` for parameters of initialisation.
      """

   
   def init(
      self, 
      *, 
      mode: int = PERIODIC, 
      period: int = -1, 
      callback: Optional[Callable[["Timer"], None]] = None, 
   ) -> None:
      """
      Initialise the timer. Example::
      
          tim.init(period=100)                         # periodic with 100ms period
          tim.init(mode=Timer.ONE_SHOT, period=1000)   # one shot firing after 1000ms
      
      Keyword arguments:
      
        - ``mode`` can be one of:
      
          - ``Timer.ONE_SHOT`` - The timer runs once until the configured
            period of the channel expires.
          - ``Timer.PERIODIC`` - The timer runs periodically at the configured
            frequency of the channel.
      """

   def deinit(self) -> None:
      """
      Deinitialises the timer. Stops the timer, and disables the timer peripheral.
      """


class WDT:
   """
   The WDT is used to restart the system when the application crashes and ends
   up into a non recoverable state. Once started it cannot be stopped or
   reconfigured in any way. After enabling, the application must "feed" the
   watchdog periodically to prevent it from expiring and resetting the system.
   
   Example usage::
   
       from machine import WDT
       wdt = WDT(timeout=2000)  # enable it with a timeout of 2s
       wdt.feed()
   
   Availability of this class: pyboard, WiPy, esp8266, esp32.
   """



   def __init__(self, *, id: int = 0, timeout: int = 5000):
      """
      Create a WDT object and start it. The timeout must be given in milliseconds.
      Once it is running the timeout cannot be changed and the WDT cannot be stopped either.
      
      Notes: On the esp32 the minimum timeout is 1 second. On the esp8266 a timeout
      cannot be specified, it is determined by the underlying system.
      """

   def feed(self) -> None:
      """
      Feed the WDT to prevent it from resetting the system. The application
      should place this call in a sensible place ensuring that the WDT is
      only fed after verifying that everything is functioning correctly.
      """


class SD:
   """
   .. warning::
   
      This is a non-standard class and is only available on the cc3200 port.
   
   
   The SD card class allows to configure and enable the memory card
   module of the WiPy and automatically mount it as ``/sd`` as part
   of the file system. There are several pin combinations that can be
   used to wire the SD card socket to the WiPy and the pins used can
   be specified in the constructor. Please check the `pinout and alternate functions
   table. <https://raw.githubusercontent.com/wipy/wipy/master/docs/PinOUT.png>`_ for
   more info regarding the pins which can be remapped to be used with a SD card.
   
   Example usage::
   
       from machine import SD
       import os
       # clk cmd and dat0 pins must be passed along with
       # their respective alternate functions
       sd = machine.SD(pins=('GP10', 'GP11', 'GP15'))
       os.mount(sd, '/sd')
       # do normal file operations
   """



   
   def __init__(
      self, 
      id: int = 0, 
      pins: Union[Tuple[str, str, str], Tuple[Pin, Pin, Pin]] = ("GP10", "GP11", "GP15")
   ):
      """
      Create a SD card object. See ``init()`` for parameters if initialization.
      """

   
   def init(
      self, 
      id: int = 0, 
      pins: Union[Tuple[str, str, str], Tuple[Pin, Pin, Pin]] = ("GP10", "GP11", "GP15")
   ) -> None:
      """
      Enable the SD card. In order to initialize the card, give it a 3-tuple:
      ``(clk_pin, cmd_pin, dat0_pin)``.
      """

   def deinit(self) -> None:
      """
      Disable the SD card.
      """


# noinspection PyShadowingNames
class SDCard(_AbstractBlockDev):
   """
   SD cards are one of the most common small form factor removable storage media.
   SD cards come in a variety of sizes and physical form factors. MMC cards are
   similar removable storage devices while eMMC devices are electrically similar
   storage devices designed to be embedded into other systems. All three form
   share a common protocol for communication with their host system and high-level
   support looks the same for them all. As such in MicroPython they are implemented
   in a single class called :class:`machine.SDCard` .
   
   Both SD and MMC interfaces support being accessed with a variety of bus widths.
   When being accessed with a 1-bit wide interface they can be accessed using the
   SPI protocol. Different MicroPython hardware platforms support different widths
   and pin configurations but for most platforms there is a standard configuration
   for any given hardware. In general constructing an ``SDCard`` object with without
   passing any parameters will initialise the interface to the default card slot
   for the current hardware. The arguments listed below represent the common
   arguments that might need to be set in order to use either a non-standard slot
   or a non-standard pin assignment. The exact subset of arguments supported will
   vary from platform to platform.
   

   Implementation-specific details
   -------------------------------
   
   Different implementations of the ``SDCard`` class on different hardware support
   varying subsets of the options above.
   
   PyBoard
   ```````
   
   The standard PyBoard has just one slot. No arguments are necessary or supported.
   
   ESP32
   `````
   
   The ESP32 provides two channels of SD/MMC hardware and also supports
   access to SD Cards through either of the two SPI ports that are
   generally available to the user. As a result the *slot* argument can
   take a value between 0 and 3, inclusive. Slots 0 and 1 use the
   built-in SD/MMC hardware while slots 2 and 3 use the SPI ports. Slot 0
   supports 1, 4 or 8-bit wide access while slot 1 supports 1 or 4-bit
   access; the SPI slots only support 1-bit access.
   
     .. note:: Slot 0 is used to communicate with on-board flash memory
               on most ESP32 modules and so will be unavailable to the
               user.
   
     .. note:: Most ESP32 modules that provide an SD card slot using the
               dedicated hardware only wire up 1 data pin, so the default
               value for *width* is 1.
   
   The pins used by the dedicated SD/MMC hardware are fixed. The pins
   used by the SPI hardware can be reassigned.
   
     .. note:: If any of the SPI signals are remapped then all of the SPI
               signals will pass through a GPIO multiplexer unit which
               can limit the performance of high frequency signals. Since
               the normal operating speed for SD cards is 40MHz this can
               cause problems on some cards.
   
   The default (and preferred) pin assignment are as follows:
   
       ====== ====== ====== ====== ======
       Slot   0      1      2      3
       ------ ------ ------ ------ ------
       Signal   Pin    Pin    Pin    Pin
       ====== ====== ====== ====== ======
       sck       6     14     18     14
       cmd      11     15
       cs                      5     15
       miso                   19     12
       mosi                   23     13
       D0        7      2
       D1        8      4
       D2        9     12
       D3       10     13
       D4       16
       D5       17
       D6        5
       D7       18
       ====== ====== ====== ====== ======
   
   cc3200
   ``````
   
   You can set the pins used for SPI access by passing a tuple as the
   *pins* argument.
   
   *Note:* The current cc3200 SD card implementation names the this class
   :class:`machine.SD` rather than :class:`machine.SDCard` .
   """



   
   def __init__(
      self, 
      slot: int = 1, 
      width: int = 1, 
      cd: Optional[Union[int, str, Pin]] = None, 
      wp: Optional[Union[int, str, Pin]] = None, 
      sck: Optional[Union[int, str, Pin]] = None, 
      miso: Optional[Union[int, str, Pin]] = None, 
      mosi: Optional[Union[int, str, Pin]] = None, 
      cs: Optional[Union[int, str, Pin]] = None, 
      freq: int = 20000000
   ):
      """
       This class provides access to SD or MMC storage cards using either
       a dedicated SD/MMC interface hardware or through an SPI channel.
       The class implements the block protocol defined by :class:`uos.AbstractBlockDev`.
       This allows the mounting of an SD card to be as simple as::
       
         uos.mount(machine.SDCard(), "/sd")
       
       The constructor takes the following parameters:
       
        - *slot* selects which of the available interfaces to use. Leaving this
          unset will select the default interface.
       
        - *width* selects the bus width for the SD/MMC interface.
       
        - *cd* can be used to specify a card-detect pin.
       
        - *wp* can be used to specify a write-protect pin.
       
        - *sck* can be used to specify an SPI clock pin.
       
        - *miso* can be used to specify an SPI miso pin.
       
        - *mosi* can be used to specify an SPI mosi pin.
       
        - *cs* can be used to specify an SPI chip select pin.
        
        - *freq* selects the SD/MMC interface frequency in Hz (only supported on the ESP32).
      """


   def readblocks(self, blocknum: int, buf: bytes, offset: int = 0, /) -> None: ... 
   
   def writeblocks(self, blocknum: int, buf: bytes, offset: int = 0, /) -> None: ...
   
   def ioctl(self, op: int, arg: int) -> Optional[int]: ...


