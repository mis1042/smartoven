import utime

import pages.about
import pages.home
from config.global_variable import *


def main():
    utime.sleep(2)
    set_var('page', 'home')
    pages.home.loadpage()
    pages.home.updatepage()
    while True:
        while getvalue('to_page') is None:
            pass
        nextpage = getvalue('to_page')
        remove_var('to_page')
        nextpage.loadpage()
        nextpage.updatepage()
