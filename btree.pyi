"""

simple BTree database

Descriptions taken from 
`https://raw.githubusercontent.com/micropython/micropython/master/docs/library/btree.rst`, etc.

=====================================

.. module:: btree
   :synopsis: simple BTree database

The ``btree`` module implements a simple key-value database using external
storage (disk files, or in general case, a random-access `stream`). Keys are
stored sorted in the database, and besides efficient retrieval by a key
value, a database also supports efficient ordered range scans (retrieval
of values with the keys in a given range). On the application interface
side, BTree database work as close a possible to a way standard `dict`
type works, one notable difference is that both keys and values must
be `bytes` objects (so, if you want to store objects of other types, you
need to serialize them to `bytes` first).

The module is based on the well-known BerkelyDB library, version 1.xx.

Example::

    import btree

    # First, we need to open a stream which holds a database
    # This is usually a file, but can be in-memory database
    # using io.BytesIO, a raw flash partition, etc.
    # Oftentimes, you want to create a database file if it doesn't
    # exist and open if it exists. Idiom below takes care of this.
    # DO NOT open database with "a+b" access mode.
    try:
        f = open("mydb", "r+b")
    except OSError:
        f = open("mydb", "w+b")

    # Now open a database itself
    db = btree.open(f)

    # The keys you add will be sorted internally in the database
    db[b"3"] = b"three"
    db[b"1"] = b"one"
    db[b"2"] = b"two"

    # Assume that any changes are cached in memory unless
    # explicitly flushed (or database closed). Flush database
    # at the end of each "transaction".
    db.flush()

    # Prints b'two'
    print(db[b"2"])

    # Iterate over sorted keys in the database, starting from b"2"
    # until the end of the database, returning only values.
    # Mind that arguments passed to values() method are *key* values.
    # Prints:
    #   b'two'
    #   b'three'
    for word in db.values(b"2"):
        print(word)

    del db[b"2"]

    # No longer true, prints False
    print(b"2" in db)

    # Prints:
    #  b"1"
    #  b"3"
    for key in db:
        print(key)

    db.close()

    # Don't forget to close the underlying stream!
    f.close()

   

"""



__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "6.0.0"  # Version set by https://github.com/hlovatt/tag2ver



from types import TracebackType
from typing import Protocol, Iterable, AnyStr, runtime_checkable, Optional, TypeVar, Tuple, Final
from typing import Type, Any, List

from uarray import array


_AnyWritableBuf: Final = TypeVar('_AnyWritableBuf', bytearray, array, memoryview)
"""
Type that allows bytearray, array, or memoryview, but only one of these and not a mixture in a single declaration.
"""


_AnyReadableBuf: Final = TypeVar('_AnyReadableBuf', bytearray, array, memoryview, bytes)
"""
Type that allows bytearray, array, memoryview, or bytes, 
but only one of these and not a mixture in a single declaration.
"""


_AnyStr: Final = TypeVar('_AnyStr', str, bytes)  # `str` for text IO and `bytes` for binary IO.
_Self: Final = TypeVar('_Self')  # The type that extends `_IOBase`.

@runtime_checkable
class _IOBase(Protocol[_AnyStr, _Self]):
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
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
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

    def read(self, size: Optional[int] = -1) -> Optional[AnyStr]:
        """
        Read up to `size` bytes from the object and return them as a `str` (text file) or `bytes` (binary file). 
        As a convenience, if `size` is unspecified or -1, all bytes until EOF are returned. 
        Otherwise, only one system call is ever made. 
        Fewer than `size` bytes may be returned if the operating system call returns fewer than `size` bytes.

        If 0 bytes are returned, and `size` was not 0, this indicates end of file. 
        If `self` is in non-blocking mode and no bytes are available, `None` is returned.
        """

    def readinto(self, b: _AnyWritableBuf) -> Optional[int]:
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

    def readlines(self, hint: Optional[int] = -1) -> List[AnyStr]:
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

    def write(self, b: _AnyReadableBuf) -> Optional[int]:
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




def open(
   stream: _IOBase[bytes, Any], 
   /, 
   *, 
   flags: int = 0, 
   pagesize: int = 0, 
   cachesize: int = 0, 
   minkeypage: int = 0
) -> _BTree:
   """
   Open a database from a random-access `stream` (like an open file). All
   other parameters are optional and keyword-only, and allow to tweak advanced
   parameters of the database operation (most users will not need them):
   
   * *flags* - Currently unused.
   * *pagesize* - Page size used for the nodes in BTree. Acceptable range
     is 512-65536. If 0, a port-specific default will be used, optimized for
     port's memory usage and/or performance.
   * *cachesize* - Suggested memory cache size in bytes. For a
     board with enough memory using larger values may improve performance.
     Cache policy is as follows: entire cache is not allocated at once;
     instead, accessing a new page in database will allocate a memory buffer
     for it, until value specified by *cachesize* is reached. Then, these
     buffers will be managed using LRU (least recently used) policy. More
     buffers may still be allocated if needed (e.g., if a database contains
     big keys and/or values). Allocated cache buffers aren't reclaimed.
   * *minkeypage* - Minimum number of keys to store per page. Default value
     of 0 equivalent to 2.
   
   Returns a BTree object, which implements a dictionary protocol (set
   of methods), and some additional methods described below.
   """


