# Kalictric
Kalictric is a kalimba equipped with a capacitive touch sensor, which transforms it into a kalimba learning tool, a composition creator and countless other things, such as a gamepad that can be used to play *Tetris* and *Minecraft*.

## Getting Started
Building Kalictric requires:
* Raspberry Pi
* MPR121 Capacitive Touch Sensor and Kalimba setup

Steps for running Kalictric:
1. Wire up the capacitive touch sensor to the Raspberry Pi. 
2. Kalictric requires TiMidity++ to play MIDI files. To install TiMidity++, run `sudo apt-get install timidity` in the Raspberry Pi terminal.
3. Run `python klaunch.py` to launch Kalictric's homescreen.
