import utime
import pages.about
from config.global_variable import *


def main():
    utime.sleep(2)
    set_var('page', 'about')
    pages.about.start_page()
    while True:
        pass
