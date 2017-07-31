#!/usr/bin/python3

import args
import sys
import display


def main():
    options = args.Args(sys.argv).parse()
    if options == None:
        #TODO(hoenir) call the daemon
        return

    d = display.Display(options)
    print("[*] Running the notification daemon in command line")
    d.run()
    print("\n[*] Exit the process and clean up the pins")
    d.clean()

if __name__ == "__main__":
    main()
