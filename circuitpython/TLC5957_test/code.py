#!CircuitPython
# coding=utf-8

"""
TLC5957 test

test to generate really basic TLC5975 protocoll
"""

__doc__ = """
TLC5957 test

test to generate really basic TLC5975 protocoll
"""


##########################################
import board
import busio
import pulseio
import digitalio

import circuitpython_TLC5957

import adafruit_fancyled.adafruit_fancyled as fancyled

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

gsclk = pulseio.PWMOut(
    board.D9, duty_cycle=(2 ** 15), frequency=(10 * 1000))

latch = digitalio.DigitalInOut(board.D7)
latch.direction = digitalio.Direction.OUTPUT
# spi_sck = digitalio.DigitalInOut(board.SCK)
# spi_sck.direction = digitalio.Direction.OUTPUT

# define pixel array
num_leds = 16
pixels = circuitpython_TLC5957.TLC5975(
    spi, latch, gsclk, num_leds)

# tlc.start_grayscale()


##########################################

##########################################

# Declare a 6-element RGB rainbow palette
palette = [
    fancyled.CRGB(1.0, 0.0, 0.0),  # Red
    fancyled.CRGB(0.5, 0.5, 0.0),  # Yellow
    fancyled.CRGB(0.0, 1.0, 0.0),  # Green
    fancyled.CRGB(0.0, 0.5, 0.5),  # Cyan
    fancyled.CRGB(0.0, 0.0, 1.0),  # Blue
    fancyled.CRGB(0.5, 0.0, 0.5),  # Magenta
]

offset = 0  # Positional offset into color palette to get it to 'spin'

while True:
    for i in range(num_leds):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancyled.palette_lookup(palette, offset + i / num_leds)
        # color = fancyled.gamma_adjust(color, brightness=0.25)
        # print("{index:>2} : {div:>2} | {mod:>2}".format(
        #     index=i,
        #     div=i // 4,
        #     mod=i % 4
        # ))
        pixels[i] = color
    pixels.show()

    offset += 0.001  # Bigger number = faster spin


##########################################
# the end
