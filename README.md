# ping messenger

ping is a simple web based messaging application designed for desktop and mobile browsers.

## Setup

Download the repository `git clone https://github.com/nspeer12/ping` and `cd ping`

Create a virtual enviornment

If python virtulenv is not installed, run `pip install virtualenv`

Then create a virtual enviornment using `python -m venv env`

Next, install the dependencies with `pip install --upgrade pip && pip install -r requirements.txt`

Finally, run the python web server `python app.py`

The web server will run on 0.0.0.0 port 8080. You can access the website locally with http://0.0.0.0:8080

To view on other devices on your local area network, run `ifconfig` on linux or mac or `ipconfig` on windows to find your ip address.
