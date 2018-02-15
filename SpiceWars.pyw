# -*- coding: cp1252 -*-

import tkinter, random, json
from tkinter import messagebox


# TODO: Use Gamelength

class SpiceWars(object):
    def __init__(self):
        config_file = open("config.json", "r")
        config = json.load(config_file)

        self._money = config['general']['startmoney']
        self._debts = config['general']['startdebts']
        self._maxdebts = config['general']['maxdebts']
        self._interest = config['general']['interest']
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

        self._holdspace = self._shiplevels["1"]["holdspace"]

        self._upgradeprice = random.randint(self._shiplevels[str(self._shiplevel + 1)]["pricemin"], self._shiplevels[str(self._shiplevel + 1)]["pricemax"])

    # print(self._shiplevels[str(1)]["pricemin"])

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


variables = SpiceWars()


def DisplayAktualisieren():
    LabelError.configure(text=variables.error)
    variables.error = ""

    Liste.delete("0", "end")
    ListeLaderaum.delete("0", "end")
    for item in variables.spices:
        Liste.insert("end", item + " " + str(variables.currentcost[item]))
        ListeLaderaum.insert("end", str(variables.owncharge[item]) + " Einheiten: " + item)

    Schiffsstatus.delete("0", "end")
    Schiffsstatus.insert("end", "Goldtaler: " + str(variables.money))
    Schiffsstatus.insert("end", "Schulden: " + str(variables.debts))
    Schiffsstatus.insert("end", "Platz im Laderaum: " + str(variables.holdspace))
    Schiffsstatus.insert("end", "--------------")
    Schiffsstatus.insert("end", "Aktuelles Level: " + str(variables.shiplevel))
    Schiffsstatus.insert("end", "Aktuelle Helferanzahl: " + str(variables.shiplevels[str(variables.shiplevel)]["shiphelper"]))
    Schiffsstatus.insert("end", "--------------")
    if variables.shiplevel + 1 <= variables.shiplevelcount:
        Schiffsstatus.insert("end", "Nächstes Level: " + str(variables.shiplevel + 1))
        Schiffsstatus.insert("end", "Upgrade Preis: " +str(variables.upgradeprice))

    ListeStaedte.delete("0", "end")
    for item in variables.harbours:
        ListeStaedte.insert("end", item)



def NeuesSpiel():
    variables.__init__()
    DisplayAktualisieren()


def kaufen():
    try:
        anzahl = int(EingabeMenge.get())
    except:
        variables.error = 'Keine Menge eingegeben'
        DisplayAktualisieren()
        return

    try:
        nummer = int(Liste.curselection()[0])
    except:
        variables.error = 'Kein Gewürz ausgewählt'
        DisplayAktualisieren()
        return

    if variables.holdspace >= anzahl:
        if variables.money >= variables.currentcost[variables.spices[nummer]] * anzahl:
            variables.holdspace = variables.holdspace - anzahl
            variables.money = variables.money - int(variables.currentcost[variables.spices[nummer]]) * anzahl
            variables.owncharge[variables.spices[nummer]] = variables.owncharge[variables.spices[nummer]] + anzahl
        else:
            variables.error = "Nicht genuegend Geld"
    else:
        variables.error = "Nicht genuegend Platz"
    EingabeMenge.delete(0, 'end')
    DisplayAktualisieren()


def verkaufen():
    try:
        anzahl = int(EingabeMenge.get())
    except:
        variables.error = "Keine Menge eingegeben"
        DisplayAktualisieren()
        return
    try:
        nummer = int(ListeLaderaum.curselection()[0])
    except:
        variables.error = "Kein Gewürz ausgewählt"
        DisplayAktualisieren()
        return

    if anzahl <= variables.owncharge[variables.spices[nummer]]:
        variables.holdspace = variables.holdspace + anzahl
        variables.money = variables.money + int(variables.currentcost[variables.spices[nummer]]) * anzahl
        variables.owncharge[variables.spices[nummer]] = variables.owncharge[variables.spices[nummer]] - anzahl
    EingabeMenge.delete(0, 'end')
    DisplayAktualisieren()


# TODO Zufaellige Kreditverweigerung

def leihen():
    try:
        menge = int(EingabeBetrag.get())
    except:
        messagebox.showinfo("- F E H L E R -", "Kein Betrag eingegeben")
        return
    if variables.debts < variables.maxdebts:
        if menge + variables.debts <= variables.maxdebts:
            variables.money += menge
            variables.debts += menge
            EingabeBetrag.delete(0, 'end')
        else:
            messagebox.showinfo("- F E H L E R -", "Leihsumme zu gross")
    else:
        messagebox.showinfo("- F E H L E R -", "Maximale Schulden erreicht")
    DisplayAktualisieren()


