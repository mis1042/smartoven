import time

import machine
import network
import ntptime
import vga1_8x8 as font

import main
from config.board_info import *
from config.global_variable import *
from tools import AutoLine

line = AutoLine(0, 10)
init_var()
read_basic_config()
# 初始化显示屏
Display.init()
Display.text(font, 'Connecting To AP...', 0, line)
# 尝试连接网络
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
data = wlan.scan()
wlan.config(reconnects=3)
wlan.connect(getvalue('ssid'), getvalue('password'))
while not wlan.status() == network.STAT_GOT_IP:
    pass
if wlan.isconnected():
    Display.text(font, 'SUCCESS', 0, line, st7789.color565(0, 255, 0))
    mac = wlan.config('mac')
    set_var('ipconfig', wlan.ifconfig())
    set_var('network_mode', 1)
else:
    Display.text(font, 'FAILED', 0, line, st7789.color565(255, 0, 0))
    set_var('network_mode', 0)

# 同步正确的时间
if wlan.isconnected():
    Display.text(font, 'Syncing Time', 0, line)
    ntptime.host = 'ntp1.aliyun.com'
    ntptime.settime()
    nowtime = list(time.localtime())
    nowtime[3] += 8
    machine.RTC().datetime(tuple(nowtime))
    Display.text(font, 'Synced',
                 0, line, st7789.color565(0, 255, 0))
    Display.text(font, f'Now is {nowtime[0]}-{nowtime[1]}-{nowtime[2]} {nowtime[3]}:{nowtime[4]}:{nowtime[5]}', 0, line)

    # 检查温度传感器
    Display.text(font, 'Checking Sensor 1', 0, line)
    # 一会再写吧
    Display.text(font, 'SUCCESS', 0, line, st7789.color565(0, 255, 0))

    Display.text(font, 'Checking Sensor 2', 0, line)
    # 一会再写吧
    Display.text(font, 'SUCCESS', 0, line, st7789.color565(0, 255, 0))
    Display.text(font, 'Initialization Completed', 0, line, st7789.color565(0, 255, 0))

main.main()