INCL: Final[int] = ...
"""
A flag for `keys()`, `values()`, `items()` methods to specify that
   scanning should be inclusive of the end key.
"""




DESC: Final[int] = ...
"""
A flag for `keys()`, `values()`, `items()` methods to specify that
   scanning should be in descending direction of keys.
"""




class _BTree:
   """

   """



   def close(self) -> None:
      """
      Close the database. It's mandatory to close the database at the end of
      processing, as some unwritten data may be still in the cache. Note that
      this does not close underlying stream with which the database was opened,
      it should be closed separately (which is also mandatory to make sure that
      data flushed from buffer to the underlying storage).
      """

   def flush(self) -> None:
      """
      Flush any data in cache to the underlying stream.
      """

   def __getitem__(self, key: bytes, /) -> bytes:
      """
      Standard dictionary methods.
      """

   def get(self, key: bytes, default: Optional[bytes] = None, /) -> Optional[bytes]:
      """
      Standard dictionary methods.
      """

   def __setitem__(self, key: bytes, val: bytes, /) -> None:
      """
      Standard dictionary methods.
      """

   def __delitem__(self, key: bytes, /) -> None:
      """
      Standard dictionary methods.
      """

   def __contains__(self, key: bytes, /) -> bool:
      """
      Standard dictionary methods.
      """

   def __iter__(self) -> Iterable[bytes]:
      """
      A BTree object can be iterated over directly (similar to a dictionary)
      to get access to all keys in order.
      """

   
   def keys(
      self, 
      start_key: Optional[bytes] = None, 
      end_key: Optional[bytes] = None, 
      flags: int = 0, 
      /
   ) -> Iterable[bytes]:
      """
      These methods are similar to standard dictionary methods, but also can
      take optional parameters to iterate over a key sub-range, instead of
      the entire database. Note that for all 3 methods, *start_key* and
      *end_key* arguments represent key values. For example, `values()`
      method will iterate over values corresponding to they key range
      given. None values for *start_key* means "from the first key", no
      *end_key* or its value of None means "until the end of database".
      By default, range is inclusive of *start_key* and exclusive of
      *end_key*, you can include *end_key* in iteration by passing *flags*
      of `btree.INCL`. You can iterate in descending key direction
      by passing *flags* of `btree.DESC`. The flags values can be ORed
      together.
      """

   
   def values(
      self, 
      start_key: Optional[bytes] = None, 
      end_key: Optional[bytes] = None, 
      flags: int = 0, 
      /
   ) -> Iterable[bytes]:
      """
      These methods are similar to standard dictionary methods, but also can
      take optional parameters to iterate over a key sub-range, instead of
      the entire database. Note that for all 3 methods, *start_key* and
      *end_key* arguments represent key values. For example, `values()`
      method will iterate over values corresponding to they key range
      given. None values for *start_key* means "from the first key", no
      *end_key* or its value of None means "until the end of database".
      By default, range is inclusive of *start_key* and exclusive of
      *end_key*, you can include *end_key* in iteration by passing *flags*
      of `btree.INCL`. You can iterate in descending key direction
      by passing *flags* of `btree.DESC`. The flags values can be ORed
      together.
      """

   
   def items(
      self, 
      start_key: Optional[bytes] = None, 
      end_key: Optional[bytes] = None, 
      flags: int = 0, 
      /
   ) -> Iterable[Tuple[bytes, bytes]]:
      """
      These methods are similar to standard dictionary methods, but also can
      take optional parameters to iterate over a key sub-range, instead of
      the entire database. Note that for all 3 methods, *start_key* and
      *end_key* arguments represent key values. For example, `values()`
      method will iterate over values corresponding to they key range
      given. None values for *start_key* means "from the first key", no
      *end_key* or its value of None means "until the end of database".
      By default, range is inclusive of *start_key* and exclusive of
      *end_key*, you can include *end_key* in iteration by passing *flags*
      of `btree.INCL`. You can iterate in descending key direction
      by passing *flags* of `btree.DESC`. The flags values can be ORed
      together.
      """


