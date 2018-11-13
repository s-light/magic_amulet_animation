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
# Define SPI bus connected to chip.
spi = busio.SPI(board.SCK, MOSI=board.MOSI)

# Define array with TLC5971 chips
num_leds = 32
pixels = [
    adafruit_tlc59711.TLC59711(spi, auto_show=False)
    for count in range(num_leds // 4)
]

# pixels = []
# for i in range(num_leds % 4):
#     pixels.append(adafruit_tlc59711.TLC59711(spi, auto_show=False))


##########################################


def map_01_to_16bit(color):
    """Map range 0..1 to 16bit 0..65535."""
    return (
        int(color.red*65535),
        int(color.green*65535),
        int(color.blue*65535)
    )


def pixels_show():
    """Call show on every pixel."""
    for i in range(num_leds // 4):
        pixels[i].show()


##########################################

# Declare a 6-element RGB rainbow palette
palette = [
    fancy.CRGB(1.0, 0.0, 0.0),  # Red
    fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
    fancy.CRGB(0.0, 1.0, 0.0),  # Green
    fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
    fancy.CRGB(0.0, 0.0, 1.0),  # Blue
    fancy.CRGB(0.5, 0.0, 0.5),  # Magenta
]

offset = 0  # Positional offset into color palette to get it to 'spin'

while True:
    for i in range(num_leds):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancy.palette_lookup(palette, offset + i / num_leds)
        # color = fancy.gamma_adjust(color, brightness=0.25)
        # print("{index:>2} : {div:>2} | {mod:>2}".format(
        #     index=i,
        #     div=i // 4,
        #     mod=i % 4
        # ))
        pixels[i // 4][i % 4] = map_01_to_16bit(color)
    # pixels_show()
    pixels[0].show()

    offset += 0.001  # Bigger number = faster spin


##########################################
# the end
