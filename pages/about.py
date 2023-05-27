# About Page

import vga1_16x16 as f16x16
import vga1_8x16 as f8x16
import pages.home
from config.board_info import *
from config.global_variable import *
from tools import AutoLine





def loadpage():
    Display.fill(0)
    line = AutoLine(40, 18)
    Display.text(f16x16, 'About', 80, 0)
    Display.text(f8x16, f'DeviceName: {str(getvalue("device_name"))}', 0, line)
    Display.text(f8x16, '', 0, line)
    Display.text(f8x16, f'DeviceID: {str(getvalue("device_id"))}', 0, line)
    Display.text(f8x16, '', 0, line)
    if getvalue('network_mode'):
        Display.text(f8x16, f'Device IP: {str(getvalue("ipconfig")[0])}', 0, line)
    else:
        Display.text(f8x16, 'Network Not Connected', 0, line, st7789.color565(255, 0, 0))


def updatepage():
    while getvalue('page') == 'about':
        if not SwitchA.value() and not SwitchB.value():
            line1 = AutoLine(40, 18)
            Display.fill(0)
            Display.text(f16x16, 'Design Team', 30, 0)
            Display.text(f8x16, 'Developer: Zhang Ziqing', 0, line1, st7789.color565(245, 169, 184))
            Display.text(f8x16, '', 0, line1)
            Display.text(f8x16, 'Introducer: Hu Lulu', 0, line1, st7789.color565(245, 169, 184))
            Display.text(f8x16, '', 0, line1)
            Display.text(f8x16, 'Writer: Luo Biao', 0, line1, st7789.color565(91, 206, 250))
            while True:
                if not SwitchA.value() or not SwitchB.value():
                    Display.fill(0)
                    loadpage()
                    break
        if not SwitchB.value() and SwitchA.value():
            set_var('page', 'home')
            set_var('to_page', pages.home)
            return
