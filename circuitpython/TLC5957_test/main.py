"""Magic Amulet Animation."""

__doc__ = """
Magic Amulet Animation.

ported from / based on animation.ino
Enjoy the colors :-)
"""

import board
import pulseio


##########################################
print(
    "\n" +
    (42 * '*') + "\n" +
    __doc__ + "\n" +
    (42 * '*') + "\n" +
    "\n"
)

##########################################
print(42 * '*')
print("test for pwm")

# on the ItsyBitsy M4 EXPRESS on pin D9 the maximum frequency is about 6MHz?!
gsclk_freqency = (6000 * 1000)  # 6MHz
gsclk = pulseio.PWMOut(
    board.D9, duty_cycle=(2 ** 15), frequency=gsclk_freqency)
print("gsclk.frequency: {:}MHz".format(gsclk.frequency / (1000*1000)))

##########################################
# helper function


# Positional offset into color palette to get it to 'spin'
offset = 0

##########################################
# main loop
print(42 * '*')
print("rainbow loop")
while True:
    for i in range(num_leds):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancyled.palette_lookup(palette, offset + i / num_leds)
        color = fancyled.gamma_adjust(color, brightness=0.01)
        pixels[i] = color
    pixels.show()

    offset += 0.01  # Bigger number = faster spin
