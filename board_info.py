from machine import Pin, ADC, SoftSPI
import st7789

# 物理引脚与逻辑引脚对应，作为常量禁止修改！
PIN0 = 33
PIN1 = 32
PIN2 = 35
PIN3 = 34
PIN4 = 39
PIN5 = 0
PIN6 = 16
PIN7 = 17
PIN8 = 28
PIN9 = 25
PIN10 = 36
PIN11 = 2
PIN13 = 18
PIN14 = 19
PIN15 = 21
PIN16 = 5

# 板载设备定义
# 板载按键
SwitchA = Pin(0, Pin.IN, Pin.PULL_UP)
SwitchB = Pin(2, Pin.IN, Pin.PULL_UP)

# 光敏传感器
Light = ADC(Pin(39))
Light.atten(ADC.ATTN_11DB)
Light.width(ADC.WIDTH_9BIT)

# 屏幕
spi = SoftSPI(baudrate=40000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(35))
Display = st7789.ST7789(spi, 240, 240, reset=Pin(12, Pin.OUT), cs=Pin(15, Pin.OUT), dc=Pin(4, Pin.OUT))