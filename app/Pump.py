#!/usr/bin/env python
from datetime import datetime, date

class PumpController:

    def __init__(self, powerPin, gpio):
        self.gpio = gpio
        self.pin = powerPin
        self.pump_start_timestamp = 0
        self.pump_status = False
        self.schedule_status = False

    def power(self, powerStatus):
        self.gpio.output(self.pin, powerStatus)

    def start_schedule_pump(self, on_time, cycle_length, end_time=date.max):
        self.schedule_status = True
        schedule_start_timestamp = datetime.utcnow()
        self.pump_start_timestamp = schedule_start_timestamp

        while self.schedule_status and schedule_start_timestamp < end_time:
            self._schedule_pump_loop(
                self.pump_start_timestamp,
                on_time,
                cycle_length
            )
            schedule_start_timestamp = datetime.utcnow()

    def stop_schedule_pump(self):
        self.schedule_status = False

    def _schedule_pump_loop(self, start_timestamp, on_time, cycle_length):
        lapsed_time = datetime.utcnow() - start_timestamp
        if lapsed_time < cycle_length:
            if not self.pump_status and lapsed_time <= on_time:
                self.pump_status = True
                self.power(self.pump_status)
            elif self.pump_status and lapsed_time > on_time:
                self.pump_status = False
                self.power(self.pump_status)
        else:
            self.pump_start_timestamp = datetime.utcnow()










