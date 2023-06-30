# About Page

import vga1_16x16 as f16x16
import vga1_8x16 as f8x16

import pages.home
from config.board_info import *
from config.global_variable import *
from tools import AutoLine, switch_to_working, check_work_plan


def loadpage():
    Display.fill(0)
    line = AutoLine(40, 18)
    ds18b20.remeasure_time = 10
    dht1.remeasure_time = 10
    Display.text(f16x16, 'About', 80, 0)
    Display.text(f8x16, f'DeviceName: {str(getvalue("device_name"))}', 0, line)
    Display.text(f8x16, '', 0, line)
    Display.text(f8x16, f'DeviceID: {str(getvalue("device_id"))}', 0, line)
    Display.text(f8x16, '', 0, line)

    if getvalue('network_mode') == 1:
        Display.text(f8x16, f'Device IP: {str(getvalue("ipconfig")[0])}', 0, line)
    elif getvalue('network_mode') == 0:
        Display.text(f8x16, 'Network Not Connected', 0, line, st7789.color565(255, 0, 0))
    else:
        Display.text(f8x16, 'Network Not Configured', 0, line, st7789.color565(255, 0, 0))

    Display.text(f8x16, '', 0, line)
    set_var('high_temp_line', line.get_line())
    Display.text(f8x16, f'Internal Temp: {str(round(ds18b20.read(), 1))} C', 0, getvalue('high_temp_line'))

    Display.text(f8x16, '', 0, line)
    set_var('low_temp_line', line.get_line())
    Display.text(f8x16, f'Ambient Temp: {str(round(dht1.read().temperature(), 1))} C', 0, getvalue('low_temp_line'))

    Display.text(f8x16, '', 0, line)
    set_var('low_hum_line', line.get_line())
    Display.text(f8x16, f'Ambient Hum: {str(round(dht1.read().humidity(), 1))} %', 0, getvalue('low_hum_line'))

    Display.text(f8x16, '', 0, line)


def updatepage():
    while getvalue('page') == 'about':

        """
        if SwitchA.value() and SwitchB.value():
            Display.fill_rect(0, getvalue('high_temp_line'), 1000, 18, st7789.color565(0, 0, 0))
            value = ds18b20.read()
            if getvalue('high_temp_error') != 1:
                Display.text(f8x16, f'Internal Temp: {str(round(value, 1))} C', 0, getvalue('high_temp_line'))
            else:
                Display.text(f8x16, f'Internal Temp: FAILED', 0, getvalue('high_temp_line'), st7789.color565(255, 0, 0))

            Display.fill_rect(0, getvalue('low_temp_line'), 240, 18, st7789.color565(0, 0, 0))
            value = dht1.read()
            if getvalue('low_temp_error') != 1:
                Display.text(f8x16, f'Ambient Temp: {str(round(value.temperature(), 1))} C', 0, getvalue('low_temp_line'))
                Display.fill_rect(0, getvalue('low_hum_line'), 240, 18, st7789.color565(0, 0, 0))
                Display.text(f8x16, f'Ambient Hum: {str(round(value.humidity(), 1))} %', 0, getvalue('low_hum_line'))
            else:
                Display.text(f8x16, f'Ambient Temp: FAILED', 0, getvalue('low_temp_line'), st7789.color565(255, 0, 0))
                Display.fill_rect(0, getvalue('low_hum_line'), 240, 18, st7789.color565(0, 0, 0))
                Display.text(f8x16, f'Ambient Hum: FAILED', 0, getvalue('low_hum_line'), st7789.color565(255, 0, 0))
            """

        if not SwitchB.value() and SwitchA.value():
            set_var('page', 'home')
            set_var('to_page', pages.home)
            return

        switch_to_working()
        check_work_plan()
