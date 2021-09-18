# **************************************************
# https://github.com/galopago
# A very simple example of RPI Pico HID USB keyboard emulator
# configurable via text file

import time
import board
import digitalio
import usb_hid
import os
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

# *************************************
# config file format structure:
# very crude!, do not include empty lines nor comments!
# first line: GPIO used
# second line: keycodes
# third line: modifiers
# *************************************
# key code names: https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html
# in this example the switch connected to GP18 emulates TAB+LEFT_ALT, and the switch connected to GP19 emulates SPACE
# wrote the lines below in keys.conf file! (remove # in the file!)

#board.GP18,board.GP19
#Keycode.TAB,Keycode.SPACE
#Keycode.LEFT_ALT,None


keys_conf_file="keys.conf"

# Pins, key code, and key modifier.
default_gpio      = [board.GP18,board.GP19]
default_keys      = [Keycode.TAB,Keycode.SPACE]
default_mod_keys  = [Keycode.LEFT_ALT,None]

# Array of key objects
key_pin_array = []
key_pin_array_debounced = []


# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # US keyboard used

print("Reading config keys file...")
flist=os.listdir()

print("Debug",board.GP18)
strconfig = "board.GP17"
iotest = digitalio.DigitalInOut(eval(strconfig))

if keys_conf_file in flist:
	print("config file found!:",keys_conf_file)
	# ****** TODO some sanity checks!!! *******	
	fp = open(keys_conf_file,'r')
	
	# reading GPIO config line
	fline = fp.readline().rstrip('\n')	
	spfline = fline.split(',')
	keypress_pins=[]
	for gpiopin in spfline:		
		keypress_pins.append(eval(gpiopin))
	# reading KEYS config line
	fline = fp.readline().rstrip('\n')	
	spfline = fline.split(',')
	keys_pressed=[]
	for keycode in spfline:		
		keys_pressed.append(eval(keycode))
	# reading MODIF KEY config line	
	fline = fp.readline().rstrip('\n')	
	spfline = fline.split(',')
	control_key=[]
	for modifkey in spfline:		
		control_key.append(eval(modifkey))
	
	fp.close()
	
else:
	print("config file not found, loading defaults!")
	keypress_pins = default_gpio
	keys_pressed  = default_keys
	control_key   = default_mod_keys

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.direction = digitalio.Direction.OUTPUT

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)
    key_pin_array_debounced.append(Debouncer(key_pin))
	
for key_conf in keypress_pins: 
	j = keypress_pins.index(key_conf)	
	print("GPIO,key,modifier:", keypress_pins[j], keys_pressed[j],control_key[j])
	
print("Waiting for switches...")

while True:
    # Check each pin
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
