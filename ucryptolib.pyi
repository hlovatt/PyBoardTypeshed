"""

cryptographic ciphers

Descriptions taken from 
`https://raw.githubusercontent.com/micropython/micropython/master/docs/library/ucryptolib.rst`, etc.

==========================================

.. module:: ucryptolib
   :synopsis: cryptographic ciphers

"""



__author__ = "Howard C Lovatt"
__copyright__ = "Howard C Lovatt, 2020 onwards."
__license__ = "MIT https://opensource.org/licenses/MIT (as used by MicroPython)."
__version__ = "3.7.2"  # Version set by https://github.com/hlovatt/tag2ver



from typing import overload, TypeVar

from uarray import array


_AnyReadableBuf = TypeVar('_AnyReadableBuf', bytearray, array, memoryview, bytes)
"""
Type that allows bytearray, array, memoryview, or bytes, 
but only one of these and not a mixture in a single declaration.
"""


_AnyWritableBuf = TypeVar('_AnyWritableBuf', bytearray, array, memoryview)
"""
Type that allows bytearray, array, or memoryview, but only one of these and not a mixture in a single declaration.
"""




# noinspection PyPep8Naming
class aes:
   """

   .. class:: aes
   
   """



   @overload
   def __init__(self, key: _AnyReadableBuf, mode: int, /):
      """
           Initialize cipher object, suitable for encryption/decryption. Note:
           after initialization, cipher object can be use only either for
           encryption or decryption. Running decrypt() operation after encrypt()
           or vice versa is not supported.
           
           Parameters are:
           
               * *key* is an encryption/decryption key (bytes-like).
               * *mode* is:
           
                   * ``1`` (or ``ucryptolib.MODE_ECB`` if it exists) for Electronic Code Book (ECB).
                   * ``2`` (or ``ucryptolib.MODE_CBC`` if it exists) for Cipher Block Chaining (CBC).
                   * ``6`` (or ``ucryptolib.MODE_CTR`` if it exists) for Counter mode (CTR).
           
               * *IV* is an initialization vector for CBC mode.
               * For Counter mode, *IV* is the initial value for the counter.
      """

   @overload
   def __init__(self, key: _AnyReadableBuf, mode: int, IV: _AnyReadableBuf, /):
      """
           Initialize cipher object, suitable for encryption/decryption. Note:
           after initialization, cipher object can be use only either for
           encryption or decryption. Running decrypt() operation after encrypt()
           or vice versa is not supported.
           
           Parameters are:
           
               * *key* is an encryption/decryption key (bytes-like).
               * *mode* is:
           
                   * ``1`` (or ``ucryptolib.MODE_ECB`` if it exists) for Electronic Code Book (ECB).
                   * ``2`` (or ``ucryptolib.MODE_CBC`` if it exists) for Cipher Block Chaining (CBC).
                   * ``6`` (or ``ucryptolib.MODE_CTR`` if it exists) for Counter mode (CTR).
           
               * *IV* is an initialization vector for CBC mode.
               * For Counter mode, *IV* is the initial value for the counter.
      """

   @overload
   def encrypt(self, in_buf: _AnyReadableBuf, /) -> bytes:
      """
           Encrypt *in_buf*. If no *out_buf* is given result is returned as a
           newly allocated `bytes` object. Otherwise, result is written into
           mutable buffer *out_buf*. *in_buf* and *out_buf* can also refer
           to the same mutable buffer, in which case data is encrypted in-place.
      """

   @overload
   def encrypt(self, in_buf: _AnyReadableBuf, out_buf: _AnyWritableBuf, /) -> None:
      """
           Encrypt *in_buf*. If no *out_buf* is given result is returned as a
           newly allocated `bytes` object. Otherwise, result is written into
           mutable buffer *out_buf*. *in_buf* and *out_buf* can also refer
           to the same mutable buffer, in which case data is encrypted in-place.
      """

   @overload
   def decrypt(self, in_buf: _AnyReadableBuf, /) -> bytes:
      """
           Like `encrypt()`, but for decryption.
      """

   @overload
   def decrypt(self, in_buf: _AnyReadableBuf, out_buf: _AnyWritableBuf, /) -> None:
      """
           Like `encrypt()`, but for decryption.
      """


