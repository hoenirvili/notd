#!/usr/bin/python3

import argparse
import json 

__DESCRIPTION = 'Notify with a blinking LED and display a number for the 4 digit 7 segment led'
__PROG ='notd'


class Args:
    def __init__(self, argv=None):
        if argv == None:
            raise ValueError('Please provide a non empty command line argument list')

        self._argv = argv[1:]

    def parse(self):
        if len(self._argv) == 1:
            return None

        return self._parse()

    def _parse(self):
        parser = argparse.ArgumentParser(__PROG, __DESCRIPTION)
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
            options['config'] = self._validate_parse_config(options['config'])
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

    def _validate_parse_config(self, c):
        if c == None:
            raise argparse.ArgumentError(argument=None,
                    message='Empty configuration passed')
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
        
        if all(k in data for k in ("gpio", "transistor", "led")) == False:
            raise argparse.ArgumentError(argument=None, 
                    message='Invalid json configuration')

        return data
