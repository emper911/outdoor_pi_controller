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
LIGHTS = 'lights'
MISC = 'misc'
stateChange = False
#GPIO global
pinMapping = {
    'lights': 17,
    'pump': 27,
    'misc': 22
}
state = {
    'power': {
        'lights': False,
        'pump': False,
        'misc': False,
    },
}


garden = Blueprint('garden', __name__, url_prefix='/garden')

def get_blueprint():
    pinList = list(pinMapping.values())
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinList, GPIO.OUT)
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
        state['power'][LIGHTS] = True if powerStatus == 'true' else False
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
        state['power'][PUMP] = True if powerStatus == 'true' else False
        power(PUMP)
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
    GPIO.output(pinMapping[output], state['power'][output])

def event_stream():
    while True:
        data_string = "data: {0}\n\n".format(json.dumps(state))
        stateChange = False
        yield data_string
        time.sleep(1)
        print(f"Event Stream: {data_string}")

