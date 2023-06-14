import time

import vga1_8x16 as f8x16

import pages.about
import pages.work
import pages.working
from config.board_info import *
from config.global_variable import *
from tools import switch_to_working, AutoLine, check_work_plan


def loadpage():
    Display.fill(0)


def updatepage():
    plans_displaying = []
    while getvalue('page') == 'home':
        nowtime = time.localtime()
        Display.text(f8x16,
                     '%d-%d-%d %02d:%02d:%02d' % (
                         nowtime[0], nowtime[1], nowtime[2], nowtime[3], nowtime[4], nowtime[5]),
                     0, 1)

        line = AutoLine(40, 18)
        Display.text(f8x16, 'Next Works:', 0, line)  # 40

        if getvalue('work_plan')[0:5] != plans_displaying[0:5]:
            plans_displaying = getvalue('work_plan')[0:5]
            Display.fill_rect(0, 58, 240, 240 - 58, st7789.color565(0, 0, 0))
            for i in plans_displaying[0:5]:
                start_time = time.localtime(i['start_time'])
                Display.text(f8x16,
                             '%d-%d-%d %02d:%02d:%02d' % (
                                 start_time[0], start_time[1], start_time[2], start_time[3], start_time[4],
                                 start_time[5]),
                             0, line)
                # Display.text(f8x16, '', 0, line)

        time.sleep_ms(100)

        if not SwitchA.value() and SwitchB.value():
            set_var('page', 'about')
            set_var('to_page', pages.about)
            return

        if SwitchA.value() and not SwitchB.value():
            set_var('page', 'work')
            set_var('to_page', pages.work)
            return

        switch_to_working()
        check_work_plan()
