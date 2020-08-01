# pandaserver: a fire escape window security system

![The Panda](/media/panda.jpg)


## Launch instructions

I dug out an old raspberry pi for this project, and only had to pick up a magnetic contact gate, some wire, and a connector for the raspberry pi's GPIO pins.  I soldiered the gate to the wire, and the wire to the GPIO header connector's pins (GND and BCM/SCL 3).  You could use any powered pin, just be sure to update the `GPIOZERO_PIN` setting in [config.py](/config.py).

I set up a virtual environment in my code folder with `python -m venv venv`, and installed required packages:

`pip install -r requirements.txt`.

Then I set the secret key:

`export SECRET_KEY='some long random string that is very secret'`.

I only check the pandaserver from my home network, so I avoid setting up a full web proxy and WSGI server.  Waitress needs to be able to bind to port 80, so I use authbind rather than run waitress as root.  This allows me to avoid specifying the locations of executables in my virtual environment, and makes setting up a service to restart the server easy.

I launch the pandaserver with `authbind python waitress_server.py &`.

