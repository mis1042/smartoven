import network
from config.global_variable import *
from config.board_info import *
import vga1_8x8 as font

Display.init()
Display.text(font, 'Connecting...', 0, 0)
# 尝试连接网络
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
data = wlan.scan()

try:
    wlan.connect(ssid, password)
except:
    pass

if wlan.isconnected():
    Display.text(font, 'SUCCESS', 0, 10)
    mac = wlan.config('mac')
    ifconfig = wlan.ifconfig()
    network_mode = 1
else:
    Display.text(font, 'FAILED', 0, 10)
    network_mode = 0
