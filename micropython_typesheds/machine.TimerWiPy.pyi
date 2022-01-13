"""
class TimerWiPy -- control hardware timers.

Descriptions taken from:
https://raw.githubusercontent.com/micropython/micropython/master/docs/library/machine.TimerWiPy.rst.
==========================================

.. note::

    This class is a non-standard Timer implementation for the WiPy.
    It is available simply as ``machine.Timer`` on the WiPy but is named in the
    documentation below as ``machine.TimerWiPy`` to distinguish it from the
    more general :ref:`machine.Timer <machine.Timer>` class.

Hardware timers deal with timing of periods and events. Timers are perhaps
the most flexible and heterogeneous kind of hardware in MCUs and SoCs,
differently greatly from a model to a model. MicroPython's Timer class
defines a baseline operation of executing a callback with a given period
(or once after some delay), and allow specific boards to define more
non-standard behaviour (which thus won't be portable to other boards).

See discussion of :ref:`important constraints <machine_callbacks>` on
Timer callbacks.

.. note::

    Memory can't be allocated inside irq handlers (an interrupt) and so
    exceptions raised within a handler don't give much information.  See
    :func:`micropython.alloc_emergency_exception_buf` for how to get around this
    limitation.
"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "7.5.3"  # Version set by https://github.com/hlovatt/tag2ver

from typing import overload, ClassVar, Callable

class Timer:
    """

   """

    ONE_SHOT: ClassVar[int] = ...
    """
   One-shot timer mode.
   """

    PERIODIC: ClassVar[int] = ...
    """
   Periodic timer mode.
   """

    PWM: ClassVar[int] = ...
    """
   PWM timer mode.
   """

    A: ClassVar[int] = ...
    """
   Selects timer channel A. 
   Must be ORed with B (``Timer.A | Timer.B``) when using a 32-bit timer.
   """

    B: ClassVar[int] = ...
    """
   Selects timer channel B. 
   Must be ORed with A (``Timer.A | Timer.B``) when using a 32-bit timer.
   """

    POSITIVE: ClassVar[int] = ...
    """
   Timer channel positive polarity selection (only relevant in PWM mode).
   """

    NEGATIVE: ClassVar[int] = ...
    """
   Timer channel negative polarity selection (only relevant in PWM mode).
   """

    TIMEOUT: ClassVar[int] = ...
    """
   Timer channel IRQ triggers on timeout (only relevant in PERIODIC or ONE_SHOT modes).
   """

    MATCH: ClassVar[int] = ...
    """
   Timer channel IRQ triggers on match (only relevant in PWM mode).
   """
    def __init__(self, id: int, mode: int, /, *, width: int = 16):
        """
      Construct a new timer object of the given id. Id of -1 constructs a
      virtual timer (if supported by a board).
      """
    def init(self, mode: int, /, *, width: int = 16) -> None:
        """
      Initialise the timer. Example::
      
          tim.init(Timer.PERIODIC)             # periodic 16-bit timer
          tim.init(Timer.ONE_SHOT, width=32)   # one shot 32-bit timer
      
      Keyword arguments:
      
        - ``mode`` can be one of:
      
          - ``TimerWiPy.ONE_SHOT`` - The timer runs once until the configured
            period of the channel expires.
          - ``TimerWiPy.PERIODIC`` - The timer runs periodically at the configured
            frequency of the channel.
          - ``TimerWiPy.PWM``      - Output a PWM signal on a pin.
      
        - ``width`` must be either 16 or 32 (bits). For really low frequencies < 5Hz
          (or large periods), 32-bit timers should be used. 32-bit mode is only available
          for ``ONE_SHOT`` AND ``PERIODIC`` modes.
      """
    def deinit(self) -> None:
        """
      Deinitialises the timer. Stops the timer, and disables the timer peripheral.
      """
    @overload
    def channel(self, channel: int, /) -> TimerChannel | None:
        """
      If only a channel identifier passed, then a previously initialized channel
      object is returned (or ``None`` if there is no previous channel).
      
      Otherwise, a TimerChannel object is initialized and returned.
      
      The operating mode is is the one configured to the Timer object that was used to
      create the channel.
      
      - ``channel`` if the width of the timer is 16-bit, then must be either ``TIMER.A``, ``TIMER.B``.
        If the width is 32-bit then it **must be** ``TIMER.A | TIMER.B``.
      
      Keyword only arguments:
      
        - ``freq`` sets the frequency in Hz.
        - ``period`` sets the period in microseconds.
      
        .. note::
      
           Either ``freq`` or ``period`` must be given, never both.
      
        - ``polarity`` this is applicable for ``PWM``, and defines the polarity of the duty cycle
        - ``duty_cycle`` only applicable to ``PWM``. It's a percentage (0.00-100.00). Since the WiPy
          doesn't support floating point numbers the duty cycle must be specified in the range 0-10000,
          where 10000 would represent 100.00, 5050 represents 50.50, and so on.
      
      .. note::
      
         When the channel is in PWM mode, the corresponding pin is assigned automatically, therefore
         there's no need to assign the alternate function of the pin via the ``Pin`` class. The pins which
         support PWM functionality are the following:
      
         - ``GP24`` on Timer 0 channel A.
         - ``GP25`` on Timer 1 channel A.
         - ``GP9``  on Timer 2 channel B.
         - ``GP10`` on Timer 3 channel A.
         - ``GP11`` on Timer 3 channel B.
      """
    @overload
    def channel(
        self,
        channel: int,
        /,
        *,
        freq: int,
        polarity: int = POSITIVE,
        duty_cycle: int = 0,
    ) -> TimerChannel:
        """
      If only a channel identifier passed, then a previously initialized channel
      object is returned (or ``None`` if there is no previous channel).
      
      Otherwise, a TimerChannel object is initialized and returned.
      
      The operating mode is is the one configured to the Timer object that was used to
      create the channel.
      
      - ``channel`` if the width of the timer is 16-bit, then must be either ``TIMER.A``, ``TIMER.B``.
        If the width is 32-bit then it **must be** ``TIMER.A | TIMER.B``.
      
      Keyword only arguments:
      
        - ``freq`` sets the frequency in Hz.
        - ``period`` sets the period in microseconds.
      
        .. note::
      
           Either ``freq`` or ``period`` must be given, never both.
      
        - ``polarity`` this is applicable for ``PWM``, and defines the polarity of the duty cycle
        - ``duty_cycle`` only applicable to ``PWM``. It's a percentage (0.00-100.00). Since the WiPy
          doesn't support floating point numbers the duty cycle must be specified in the range 0-10000,
          where 10000 would represent 100.00, 5050 represents 50.50, and so on.
      
      .. note::
      
         When the channel is in PWM mode, the corresponding pin is assigned automatically, therefore
         there's no need to assign the alternate function of the pin via the ``Pin`` class. The pins which
         support PWM functionality are the following:
      
         - ``GP24`` on Timer 0 channel A.
         - ``GP25`` on Timer 1 channel A.
         - ``GP9``  on Timer 2 channel B.
         - ``GP10`` on Timer 3 channel A.
         - ``GP11`` on Timer 3 channel B.
      """
    @overload
    def channel(
        self,
        channel: int,
        /,
        *,
        period: int,
        polarity: int = POSITIVE,
        duty_cycle: int = 0,
    ) -> TimerChannel:
        """
      If only a channel identifier passed, then a previously initialized channel
      object is returned (or ``None`` if there is no previous channel).
      
      Otherwise, a TimerChannel object is initialized and returned.
      
      The operating mode is is the one configured to the Timer object that was used to
      create the channel.
      
      - ``channel`` if the width of the timer is 16-bit, then must be either ``TIMER.A``, ``TIMER.B``.
        If the width is 32-bit then it **must be** ``TIMER.A | TIMER.B``.
      
      Keyword only arguments:
      
        - ``freq`` sets the frequency in Hz.
        - ``period`` sets the period in microseconds.
      
        .. note::
      
           Either ``freq`` or ``period`` must be given, never both.
      
        - ``polarity`` this is applicable for ``PWM``, and defines the polarity of the duty cycle
        - ``duty_cycle`` only applicable to ``PWM``. It's a percentage (0.00-100.00). Since the WiPy
          doesn't support floating point numbers the duty cycle must be specified in the range 0-10000,
          where 10000 would represent 100.00, 5050 represents 50.50, and so on.
      
      .. note::
      
         When the channel is in PWM mode, the corresponding pin is assigned automatically, therefore
         there's no need to assign the alternate function of the pin via the ``Pin`` class. The pins which
         support PWM functionality are the following:
      
         - ``GP24`` on Timer 0 channel A.
         - ``GP25`` on Timer 1 channel A.
         - ``GP9``  on Timer 2 channel B.
         - ``GP10`` on Timer 3 channel A.
         - ``GP11`` on Timer 3 channel B.
      """

class TimerChannel:
    """
   class TimerChannel --- setup a channel for a timer
   ==================================================
   
   Timer channels are used to generate/capture a signal using a timer.
   
   TimerChannel objects are created using the Timer.channel() method.
   """

    def irq(
        self,
        *,
        trigger: int,
        priority: int = 1,
        handler: Callable[[Timer], None] | None = None,
    ) -> Callable[[Timer], None] | None:
        """
       The behaviour of this callback is heavily dependent on the operating
       mode of the timer channel:
       
           - If mode is ``TimerWiPy.PERIODIC`` the callback is executed periodically
             with the configured frequency or period.
           - If mode is ``TimerWiPy.ONE_SHOT`` the callback is executed once when
             the configured timer expires.
           - If mode is ``TimerWiPy.PWM`` the callback is executed when reaching the duty
             cycle value.
       
       The accepted params are:
       
           - ``priority`` level of the interrupt. Can take values in the range 1-7.
             Higher values represent higher priorities.
           - ``handler`` is an optional function to be called when the interrupt is triggered.
           - ``trigger`` must be ``TimerWiPy.TIMEOUT`` when the operating mode is either ``TimerWiPy.PERIODIC`` or
             ``TimerWiPy.ONE_SHOT``. In the case that mode is ``TimerWiPy.PWM`` then trigger must be equal to
             ``TimerWiPy.MATCH``.
       
       Returns a callback object.
      """
    @overload
    def freq(self) -> int:
        """
      Get or set the timer channel frequency (in Hz).
      """
    @overload
    def freq(self, value: int, /) -> None:
        """
      Get or set the timer channel frequency (in Hz).
      """
    @overload
    def period(self) -> int:
        """
      Get or set the timer channel period (in microseconds).
      """
    @overload
    def period(self, value: int, /) -> None:
        """
      Get or set the timer channel period (in microseconds).
      """
    @overload
    def duty_cycle(self) -> int:
        """
      Get or set the duty cycle of the PWM signal. It's a percentage (0.00-100.00). Since the WiPy
      doesn't support floating point numbers the duty cycle must be specified in the range 0-10000,
      where 10000 would represent 100.00, 5050 represents 50.50, and so on.
      """
    @overload
    def duty_cycle(self, value: int, /) -> None:
        """
      Get or set the duty cycle of the PWM signal. It's a percentage (0.00-100.00). Since the WiPy
      doesn't support floating point numbers the duty cycle must be specified in the range 0-10000,
      where 10000 would represent 100.00, 5050 represents 50.50, and so on.
      """
