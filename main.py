import pages.page0
from config.board_info import *
import vga1_8x8 as f8x8
import vga1_16x16 as f16x16
import utime
from pages import *


def main():
    init()
    pages.page0.loadpage()


def init():
    utime.sleep(1)
    Display.text(f8x8, 'Loading System', 0, 20)
    utime.sleep(1)
    Display.fill(0)
    Display.text(f16x16, "Welcome", 0, 0)
    utime.sleep(1)
    Display.fill(0)


if __name__ == '__main__':
    main()
