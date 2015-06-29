""" Util module that contains some utilities
It's just a collection of a bunch utilities functions. Most
of them are assertion for types.
"""

from threading import Lock
import struct


class XMException(Exception):
    """Base class for exceptions related to XM.
    """
    pass


class XMValueError(XMException):
    """Exception with the same meaning as the standard
    ValueError, but it's related to XM.
    """
    pass


def assert_type(value, cinfo):
    """ Generic functions that checks if a given value is of the given
    type raising ValueError if it isn't.

    Args:
      value: the value to check the type of
      cinfo (classinfo): the type the value must be

    Raises:
      XMValueError: if `value` isn't of type `cinfo`
    """
    if not isinstance(value, cinfo):
        raise XMValueError(
            'Expected must be of {extype} type instead of {curtype}'.format(
                extype=cinfo.__name__,
                curtype=type(value).__name__))


def assert_bytes(value):
    """ Utility function that checks if a given value is bytes.

    Args:
      value: the value to check the type of

    Raises:
      XMValueError: if `value` isn't bytes
    """
    assert_type(value, bytes)


def assert_int(value):
    """ Utility function that checks if a given value is int.

    Args:
      value: the value to check the type of

    Raises:
      XMValueError: if `value` isn't int
    """
    assert_type(value, int)


def assert_in_range(value, start, end):
    """ Utility function that checks if a given value is between
    two given values(included).

    Args:
      value: the value to check if it is between `s` and `e`
      start: the lowest bound of the range(included)
      end: the highest bound of the range(included)

    Raises:
      XMValueError: if `value` isn't in range [`value`, `end`]
    """
    if not start <= value <= end:
        raise XMValueError('{v} must be between {s} and {e}'.format(v=value,
                                                                    s=start,
                                                                    e=end))


def assert_uint8(value):
    """ Utility function that checks if a given value is uint8.

    Args:
      value: the value to check the type of

    Raises:
      XMValueError: if `value` isn't int or it's outside range [0,0XFF]
    """
    assert_int(value)
    assert_in_range(value, 0, 0XFF)


def assert_uint16(value):
    """ Utility function that checks if a given value is uint16.

    Args:
      value: the value to check the type of

    Raises:
      XMValueError: if `value` isn't int or it's outside range [0,0XFFFF]
    """
    assert_int(value)
    assert_in_range(value, 0, 0xFFFF)


def int8_to_byte(i):
    """ Utility function that converts an integer to its byte representation
    in little endian order. If `i` is not representable in a single byte it will
    raise OverflowError.

    Args:
      i (int): integer to convert

    Returns:
      bytes: the byte representation

    Raises:
      XMOverflowError: if `i` is not representable in 1 byte
    """
    return i.to_bytes(1, byteorder='little', signed=True)


def uint8_to_byte(i):
    """ Utility function that converts an unsigned integer to its byte
    representation in little endian order. If `i` is not representable
    in a single byte it will raise OverflowError.

    Args:
      i (int): integer to convert

    Returns:
      bytes: the byte representation

    Raises:
      OverflowError: if `i` is not representable in 1 byte
    """
    return i.to_bytes(1, byteorder='little', signed=False)


def uint16_to_bytes(value):
    """ Utility function that converts an unsigned integer to its bytes
    representation in little endian order. If `i` is not representable
    in 2 bytes or if it is signed it will raise OverflowError.

    Args:
      i (int): integer to convert

    Returns:
      bytes: the byte representation.
    """
    return struct.pack('!H', value)


def str_to_bool(s):
    """Utility function that tries to convert a string
    to a boolean. In particular it returns True whether `s`
    is 'True' or any integer different than 0, and False otherwise.
    If the cast is impossible XMValueError is raised.

    Args:
        s (str): string to convert

    Raises:
        XMValueEror: if the cast fails
    """
    s = s.lower()
    if s == 'true':
        return True
    if s == 'false':
        return False
    try:
        i = int(s)
        return i != 0
    except ValueError:
        raise XMValueError


def str_to_int(s):
    """Utility function that converts a string into an integer.
    If the cast is impossible then XMValueError is raised.

    Args:
        s (str): string to convert

    Raises:
        XMValueError: if the cast fails
    """
    try:
        return int(s)
    except ValueError:
        raise XMValueError


class UnableToLock(XMException):
    """Exception raised by LockAdapter if it wasn't able
    to lock.
    """
    pass


class LockAdapter:
    """Class that wraps every method not starting with '_' in such a way
    that it will be possible to call those methods on the istance of
    LockAdapter with thread safety.
    It's possible to set a timeout if blocking for an undefined period
    is not acceptable. If locking failed then UnableToLock is raised.

    Example:

    $ i = 42
    $ la = LockAdapter(i)
    $ i.to_bytes(1, byteorder='little')   // threadsafe
    """

    def __init__(self, obj, timeout=0.005):
        """Create a new LockAdapter that wraps the methods in `obj`.
        After creation the instance will have all the methods of `obj` so
        to use it just call the method you want to.

        Args:
          obj: object to wrap
          timeout (int, optional): optional timeout to lock
        """
        self._lock = Lock()
        self._timeout = timeout
        self._obj = obj
        methods = [
            md for md in self._obj.__dir__()
            if not md.startswith('_') and callable(getattr(self._obj, md))
        ]

        dic = {}
        for method in methods:
            dic[method] = self._gen_call(method)
            dic[method].__name__ = method
            dic[method].__doc__ = getattr(self._obj, method).__doc__
        self.__dict__.update(dic)

    def _gen_call(self, method):
        """Helper function that generates a new thread safe callable
        wrapping the given `method`.

        Args:
          method (method): method to wrap

        Return:
          method: the thread safe version of `method`
        """

        def call(*args, **kwargs):
            """Inner function that actually wraps the method that
            forwards the arguments to the method.

            Args:
              args: argument list to pass to the method
              kwargs: keyword arguments to pass to the method

            Raises:
              UnableToLock: if locking was impossible in the given
              timeout.
            """
            if not self._timeout:
                with self._lock:
                    return getattr(self._obj, method)(*args, **kwargs)
            else:
                if not self._lock.acquire(timeout=self._timeout):
                    raise UnableToLock(
                        'Unable to lock for method {}'.format(method.__name__))
                try:
                    return getattr(self._obj, method)(*args, **kwargs)
                finally:
                    self._lock.release()

        return call
