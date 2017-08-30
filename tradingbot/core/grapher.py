import time
from threading import Thread
from tradingAPI import API



class Grapher(object):
    def __init__(self, conf, logger):
        self.logger = logger
        self.logger.debug("Grapher initialized")
        self.api = API()
        self.config = conf
        self.monitor = conf.config['MONITOR']
        self.prefs = eval(self.monitor['stocks'])
        self.stocks = []
        self.terminate = False

    def _wait(self, interval, condition):
        while condition:
            for x in range(interval):
                time.sleep(1)
            break

    def start(self):
        self.api.launch()
        self.logger.debug("Launched browser")
        self.api.login(self.monitor['username'], self.monitor['password'])
        self.logger.debug("Logged in")
        if not int(self.monitor['initiated']):
            self.addPrefs()
        T1 = Thread(target=self.updatePrice)
        T2 = Thread(target=self.candlestickUpdate)
        T1.deamon = True
        T2.deamon = True
        T1.start()
        self.logger.debug("Price updater thread #1 launched")
        T2.start()
        self.logger.debug("Candlestick updater thread #2 launched")

    def stop(self):
        self.terminate = True
        self.api.logout()

    def addPrefs(self):
        self.api.clearPrefs()
        self.api.addPrefs(self.prefs)
        self.config.config['MONITOR']['initiated'] = '1'
        self.config.write()
        self.logger.debug('Preferencies added')

    def updatePrice(self):
        while self.terminate == False:
            self.api.checkStocks(self.prefs)
            time.sleep(1)

    def candlestickUpdate(self):
        while self.terminate == False:
            self._wait(60, self.terminate == False)
            for stock in self.api.stocks:
                if not [x for x in self.stocks if x.name == stock.name]:
                    self.stocks.append(CandlestickStock(stock.name))
                candle = [x for x in self.stocks if x.name == stock.name][0]
                prices = [var[1] for var in stock.vars]
                sent = [var[2] for var in stock.vars][-1]
                candle.addRecord(max(prices), min(prices), prices[0],
                                 prices[-1])
                candle.sentiment = sent
                self.api.stocks = []


class CandlestickStock(object):
    def __init__(self, name):
        self.name = name
        self.records = []

    def addRecord(self, openstock, maxstock, minstock, closestock):
        self.records.append([openstock, maxstock, minstock, closestock])