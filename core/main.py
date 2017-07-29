#!/usr/bin/python

from args import Arguments
from sys import argv
from display import Display


def main():
    arguments = Arguments(argv)
    display_args = arguments.parse()
    if display_args == None:
        return
    display = Display(display_args)
    display.run()

if __name__ == "__main__":
    main()
