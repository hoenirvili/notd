#!/usr/bin/python3

import args
import sys
import display


def main():
    options = args.Args(argv).parse()
    if options == None:
        #TODO(hoenir) call the daemon
        return

    display = display.Display(options)
    print("[*] Running the notification daemon in command line")
    display.run()
    print("[*] Exit the process and clean up the pins")
    display.clean()

if __name__ == "__main__":
    main()
