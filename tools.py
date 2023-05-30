import time
from config.global_variable import *


class AutoLine:
    def __init__(self, start, space):
        self.start = start
        self.space = space
        self.line = start

    def __int__(self):
        self.line += self.space
        return self.line - self.space

    def get_line(self):
        self.line += self.space
        return self.line - self.space


class TempSensor:

    def __init__(self, device_object):
        self.device_object = device_object
        self.last_read = 0
        self.value = 0

    def measure(self):
        pass

    def read(self):
        if self.last_read == 0 or time.time() - self.last_read >= 1:
            self.measure()
            return self.value
        else:
            return self.value

    def read_tmp(self):
        return self.value


class HighTemp(TempSensor):
    def __init__(self, device_object, rom):
        TempSensor.__init__(self, device_object)
        self.device_object = device_object
        self.last_read = 0
        self.value = 0
        self.rom = rom

    def measure(self):
        start_measure = time.time()
        error = 0
        while True:
            if time.time() - start_measure >= 5:
                set_var('high_temp_error', 1)
                return
            try:
                self.device_object.convert_temp()
                time.sleep_ms(750)
                self.value = self.device_object.read_temp(self.rom)
                remove_var('high_temp_error')
                return
            except:
                error += 1
                if error >= 3:
                    set_var('high_temp_error', 1)
                    return


class LowTemp(TempSensor):
    def __init__(self, device_object):
        TempSensor.__init__(self, device_object)
        self.last_read = 0

    def measure(self):
        start_measure = time.time()
        error = 0
        while True:
            if time.time() - start_measure >= 5:
                set_var('low_temp_error', 1)
                return
            try:
                self.device_object.measure()
                time.sleep_ms(1000)
                self.value = self.device_object
                remove_var('low_temp_error')
                return
            except:
                error += 1
                if error >= 3:
                    set_var('low_temp_error', 1)
                    return