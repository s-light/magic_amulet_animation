"""Test for PWM frequency."""
import time

import board
import pulseio

##########################################
print(42 * '*')
print("test for pwm")

# maximum frequency is currently hardcoded to 6MHz
# https://github.com/adafruit/circuitpython/blob/master/ports/atmel-samd/common-hal/pulseio/PWMOut.c#L119
pwm = pulseio.PWMOut(board.D9, duty_cycle=(2 ** 15), frequency=(6000 * 1000))
# freqency = (6000 * 1000)  # 6MHz
# pwm = pulseio.PWMOut(
#     board.D9, duty_cycle=(2 ** 15), frequency=freqency)
print("gsclk.frequency: {:}MHz".format(pwm.frequency / (1000*1000)))

##########################################
# main loop
print(42 * '*')
print("loop")
while True:
    time.sleep(10)
    print(time)

#
# ```
# Adafruit CircuitPython 3.1.1 on 2018-11-02; Adafruit ItsyBitsy M4 Express with samd51g19
# >>> import board
# >>> import pulseio
# >>> pwm = pulseio.PWMOut(board.D9, duty_cycle=(2 ** 15), frequency=(6001 * 1000))
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ValueError: Invalid PWM frequency
# ```
#
# ```
# Adafruit CircuitPython 3.1.1 on 2018-11-02; Adafruit ItsyBitsy M4 Express with samd51g19
# >>> import board
# >>> import pulseio
# >>> pwm = pulseio.PWMOut(board.D9, duty_cycle=(2 ** 15), frequency=(6000 * 1000))
# >>> pwm.frequency
# 6000000
# >>>
# ```
