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

from app import Pump
from app import DistanceSensor

#####################################################################
############################  GLOBALS  ##############################
#####################################################################
PUMP = 'pump'
LIGHTS = 'lights'
MISC = 'misc'
WATERLEVEL = 'waterlevel'
WATERLEVEL_TRIGGER = 'waterlevel_trigger'
WATERLEVEL_ECHO = 'waterlevel_echo'

stateChange = False
#GPIO global
pinMapping = {
    'input': {
        'waterlevel_echo': 12,
    },
    'output': {
        'lights': 17,
        'pump': 18,
        'misc': 22,
        'waterlevel_trigger': 23,
    }
}
state = {
    'power': {
        'lights': False,
        'pump': False,
        'misc': False,
        'waterlevel': False
    },
    'sensors': {
        'waterlevel': -1,
    }
}


garden = Blueprint('garden', __name__, url_prefix='/garden')
pump_1 = None
distanceSensor_1 = None

def get_blueprint():
    global pump_1, distanceSensor_1
    pinInputList = list(pinMapping['input'].values())
    pinOutputList = list(pinMapping['output'].values())
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinInputList, GPIO.IN)
    GPIO.setup(pinOutputList, GPIO.OUT)

    pump_1 = Pump.PumpController(powerPin=pinMapping['output'][PUMP], gpio=GPIO)
    distanceSensor_1 = DistanceSensor.DistanceSensorController(
        triggerPin = pinMapping['output'][WATERLEVEL_TRIGGER],
        echoPin = pinMapping['input'][WATERLEVEL_ECHO],
        gpio = GPIO
    )

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
        powerStatus = request.args.get('powerStatus') == 'true'
        state['power'][LIGHTS] = powerStatus
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
        powerStatus = request.args.get('powerStatus') == 'true'
        state['power'][PUMP] = powerStatus
        pump_1.power(powerStatus)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})


@garden.route('/pump/schedule', methods=['GET'])
def pumpSchedule():
    if request.method == 'GET':
        status = request.args.get('status')
        if status == 'on':
            state['power'][PUMP] = True
            onTime = request.args.get('onTime')
            cycleLength = request.args.get('cycle')
            endTime = request.args.get('endTime')
            if endTime:
                pump_1.start_schedule_pump(onTime, cycleLength, endTime)
            else:
                pump_1.start_schedule_pump(onTime, cycleLength)

        else:
            state['power'][PUMP] = False
            pump_1.stop_schedule_pump()


@garden.route('/misc', methods=['GET'])
def misc():
    print("misc")
    error = None
    global stateChange
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus') == 'true'
        state['power'][MISC] = powerStatus
        power(MISC)
        stateChange = True
    else:
        error = 'Invalid request method'
        return error, 404

    return jsonify({'powerStatus': powerStatus})


@garden.route('/waterlevel', methods=['GET'])
def water_level():
    print("waterlevel")
    error = None
    global stateChange
    if request.method == 'GET':
        powerStatus = request.args.get('powerStatus') == 'true'
        state['power'][WATERLEVEL] = powerStatus
        stateChange = True
        if powerStatus:
            distanceSensor_1.startMeasuring(state['sensors'], WATERLEVEL)
        else:
            distanceSensor_1.stopMeasuring()

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
