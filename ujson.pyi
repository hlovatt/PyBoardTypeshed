"""
JSON encoding and decoding

Descriptions taken from 
`https://raw.githubusercontent.com/micropython/micropython/master/docs/library/json.rst`, etc.
=========================================

.. module:: json
   :synopsis: JSON encoding and decoding

|see_cpython_module| :mod:`python:json`.

This modules allows to convert between Python objects and the JSON
data format.
"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "6.2.1"  # Version set by https://github.com/hlovatt/tag2ver

from types import TracebackType
from typing import Any, Tuple, AnyStr, Final, TypeVar, runtime_checkable, Protocol
from typing import Type

from uarray import array


_AnyReadableBuf: Final = TypeVar('_AnyReadableBuf', bytearray, array, memoryview, bytes)
"""
Type that allows bytearray, array, memoryview, or bytes, 
but only one of these and not a mixture in a single declaration.
"""


_AnyWritableBuf: Final = TypeVar('_AnyWritableBuf', bytearray, array, memoryview)
"""
Type that allows bytearray, array, or memoryview, but only one of these and not a mixture in a single declaration.
"""


_AnyStr: Final = TypeVar('_AnyStr', str, bytes)  # `str` for text IO and `bytes` for binary IO.
_Self: Final = TypeVar('_Self')  # The type that extends `IOBase`.

@runtime_checkable
class IOBase(Protocol[_AnyStr, _Self]):
    """A `Protocol` (structurally typed) for an IOStream."""

    __slots__ = ()
    
    def __enter__(self) -> _Self:
        """
        Called on entry to a `with` block.
        The `with` statement will bind this method’s return value to the target(s) specified in the `as` clause 
        of the statement, if any.
        """
        
    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """
        Called on exit of a `with` block.
        The parameters describe the exception that caused the context to be exited. 
        If the context was exited without an exception, all three arguments will be `None`.

        If an exception is supplied, and the method wishes to suppress the exception 
        (i.e., prevent it from being propagated), it should return a true value. 
        Otherwise, the exception will be processed normally upon exit from this method.

        *Note* that `__exit__()` methods should not re-raise the passed-in exception; 
        this is the caller’s responsibility.
        """
        
    def __next__(self) -> _AnyStr:
        """
        
        """
    
    def __iter__(self) -> _Self:
        """
        
        """

    def close(self) -> None:
        """
        Flushes the write buffers and closes the IO stream; best not called directly, use a `with` block instead.
        Calling `f.close()` without using a `with` block might result in content not being completely written to the 
        disk, even if the program exits successfully.
        A closed file cannot be read or written any more. 
        Any operation which requires that the file be open will raise a `ValueError` after the file has been closed. 
        Calling `f.close()` more than once is allowed.
        """

    def flush(self) -> None:
        """
        Flushes the write buffers of the IO stream.
        `flush()` does not necessarily write the file’s data to disk. 
        Use `f.flush()` followed by `os.sync()` to ensure this behavior.
        
        This method does nothing for read-only and non-blocking streams.
        """

    def read(self, size: int | None = -1) -> AnyStr | None:
        """
        Read up to `size` bytes from the object and return them as a `str` (text file) or `bytes` (binary file). 
        As a convenience, if `size` is unspecified or -1, all bytes until EOF are returned. 
        Otherwise, only one system call is ever made. 
        Fewer than `size` bytes may be returned if the operating system call returns fewer than `size` bytes.

        If 0 bytes are returned, and `size` was not 0, this indicates end of file. 
        If `self` is in non-blocking mode and no bytes are available, `None` is returned.
        """

    def readinto(self, b: _AnyWritableBuf) -> int | None:
        """
        Read bytes into a pre-allocated, writable bytes-like object b, and return the number of bytes read. 
        For example, b might be a bytearray. 
        
        If `self` is in non-blocking mode and no bytes are available, `None` is returned.
        """

    def readline(self, size: int = -1) -> AnyStr:
        """
        Read and return, as a `str` (text file) or `bytes` (binary file), one line from the stream. 
        If size is specified, at most size bytes will be read.
        
        The line terminator is always `b'
'` for binary files; 
        for text files, the newline argument to `open()` can be used to select the line terminator(s) recognized.
        """

    def readlines(self, hint: int | None = -1) -> list[AnyStr]:
        """
        Read and return a list of lines, as a `list[str]` (text file) or `list[bytes]` (binary file), from the stream. 
        `hint` can be specified to control the number of lines read: 
        no more lines will be read if the total size (in bytes/characters) of all lines so far exceeds `hint`.

        `hint` values of 0 or less, as well as `None`, are treated as no hint.
        The line terminator is always `b'
'` for binary files; 
        for text files, the newline argument to `open()` can be used to select the line terminator(s) recognized.

        *Note* that it’s already possible to iterate on file objects using `for line in file: ...` 
        without calling `file.readlines()`.
        """

    def write(self, b: _AnyReadableBuf) -> int | None:
        """
        Write the given bytes-like object, `b`, to the underlying raw stream, and return the number of bytes written. 
        This can be less than the length of `b` in bytes, depending on specifics of the underlying raw stream, 
        and especially if it is in non-blocking mode. 
        `None` is returned if the raw stream is set not to block and no single byte could be readily written to it. 
        
        The caller may release or mutate `b` after this method returns, 
        so the implementation only access `b` during the method call.
        """

    def seek(self, offset: int, whence: int = 0) -> int:
        """
        Change the stream position to the given byte `offset`. 
        `offset` is interpreted relative to the position indicated by `whence`.
        The default value for whence is 0. 
        
        Values for whence are:

          * 0 – start of the stream (the default); offset should be zero or positive.
          * 1 – current stream position; offset may be negative.
          * 2 – end of the stream; offset is usually negative.
        
        Returns the new absolute position.
        """

    def tell(self) -> int:
        """
        Return the current stream position.
        """


def dump(obj: Any, stream: IOBase[str, Any], separators: Tuple[str, str] | None = None, /) -> None:
   """
   Serialise *obj* to a JSON string, writing it to the given *stream*.
   
   If specified, separators should be an ``(item_separator, key_separator)``
   tuple. The default is ``(', ', ': ')``. To get the most compact JSON
   representation, you should specify ``(',', ':')`` to eliminate whitespace.
   """

def dumps(obj: Any, separators: Tuple[str, str] | None = None) -> str:
   """
   Return *obj* represented as a JSON string.
   
   The arguments have the same meaning as in `dump`.
   """

def load(stream: IOBase[str, Any]) -> Any:
   """
   Parse the given *stream*, interpreting it as a JSON string and
   deserialising the data to a Python object.  The resulting object is
   returned.
   
   Parsing continues until end-of-file is encountered.
   A :exc:`ValueError` is raised if the data in *stream* is not correctly formed.
   """

def loads(str: AnyStr) -> Any:
   """
   Parse the JSON *str* and return an object.  Raises :exc:`ValueError` if the
   string is not correctly formed.
   """
