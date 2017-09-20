# -*- coding: utf-8 -*-

"""
tradingbot.core.events
~~~~~~~~~~~~~~

This module provides events and signals for threading module.
"""

import time
import threading


class LIVE(threading.Event):
    """signal object for threads"""
    def __init__(self):
        super().__init__()

    def wait_terminate(self, interval):
        for x in range(interval):
            if LIVE.is_set():
                time.sleep(1)
            else:
                return False
