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

        print(c)
        
