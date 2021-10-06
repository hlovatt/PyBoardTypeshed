"""
basic "operating system" services

Descriptions taken from 
`https://raw.githubusercontent.com/micropython/micropython/master/docs/library/os.rst`, etc.
==============================================

.. module:: os
   :synopsis: basic "operating system" services

|see_cpython_module| :mod:`python:os`.

The ``os`` module contains functions for filesystem access and mounting,
terminal redirection and duplication, and the ``uname`` and ``urandom``
functions.
"""

__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "6.1.0"  # Version set by https://github.com/hlovatt/tag2ver

from abc import abstractmethod
from types import TracebackType
from typing import Tuple, AnyStr, Final, TypeVar, runtime_checkable, Protocol
from typing import Optional, Type, List, overload, Literal

from uarray import array

_StrOrBytesT: Final = TypeVar('_StrOrBytesT', str, bytes)

class _PathLike(Protocol[_StrOrBytesT]):
    @abstractmethod
    def __fspath__(self) -> _StrOrBytesT:
        """Return the file system path representation of the object, preferably as a `str`."""
    
_AnyPath: Final = str | bytes | _PathLike[str] | _PathLike[bytes]
_FdOrAnyPath: Final = int | _AnyPath


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


def uname() -> Tuple[str, str, str, str, str]:
   """
   Return a tuple (possibly a named tuple) containing information about the
   underlying machine and/or its operating system.  The tuple has five fields
   in the following order, each of them being a string:
   
        * ``sysname`` -- the name of the underlying system
        * ``nodename`` -- the network name (can be the same as ``sysname``)
        * ``release`` -- the version of the underlying system
        * ``version`` -- the MicroPython version and build date
        * ``machine`` -- an identifier for the underlying hardware (eg board, CPU)
   """

def urandom(n: int, /) -> bytes:
   """
   Return a bytes object with *n* random bytes. Whenever possible, it is
   generated by the hardware random number generator.
   """

def chdir(path: _FdOrAnyPath, /) -> None:
   """
   Change current directory.
   """

def getcwd() -> str:
   """
   Get the current directory.
   """

@overload
def ilistdir() -> List[Tuple[str, int, int] | Tuple[str, int, int, int]]:
   """
   This function returns an iterator which then yields tuples corresponding to
   the entries in the directory that it is listing.  With no argument it lists the
   current directory, otherwise it lists the directory given by *dir*.
   
   The tuples have the form *(name, type, inode[, size])*:
   
    - *name* is a string (or bytes if *dir* is a bytes object) and is the name of
      the entry;
    - *type* is an integer that specifies the type of the entry, with 0x4000 for
      directories and 0x8000 for regular files;
    - *inode* is an integer corresponding to the inode of the file, and may be 0
      for filesystems that don't have such a notion.
    - Some platforms may return a 4-tuple that includes the entry's *size*.  For
      file entries, *size* is an integer representing the size of the file
      or -1 if unknown.  Its meaning is currently undefined for directory
      entries.
   """

@overload
def ilistdir(dir: int, /) -> List[Tuple[str, int, int] | Tuple[str, int, int, int]]:
   """
   This function returns an iterator which then yields tuples corresponding to
   the entries in the directory that it is listing.  With no argument it lists the
   current directory, otherwise it lists the directory given by *dir*.
   
   The tuples have the form *(name, type, inode[, size])*:
   
    - *name* is a string (or bytes if *dir* is a bytes object) and is the name of
      the entry;
    - *type* is an integer that specifies the type of the entry, with 0x4000 for
      directories and 0x8000 for regular files;
    - *inode* is an integer corresponding to the inode of the file, and may be 0
      for filesystems that don't have such a notion.
    - Some platforms may return a 4-tuple that includes the entry's *size*.  For
      file entries, *size* is an integer representing the size of the file
      or -1 if unknown.  Its meaning is currently undefined for directory
      entries.
   """

