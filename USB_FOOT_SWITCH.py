"""CircuitPython Essentials HID Keyboard example"""
import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

# A simple neat keyboard demo in CircuitPython

# The pins we'll use, each will have an internal pullup
keypress_pins = [board.GP18, board.GP19]
# Our array of key objects
key_pin_array = []
key_pin_array_debounced = []
# The Keycode sent for each button, will be paired with a control key
keys_pressed = [Keycode.TAB, Keycode.SPACE]
#keys_pressed = [Keycode.TAB, "ABCDE"]
control_key = [Keycode.LEFT_ALT,None]

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)
    key_pin_array_debounced.append(Debouncer(key_pin))

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.direction = digitalio.Direction.OUTPUT

print("Waiting for key pin...")

while True:
    # Check each pin
#    for key_pin in key_pin_array:
	for key_pin_debounced in key_pin_array_debounced:    
		key_pin_debounced.update()
		i = key_pin_array_debounced.index(key_pin_debounced)

    	
		if key_pin_debounced.fell:
			print("Switch pressed.")
			led.value = True
			key = keys_pressed[i]  # Get the corresponding Keycode or string
			mod_key = control_key[i]
			#control_key = control_key[i]  # Get the corresponding Keycode or string
			if isinstance(key, str):  # If it's a string...
				keyboard_layout.write(key)  # ...Print the string
			else:  # If it's not a string...
				if control_key[i] == None:
					keyboard.press(key)  # "Single Key"
				else:		
					keyboard.press(mod_key, key)  # "Key with modifier"...
        
		if key_pin_debounced.rose:
			print("Switch released")
			led.value = False
			keyboard.release_all()  # ..."Release"!
    	

	time.sleep(0.01)
