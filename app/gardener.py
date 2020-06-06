#!/usr/bin/env python
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(PinMapping.values(), GPIO.OUT)
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, Response, session, url_for, jsonify
)

#####################################################################
############################  GLOBALS  ##############################
#####################################################################
PUMP = 'pump'
LIGHTS = 'lights'
MISC = 'misc'
#GPIO globals
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
def sendStateStream():
    if stateChange:
        stateChange = False
        return Response(event_stream(), mimetype='text/event-stream')


@garden.route('/lights', methods=['GET'])
def lights():
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
    error = None
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus')
        power(PUMP, powerStatus)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})


@garden.route('/misc', methods=['GET'])
def misc(name):
    error = None
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
    state['power'][output] = powerStatus
    # GPIO.output(PinMapping[output], powerStatus)

def event_stream():
    return state