@overload
def ilistdir(dir: str, /) -> List[Tuple[str, int, int] | Tuple[str, int, int, int]]:
   """
   This function returns an iterator which then yields tuples corresponding to
   the entries in the directory that it is listing.  With no argument it lists the
   current directory, otherwise it lists the directory given by *dir*.
   
   The tuples have the form *(name, type, inode[, size])*:
   
    - *name* is a string (or bytes if *dir* is a bytes object) and is the name of
      the entry;
    - *type* is an integer that specifies the type of the entry, with 0x4000 for
      directories and 0x8000 for regular files;
    - *inode* is an integer corresponding to the inode of the file, and may be 0
      for filesystems that don't have such a notion.
    - Some platforms may return a 4-tuple that includes the entry's *size*.  For
      file entries, *size* is an integer representing the size of the file
      or -1 if unknown.  Its meaning is currently undefined for directory
      entries.
   """

@overload
def ilistdir(dir: bytes, /) -> List[Tuple[bytes, int, int] | Tuple[bytes, int, int, int]]:
   """
   This function returns an iterator which then yields tuples corresponding to
   the entries in the directory that it is listing.  With no argument it lists the
   current directory, otherwise it lists the directory given by *dir*.
   
   The tuples have the form *(name, type, inode[, size])*:
   
    - *name* is a string (or bytes if *dir* is a bytes object) and is the name of
      the entry;
    - *type* is an integer that specifies the type of the entry, with 0x4000 for
      directories and 0x8000 for regular files;
    - *inode* is an integer corresponding to the inode of the file, and may be 0
      for filesystems that don't have such a notion.
    - Some platforms may return a 4-tuple that includes the entry's *size*.  For
      file entries, *size* is an integer representing the size of the file
      or -1 if unknown.  Its meaning is currently undefined for directory
      entries.
   """

@overload
def ilistdir(dir: _PathLike[str], /) -> List[Tuple[str, int, int] | Tuple[str, int, int, int]]:
   """
   This function returns an iterator which then yields tuples corresponding to
   the entries in the directory that it is listing.  With no argument it lists the
   current directory, otherwise it lists the directory given by *dir*.
   
   The tuples have the form *(name, type, inode[, size])*:
   
    - *name* is a string (or bytes if *dir* is a bytes object) and is the name of
      the entry;
    - *type* is an integer that specifies the type of the entry, with 0x4000 for
      directories and 0x8000 for regular files;
    - *inode* is an integer corresponding to the inode of the file, and may be 0
      for filesystems that don't have such a notion.
    - Some platforms may return a 4-tuple that includes the entry's *size*.  For
      file entries, *size* is an integer representing the size of the file
      or -1 if unknown.  Its meaning is currently undefined for directory
      entries.
   """

@overload
def ilistdir(dir: _PathLike[bytes], /) -> List[Tuple[bytes, int, int] | Tuple[bytes, int, int, int]]:
   """
   This function returns an iterator which then yields tuples corresponding to
   the entries in the directory that it is listing.  With no argument it lists the
   current directory, otherwise it lists the directory given by *dir*.
   
   The tuples have the form *(name, type, inode[, size])*:
   
    - *name* is a string (or bytes if *dir* is a bytes object) and is the name of
      the entry;
    - *type* is an integer that specifies the type of the entry, with 0x4000 for
      directories and 0x8000 for regular files;
    - *inode* is an integer corresponding to the inode of the file, and may be 0
      for filesystems that don't have such a notion.
    - Some platforms may return a 4-tuple that includes the entry's *size*.  For
      file entries, *size* is an integer representing the size of the file
      or -1 if unknown.  Its meaning is currently undefined for directory
      entries.
   """

@overload
def listdir() -> List[str]:
   """
   With no argument, list the current directory.  Otherwise list the given directory.
   """

@overload
def listdir(dir: int, /) -> List[str]:
   """
   With no argument, list the current directory.  Otherwise list the given directory.
   """

@overload
def listdir(dir: str, /) -> List[str]:
   """
   With no argument, list the current directory.  Otherwise list the given directory.
   """

@overload
def listdir(dir: bytes, /) -> List[bytes]:
   """
   With no argument, list the current directory.  Otherwise list the given directory.
   """

