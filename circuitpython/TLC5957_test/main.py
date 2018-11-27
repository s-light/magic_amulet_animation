"""Magic Amulet Animation."""

__doc__ = """
Magic Amulet Animation.

ported from / based on animation.ino
Enjoy the colors :-)

TODO: port it :-)
"""

import board

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


# Positional offset into color palette to get it to 'spin'
offset = 0

##########################################
# main loop
print(42 * '*')
print("rainbow loop")
while True:
    for i in range(animation.num_leds):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancyled.palette_lookup(
            animation.palette, offset + i / animation.num_leds)
        color = fancyled.gamma_adjust(color, brightness=0.01)
        animation.pixels[i] = color
    animation.pixels.show()

    offset += 0.01  # Bigger number = faster spin
