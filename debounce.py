# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=invalid-name

import board
import digitalio
from adafruit_debouncer import Debouncer

pin = digitalio.DigitalInOut(board.GP18)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

switch = Debouncer(pin)

while True:
    switch.update()
    if switch.fell:
        print("Just pressed")
        led.value = True
        
    if switch.rose:
        print("Just released")
        led.value = False