@overload
def listdir(dir: _PathLike[str], /) -> List[str]:
   """
   With no argument, list the current directory.  Otherwise list the given directory.
   """

@overload
def listdir(dir: _PathLike[bytes], /) -> List[bytes]:
   """
   With no argument, list the current directory.  Otherwise list the given directory.
   """

def mkdir(path: _AnyPath, /) -> None:
   """
   Create a new directory.
   """

def remove(path: _AnyPath, /) -> None:
   """
   Remove a file.
   """

def rmdir(path: _AnyPath, /) -> None:
   """
   Remove a directory.
   """

def rename(old_path: _AnyPath, new_path: _AnyPath, /) -> None:
   """
   Rename a file.
   """

def stat(path: _FdOrAnyPath, /) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
   """
   Get the status of a file or directory.
   """

def statvfs(path: _FdOrAnyPath, /) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
   """
   Get the status of a fileystem.
   
   Returns a tuple with the filesystem information in the following order:
   
        * ``f_bsize`` -- file system block size
        * ``f_frsize`` -- fragment size
        * ``f_blocks`` -- size of fs in f_frsize units
        * ``f_bfree`` -- number of free blocks
        * ``f_bavail`` -- number of free blocks for unprivileged users
        * ``f_files`` -- number of inodes
        * ``f_ffree`` -- number of free inodes
        * ``f_favail`` -- number of free inodes for unprivileged users
        * ``f_flag`` -- mount flags
        * ``f_namemax`` -- maximum filename length
   
   Parameters related to inodes: ``f_files``, ``f_ffree``, ``f_avail``
   and the ``f_flags`` parameter may return ``0`` as they can be unavailable
   in a port-specific implementation.
   """

def sync() -> None:
   """
   Sync all filesystems.
   """

def dupterm(stream_object: _IOBase | None, index: int = 0, /) -> _IOBase | None:
   """
   Duplicate or switch the MicroPython terminal (the REPL) on the given `stream`-like
   object. The *stream_object* argument must be a native stream object, or derive
   from ``io.IOBase`` and implement the ``readinto()`` and
   ``write()`` methods.  The stream should be in non-blocking mode and
   ``readinto()`` should return ``None`` if there is no data available for reading.
   
   After calling this function all terminal output is repeated on this stream,
   and any input that is available on the stream is passed on to the terminal input.
   
   The *index* parameter should be a non-negative integer and specifies which
   duplication slot is set.  A given port may implement more than one slot (slot 0
   will always be available) and in that case terminal input and output is
   duplicated on all the slots that are set.
   
   If ``None`` is passed as the *stream_object* then duplication is cancelled on
   the slot given by *index*.
   
   The function returns the previous stream-like object in the given slot.
   """

def mount(fsobj: "AbstractBlockDev", mount_point: str, /, *, readonly: bool = False) -> _IOBase | None:
   """
    Mount the filesystem object *fsobj* at the location in the VFS given by the
    *mount_point* string.  *fsobj* can be a a VFS object that has a ``mount()``
    method, or a block device.  If it's a block device then the filesystem type
    is automatically detected (an exception is raised if no filesystem was
    recognised).  *mount_point* may be ``'/'`` to mount *fsobj* at the root,
    or ``'/<name>'`` to mount it at a subdirectory under the root.
    
    If *readonly* is ``True`` then the filesystem is mounted read-only.
    
    During the mount process the method ``mount()`` is called on the filesystem
    object.
    
    Will raise ``OSError(EPERM)`` if *mount_point* is already mounted.
    
    
    Filesystem mounting
    -------------------
    
    Some ports provide a Virtual Filesystem (VFS) and the ability to mount multiple
    "real" filesystems within this VFS.  Filesystem objects can be mounted at either
    the root of the VFS, or at a subdirectory that lives in the root.  This allows
    dynamic and flexible configuration of the filesystem that is seen by Python
    programs.  Ports that have this functionality provide the :func:`mount` and
    :func:`umount` functions, and possibly various filesystem implementations
    represented by VFS classes.
   """

