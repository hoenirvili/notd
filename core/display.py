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

class Display:
    def __init__(self, arguments=None):
        if arguments == None:
            raise ValueError("Invalid arguments passed")

        self._number = arguments['number']
        self._transistor = arguments['config']['transistor']
        self._led = arguments['config']['led']
        self._gpio = arguments['config']['gpio']
        self._green = arguments['green']
        self._red = arguments['red']
        self._on = True

    def _handler(self, signum, frame):
        self._on = False
        
    def run(self):
        signal.signal(signal.SIGINT, self._handler)

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

        # set all gpio anode pins to low
        for _, value in self._gpio.items():
            GPIO.setup(value, GPIO.OUT, initial=GPIO.LOW)
        # set all base transistor pins to low
        GPIO.setup(self._transistor, GPIO.OUT, initial=GPIO.LOW)
        # set all anode pin leds to low
        GPIO.setup((self._led["green"], self._led["red"]), GPIO.OUT, initial=GPIO.LOW)

        # extract every digit and make a list out of them
        nums = list()
        a = self._number
        while a != 0:
             nums.append(a % 10)
             a = int(a / 10)
        
        # extract all gpio 4 digit letter pins and
        # make a tuple out of them to be feed up
        # to the GPIO.output
        pins = (self._gpio["A"], 
            self._gpio["B"], 
            self._gpio["C"], 
            self._gpio["D"], 
            self._gpio["E"], 
            self._gpio["F"], 
            self._gpio["G"], 
            self._gpio["DP"])

        # choose what led to light up first
        name = "green"
        if self._red == True:
            name = "red"
        GPIO.output(self._led[name], GPIO.HIGH)
        sleep(1)
        GPIO.output(self._led[name], GPIO.LOW)
        
        n = len(nums)
        while self._on:
            for i in range(n):
                GPIO.output(pins, digits[nums[i]])
                GPIO.output(self._transistor, bases[i])
                sleep(.001)
        
    def clean(self):
        GPIO.cleanup()
