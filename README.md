# Next Clip Launcher

This is a control surface script for Ableton 10 written in Python 2.

The goal of this script is to allow the user to launch the next clip of a track
(in session view) but only after the playing clip finishes completely.
It does this by firing the next clip at the right moment considering the 
global clip launch quantization.

This single functionality that can be triggered by sending
a Note On message (currently Note 0 (C-2) on midi channel 2).