def umount(mount_point: str, /) -> None:
   """
    Unmount a filesystem. *mount_point* can be a string naming the mount location,
    or a previously-mounted filesystem object.  During the unmount process the
    method ``umount()`` is called on the filesystem object.
    
    Will raise ``OSError(EINVAL)`` if *mount_point* is not found.
   """


class VfsFat("AbstractBlockDev"):
   """

   """



   def __init__(self, block_dev: "AbstractBlockDev", /):
      """
       Create a filesystem object that uses the FAT filesystem format.  Storage of
       the FAT filesystem is provided by *block_dev*.
       Objects created by this constructor can be mounted using :func:`mount`.
      """

   
   @staticmethod
   def mkfs(block_dev: "AbstractBlockDev", /) -> None:
      """
           Build a FAT filesystem on *block_dev*.
      """


class VfsLfs1("AbstractBlockDev"):
   """

   """



   
   def __init__(
      self, 
      block_dev: "AbstractBlockDev", 
      readsize: int = 32, 
      progsize: int = 32, 
      lookahead: int = 32, 
      /,
   ):
      """
       Create a filesystem object that uses the `littlefs v1 filesystem format`_.
       Storage of the littlefs filesystem is provided by *block_dev*, which must
       support the :ref:`extended interface <block-device-interface>`.
       Objects created by this constructor can be mounted using :func:`mount`.
       
       See :ref:`filesystem` for more information.
      """

   
   @staticmethod
   def mkfs(
      block_dev: "AbstractBlockDev", 
      readsize: int = 32, 
      progsize: int = 32, 
      lookahead: int = 32, 
      /,
   ) -> None:
      """
           Build a Lfs1 filesystem on *block_dev*.
           
           .. note:: There are reports of littlefs v1 failing in certain situations,
                 for details see `littlefs issue 347`_.
      """


class VfsLfs2("AbstractBlockDev"):
   """

   """



   
   def __init__(
      self, 
      block_dev: "AbstractBlockDev", 
      readsize: int = 32, 
      progsize: int = 32, 
      lookahead: int = 32, 
      mtime: bool = True,
      /,
   ):
      """
       Create a filesystem object that uses the `littlefs v2 filesystem format`_.
       Storage of the littlefs filesystem is provided by *block_dev*, which must
       support the :ref:`extended interface <block-device-interface>`.
       Objects created by this constructor can be mounted using :func:`mount`.
       
       The *mtime* argument enables modification timestamps for files, stored using
       littlefs attributes.  This option can be disabled or enabled differently each
       mount time and timestamps will only be added or updated if *mtime* is enabled,
       otherwise the timestamps will remain untouched.  Littlefs v2 filesystems without
       timestamps will work without reformatting and timestamps will be added
       transparently to existing files once they are opened for writing.  When *mtime*
       is enabled `os.stat` on files without timestamps will return 0 for the timestamp.
       
       See :ref:`filesystem` for more information.
      """

   
   @staticmethod
   def mkfs(
      block_dev: "AbstractBlockDev", 
      readsize: int = 32, 
      progsize: int = 32, 
      lookahead: int = 32, 
      mtime: bool = True,
      /,
   ) -> None:
      """
           Build a Lfs2 filesystem on *block_dev*.
           
           .. note:: There are reports of littlefs v2 failing in certain situations,
                 for details see `littlefs issue 295`_.
      """


