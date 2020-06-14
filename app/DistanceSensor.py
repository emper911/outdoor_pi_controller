import time
from datetime import datetime


class DistanceSensorController:
    def __init__(self, triggerPin, echoPin, gpio):
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        self.gpio = gpio
        self.measuring = False

    def getDistance(self):
        print("Calculating distance")
        self.gpio.output(self.triggerPin, self.gpio.HIGH)
        time.sleep(0.00001)
        self.gpio.output(self.triggerPin, self.gpio.LOW)

        while self.gpio.input(self.echoPin) == 0:
            pulse_start_time = time.time()
        while self.gpio.input(self.echoPin) == 1:
                pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        distance = round(pulse_duration * 17150, 2)

        print ("Distance:",distance,"cm")
        return distance

    def startMeasuring(self, outputTarget, outputTargetName, cycleLength=60000):
        self.measuring = True
        start_timestamp = datetime.utcnow()
        measured = False
        while self.measuring:
            lapsedTime = datetime.utcnow() - start_timestamp
            if lapsedTime < cycleLength:
                if not measured:
                    outputTarget[outputTargetName] = self.getDistance()
                    measured = True
            else:
                start_timestamp = datetime.utcnow()
                measured = False

    def stopMeasuring(self):
        self.measuring = False

