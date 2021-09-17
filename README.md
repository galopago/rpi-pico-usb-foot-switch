# USB FOOT SWITCH BASED ON RPI PICO

USB Foot switch based on Rpi Pico. Configurable via text file, can emulate keystrokes and combination of keys!

![DIN-RAIL](docs/footswitch.png)

![PIECES](docs/footswitchopen.png)

Read this in other languages: [Español](docs/README.es.md)

## Directory structure

* The root folder contains circuit python program and config file
* utils directory contains binary files
* lib directory contains additional circuit python libraries
* docs additional files

## How to use this repository

The project is developed in CircuitPython V6.3
* Plug a Micro USB to USB cable to the RPI Pico (Don't plug into the computer yet).
* Press bootsel button and keep pressed, then plug the RPI Pico into an USB port, when plugged release bootsel button.
* RPI Pico should appear as an USB drive in your OS desktop.(named Pi RP2 Boot)
* Copy Circuit Python installer from the utils directory to the USB drive 
* Copy the contents of lib directory to the lib directory of the USB drive 
* Copy keys.conf file to the root folder of the USB drive 
* Copy code.py file to the root folder of the USB drive (overwrite)
* Unplug and Plug again



## License
[![CC-BY](https://i.creativecommons.org/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

This is an Open Hardware project an is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
