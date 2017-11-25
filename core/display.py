#!/usr/bin/python3

import json
import time

import click

import RPi.GPIO as GPIO

__all__ = ['Display']


def info(message, debug):
    """
    info will display debug messages
    """
    if debug:
        click.echo(message)


class Display(object):
    __config = {
        "gpio": {
            "A": 7,
            "B": 11,
            "C": 12,
            "D": 13,
            "E": 15,
            "F": 16,
            "G": 18,
            "DP": 22
        },
        "transistor": [31, 33, 35, 37],
        "led": {
            "red": 38,
            "green": 40
        }
    }

    __digits = {
        0: (1, 1, 1, 1, 1, 1, 0, 0),
        1: (0, 1, 1, 0, 0, 0, 0, 0),
        2: (1, 1, 0, 1, 1, 0, 1, 0),
        3: (1, 1, 1, 1, 0, 0, 1, 0),
        4: (0, 1, 1, 0, 0, 1, 1, 0),
        5: (1, 0, 1, 1, 0, 1, 1, 0),
        6: (1, 0, 1, 1, 1, 1, 1, 0),
        7: (1, 1, 1, 0, 0, 0, 0, 0),
        8: (1, 1, 1, 1, 1, 1, 1, 0),
        9: (1, 1, 1, 1, 0, 1, 1, 0)
    }

    __bases = {
        0: (0, 0, 0, 1),
        1: (0, 0, 1, 0),
        2: (0, 1, 0, 0),
        3: (1, 0, 0, 0),
    }

    MAX_DISPLAY_VALUE = 9999

    def __init__(self,
                 number,
                 *,
                 config_path='',
                 red=False,
                 green=False,
                 debug=False):
        if not isinstance(
                number, int) or number < 0 or number > self.MAX_DISPLAY_VALUE:
            raise TypeError('Invalid number param given')

        self._number = number
        if config_path != '':
            self.__config = json.JSONDecoder().decode(config_path)

        self._red = red
        self._green = green
        self._debug = debug
        self._knob = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def turn_knob(self):
        if self._knob:
            self._knob = False
        else:
            self._knob = True

    def open(self):
        info("[*] Using the pi library RPi.GPIO version {}".format(
            GPIO.VERSION), self._debug)
        info("[*] Using the raspberry {}".format(GPIO.RPI_INFO['TYPE']),
             self._debug)

        # Pin numbers on the P1 header of the Raspberry Pi board.
        # The advantage of using this numbering system is that your
        # hardware will always work, regardless of the board revision of the
        # RPi.
        GPIO.setmode(GPIO.BOARD)
        # It is possible that you have more than one script/circuit
        # on the GPIO of your Raspberry Pi. As a result of this,
        # if RPi.GPIO detects that a pin has been configured
        # to something other than the default (input), you get a
        # warning when you try to configure a script.
        GPIO.setwarnings(False)

        info("[*] Set all gpio pins to low", self._debug)
        # set all gpio anode pins to low
        gpio = self.__config['gpio']
        for _, value in gpio.items():
            GPIO.setup(value, GPIO.OUT, initial=GPIO.LOW)

        led = self.__config['led']
        transistor = self.__config['transistor']

        info("[*] Set all base transitors pins to low", self._debug)
        GPIO.setup(transistor, GPIO.OUT, initial=GPIO.LOW)
        info("[*] Set all anode led pins to low", self._debug)
        GPIO.setup((led["green"], led["red"]), GPIO.OUT, initial=GPIO.LOW)

        # extract every digit and make a list out of them in the reverse order
        nums = list(map(int, "%02d" % self._number))[::-1]

        # extract all gpio 4 digit letter pins and
        # make a tuple out of them to be feed up
        # to the GPIO.output
        pins = (gpio["A"], gpio["B"], gpio["C"], gpio["D"], gpio["E"],
                gpio["F"], gpio["G"], gpio["DP"])

        # choose what led to light up first
        name = "green"
        if self._red:
            name = "red"

        GPIO.output(led[name], GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led[name], GPIO.LOW)
        n = len(nums)
        while self._knob is True:
            for i in range(n):
                GPIO.output(pins, self.__digits[nums[i]])
                GPIO.output(transistor, self.__bases[i])
                time.sleep(0.001)

    def close(self):
        info("[*] Cleaning gpio pins", self._debug)
        GPIO.cleanup()
