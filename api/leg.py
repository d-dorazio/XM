"""This is the interface 'client-side' of the protocol to communicate
with the motors. It's just a collection of a bunch of utilities.
To get an overview of the protocol refer to the arduino protocol documentation.
"""

from serial import Serial
from enum import Enum, unique
from util import (assert_uint8, assert_uint16, assert_bytes, int8_to_byte,
                  uint8_to_byte, uint16_to_bytes, XMException)


@unique
class ArduinoMessages(Enum):
    """This enum contains the current
    supported messages by the protocol. To access the real
    value access '.value'. To check if the received message is a `Ack`
    just do a binary and with `Ack`, because the response is the binary or
    between the message and `Ack` or `NAck`.
    The motors will move asyncronously if the character of the message
    is lowered, syncronously otherwise.

    Attributes:
        Unsupported: unsupported message by the protocol
        NAck: something went wrong
        Ack: something went just fine
        Forward: move forward
        Backward: move backward
        Left: move left
        Right: move right
        Stop: stop
        Set_Speed: sets the motors speed
        Set_MoveTime: sets the time motors during which motors will move
                    syncronously
    """
    Unsupported = int8_to_byte(-2)
    NAck = int8_to_byte(0)
    Ack = int8_to_byte(1)
    Forward = int8_to_byte(ord('F'))
    Backward = int8_to_byte(ord('B'))
    Left = int8_to_byte(ord('L'))
    Right = int8_to_byte(ord('R'))
    Stop = int8_to_byte(ord('Z'))
    Set_Speed = int8_to_byte(ord('X'))
    Set_MoveTime = int8_to_byte(ord('T'))


def create_ack(msg):
    """Creates a `Ack` relative to a given message.

    Args:
        msg(ArduinoMessages): msg to create the `Ack` from.

    Returns:
        byte: the final message
    """
    return int8_to_byte(msg[0] | ArduinoMessages.Ack.value[0])


def create_nack(msg):
    """Creates a `NAck` relative to a given message.

    Args:
        msg(ArduinoMessages): msg to create the `NAck` from.

    Returns:
        byte: the final message
    """
    return int8_to_byte(msg[0] | ArduinoMessages.NAck.value[0])


class LegsException(XMException):
    """Exception raised whenever an error related to `Legs`
    occurs.
    """
    pass


class Legs:
    """This class manages the communication with Arduino.
    It provides a bunch of simple to use functions, which
    are safe.

    Attributes:
        serial(Serial): serial port to use for the communication
    """

    def __init__(self, port):
        """Creates a new Legs instance.

        Args:
            port(str or int): identifier of the port to use either
                '/dev/ttyACM0' or 0.
        """
        self.serial = Serial(port)

    def _read_expected(self, expected, actionstr=''):
        """Helper function that reads from the serial
        and compares the result with `expected` raising
        `LegsException` if aren't equal. Now the messages
        returns only a messages however in the future this may
        change so just prevent future errors.

        Args:
            expected(iterables of bytes): expected result
            actionstr(str): name of the action we are performing

        Raises:
            LegsException: if the what we have read isn't equal
                to the expected
        """
        assert_bytes(expected)

        r = b''
        for _ in range(len(expected)):
            r = r + self.serial.read()
        if r != expected:
            raise LegsException(
                'Unable to {actionstr} due to error: {errcode}'.format(
                    actionstr=actionstr,
                    errcode=str(r)))

    def _send_n_read(self, msg, actionstr, async=False, ack=None):
        """Helper function that sends the given `msg` and reads
        the `ack` or if it is None it will use `create_ack` on
        `msg` to get the expected result.

        Args:
            msg(byte): message to send
            actionstr(str): action description
            async(bool): if True the `msg` will be lowered, otherwise
                Nothing will be performed
            ack(byte): if None the expected byte will be created calling
                `create_ack` on `msg` otherwise it will be used as the
                expected value.
        """
        assert_bytes(msg)
        if async:
            msg = msg.lower()
        self.serial.write(msg)
        ack = ack or create_ack(msg)
        self._read_expected(ack, actionstr)

    def forward(self, async=False):
        """Utility function that makes the rover move forward.

        Args:
            async(bool): if True it will return immediatly, otherwise
                it will wait until the rover stops.
        """
        self._send_n_read(ArduinoMessages.Forward.value, 'move forward',
                          async=async)

    def backward(self, async=False):
        """Utility function that makes the rover move backward.

        Args:
            async(bool): if True it will return immediatly, otherwise
                it will wait until the rover stops.
        """
        self._send_n_read(ArduinoMessages.Backward.value, 'move backward',
                          async=async)

    def left(self, async=False):
        """Utility function that makes the rover move left.

        Args:
            async(bool): if True it will return immediatly, otherwise
                it will wait until the rover stops.
        """
        self._send_n_read(ArduinoMessages.Left.value, 'rotate left',
                          async=async)

    def right(self, async=False):
        """Utility function that makes the rover move right.

        Args:
            async(bool): if True it will return immediatly, otherwise
                it will wait until the rover stops.
        """
        self._send_n_read(ArduinoMessages.Right.value, 'rotate right',
                          async=async)

    def stop(self):
        """Utility function that stops the rover.
        """
        self._send_n_read(ArduinoMessages.Stop.value, 'stop', async=True)

    def set_speed(self, speed_value):
        """Utility function that sets the speed of the rover.
        The value must be between 0 and 255

        Args:
            speed_value(int): speed value
        """
        assert_uint8(speed_value)
        speed_value = uint8_to_byte(speed_value)
        self._send_n_read(ArduinoMessages.Set_Speed.value + speed_value,
                          'set speed',
                          ack=create_ack(ArduinoMessages.Set_Speed.value))

    def set_movetime(self, time):
        """Utility function that sets the time during which
        the rover will move if syncronous mode. The value must
        be between 0 and 65535.

        Args:
            time(int): time to wait in syncronous mode.
        """
        assert_uint16(time)
        time = uint16_to_bytes(time)
        self._send_n_read(ArduinoMessages.Set_MoveTime.value + time,
                          'set move time',
                          ack=create_ack(ArduinoMessages.Set_MoveTime.value))
