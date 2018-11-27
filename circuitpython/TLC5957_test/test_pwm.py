"""Test for PWM frequency."""
import time

import board
import pulseio

##########################################
print(42 * '*')
print("test for pwm")

# on the ItsyBitsy M4 EXPRESS on pin D9 the maximum frequency is about 6MHz?!
freqency = (6000 * 1000)  # 6MHz
pwm = pulseio.PWMOut(
    board.D9, duty_cycle=(2 ** 15), frequency=freqency)
print("gsclk.frequency: {:}MHz".format(pwm.frequency / (1000*1000)))

##########################################
# main loop
print(42 * '*')
print("loop")
while True:
    time.sleep(10)
    print(time)
