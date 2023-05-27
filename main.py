import utime
from config.global_variable import *
import pages.home
import pages.about


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
