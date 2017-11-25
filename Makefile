install:
	sudo python -m pip install .

upload:
	rsync -avz /home/hoenir/Work/notd pi@192.168.1.104:/home/pi/Work/
