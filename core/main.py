#!/usr/bin/python3

from args import Arguments
from sys import argv
from display import Display


def main():
    options = Arguments(argv).parse()
    
    if options == None:
        # daemon = Daemon()
        # daemon.start()
        return

    Display(options).run()

if __name__ == "__main__":
    main()
