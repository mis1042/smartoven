import _thread
import time

import machine
import network
import ntptime
import ujson
import vga1_8x16 as font
from machine import RTC

import main
from config.board_info import *
from config.global_variable import *
from mqtt import connect_to_server, receive
from tools import AutoLine, check_sensors, SensorError

# 初始化
line = AutoLine(0, 18)
init_var()
read_basic_config()
Display.init()
heater.off()
set_var('work_plan', [])

if not SwitchA.value() and not SwitchB.value():
    # main.main()

    with open(config_file, 'r') as f:
        content = ujson.loads(f.read())
    content['Network_Config']['ssid'] = "ssid"
    content['Network_Config']['password'] = "password"
    with open(config_file, 'w') as f:
        f.write(ujson.dumps(content))
    Display.text(font, 'Network Configure Reseted', 0, line, st7789.color565(255, 0, 0))
    Display.text(font, 'Rebooting...', 0, line, st7789.color565(255, 0, 0))
    time.sleep(1)
    machine.reset()

# 检查网络配置
if getvalue('ssid') != 'ssid' and getvalue('password') != 'password':
    Display.text(font, 'Connecting To AP...', 0, line)
    # 尝试连接网络
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    data = wlan.scan()
    wlan.config(reconnects=3)
    wlan.connect(getvalue('ssid'), getvalue('password'))
    start_time = time.time()
    while not wlan.status() == network.STAT_GOT_IP:
        if time.time() - start_time >= 10:
            break

    if wlan.isconnected():
        Display.text(font, 'SUCCESS', 0, line, st7789.color565(0, 255, 0))
        set_var('ipconfig', wlan.ifconfig())
        set_var('network_mode', 1)
    else:
        Display.text(font, 'FAILED', 0, line, st7789.color565(255, 0, 0))
        set_var('network_mode', 0)
else:
    Display.text(font, 'Network Not Configured', 0, line, st7789.color565(255, 0, 0))
    set_var('network_mode', -1)

# 尝试使用NTP获取时间
if getvalue('network_mode') == 1:
    ntptime.host = getvalue('ntp')
    Display.text(font, 'Getting Time From NTP...', 0, line)
    retry = 0
    for i in range(3):
        try:
            ntptime.settime()
            (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
            rtc = RTC()
            rtc.datetime((year, month, mday, 0, hour + 8, minute, second, 0))
            Display.text(font, 'SUCCESS', 0, line, st7789.color565(0, 255, 0))
            break

        except Exception as e:
            print(e)
            retry += 1
            if retry >= 3:
                Display.text(font, 'FAILED', 0, line, st7789.color565(255, 0, 0))
                break

# 连接到服务器
if getvalue('network_mode') == 1:
    Display.text(font, 'Connecting To Server...', 0, line)
    server = getvalue('server')
    port = getvalue('port')
    client_id = getvalue('device_id')
    try:
        connect_to_server(server, port, str(client_id), getvalue('connect_username'), getvalue('connect_password'))
        Display.text(font, 'SUCCESS', 0, line, st7789.color565(0, 255, 0))
        _thread.start_new_thread(receive, ())
    except Exception as e:
        Display.text(font, 'FAILED', 0, line, st7789.color565(255, 0, 0))
        set_var('network_mode', 0)
        print(e)

# 检查温度传感器
errors = 0
Display.text(font, 'Checking Temp Sensors', 0, line)
try:
    [high_temp, low_temp] = check_sensors(ds18b20, dht1)
    Display.text(font, f'SUCCESS,Value is {round(high_temp, 1)} C', 0, line, st7789.color565(0, 255, 0))
    Display.text(font, f'SUCCESS,Value is {round(low_temp.temperature(), 1)} C', 0, line, st7789.color565(0, 255, 0))
    Display.text(font, f'SUCCESS,Value is {round(low_temp.humidity(), 1)} %', 0, line, st7789.color565(0, 255, 0))
except SensorError:
    if getvalue('high_temp_error'):
        errors += 1
        Display.text(font, 'Temp Sensor 1 FAILED', 0, line, st7789.color565(255, 0, 0))
    else:
        errors += 1
        Display.text(font, 'Temp Sensor 2 FAILED', 0, line, st7789.color565(255, 0, 0))

while errors > 0:
    pass

Display.text(font, 'Initialization Completed', 0, line, st7789.color565(0, 255, 0))
main.main()
heater.off()
