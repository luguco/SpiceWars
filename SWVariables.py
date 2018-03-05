import json, random


class SpiceWars(object):
    def __init__(self):
        config_file = open("config.json", "r")
        config = json.load(config_file)

        self._money = config['general']['startmoney']
        self._debts = config['general']['startdebts']
        self._maxdebts = config['general']['maxdebts']
        self._interest = config['general']['interest']
        self._cost_shiphelper = config['general']['cost_shiphelper']
        self._remainlength = config['general']['gamelength'] * 7
        self._event_probability = config['general']['event_probability']
        self._currentlength = 0
        self._spices = []
        self._currentcost = {}
        self._mincost = {}
        self._maxcost = {}
        self._owncharge = {}
        self._harbours = []
        self._error = ""
        self._shiplevels = {}
        self._shiplevelcount = 0
        self._shiplevel = 1
        self._upgradeprice = 0
        self._shiphelper = 0
        self._actualhabour = "Heimhafen"
        self._events = {}

        for spice, values in config['spices'].items():
            self._spices.append(spice)
            self._mincost[spice] = values['pricemin']
            self._maxcost[spice] = values['pricemax']
            self._owncharge[spice] = values['startvolume']
            self._currentcost[spice] = values['startprice']

        for harbour in config['harbours']:
            self._harbours.append(harbour)

        for shiplevel, values in config['shiplevel'].items():
            self._shiplevels[shiplevel] = values
            self._shiplevelcount += 1
            
        for event, values in config['events'].items():
            self._events[event] = values
            
        self._holdspace = self._shiplevels["1"]["holdspace"]

        self._upgradeprice = random.randint(self._shiplevels[str(self._shiplevel + 1)]["pricemin"],
                                            self._shiplevels[str(self._shiplevel + 1)]["pricemax"])

        #print(self._events)

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        self._money = value

    @property
    def debts(self):
        return self._debts

    @debts.setter
    def debts(self, value):
        self._debts = value

    @property
    def holdspace(self):
        return self._holdspace

    @holdspace.setter
    def holdspace(self, value):
        self._holdspace = value

    @property
    def maxdebts(self):
        return self._maxdebts

    # FIXME: Unused
    @maxdebts.setter
    def maxdebts(self, value):
        self._maxdebts = value

    @property
    def interest(self):
        return self._interest

    # FIXME: Unused
    @interest.setter
    def interest(self, value):
        self._interest = value

    @property
    def spices(self):
        return self._spices

    @spices.setter
    def spices(self, value):
        self._spices = value

    @property
    def currentcost(self):
        return self._currentcost

    @currentcost.setter
    def currentcost(self, value):
        self._currentcost = value

    @property
    def mincost(self):
        return self._mincost

    @mincost.setter
    def mincost(self, value):
        self._mincost = value

    @property
    def maxcost(self):
        return self._maxcost

    @maxcost.setter
    def maxcost(self, value):
        self._maxcost = value

    @property
    def owncharge(self):
        return self._owncharge

    @owncharge.setter
    def owncharge(self, value):
        self._owncharge = value

    @property
    def harbours(self):
        return self._harbours

    # FIXME: Unused
    @harbours.setter
    def harbours(self, value):
        self._harbours = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    @property
    def shiplevel(self):
        return self._shiplevel

    @shiplevel.setter
    def shiplevel(self, value):
        self._shiplevel = value

    @property
    def shiplevels(self):
        return self._shiplevels

    # FIXME Unused
    @shiplevels.setter
    def shiplevels(self, value):
        self._shiplevels = value

    @property
    def shiplevelcount(self):
        return self._shiplevelcount

    # FIXME Unused
    @shiplevelcount.setter
    def shiplevelcount(self, value):
        self._shiplevelcount = value

    @property
    def upgradeprice(self):
        return self._upgradeprice

    @upgradeprice.setter
    def upgradeprice(self, value):
        self._upgradeprice = value

    @property
    def shiphelper(self):
        return self._shiphelper

    @shiphelper.setter
    def shiphelper(self, value):
        self._shiphelper = value

    @property
    def cost_shiphelper(self):
        return self._cost_shiphelper

    @cost_shiphelper.setter
    def cost_shiphelper(self, value):
        self._cost_shiphelper = value

    @property
    def remainlength(self):
        return self._remainlength

    @remainlength.setter
    def remainlength(self, value):
        self._remainlength = value

    @property
    def currentlength(self):
        return self._currentlength

    @currentlength.setter
    def currentlength(self, value):
        self._currentlength = value

    @property
    def actualhabour(self):
        return self._actualhabour

    @actualhabour.setter
    def actualhabour(self, value):
        self._actualhabour = value

    @property
    def events(self):
        return self._events

    @property
    def event_probability(self):
        return self._event_probability
