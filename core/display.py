#!/usr/bin/python3

import signal
import RPi.GPIO as GPIO
from time import sleep

digits = {
    0: (1,1,1,1,1,1,0,0),
    1: (0,1,1,0,0,0,0,0),
    2: (1,1,0,1,1,0,1,0),
    3: (1,1,1,1,0,0,1,0),
    4: (0,1,1,0,0,1,1,0),
    5: (1,0,1,1,0,1,1,0),
    6: (1,0,1,1,1,1,1,0),
    7: (1,1,1,0,0,0,0,0),
    8: (1,1,1,1,1,1,1,0),
    9: (1,1,1,1,0,1,1,0)
}

bases = {
    0: (0, 0, 0, 1),
    1: (0, 0, 1, 0),
    2: (0, 1, 0, 0),
    3: (1, 0, 0, 0),
}

time = 0.001

class Display:
    def __init__(self, arguments=None):
        if arguments == None:
            return

        self.number = arguments['number']
        self.transistor = arguments['config']['transistor']
        self.led = arguments['config']['led']
        self.gpio = arguments['config']['gpio']
        self.green = arguments['green']
        self.red = arguments['red']
    def run(self):
        # Pin numbers on the P1 header of the Raspberry Pi board. 
        # The advantage of using this numbering system is that your 
        # hardware will always work, regardless of the board revision of the RPi.
        GPIO.setmode(GPIO.BOARD)
        # It is possible that you have more than one script/circuit 
        # on the GPIO of your Raspberry Pi. As a result of this, 
        # if RPi.GPIO detects that a pin has been configured 
        # to something other than the default (input), you get a 
        # warning when you try to configure a script. 
        GPIO.setwarnings(False)

        # setup all pins to low
        for _, value in self.gpio.items():
            GPIO.setup(value, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.transistor, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup((self.led["green"], self.led["red"]), GPIO.OUT, initial=GPIO.LOW)

        # extract every digit
        nums = list()
        a = self.number
        while a != 0:
             nums.append(a % 10)
             a = int(a / 10)
        n = len(nums)
        
        pins = (self.gpio["A"], 
            self.gpio["B"], 
            self.gpio["C"], 
            self.gpio["D"], 
            self.gpio["E"], 
            self.gpio["F"], 
            self.gpio["G"], 
            self.gpio["DP"])

        # choose what led to light up first
        name = "green"
        if self.red == True:
            name = "red"
        GPIO.output(self.led[name], GPIO.HIGH)
        sleep(1)
        GPIO.output(self.led[name], GPIO.LOW)
        
        for k in range(1000): # TODO(hoenir) remove this 
            # led the digits in order from left to right on the display
            for i in range(n): # for every digit we have
                GPIO.output(pins, digits[nums[i]]) # pins -> row combination
                GPIO.output(self.transistor, bases[i]) # base pin transistors -> combination
                sleep(.001) # sleep for 1 second

    def clean(self):
        GPIO.cleanup()
