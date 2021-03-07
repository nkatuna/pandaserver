# pandaserver: a fire escape window security system

I keep a musical instrument in my office within view of a fire escape window.  **pandaserver** is the web interface for my cheap security system that keeps watch over the window.  It is also a demo project for friends looking to set up their own lightweight webservers.

![The Panda](/media/panda.jpg)


## Launch instructions

I dug out an old raspberry pi for this project, and only had to pick up a camera, a magnetic contact gate, some wire, and a connector for the raspberry pi's GPIO pins.  I soldiered the gate to the wire, and the wire to the GPIO header connector's pins (GND and BCM/SCL 3).  You could use any powered pin, just be sure to update the `GPIOZERO_PIN` setting in [config.py](/config.py).

Before writing any code, I set up a virtual environment in my code folder with `python -m venv venv` and initialized a git repo (`git init`).

If you would like to run the **pandaserver** on your home raspberry pi, clone this repo (follow github instructions) and installed required packages:

`pip install -r requirements.txt`.

Then set the secret key:

`export SECRET_KEY='some long random string that is very secret'`.

I only check the pandaserver from my home network, so I avoid setting up a full proxy server.  Waitress, the WSGI interface, needs to be able to bind to port 80.  I use authbind rather than run waitress as root.

I launch the pandaserver with `authbind python waitress_server.py &`.


