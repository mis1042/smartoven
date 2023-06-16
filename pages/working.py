import vga1_16x16 as f16x16
import vga1_8x16 as f8x16

import pages.home
from config.board_info import *
from tools import *


def loadpage():
    # Display The Title
    Display.fill(0)
    Display.text(f16x16, 'Working', 65, 0)


def updatepage():
    target_temp = getvalue('work_config')[0]
    work_time = getvalue('work_config')[1]
    when_finish = time.time() + work_time * 60

    while getvalue('page') == 'working':
        line = AutoLine(40, 18)

        if getvalue('update_config'):
            target_temp = getvalue('work_config')[0]
            work_time = getvalue('work_config')[1]
            if work_time == 0:
                break
            when_finish = time.time() + work_time * 60
            remove_var('update_config')
            Display.fill(0)
            loadpage()
        try:

            if flame.value():
                raise FireDetected

            [high_temp, low_temp] = check_sensors(ds18b20, dht1)
            now_internal_temp = round(high_temp, 1)
            now_ambient_temp = low_temp.temperature()
            now_ambient_hum = low_temp.humidity()
            remain_time = when_finish - time.time()

            working_info = [now_internal_temp, now_ambient_temp, now_ambient_hum, target_temp, remain_time]
            set_var('working_status', 'working')
            set_var('working_info', working_info)

            if remain_time <= 0:
                break

            if now_internal_temp <= target_temp:
                status = 'Heating'
                heater.on()
            else:
                status = 'Cooling'
                heater.off()

            time_tuple = time.localtime(remain_time)
            Display.text(f8x16, 'Remain:%02d:%02d:%02d' % (time_tuple[3], time_tuple[4], time_tuple[5]), 0, line)
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, f'Target_Temp:{target_temp}', 0, line)
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, f'Internal_Temp:{now_internal_temp}', 0, line)
            Display.text(f8x16, '', 0, line)
            if status == 'Heating':
                Display.text(f8x16, f'Status:{status}', 0, line, st7789.color565(255, 0, 0))
            else:
                Display.text(f8x16, f'Status:{status}', 0, line, st7789.color565(0, 0, 255))
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, f'Ambient_Temp:{now_ambient_temp}', 0, line)
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, f'Ambient_Hum:{now_ambient_hum}', 0, line)

        except SensorError:
            Display.fill(0)
            heater.off()
            error = ''
            set_var('working_status', 'Sensor Error')
            if getvalue('high_temp_error'):
                error += "Sensor 1 "
            if getvalue('low_temp_error'):
                error += "Sensor 2"

            line = AutoLine(40, 18)
            Display.text(f8x16, f'{error} Error', 0, line, st7789.color565(255, 0, 0))
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, 'Please Check', 0, line, st7789.color565(255, 0, 0))
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, 'Press Any Switch to Continue', 0, line, st7789.color565(255, 0, 0))
            while SwitchA.value() and SwitchB.value():
                pass
            Display.fill(0)
            loadpage()

        except FireDetected:
            set_var('working_status', 'Fire Detected')
            Display.fill(0)
            heater.off()
            line = AutoLine(40, 18)
            Display.text(f8x16, 'Warning!!!', 0, line, st7789.color565(255, 0, 0))
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, 'Fire Detected', 0, line, st7789.color565(255, 0, 0))
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, 'Please Check', 0, line, st7789.color565(255, 0, 0))
            Display.text(f8x16, '', 0, line)
            Display.text(f8x16, 'Press Any Switch to Quit', 0, line, st7789.color565(255, 0, 0))
            while SwitchA.value() and SwitchB.value():
                pass
            Display.fill(0)
            loadpage()

        if not SwitchA.value() and not SwitchB.value():
            break

    heater.off()
    remove_var('working_status')
    remove_var('working_info')
    set_var('page', 'home')
    set_var('to_page', pages.home)
    return
