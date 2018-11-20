
# The MIT License (MIT).
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
# Copyright (c) 2018 Stefan Krüger s-light.eu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`circuitpython_TLC5957`.

====================================================

CircuitPython module for the
TLC5957 16-bit 48 channel LED PWM driver.
See examples/simpletest_multi.py for a demo of the usage.

* Author(s): Stefan Kruger

Implementation Notes
--------------------

**Hardware:**

* Adafruit `12-Channel 16-bit PWM LED Driver - SPI Interface - TLC5957
  <https://www.adafruit.com/product/1455>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the ESP8622, M0 or M4-based boards:
  https://github.com/adafruit/circuitpython/releases
"""
__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_TLC5957.git"


# Globally disable invalid-name check as this chip by design has short channel
# and register names.  It is confusing to rename these from what the datasheet
# refers to them as.
# pylint: disable=invalid-name

# Globally disable too many instance attributes check.  Again this is a case
# where pylint doesn't have the right context to make this call.  The chip by
# design has many channels which must be exposed.
# pylint: disable=too-many-instance-attributes

# Globally disable protected access.  Once again pylint can't figure out the
# context for using internal decorate classes below.
# In these cases protectected access is by design for the internal class.
# pylint: disable=protected-access

# Yet another pylint issue, it fails to recognize a decorator class by
# definition has no public methods.  Disable the check.
# pylint: disable=too-few-public-methods


import time

# from enum import Enum, unique
# https://docs.python.org/3/library/enum.html
# currently not supported by CircuitPython


def _shift_in(target_byte, val):
    # Shift in a new bit value to the provided target byte.  The byte will be
    # shift one position left and a new bit inserted that's a 1 if val is true,
    # of a 0 if false.
    target_byte <<= 1
    if val:
        target_byte |= 0x01
    return target_byte


def _get_7bit_uint(buffer, start):
    """Return 7bit interpreted as unsigned integer."""
    # 0b1111111
    pass


class TLC5957:
    """Multi TLC5957 16-bit 48 channel LED PWM driver.

    This chip is designed to drive 16 RGB LEDs with 16-bit PWM per Color.
    The class has an interface compatible with the FancyLED.
    and with this is similar to the NeoPixel and DotStar Interfaces.

    :param ~busio.SPI spi: An instance of the SPI bus connected to the chip.
        The clock and MOSI/outout must be set
        the MISO/input is currently unused.
        Maximal data clock frequence is:
            - TLC5957: 33MHz
    :param ~digitalio.DigitalInOut LAT: The chip LAT (latch) pin object
        that implements the DigitalInOut API.
    :param bool pixel_count: Number of RGB-LEDs (=Pixels) are connected.
    """

    """
    TLC5957 data / register structure

    some detailed information on the protocol based on
    http://www.ti.com/lit/ds/symlink/t
    TODO!!
    """

    ##########################################
    # helper
    ##########################################

    CHIP_LED_COUNT = 16
    CHIP_BUFFER_BIT_COUNT = 48
    CHIP_BUFFER_BYTE_COUNT = CHIP_BUFFER_BIT_COUNT // 8

    # 3.10 Function Commands Summary (page 30)
    # http:#www.ti.com/lit/ug/slvuaf0/slvuaf0.pdf#page=30&zoom=auto,-110,464
    # WRTGS
    #     48-bit GS data write
    #     copy common 48bit to GS-data-latch[GS-counter]
    #     GS-counter -1
    # LATGS
    #     latch grayscale
    #     (768-bit GS data latch)
    #     copy common 48bit to GS-data-latch[0]
    #     if XREFRESH = 0
    #         GS-data-latch copy to GS-data-latch 2
    #     if XREFRESH = 1
    #         GS-data-latch copy to GS-data-latch 2
    # WRTFC
    #     write FC data
    #     copy common 48bit to FC-data
    #     if used after FCWRTEN
    # LINERESET
    #     Line Counter register clear.
    #     copy common 48bit to GS-data-latch[0]
    #     data-latch-counter reset
    #     if XREFRESH = 0
    #         Autorefresh enabled
    #         wehn GS-counter == 65535: GS-data-latch copy to GS-data-latch 2
    #     if XREFRESH = 1
    #         Autorefresh disabled
    #         GS-data-latch copy to GS-data-latch 2
    #         GS-counter reset
    #         OUTx forced off
    #     change group pattern when received
    # READFC
    #     read FC data
    #     copy FC-data to common 48bit
    #     (can be read at SOUT)
    # TMGRST
    #     reset line-counter
    #     GS-counter = 0
    #     OUTx forced off
    # FCWRTEN
    #     enable writes to FC
    #     this must send before WRTFC

    class function_command(object):
        """ENUM for available function commands."""

        WRTGS = 1
        LATGS = 3
        WRTFC = 5
        LINERESET = 7
        READFC = 11
        TMGRST = 13
        FCWRTEN = 15

    ##########################################
    # 3.3.3 Function Control (FC) Register
    # BIT     NAME            default     description
    # 0-1     LODVTH          01          LED Open Detection Voltage
    # 2-3     SEL_TD0         01          TD0 select. SOUT hold time.
    # 4       SEL_GDLY        1           Group Delay. 0 = No Delay
    # 5       XREFRESH        0           auto data refresh mode.
    #                                     on LATGS/LINERESET → data copied
    #                                       from GS1 to GS2
    #                                     0 = enabled → GS-counter continues
    #                                     1 = disabled → GS-counter reset;
    #                                       OUTx forced off
    # 6       SEL_GCK_EDGE    0           GCLK edge select.
    #                                     0 = OUTx toggle only on
    #                                       rising edge of GLCK
    #                                     1 = OUTx toggle on
    #                                       rising & falling edge of GLCK
    # 7       SEL_PCHG        0           Pre-charge working mode select
    # 8       ESPWM           0           ESPWM mode enable bit.
    #                                       (0 = enabled, 1 = disabled)
    # 9       LGSE3           0           Compensation for Blue LED.
    #                                       (0 = disabled, 1 = enabled)
    # 10      SEL_SCK_EDGE    0           SCLK edge select
    #                                       (0 = rising edge, 1 = both edges)
    # 11-13   LGSE1           000         Low Gray Scale Enhancement for
    #                                       Red/Green/Blue color
    # 14-22   CCB             100000000   Color brightness control data Blue
    #                                       (000h-1FFh)
    # 23-31   CCG             100000000   Color brightness control data Green
    #                                       (000h-1FFh)
    # 32-40   CCR             100000000   Color brightness control data Red
    #                                       (000h-1FFh)
    # 41-43   BC              100         Global brightness control data
    #                                       (0h-7h)
    # 44      PokerTransMode  0           Poker trans mode enable bit.
    #                                       (0 = disabled, 1 = enabled)
    # 45-47   LGSE2           000         first line performance improvment

    ##########################################
    # class _GS_Value:
    #     # Internal decorator to simplify exposing each 16-bit LED PWM channel
    #     # These will get/set the appropriate bytes in the shift register with
    #     # the specified values.
    #
    #     def __init__(self, byte_offset):
    #         # Keep track of the byte within the shift register where this
    #         # 16-bit value starts.  Luckily these are all aligned on byte
    #         # boundaries.  Note the byte order is big endian (MSB first).
    #         self._byte_offset = byte_offset
    #
    #     def __get__(self, obj, obj_type):
    #         # Grab the 16-bit value at the offset for this channel.
    #         return (obj._buffer[self._byte_offset] << 8) | \
    #                 obj._buffer[self._byte_offset+1]
    #
    #     def __set__(self, obj, val):
    #         # Set the 16-bit value at the offset for this channel.
    #         assert 0 <= val <= 65535
    #         obj._buffer[self._byte_offset] = (val >> 8) & 0xFF
    #         obj._buffer[self._byte_offset+1] = val & 0xFF

    ##########################################

    def __init__(self, spi, latch, gsclk, pixel_count=1):
        """Init."""
        self._spi = spi
        self._latch = latch
        self._gsclk = gsclk
        # how many pixels are there?
        self.pixel_count = pixel_count
        # calculate how many chips are connected
        self.chip_count = self.pixel_count // 16

        # This device is just a big 48 byte long shift register
        # without any fancy update protocol.
        # Blast out all the bits to update, that's it!
        # create raw output data
        self._buffer = bytearray(
            self.CHIP_BUFFER_BYTE_COUNT * self.chip_count)
        # self._buffer = _GS_Value

    def _write_buffer(self):
        # Write out the current state to the shift register.

        buffer_start = 0
        write_count = (self.CHIP_BUFFER_BYTE_COUNT * self.chip_count) - 2

        for index in range(self.CHIP_LED_COUNT):
            try:
                # wait untill we have access to / locked SPI bus
                while not self._spi.try_lock():
                    pass
                # configure
                self._spi.configure(
                    baudrate=(1 * 1000000), polarity=0, phase=0)
                # write data
                self._spi.write(self._buffer, buffer_start, write_count)
            finally:
                # Ensure the SPI bus is unlocked.
                self._spi.unlock()
            buffer_start += write_count
            # special
            if (index == self.CHIP_LED_COUNT-1):
                self._write_buffer_with_function_command(
                    self.function_command.LATGS, buffer_start)
            else:
                self._write_buffer_with_function_command(
                    self.function_command.WRTGS, buffer_start)
            buffer_start += 2

    def _write_buffer_with_function_command(
        self,
        function_command,
        buffer_start
    ):
        """Bit-Banging SPI write to sync latch pulse."""
        value = (
            (self._buffer[buffer_start + 0] << 8) |
            self._buffer[buffer_start + 1]
        )

        self._spi.clock.value = 0
        self._spi.MOSI.value = 0
        self._latch.value = 0
        for value in range(self.CHIP_LED_COUNT):
            if ((self.CHIP_LED_COUNT - function_command) == value):
                self._latch.value = 1

            # b1000000000000000
            if (value & 0x8000):
                self._spi.MOSI.value = 1
            else:
                self._spi.MOSI.value = 0
            value <<= 1

            self._spi.clock.value = 1
            # 10us
            time.sleep(0.00001)
            self._spi.clock.value = 0

        self._latch.value = 0

    def show(self):
        """Write out Grayscale Values to chips."""
        self._write_buffer()

    # def start_grayscale()(self):
    #     self._gsclk

    # # Define properties for global brightness control channels.
    # @property
    # def red_brightness(self):
    #     """
    #     Red brightness for all channels on all chips.
    #
    #     This is a 7-bit value from 0-127.
    #     """
    #     return self._bcr
    #
    # @red_brightness.setter
    # def red_brightness(self, val):
    #     assert 0 <= val <= 127
    #     self._bcr = val
    #     if self.auto_show:
    #         self._write()
    #
    # @property
    # def green_brightness(self):
    #     """
    #     Green brightness for all channels on all chips.
    #
    #     This is a 7-bit value from 0-127.
    #     """
    #     return self._bcg
    #
    # @green_brightness.setter
    # def green_brightness(self, val):
    #     assert 0 <= val <= 127
    #     self._bcg = val
    #     if self.auto_show:
    #         self._write()
    #
    # @property
    # def blue_brightness(self):
    #     """
    #     Blue brightness for all channels on all chips.
    #
    #     This is a 7-bit value from 0-127.
    #     """
    #     return self._bcb
    #
    # @blue_brightness.setter
    # def blue_brightness(self, val):
    #     assert 0 <= val <= 127
    #     self._bcb = val
    #     if self.auto_show:
    #         self._write()

    def _get_16bit_value_from_buffer(self, buffer_start):
        return (
            (self._buffer[buffer_start + 0] << 8) |
            self._buffer[buffer_start + 1]
        )

    def _set_16bit_value_in_buffer(self, buffer_start, value):
        assert 0 <= value <= 65535
        self._buffer[buffer_start + 0] = (value >> 8) & 0xFF
        self._buffer[buffer_start + 1] = value & 0xFF

    # Define index and length properties to set and get each channel as
    # atomic RGB tuples.  This provides a similar feel as using neopixels.
    def __len__(self):
        """Retrieve TLC5975the total number of Pixels available."""
        return self.pixel_count

    def __getitem__(self, key):
        """
        Retrieve the R, G, B values for the provided channel as a 3-tuple.

        Each value is a 16-bit number from 0-65535.
        """
        if 0 < key > (self.pixel_count-1):
            return (
                self._get_16bit_value_from_buffer(key + 0),
                self._get_16bit_value_from_buffer(key + 2),
                self._get_16bit_value_from_buffer(key + 4)
            )
        else:
            raise IndexError

    def __setitem__(self, key, value):
        """
        Set the R, G, B values for the provided channel.

        Specify a 3-tuple of R, G, B values that are each 16-bit numbers
        (0-65535).
        """
        if 0 < key > (self.pixel_count-1):
            assert len(value) == 3
            if isinstance(value[0], float):
                # check if values are in range
                assert 0 <= value[0] <= 1
                assert 0 <= value[1] <= 1
                assert 0 <= value[2] <= 1
                # convert to 16bit value
                value = (
                    int(value[0] * 65535),
                    int(value[1] * 65535),
                    int(value[2] * 65535)
                )
            # check if values are in range
            assert 0 <= value[0] <= 65535
            assert 0 <= value[1] <= 65535
            assert 0 <= value[2] <= 65535
            # update buffer
            self._set_16bit_value_in_buffer(key + 0, value[0])
            self._set_16bit_value_in_buffer(key + 2, value[1])
            self._set_16bit_value_in_buffer(key + 4, value[2])
        else:
            raise IndexError

##########################################
