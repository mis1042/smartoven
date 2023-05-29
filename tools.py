import time


class AutoLine:
    def __init__(self, start, space):
        self.start = start
        self.space = space
        self.line = start

    def __int__(self):
        self.line += self.space
        return self.line - self.space


class HighTemp:
    def __init__(self, device_object, rom):
        self.device_object = device_object
        self.rom = rom
        self.last_read = 0
        self.temp = 0

    def read(self):
        if self.last_read == 0 or time.time() - self.last_read >= 1:
            self.device_object.convert_temp()
            time.sleep_ms(750)
            self.temp = self.device_object.read_temp(self.rom)
            return self.temp
        else:
            return self.temp


