# -*- coding: utf-8 -*-

"""
tradingbot.core.grapher
~~~~~~~~~~~~~~

This module provides grapher object that manipulates
monitor account and update records and datasets.
"""

import os.path
import time
import sys
from getpass import getpass
from optparse import OptionParser
from .color import *
from .logger import logger
from ..configurer import Configurer
from .algorithm import Scalper


class Bot(object):
    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "data.yml")
        self.configurer = Configurer(path)
        self.getArgvs()
        logger.setlevel(self.options.verbosity)

    def getArgvs(self):
        parser = OptionParser()
        parser.add_option("-v", "--verbosity",
                          dest="verbosity",
                          default='info',
                          help="Set the level of verbosity.",
                          action="store",
                          type="string")
        parser.add_option("--verbosity_api",
                          dest="verbosity_api",
                          help="Set the level of verbosity of the API.",
                          action="store",
                          type="string")
        parser.add_option("-w", "--wait",
                          dest="wait",
                          default=1,
                          help="minute to attend before starting main algo.",
                          action="store",
                          type="int")
        parser.add_option("--conf",
                          dest="conf",
                          default=False,
                          help="Config only.",
                          action="store_true")
        (options, args) = parser.parse_args()
        if not hasattr(options, 'verbosity_api'):
            options.verbosity_api = options.verbosity
        self.options = options

    def _start_conf(self):
        print(printer.header("config"))
        print("Add your credentials")
        print("for Trading212")
        print(bold(blue("--------------------")))
        username = input(printer.user_input("Username: "))
        password = getpass(printer.user_input("Password: "))
        print(bold(blue("--------------------")))
        print("Add your information")
        print("for a monitoring")
        print("account")
        print(bold(blue("--------------------")))
        username2 = input(printer.user_input("Username: "))
        password2 = getpass(printer.user_input("Password: "))
        prefs = input(printer.user_input(
            "Favourite stocks (sep by spaces): "))
        stocks = []
        if prefs:
            stocks = prefs.split(' ')
        strategy = input(printer.user_input("Strategy: "))
        general = {'username': username, 'password': password}
        monitor = {'username': username2, 'password': password2,
                   'stocks': stocks, 'initiated': 0}
        self.configurer.config['strategy'] = {
            'strategy': strategy}
        self.configurer.config['general'] = general
        self.configurer.config['monitor'] = monitor
        self.configurer.save()

    def conf(self):
        if self.configurer.checkFile():
            self.configurer.read()
        else:
            self.__start_conf()

    def start(self):
        if self.options.conf:
            try:
                self.__start_conf()
                print("config saved")
            except Exception:
                raise
            finally:
                sys.exit()
        self.conf()
        self.configurer.config['logger_level'] = self.options.verbosity
        self.configurer.config['logger_level_api'] = self.options.verbosity_api
        self.configurer.save()
        self.scalper = Scalper(self.configurer)
        self.scalper.start(self.options.wait)

    def stop(self):
        self.scalper.stop()


def main():
    bot = Bot()
    try:
        bot.start()
        while True:
            time.sleep(1)
    except Exception as e:
        logger.error(e)
    except KeyboardInterrupt as e:
        sys.stderr.write('\r' + printer.info(red("exiting...\n")))
        bot.stop()
        sys.exit()


if __name__ == "__main__":
    main()
