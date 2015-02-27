#!/usr/bin/env python

# TM1638 playground

import TM1638
import time

# These are the pins the display is connected to. Adjust accordingly.
# In addition to these you need to connect to 5V and ground.

DIO = 17
CLK = 21
STB = 22

display = TM1638.TM1638(DIO, CLK, STB)

display.enable(1)



display.send_char(0, 0b00111111)
display.send_char(1, 0b00000110)
display.send_char(2, 0b01011011)
display.send_char(3, 0b01001111)
display.send_char(4, display.FONT['4'])
display.send_char(5, display.FONT['C'])
display.send_char(6, 0b01000000)
display.send_char(7, 0b10000000)
display.set_text("tug12345")
display.set_text("123.4532")
display.set_text("1235.0")
display.set_text(".2350")
#display.set_led(0,0)
#isplay.set_led(1,1)
#display.set_led(2,2)
display.set_text(" ")

