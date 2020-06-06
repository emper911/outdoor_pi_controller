#!/usr/bin/env python
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(PinMapping.values(), GPIO.OUT)
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
#GPIO global
pinMapping = {
    'pump': 11,
    'lights': 13,
    'misc': 15
}
state = {
    'power': {
        'lights': False,
        'pump': False,
        'misc': False,
    },
}
stateChange = False


#####################################################################
############################  App Routes  ###########################
#####################################################################
garden = Blueprint('garden', __name__, url_prefix='/garden')
def get_blueprint():
    return garden


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
        power(LIGHTS, powerStatus)
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
        power(PUMP, powerStatus)
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
        power(MISC, powerStatus)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})

#####################################################################
########################## Helper Functions  ########################
#####################################################################
def power(output, powerStatus):
    state['power'][output] = True if powerStatus == 'true' else False
    # GPIO.output(PinMapping[output], powerStatus)

def event_stream():
    while True:
        data_string = "data: {0}\n\n".format(json.dumps(state))
        stateChange = False
        yield data_string
        time.sleep(1)
        print(f"Event Stream: {data_string}")

