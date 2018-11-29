"""TLC5957 & FancyLED."""

__doc__ = """
animation.py - TLC5957 & FancyLED & 2D Array / Mapping.

this is sub file for the magic amulet animation things.
it combines the TLC5957 library with FancyLED and 2D Array / Mapping.

Enjoy the colors :-)
"""

import board
# import busio
import bitbangio
import pulseio
import digitalio

import slight_tlc5957
import adafruit_fancyled.adafruit_fancyled as fancyled


##########################################
if __name__ == '__main__':
    print(
        "\n" +
        (42 * '*') + "\n" +
        __doc__ + "\n" +
        (42 * '*') + "\n" +
        "\n"
    )

##########################################
print(42 * '*')
print("initialise digitalio pins for SPI")
spi_clock = digitalio.DigitalInOut(board.SCK)
spi_clock.direction = digitalio.Direction.OUTPUT
spi_mosi = digitalio.DigitalInOut(board.MOSI)
spi_mosi.direction = digitalio.Direction.OUTPUT
spi_miso = digitalio.DigitalInOut(board.MISO)
spi_miso.direction = digitalio.Direction.INPUT

# print((42 * '*') + "\n" + "init busio.SPI")
# spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
print("init bitbangio.SPI")
spi = bitbangio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# on the ItsyBitsy M4 EXPRESS on pin D9 the maximum frequency is about 6MHz?!
gsclk_freqency = (6000 * 1000)  # 6MHz
gsclk = pulseio.PWMOut(
    board.D9, duty_cycle=(2 ** 15), frequency=gsclk_freqency)
print("gsclk.frequency: {:}MHz".format(gsclk.frequency / (1000*1000)))

latch = digitalio.DigitalInOut(board.D7)
latch.direction = digitalio.Direction.OUTPUT

##########################################
print(42 * '*')
print("define pixel array / init TLC5957")
rows = 4
cols = 4
num_leds = rows * cols
pixels = slight_tlc5957.TLC5957(
    spi=spi,
    latch=latch,
    gsclk=gsclk,
    spi_clock=spi_clock,
    spi_mosi=spi_mosi,
    spi_miso=spi_miso,
    pixel_count=num_leds)

pixel_map = [
    [15, 14, 13, 12],
    [11, 10,  9,  8],
    [7,   6,  5,  4],
    [3,   2,  1,  0],
]

print(
    "Pixels & Mapping:\n"
    "  rows           {rows:>2}\n"
    "  cols           {cols:>2}\n"
    "  pixel_count    {pixel_count:>2}\n"
    "  chip_count     {chip_count:>2}\n"
    "  channel_count  {channel_count:>2}\n"
    "".format(
        rows=rows,
        cols=cols,
        pixel_count=pixels.pixel_count,
        chip_count=pixels.chip_count,
        channel_count=pixels.channel_count,
    )
)


##########################################
# helper function

def map_range(x, in_min, in_max, out_min, out_max):
    """Map Value from one range to another."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_range_int(x, in_min, in_max, out_min, out_max):
    """Map Value from one range to another."""
    return int(
        (x - in_min) * (out_max - out_min)
        //
        (in_max - in_min) + out_min
    )


##########################################
# mapping function

def get_pixel_index_from_row_col(row, col):
    """Get pixel_index from row and column index."""
    pixel_index = pixel_map[row][col]
    return pixel_index


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


##########################################
# test functions

def test_set_corners_to_colors():
    """Test Function: Set all 4 corners to different collors."""
    print(42 * '*')
    print("set corners to colors")
    pixels[get_pixel_index_from_row_col(0, 0)] = (1.0, 0.5, 0.0)
    pixels[get_pixel_index_from_row_col(0, 3)] = (0.5, 0.0, 1.0)
    pixels[get_pixel_index_from_row_col(3, 0)] = (0.1, 0.5, 0.0)
    pixels[get_pixel_index_from_row_col(3, 3)] = (0.0, 0.5, 1.0)
    pixels.show()


def test_set_2d_colors():
    """Test Function: Set all LEDs to 2D color-range."""
    print("set color range")
    for x in range(cols):
        # xN = x / cols
        xN = map_range_int(x, 0, cols, 1, 100)
        for y in range(rows):
            # yN = y / rows
            yN = map_range_int(y, 0, rows, 1, 100)
            # print(
            #     "x: {:>2} xN: {:>2} "
            #     "y: {:>2} yN: {:>2} "
            #     "pixel_index: {:>2}".format(
            #         x, xN,
            #         y, yN,
            #         get_pixel_index_from_row_col(x, y)
            #     )
            # )
            pixels[get_pixel_index_from_row_col(x, y)] = (xN, yN, 0)

    pixels.show()


def test_loop_2d_colors():
    """Test Function: Set all LEDs to 2D color-range."""
    # Positional offset for blue part
    offset = 0
    print(42 * '*')
    print("loop")
    while True:
        offsetN = map_range_int(offset, 0.0, 1.0, 1, 200)
        for x in range(cols):
            xN = map_range_int(x, 0, cols, 1, 500)
            for y in range(rows):
                yN = map_range_int(y, 0, rows, 1, 500)
                pixels[get_pixel_index_from_row_col(x, y)] = (xN, yN, offsetN)
        pixels.show()
        offset += 0.01  # Bigger number = faster spin
        if offset > 1.0:
            offset = 0


def test_main():
    """Test Main."""
    import time

    test_set_corners_to_colors()
    time.sleep(10)
    test_set_2d_colors()
    time.sleep(10)
    test_loop_2d_colors()


##########################################
# main loop

if __name__ == '__main__':
    test_main()
