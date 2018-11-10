#!CircuitPython
# coding=utf-8

"""
Magic Amulet Animation.

first try to port arduino FastLED code to CircuitPython.
in this first test we use the TLC5971 boards as output.
(see [LEDBoard_4x4_16bit](https://github.com/s-light/LEDBoard_4x4_16bit)
for the aktuall hardware used..)
"""

__doc__ = """
Magic Amulet Animation.

first try to port arduino FastLED code to CircuitPython.
"""


##########################################
import board
import busio

import adafruit_tlc59711
import adafruit_fancyled.adafruit_fancyled as fancy


##########################################
print(
    "\n" +
    (42 * '*') + "\n" +
    __doc__ + "\n" +
    (42 * '*') + "\n" +
    "\n"
)


##########################################
# Define SPI bus connected to chip.  You only need the clock and MOSI (output)
# line to use this chip.
spi = busio.SPI(board.SCK, MOSI=board.MOSI)

# Define the TLC59711 instance.
leds = adafruit_tlc59711.TLC59711(spi, auto_show=False)

num_leds = 20
pixels = [
    adafruit_tlc59711.TLC59711(spi, auto_show=False)
    for count in range(num_leds % 4)
]

# pixels = []
# for i in range(num_leds % 4):
#     pixels.append(adafruit_tlc59711.TLC59711(spi, auto_show=False))


##########################################
# There are a couple ways to control the channels of the chip.
# The first is using an interface like a strip of NeoPixels.  Index into the
# class for the channel and set or get its R, G, B tuple value.  Note the
# component values are 16-bit numbers that range from 0-65535 (off to full
# brightness).  Remember there are only 4 channels available too (0 to 3).
# For example set channel 0 (R0, G0, B0) to half brightness:
leds[0] = (0, 65535, 1000)
leds[1] = (1, 0, 0)
leds[2] = (0, 1, 0)
leds[3] = (0, 0, 1)

leds.show()
leds[0] = (0, 1000, 1000)


leds.show()
leds.show()
leds.show()
leds.show()

leds.show()
leds.show()
leds.show()
leds.show()

leds.show()
leds.show()
leds.show()
leds.show()

leds.show()
leds.show()
leds.show()
leds.show()


##########################################


def map_01_to_16bit(color):
    """Map range 0..1 to 16bit 0..65535."""
    return (
        int(color.red*65535),
        int(color.green*65535),
        int(color.blue*65535))


##########################################

# Declare a 6-element RGB rainbow palette
palette = [fancy.CRGB(1.0, 0.0, 0.0),  # Red
           fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
           fancy.CRGB(0.0, 1.0, 0.0),  # Green
           fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
           fancy.CRGB(0.0, 0.0, 1.0),  # Blue
           fancy.CRGB(0.5, 0.0, 0.5)]  # Magenta

offset = 0  # Positional offset into color palette to get it to 'spin'

while True:
    for i in range(num_leds):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancy.palette_lookup(palette, offset + i / num_leds)
        color = fancy.gamma_adjust(color, brightness=0.25)
        # leds[i] = color.pack()
        # print(color)
        leds[i // 4][i % 4] = map_01_to_16bit(color)
    leds.show()

    offset += 0.02  # Bigger number = faster spin


##########################################
# tests
# import adafruit_fancyled.adafruit_fancyled as fancy
# color = fancy.CRGB(1.0, 0.0, 0.0)
# (color.red*65535, color.green*65535, color.blue*65535)
