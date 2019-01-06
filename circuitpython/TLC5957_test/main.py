"""Magic Amulet Animation."""

__doc__ = """
Magic Amulet Animation.

ported from / based on animation.ino
Enjoy the colors :-)

TODO: port it :-)
"""

import time

# import board

import adafruit_fancyled.adafruit_fancyled as fancyled
import animation


##########################################
print(
    "\n" +
    (42 * '*') + "\n" +
    __doc__ + "\n" +
    (42 * '*') + "\n" +
    "\n"
)

##########################################
# helper function


##########################################
# function


##########################################
# main

def main_setup():
    """Setup."""
    print(42 * '*')
    # time.sleep(0.5)
    # animation.pmap.print_mapping()

    animation.pixels.set_pixel_all_16bit_value(1, 1, 1)
    # animation.pixels.set_pixel_all_16bit_value(100, 100, 100)
    # animation.pixels.show()
    # animation.wait_with_print(1)
    animation.pixels_init_BCData()
    animation.pixels.show()
    # animation.wait_with_print(1)


def main_loop():
    """Loop."""
    # myIRHelper.check()
    animation.animation_helper.main_loop()
    # myIRHelper.check()
    # time.sleep(0.1)


if __name__ == '__main__':
    # print(42 * '*')
    print("setup")
    main_setup()
    print(42 * '*')
    print("loop")
    while True:
        main_loop()
