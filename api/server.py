#!/usr/bin/env python
from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import signal
import sys

PUMP = "pump"
LIGHTS = "lights"
MISC = "misc"

app = Flask(__name__, static_url_path='../client/public')

state = {
    "power": {
        "lights": False,
        "pump": False,
        "misc": False,
    }
}

#####################################################################
############################  App Routes  ###########################
#####################################################################

# INDEX HTML
@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/lights", methods=['GET'])
def lights():
    error = None
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        power(LIGHTS, powerStatus)
    else:
        error = "Invalid request method"
        return error, 404

    return jsonify({"powerStatus": powerStatus})


@app.route("/pump", methods=['GET'])
def pump():
    error = None
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        power(PUMP, powerStatus)
    else:
        error = "Invalid request method"
        return error, 404

    return jsonify({"powerStatus": powerStatus})


@app.route("/misc", methods=['GET'])
def misc(name):
    error = None
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        power(MISC, powerStatus)
    else:
        error = "Invalid request method"
        return error, 404

    return jsonify({"powerStatus": powerStatus})


#####################################################################
########################  Helper Functions  #########################
#####################################################################
def power(output, powerStatus):
    state["power"][output] = powerStatus
    GPIO.output(PinMapping[output], powerStatus)


def signal_handler(sig, frame):
    print('Server is terminating! Cleaning up GPIO PINS on exit!')
    GPIO.cleanup()
    sys.exit(0)


#####################################################################
###########################  ENTRY POINT  ###########################
#####################################################################
if __name__ == "__main__":
    # Exit gracefully
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    #GPIO globals
    PinMapping = {
        "PUMP": 11,
        "LIGHTS": 13,
        "MISC": 15
    }

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PinMapping.values(), GPIO.OUT)

    #Flask app start
    app.run()

