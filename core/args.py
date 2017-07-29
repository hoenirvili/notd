#!/usr/bin/python3

import argparse
import json

DESCRIPTION = 'Notify with a blinking LED and display a number for the 4 digit 7 segment led'
PROG ='notd'

class Arguments:
    def __init__(self, argv=None):

        if argv == None:
            raise argparse.ArgumentError(argument=None,
                    message='Please provide a non empty command line argument list')

        self._argv = argv[1:]

    def parse(self):
        return self._parse()

    def _parse(self):
        parser = argparse.ArgumentParser(prog = PROG, description = DESCRIPTION)
        group = parser.add_mutually_exclusive_group()
        parser.add_argument('-n',
                type=int, 
                dest='number',
                help='an integer to be displayed')
        parser.add_argument('-c', 
                '--config',
                dest='config',
                type=argparse.FileType('r'), 
                default='settings.json',
                help='custom gpio pin json settings file')
        group.add_argument('-r', 
                '--red',
                help='light up the red led', 
                action='store_true', 
                default=False)
        group.add_argument('-g', 
                '--green',
                help='light up the green led',
                action='store_true', 
                default=False)
        
        options = vars(parser.parse_args(self._argv))
        try:
            self._valid_number(options['number'])
            self._valid_leds(options['red'], options['green'])
            data = self._valid_config(options['config'])
            if data != None:
                options['config'] = data
        except argparse.ArgumentError as e:
            print(e)
            return None 

        return options

    def _valid_number(self, n):
        if n == None:
            return

        if n < 0 or n > 9999:
            raise argparse.ArgumentError(argument=None,
                    message='Invalid number, only 4 digit number are supported')

    def _valid_config(self, c):
        if c == None:
            return

        data = None
        try:
            data = json.load(c)
        except json.JSONDecodeError as e:
            raise argparse.ArgumentError(argument = None,
                    message = "Empty or invalid file provided as gpio settings, please specify one or restore the default")

        try:
            c.close()
        except ValueError as e:
            raise argparse.ArgumentError(argument=None,
                    message='Can\'t close the file')

        return data

    def _valid_leds(self, red, green):
        if red == False and green == False:
            raise argparse.ArgumentError(argument = None,
                    message = 'Please pass the led to light up')
