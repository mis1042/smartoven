import time
import utime
import network
import ntptime
import vga1_8x16 as font
import ujson
import machine
import main
from config.board_info import *
from config.global_variable import *
from tools import AutoLine, check_sensors, SensorError

# 初始化
line = AutoLine(0, 18)
init_var()
read_basic_config()
Display.init()

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
    utime.sleep(1)
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

# 同步正确的时间
if getvalue('network_mode') == 1:
    error = 0
    Display.text(font, 'Syncing Time', 0, line)
    while True:
        try:
            ntptime.NTP_DELTA = 3155644800  # 设置  UTC+8偏移时间（秒），不设置就是UTC0
            ntptime.host = getvalue('ntp')  # 可选ntp服务器为阿里云服务器，默认是"pool.ntp.org"
            ntptime.settime()
            nowtime = time.localtime()
            Display.text(font, 'Synced', 0, line, st7789.color565(0, 255, 0))
            Display.text(font, 'Now is %d-%d-%d %02d:%02d:%02d' % (
                nowtime[0], nowtime[1], nowtime[2], nowtime[3], nowtime[4], nowtime[5]), 0, line)
            break
        except:
            error += 1
            if error >= 3:
                Display.text(font, 'Sync Time Failed', 0, line, st7789.color565(255, 0, 0))
                Display.text(font, 'Check Your Network and Reboot', 0, line, st7789.color565(255, 0, 0))
                break
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
