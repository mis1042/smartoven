import vga1_16x16 as f16x16
import vga1_8x16 as f8x16

import pages.home
import pages.working
from config.board_info import *
from tools import *

line = AutoLine(40, 18)


def loadpage():
    set_var('selected', 0)
    line = AutoLine(40, 18)
    # Display The Title
    Display.fill(0)
    Display.text(f16x16, 'Work Config', 30, 0)
    set_var('target_temp_line', line.get_line())
    Display.text(f8x16, 'Target Temp: 040 C', 0, getvalue('target_temp_line'))
    Display.text(f8x16, '', 0, line)
    set_var('work_time_line', line.get_line())
    Display.text(f8x16, 'Work Time: 010 min', 0, getvalue('work_time_line'))
    Display.text(f16x16, 'START', 80, 180)


def updatepage():
    # target_temp:  Min 40 Max:120
    # work_time_base Min 10  Max 180
    target_temp = 40
    work_time = 10

    while getvalue('page') == 'work':
        if getvalue('selected') == 0:
            target_temp = math.ceil(40 + 80 * no_adc_wrong(potentiometer_temp) / 369)
            work_time = math.ceil(10 + 170 * no_adc_wrong(potentiometer_time) / 369)
            if target_temp > 120:
                target_temp = 120
            if work_time > 180:
                work_time = 180
            __update_target_temp(target_temp)
            __update_work_time(work_time)

        if not SwitchA.value() or not SwitchB.value():
            pressed = ''
            if not SwitchA.value():
                pressed = 'A'
            elif not SwitchB.value():
                pressed = 'B'
            press_time = time.time()

            # wait_for_release(SwitchA, SwitchB)
            while not SwitchA.value() or not SwitchB.value():
                if time.time() - press_time >= 1.5:
                    break
            release_time = time.time()

            if release_time - press_time >= 1.5:

                if getvalue('selected') == 0:
                    set_var('selected', 1)
                    Display.rect(75, 175, 90, 26, st7789.color565(255, 255, 255))
                    wait_for_release(SwitchA, SwitchB)

                elif getvalue('selected') == 1:
                    set_var('work_config', [target_temp, work_time])
                    set_var('page', 'working')
                    set_var('to_page', pages.working)
                    return

            else:
                if getvalue('selected') == 1:
                    set_var('selected', 0)
                    Display.rect(75, 175, 90, 26, st7789.color565(0, 0, 0))
                    wait_for_release(SwitchA, SwitchB)
                    continue

                if pressed == 'A':
                    set_var('page', 'home')
                    set_var('to_page', pages.home)
                    return


def __update_work_time(work_time):
    Display.rect(0, getvalue('work_time_line') - 2, 240, 20, st7789.color565(0, 0, 0))
    Display.text(f8x16, 'Work Time: %3d min' % work_time, 0, getvalue('work_time_line'))


def __update_target_temp(target_temp):
    Display.rect(0, getvalue('target_temp_line') - 2, 240, 20, st7789.color565(0, 0, 0))
    Display.text(f8x16, 'Target Temp: %3d C' % target_temp, 0, getvalue('target_temp_line'))


"""
Display.text(f16x16, 'START', 80, 180)
Display.rect(75, 175, 90, 26, 0xffffff)
"""
