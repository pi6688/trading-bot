import time
# from numpy import mean

from .color import *
from .grapher import Grapher


class Pivot(object):
    def __init__(self, api, conf, logger):
        self.logger = logger
        self.logger.debug("Pivot algortihm initialized")
        self.api = api
        self.conf = conf
        self.graph = Grapher(self.conf, self.logger)
        self.predict_stocks = []

    def getPivotPoints(self):
        for stock in self.graph.stocks:
            high = max([float(x[1]) for x in stock.records])
            low = min([float(x[2]) for x in stock.records])
            close = [float(x[3]) for x in stock.records][-1]
            if not [x for x in self.predict_stocks if x.name == stock.name]:
                self.predict_stocks.append(predictStock(stock.name))
            predict_stock = [x for x in self.predict_stocks if x.name == stock.name][0]
            predict_stock.pp = (high + low + close) / 3
            predict_stock.sl = []
            predict_stock.sl.append((predict_stock.pp * 2) - high)
            predict_stock.sl.append(predict_stock.pp - (high - low))
            predict_stock.rl = []
            predict_stock.rl.append((predict_stock.pp * 2) - low)
            predict_stock.rl.append(predict_stock.pp + (high - low))
            self.logger.info(bold(predict_stock.name) + ': ' +\
                str([round(predict_stock.pp, 3), round(predict_stock.sl[0], 3), round(predict_stock.rl[0], 3)]))

    def isWorth(self, name):
        stock = [x.sl for x in self.predict_stocks]
        for support in stock:
            for sup_level in support:
                if self.graph.isDoji(name) and self.graph.isClose(name, sup_level):
                    self.logger.info("It worth to {mode} on {prize}"\
                        .format(mode=bold(green(buy)), price=bold(sup_level)))

    def start(self):
        self.graph.start()
        for y in range(2):
            time.sleep(60)
            self.getPivotPoints()
            for x in self.predict_stocks:
                self.isWorth(x.name)

    def stop(self):
        self.graph.stop()

class predictStock(object):
    def __init__(self, name):
        self.name = name
        self.prediction = 0