@runtime_checkable
class AbstractBlockDev(Protocol):
   """
   Block devices
   -------------
   
   A block device is an object which implements the block protocol. This enables a
   device to support MicroPython filesystems. The physical hardware is represented
   by a user defined class. The :class:`AbstractBlockDev` class is a template for
   the design of such a class: MicroPython does not actually provide that class,
   but an actual block device class must implement the methods described below.
   
   A concrete implementation of this class will usually allow access to the
   memory-like functionality of a piece of hardware (like flash memory). A block
   device can be formatted to any supported filesystem and mounted using ``os``
   methods.
   
   See :ref:`filesystem` for example implementations of block devices using the
   two variants of the block protocol described below.
   
   .. _block-device-interface:
   
   Simple and extended interface
   .............................
   
   There are two compatible signatures for the ``readblocks`` and ``writeblocks``
   methods (see below), in order to support a variety of use cases.  A given block
   device may implement one form or the other, or both at the same time. The second
   form (with the offset parameter) is referred to as the "extended interface".
   
   Some filesystems (such as littlefs) that require more control over write
   operations, for example writing to sub-block regions without erasing, may require
   that the block device supports the extended interface.
   """



   def __init__(self):
      """
       Construct a block device object.  The parameters to the constructor are
       dependent on the specific block device.
      """

   
   @overload
   def readblocks(self, block_num: int, buf: bytearray, /) -> None:
      """
           The first form reads aligned, multiples of blocks.
           Starting at the block given by the index *block_num*, read blocks from
           the device into *buf* (an array of bytes).
           The number of blocks to read is given by the length of *buf*,
           which will be a multiple of the block size.
           
           The second form allows reading at arbitrary locations within a block,
           and arbitrary lengths.
           Starting at block index *block_num*, and byte offset within that block
           of *offset*, read bytes from the device into *buf* (an array of bytes).
           The number of bytes to read is given by the length of *buf*.
      """

   
   @overload
   def readblocks(self, block_num: int, buf: bytearray, offset: int, /) -> None:
      """
           The first form reads aligned, multiples of blocks.
           Starting at the block given by the index *block_num*, read blocks from
           the device into *buf* (an array of bytes).
           The number of blocks to read is given by the length of *buf*,
           which will be a multiple of the block size.
           
           The second form allows reading at arbitrary locations within a block,
           and arbitrary lengths.
           Starting at block index *block_num*, and byte offset within that block
           of *offset*, read bytes from the device into *buf* (an array of bytes).
           The number of bytes to read is given by the length of *buf*.
      """

   
   @overload
   def writeblocks(self, block_num: int, buf: bytes | bytearray, /) -> None:
      """
           The first form writes aligned, multiples of blocks, and requires that the
           blocks that are written to be first erased (if necessary) by this method.
           Starting at the block given by the index *block_num*, write blocks from
           *buf* (an array of bytes) to the device.
           The number of blocks to write is given by the length of *buf*,
           which will be a multiple of the block size.
           
           The second form allows writing at arbitrary locations within a block,
           and arbitrary lengths.  Only the bytes being written should be changed,
           and the caller of this method must ensure that the relevant blocks are
           erased via a prior ``ioctl`` call.
           Starting at block index *block_num*, and byte offset within that block
           of *offset*, write bytes from *buf* (an array of bytes) to the device.
           The number of bytes to write is given by the length of *buf*.
           
           Note that implementations must never implicitly erase blocks if the offset
           argument is specified, even if it is zero.
      """

   
   @overload
   def writeblocks(self, block_num: int, buf: bytes | bytearray, offset: int, /) -> None:
      """
           The first form writes aligned, multiples of blocks, and requires that the
           blocks that are written to be first erased (if necessary) by this method.
           Starting at the block given by the index *block_num*, write blocks from
           *buf* (an array of bytes) to the device.
           The number of blocks to write is given by the length of *buf*,
           which will be a multiple of the block size.
           
           The second form allows writing at arbitrary locations within a block,
           and arbitrary lengths.  Only the bytes being written should be changed,
           and the caller of this method must ensure that the relevant blocks are
           erased via a prior ``ioctl`` call.
           Starting at block index *block_num*, and byte offset within that block
           of *offset*, write bytes from *buf* (an array of bytes) to the device.
           The number of bytes to write is given by the length of *buf*.
           
           Note that implementations must never implicitly erase blocks if the offset
           argument is specified, even if it is zero.
      """

   @overload
   def ioctl(self, op: int, arg: int) -> int | None:
      """
           Control the block device and query its parameters.  The operation to
           perform is given by *op* which is one of the following integers:
           
             - 1 -- initialise the device (*arg* is unused)
             - 2 -- shutdown the device (*arg* is unused)
             - 3 -- sync the device (*arg* is unused)
             - 4 -- get a count of the number of blocks, should return an integer
               (*arg* is unused)
             - 5 -- get the number of bytes in a block, should return an integer,
               or ``None`` in which case the default value of 512 is used
               (*arg* is unused)
             - 6 -- erase a block, *arg* is the block number to erase
           
           As a minimum ``ioctl(4, ...)`` must be intercepted; for littlefs
           ``ioctl(6, ...)`` must also be intercepted. The need for others is
           hardware dependent.
           
           Prior to any call to ``writeblocks(block, ...)`` littlefs issues
           ``ioctl(6, block)``. This enables a device driver to erase the block
           prior to a write if the hardware requires it. Alternatively a driver
           might intercept ``ioctl(6, block)`` and return 0 (success). In this case
           the driver assumes responsibility for detecting the need for erasure.
           
           Unless otherwise stated ``ioctl(op, arg)`` can return ``None``.
           Consequently an implementation can ignore unused values of ``op``. Where
           ``op`` is intercepted, the return value for operations 4 and 5 are as
           detailed above. Other operations should return 0 on success and non-zero
           for failure, with the value returned being an ``OSError`` errno code.
      """

   @overload
   def ioctl(self, op: Literal[4, 5], arg: int) -> int:
      """
           Control the block device and query its parameters.  The operation to
           perform is given by *op* which is one of the following integers:
           
             - 1 -- initialise the device (*arg* is unused)
             - 2 -- shutdown the device (*arg* is unused)
             - 3 -- sync the device (*arg* is unused)
             - 4 -- get a count of the number of blocks, should return an integer
               (*arg* is unused)
             - 5 -- get the number of bytes in a block, should return an integer,
               or ``None`` in which case the default value of 512 is used
               (*arg* is unused)
             - 6 -- erase a block, *arg* is the block number to erase
           
           As a minimum ``ioctl(4, ...)`` must be intercepted; for littlefs
           ``ioctl(6, ...)`` must also be intercepted. The need for others is
           hardware dependent.
           
           Prior to any call to ``writeblocks(block, ...)`` littlefs issues
           ``ioctl(6, block)``. This enables a device driver to erase the block
           prior to a write if the hardware requires it. Alternatively a driver
           might intercept ``ioctl(6, block)`` and return 0 (success). In this case
           the driver assumes responsibility for detecting the need for erasure.
           
           Unless otherwise stated ``ioctl(op, arg)`` can return ``None``.
           Consequently an implementation can ignore unused values of ``op``. Where
           ``op`` is intercepted, the return value for operations 4 and 5 are as
           detailed above. Other operations should return 0 on success and non-zero
           for failure, with the value returned being an ``OSError`` errno code.
      """

   @overload
   def ioctl(self, op: Literal[1, 2, 3, 6], arg: int) -> int | None:
      """
           Control the block device and query its parameters.  The operation to
           perform is given by *op* which is one of the following integers:
           
             - 1 -- initialise the device (*arg* is unused)
             - 2 -- shutdown the device (*arg* is unused)
             - 3 -- sync the device (*arg* is unused)
             - 4 -- get a count of the number of blocks, should return an integer
               (*arg* is unused)
             - 5 -- get the number of bytes in a block, should return an integer,
               or ``None`` in which case the default value of 512 is used
               (*arg* is unused)
             - 6 -- erase a block, *arg* is the block number to erase
           
           As a minimum ``ioctl(4, ...)`` must be intercepted; for littlefs
           ``ioctl(6, ...)`` must also be intercepted. The need for others is
           hardware dependent.
           
           Prior to any call to ``writeblocks(block, ...)`` littlefs issues
           ``ioctl(6, block)``. This enables a device driver to erase the block
           prior to a write if the hardware requires it. Alternatively a driver
           might intercept ``ioctl(6, block)`` and return 0 (success). In this case
           the driver assumes responsibility for detecting the need for erasure.
           
           Unless otherwise stated ``ioctl(op, arg)`` can return ``None``.
           Consequently an implementation can ignore unused values of ``op``. Where
           ``op`` is intercepted, the return value for operations 4 and 5 are as
           detailed above. Other operations should return 0 on success and non-zero
           for failure, with the value returned being an ``OSError`` errno code.
      """
