import time

import vga1_8x16 as f8x16

import pages.about
from config.board_info import *
from config.global_variable import *


def loadpage():
    Display.fill(0)


def updatepage():
    while getvalue('page') == 'home':
        Display.rect(0, 0, 240, 18, st7789.color565(0, 0, 0))
        nowtime = time.localtime()
        Display.text(f8x16,
                     '%d-%d-%d %02d:%02d:%02d' % (nowtime[0], nowtime[1], nowtime[2], nowtime[3], nowtime[4], nowtime[5]),
                     0, 1)
        time.sleep_ms(10)
        if not SwitchA.value() and SwitchB.value():
            set_var('page', 'about')
            set_var('to_page', pages.about)
            return