def zurueckzahlen():
    try:
        menge = int(EingabeBetrag.get())
    except:
        messagebox.showinfo("- F E H L E R -", "Kein Betrag eingegeben")
        return
    if menge > variables.debts:
        menge = variables.debts
    zuzahlen = menge + menge * (variables.interest / 100)
    if zuzahlen > 0:
        zuzahlen += 0.4
        zuzahlen = int(round(zuzahlen))

    if variables.money - zuzahlen >= 0:
        variables.money -= int(zuzahlen)
        variables.debts -= int(menge)
        EingabeBetrag.delete(0, 'end')
        DisplayAktualisieren()
    else:
        messagebox.showinfo("- F E H L E R -", "Nicht genuegend Geld")


# ERROR: Zum gleichen Hafen segeln -> Unsinnig
def Weitersegeln():
    nummer = 0
    try:
        nummer = int(ListeStaedte.curselection()[0])
    except:
        messagebox.showinfo("- F E H L E R -", "Keine Stadt ausgewählt")
        return
    stadt = ListeStaedte.get(nummer)
    messagebox.showinfo("- R E I S E I N F O -",
                        "Ihre Reise geht nach " + stadt + ".\n Der Wind steht gut.\n Sie brauchen 2 Wochen")

    for spice in variables.spices:
        variables.currentcost[spice] = random.randint(variables.mincost[spice], variables.maxcost[spice])
    DisplayAktualisieren()


def Upgrade():
    return


def Downgrade():
    return


# GUI ----------------------------------------
# Hauptfenster
Fenster = tkinter.Tk()
Fenster.title("SpiceWars")

# -------------------------
Liste = tkinter.Listbox(width=30, height=10)
Liste.grid(padx=5, pady=5, row=1, column=1, columnspan=1, rowspan=3)

LabelMenge = tkinter.Label(Fenster, text='Menge: ')
LabelMenge.grid(padx=5, pady=5, row=1, column=2)
EingabeMenge = tkinter.Entry(Fenster, width=4)
EingabeMenge.grid(padx=5, pady=5, row=1, column=3)

LabelError = tkinter.Label(Fenster, text='ERROR')
LabelError.grid(padx=5, pady=5, row=2, column=2)

ButtonKaufen = tkinter.Button(Fenster, text=' kaufen  >>> ', command=kaufen)
ButtonKaufen.grid(padx=5, pady=5, row=3, column=2, columnspan=2, sticky=tkinter.W + tkinter.E)
ButtonVerkaufen = tkinter.Button(Fenster, text=' <<< verkaufen ', command=verkaufen)
ButtonVerkaufen.grid(padx=5, pady=5, row=4, column=2, columnspan=2, sticky=tkinter.W + tkinter.E)

LabelBetrag = tkinter.Label(Fenster, text='Betrag: ')
LabelBetrag.grid(padx=35, pady=5, row=4, column=5, sticky=tkinter.W)
EingabeBetrag = tkinter.Entry(Fenster, width=4)
EingabeBetrag.grid(padx=5, pady=5, row=4, column=5)

ListeLaderaum = tkinter.Listbox(width=30, height=10)
ListeLaderaum.grid(padx=5, pady=5, row=1, column=5, columnspan=2, rowspan=3)

ButtonLeihen = tkinter.Button(Fenster, text=' Leihen <<< ', command=leihen)
ButtonLeihen.grid(row=5, padx=5, pady=25, column=2, columnspan=2, sticky=tkinter.W + tkinter.E)

ButtonZahlen = tkinter.Button(Fenster, text=' >>> Zurückzahlen ', command=zurueckzahlen)
ButtonZahlen.grid(row=5, padx=35, pady=25, column=5, sticky=tkinter.W + tkinter.E)
# -----------------------
ListeStaedte = tkinter.Listbox(width=30, height=6)
ListeStaedte.grid(padx=5, pady=20, row=4, column=1, columnspan=1, rowspan=3)

ButtonBewegen = tkinter.Button(Fenster, text=' weitersegeln ... ', command=Weitersegeln)
ButtonBewegen.grid(row=6, column=2, padx=5, pady=25, columnspan=2, sticky=tkinter.W + tkinter.E)

ButtonNeustart = tkinter.Button(Fenster, text=' neues Spiel ', command=NeuesSpiel)
ButtonNeustart.grid(row=6, column=5, padx=35, pady=25, sticky=tkinter.W + tkinter.E)

# Upgrades --------------

ListeUpgrades = tkinter.Listbox(width=30, height=10)
ListeUpgrades.grid(padx=5, pady=5, row=3, column=7, columnspan=2, rowspan=3)

UpgradeButton = tkinter.Button(Fenster, text='Verbessern', command=Upgrade)
UpgradeButton.grid(padx=5, pady=5, row=6, column=7, columnspan=1, rowspan=1)

DowngradeButton = tkinter.Button(Fenster, text='Abrüsten', command=Downgrade)
DowngradeButton.grid(padx=5, pady=5, row=6, column=8, columnspan=1, rowspan=1)
# ------------------------

# Schiffsstatus-----------
Schiffsstatus = tkinter.Listbox(width=30, height=5)
Schiffsstatus.grid(padx=5, pady=5, row=1, column=7, columnspan=2, rowspan=1)

NeuesSpiel()
# ---------------------
Fenster.mainloop()
