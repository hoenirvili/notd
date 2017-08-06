#!/usr/bin/python3

import args
import sys
import display
import signal
import server

def main():
    options = args.Args(sys.argv).parse()
    # tcp server mode
    if options == None:
        #server.run("localhost", 5555)
        return

    # we are in command line mode
    d = display.Display(options)
    signal.signal(signal.SIGINT, lambda signum, frame: d.stop())
    print("[*] Running the notification daemon in command line")
    d.run()
    print("\n[*] Exit the process and clean up the pins")
    d.clean()

if __name__ == "__main__":
    main()
