#!/usr/bin/python3

# for now make this so it won't complain
try:
    import RPi.GPIO as GPIO
except:
    pass


digits = {
    0: (1,1,1,1,1,1,0),
    1: (0,1,1,0,0,0,0),
    2: (1,1,0,1,1,0,1),
    3: (1,1,1,1,0,0,1),
    4: (0,1,1,0,0,1,1),
    5: (1,0,1,1,0,1,1),
    6: (1,0,1,1,1,1,1),
    7: (1,1,1,0,0,0,0),
    8: (1,1,1,1,1,1,1),
    9: (1,1,1,1,0,1,1)
}

time = 0.001

class Display:
    def __init__(self, arguments=None):
        if arguments == None:
            return

        self.number = arguments['number']
        self.gpio = arguments['config']['gpio_conf']
        self.transistors = arguments['config']['transistor_conf']
        self.led = arguments['config']['led_conf']
        self.green = arguments['green']
        self.red = arguments['red']

    def run(self):
        nums = list()
        a = self.number
        while a != 0:
             nums.append(a%10)
             a = int(a/10)

        nums.reverse()
        n = len(nums)

        for num in nums:
            for enum in digits[num]:

        self._setup_gpio()

    def clean(self):
        self._cleanup_gpio()

    def _setup_gpio(self):
        # Pin numbers on the P1 header of the Raspberry Pi board. 
        # The advantage of using this numbering system is that your 
        # hardware will always work, regardless of the board revision of the RPi.
        GPIO.setmode(GPIO.BOARD)
        # It is possible that you have more than one script/circuit 
        # on the GPIO of your Raspberry Pi. As a result of this, 
        # if RPi.GPIO detects that a pin has been configured 
        # to something other than the default (input), you get a 
        # warning when you try to configure a script. 
        GPIO.setwarnings(False)
        self._all_pins_low()

    def _all_pins_low(self):
        for gpio in self.gpio:
           GPIO.setup(gpio['pin'], GPIO.OUT, initial=GPIO.LOW)

        for base in self.transistors:
            GPIO.setup(base['pin'], GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.led[0]['pin'], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.led[1]['pin'], GPIO.OUT, initial=GPIO.LOW)


    def _cleanup_gpio(self):
        GPIO.cleanup()


