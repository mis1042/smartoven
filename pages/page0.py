# About Page
from config.board_info import *
import vga1_8x8 as f8x8
import vga1_16x16 as f16x16


def loadpage():
    Display.fill(0)
    Display.text(f16x16, 'About', 80, 0)
    Display.text(f8x8, 'Author:', 0, 30)
    Display.text(f8x8, 'Misaka10042', 0, 40)
