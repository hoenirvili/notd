#!/usr/bin/python3

import argparse
import json 

DESCRIPTION = 'Notify with a blinking LED and display a number for the 4 digit 7 segment led'
PROG ='notd'

errInvalidJson = argparse.ArgumentError(argument=None, message='Invalid json configuration')

class Arguments:
    def __init__(self, argv=None):
        if argv == None:
            raise argparse.ArgumentError(argument=None,
                    message='Please provide a non empty command line argument list')

        self._argv = argv[1:]

    def parse(self):
        if len(self._argv) == 1:
            return None

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
            self._validate_number(options['number'])
            self._valid_leds(options['red'], options['green'])
            options['config'] = self._validate_config_decorate(options['config'])

        except argparse.ArgumentError as e:
            print(e)
            return None 

        return options

    def _validate_number(self, n):
        if n == None:
             raise argparse.ArgumentError(argument=None,
                    message='Empty number passed')

        if n < 0 or n > 9999:
            raise argparse.ArgumentError(argument=None,
                    message='Invalid number, only 4 digit numbers are supported')

    def _validate_config_decorate(self, c):

        if c == None:
            raise argparse.ArgumentError(argument=None,
                    message='Empty configuration passed')

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
        
        if all(k in data for k in ("gpio_conf", "transistor_conf", "led_conf")) == False:
            raise errInvalidJson
            
        anodes = 8
        n = 0
        for gpio in data['gpio_conf']:
            n = n+1 
            if gpio['led'] == '' or gpio['pin'] == 0:
                raise errInvalidJson

        if n != anodes:
            raise errInvalidJson

        bases = 4
        n = 0
        for base in data['transistor_conf']:
            n = n+1
            if base['digit'] == '' or base['pin'] == 0:
                raise errInvalidJson

        if n != bases:
            raise errInvalidJson

        leds = 2
        n = 0
        for led in data['led_conf']:
            n = n+1
            if led['led'] != 'red' and  led['led'] != 'green' or led['pin'] == 0:
                raise errInvalidJson

        if n != leds:
            raise errInvalidJson 


        return data

    def _valid_leds(self, red, green):
        if red == False and green == False:
            raise errInvalidJson
