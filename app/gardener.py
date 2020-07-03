#!/usr/bin/env python
import RPi.GPIO as GPIO
import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, Response, session, url_for, jsonify
)
from flask_cors import cross_origin
import time

#####################################################################
############################  GLOBALS  ##############################
#####################################################################
PUMP = 'pump'
PUMP2 = 'pump2'
LIGHTS = 'lights'
MISC = 'misc'
stateChange = False
#GPIO global
pinMapping = {
    'lights': 17,
    'pump': 18,
    'pump2': 22,
    'misc': 23
}
state = {
    'power': {
        'lights': False,
        'pump': False,
        'pump2': False,
        'misc': False,
    },
}


garden = Blueprint('garden', __name__, url_prefix='/garden')

def get_blueprint():
    pinList = list(pinMapping.values())
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinList, GPIO.OUT, initial=1)
    return garden
#####################################################################
############################  App Routes  ###########################
#####################################################################
def cleanup_gpios():
    GPIO.cleanup()
    print("cleaning up gpios...")


@garden.route('/state', methods=['GET'])
def getState():
    return jsonify(state)


@garden.route('/stream', methods=['GET'])
@cross_origin()
def sendStateStream():
    return Response(event_stream(), mimetype='text/event-stream')


@garden.route('/lights', methods=['GET'])
def lights():
    global stateChange
    print("lights")
    error = None
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        state['power'][LIGHTS] = powerStatus == 'true'
        power(LIGHTS)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})


@garden.route('/pump', methods=['GET'])
def pump():
    print("pump")
    error = None
    global stateChange
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        state['power'][PUMP] = powerStatus == 'true'
        power(PUMP)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})

@garden.route('/pump2', methods=['GET'])
def pump2():
    print("pump2")
    error = None
    global stateChange
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        state['power'][PUMP2] = powerStatus == 'true'
        power(PUMP2)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})


@garden.route('/misc', methods=['GET'])
def misc():
    print("misc")
    error = None
    global stateChange
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        state['power'][MISC] = True if powerStatus == 'true' else False
        power(MISC)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})

#####################################################################
########################## Helper Functions  ########################
#####################################################################
def power(output):
    powerStatus = not state['power'][output] # Relays being used are in reverse order
    GPIO.output(pinMapping[output], powerStatus)

def event_stream():
    while True:
        data_string = "data: {0}\n\n".format(json.dumps(state))
        stateChange = False
        yield data_string
        time.sleep(1)
        print(f"Event Stream: {data_string}")
