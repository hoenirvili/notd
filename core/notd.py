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

    display = Display(options)
    print("[*] Running the display mode")
    display.run()
    print("[*] Exit the display mode, clean up")
    display.clean()

if __name__ == "__main__":
    main()
