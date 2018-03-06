# -*- coding: cp1252 -*-

import tkinter, random, SWVariables as sw
from tkinter import messagebox

# Initierung der Variablen-Klasse
variables = sw.SpiceWars()


def DisplayAktualisieren():
    if variables.remainlength <= 0:
        messagebox.showinfo("- I N F O -",
                            "Herzlichen Glückwunsch!\nDas Spiel ist beendet!\n\nDu hast folgendes erreicht:\nGeld: " + str(
                                variables.money) + "\nSchulden: " + str(variables.debts) + "\nLevel: " + str(
                                variables.shiplevel) + "\nHelfer: " + str(variables.shiphelper))

    LabelError.configure(text=variables.error)
    variables.error = ""
    LabelZeit.configure(text="Spielzeit: " + str(int(variables.currentlength)) + " Tage")
    LabelRestzeit.configure(text="Restzeit: " + str(int(variables.remainlength)) + " Tage")
    Liste.delete("0", "end")
    ListeLaderaum.delete("0", "end")
    for item in variables.spices:
        Liste.insert("end", item + " " + str(variables.currentcost[item]))
        ListeLaderaum.insert("end", str(variables.owncharge[item]) + " Einheiten: " + item)

    Schiffsstatus.delete("0", "end")
    Schiffsstatus.insert("end", "Goldtaler: " + str(variables.money))
    Schiffsstatus.insert("end", "Schulden: " + str(variables.debts))
    Schiffsstatus.insert("end", "Platz im Laderaum: " + str(variables.holdspace))
    Schiffsstatus.insert("end", "Hafen: " + str(variables.actualhabour))
    Schiffsstatus.insert("end", "--------------")
    Schiffsstatus.insert("end", "Aktuelles Level: " + str(variables.shiplevel))
    Schiffsstatus.insert("end", "Aktuelle Helferanzahl: " + str(variables.shiphelper))
    Schiffsstatus.insert("end",
                         "Max Helferanzahl: " + str(variables.shiplevels[str(variables.shiplevel)]["shiphelper"]))
    Schiffsstatus.insert("end", "--------------")
    if variables.shiplevel + 1 <= variables.shiplevelcount:
        Schiffsstatus.insert("end", "Nächstes Level: " + str(variables.shiplevel + 1))
        Schiffsstatus.insert("end", "Upgrade Preis: " + str(variables.upgradeprice))

    ListeUpgrades.delete("0", "end")
    ListeUpgrades.insert("end", "Schiff")
    ListeUpgrades.insert("end", "Helfer")

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
    if anzahl < 1:
        messagebox.showinfo("- F E H L E R -", "Zu geringe Menge")
        return
    if variables.holdspace >= anzahl:
        if variables.money >= variables.currentcost[variables.spices[nummer]] * anzahl:
            variables.holdspace = variables.holdspace - anzahl
            variables.money = variables.money - int(variables.currentcost[variables.spices[nummer]]) * anzahl
            working = True
            while working:
                if anzahl > variables.shiphelper + 1:
                    add = variables.shiphelper + 1
                    anzahl -= add
                else:
                    add = anzahl
                    anzahl -= add
                    working = False
                variables.remainlength -= 0.2
                variables.currentlength += 0.2
                variables.owncharge[variables.spices[nummer]] = variables.owncharge[variables.spices[nummer]] + add
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

    if anzahl < 1:
        messagebox.showinfo("- F E H L E R -", "Zu geringe Menge")
        return

    if anzahl <= variables.owncharge[variables.spices[nummer]]:
        variables.holdspace = variables.holdspace + anzahl
        variables.money = variables.money + int(variables.currentcost[variables.spices[nummer]]) * anzahl
        working = True
        while working:
            if anzahl > variables.shiphelper + 1:
                remove = variables.shiphelper + 1
                anzahl -= remove
            else:
                remove = anzahl
                anzahl -= remove
                working = False
            variables.remainlength -= 0.2
            variables.currentlength += 0.2
            variables.owncharge[variables.spices[nummer]] = variables.owncharge[variables.spices[nummer]] - remove
    EingabeMenge.delete(0, 'end')
    DisplayAktualisieren()


# TODO Zufaellige Kreditverweigerung

def leihen():
    try:
        menge = int(EingabeBetrag.get())
    except:
        messagebox.showinfo("- F E H L E R -", "Kein Betrag eingegeben")
        return

    if menge < 1:
        messagebox.showinfo("- F E H L E R -", "Zu geringer Betrag")
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

    if menge < 1:
        messagebox.showinfo("- F E H L E R -", "Zu geringer Betrag")
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


def Weitersegeln():
    try:
        nummer = int(ListeStaedte.curselection()[0])
    except:
        messagebox.showinfo("- F E H L E R -", "Keine Stadt ausgewählt")
        return
    stadt = ListeStaedte.get(nummer)
    if variables.actualhabour == stadt:
        messagebox.showinfo("- F E H L E R -", "Du bist bereits in diesem Hafen")
        return

    variables.actualhabour = stadt
    EventManager()
    DisplayAktualisieren()


def Upgrade():
    try:
        nummer = int(ListeUpgrades.curselection()[0])
    except:
        messagebox.showinfo("- F E H L E R -", "Nichts ausgewählt")
        return
    if nummer == 0:
        if variables.shiplevel + 1 <= variables.shiplevelcount:
            if variables.money >= variables.upgradeprice:
                variables.shiplevel += 1
                variables.holdspace = variables.shiplevels[str(variables.shiplevel)]['holdspace']
                variables.money -= variables.upgradeprice

                if variables.shiplevel + 1 <= variables.shiplevelcount:
                    variables.upgradeprice = random.randint(
                        variables.shiplevels[str(variables.shiplevel + 1)]["pricemin"],
                        variables.shiplevels[str(variables.shiplevel + 1)]["pricemax"])
            else:
                messagebox.showinfo("- F E H L E R -", "Nicht genügend Geld")
        else:
            messagebox.showinfo("- F E H L E R -", "Maximale Upgradestufe erreicht!")
    elif nummer == 1:
        if variables.shiphelper < variables.shiplevels[str(variables.shiplevel)]["shiphelper"]:
            if variables.money >= variables.cost_shiphelper:
                variables.shiphelper += 1
                variables.money -= variables.cost_shiphelper
            else:
                messagebox.showinfo("- F E H L E R-", "Nicht genügend Geld")
        else:
            messagebox.showinfo("- F E H L E R -", "Maximale Helferanzahl erreicht")
    DisplayAktualisieren()


def Downgrade():
    try:
        nummer = int(ListeUpgrades.curselection()[0])
    except:
        messagebox.showinfo("- F E H L E R -", "Nichts ausgewählt")
        return
    if nummer == 0:
        if variables.shiplevel > 1:
            variables.shiplevel -= 1
            variables.holdspace = variables.shiplevels[str(variables.shiplevel)]['holdspace']
            variables.money += int((random.randint(
                variables.shiplevels[str(variables.shiplevel + 1)]["pricemin"],
                variables.shiplevels[str(variables.shiplevel + 1)]["pricemax"]) / 30))

            variables.upgradeprice = random.randint(
                variables.shiplevels[str(variables.shiplevel + 1)]["pricemin"],
                variables.shiplevels[str(variables.shiplevel + 1)]["pricemax"])
        else:
            messagebox.showinfo("- F E H L E R -", "Kein Downgrade moeglich")
    elif nummer == 1:
        if variables.shiphelper > 0:
            variables.shiphelper -= 1
        else:
            messagebox.showinfo("- F E H L E R -", "Du hast keine Helfer")
    DisplayAktualisieren()


def EventManager():
    # Neuen Gewürzepreis festlegen
    for spice in variables.spices:
        variables.currentcost[spice] = random.randint(variables.mincost[spice], variables.maxcost[spice])
    # Neuen Schiffslevelpreis Festlegen
    if variables.shiplevel + 1 <= variables.shiplevelcount:
        variables.upgradeprice = random.randint(variables.shiplevels[str(variables.shiplevel + 1)]["pricemin"],
                                                variables.shiplevels[str(variables.shiplevel + 1)]["pricemax"])

    keys = list(variables.events.keys())
    random.shuffle(keys)
    for eventnr in keys:

        rand = random.randint(1, 100)
        if rand <= 100 * variables.event_probability:
            event = variables.events[eventnr]
            labeltext = "<<<Events>>>"
            labeltext = labeltext + "\n" + event['eventname']

            messagebox.showinfo("- R E I S E I N F O -",
                                "Ihre Reise geht nach " + variables.actualhabour + "\nDas Event '" + event[
                                    'eventname'] + "' findet statt")

            for spice in variables.spices:
                variables.currentcost[spice] = int(variables.currentcost[spice] * event['cost_multiplier'])

            for helper in range(0, variables.shiphelper):
                if variables.money >= 200 * event['cost_shiphelper_mulitplier']:
                    variables.money -= 200 * event['cost_shiphelper_mulitplier']
                else:
                    variables.shiphelper -= 1
                    messagebox.showinfo("- I N F O -",
                                        "Ein Helfer hat gekündigt, nachdem du ihn\nnicht mehr bezahlen konntest")

            if variables.shiplevel + 1 <= variables.shiplevelcount:
                variables.upgradeprice = int(variables.upgradeprice * event['cost_shipupgrade_multiplier'])

            rand = random.randint(1, 100)
            if rand <= 100 * event['attack_probability']:
                labeltext = labeltext + "\nGestohlenes Geld: " + str(int(variables.money * event['stolen_money']))
                variables.money -= int(variables.money * event['stolen_money'])

                labeltext = labeltext + "\nGestohlene Helfer: " + str(
                    int(variables.shiphelper * event['stolen_helper']))
                variables.shiphelper -= int(variables.shiphelper * event['stolen_helper'])

                labeltext = labeltext + "\nTote Helfer: " + str(int(variables.shiphelper * event['dead_helper']))
                variables.shiphelper -= int(variables.shiphelper * event['dead_helper'])

            UeberschriftEvents.configure(text=labeltext)
            rand = random.randint(1, 100)

            variables.remainlength -= int(14 * event['travelspeed_multiplier'])
            variables.currentlength += int(14 * event['travelspeed_multiplier'])

            if rand <= 100 * event['you_are_dead']:
                messagebox.showinfo("- E V E N T -", "Du bist tod")
                variables.remainlength = 0

            return

    UeberschriftEvents.configure(text="<<<Events>>>")
    messagebox.showinfo("- R E I S E I N F O -",
                        "Ihre Reise geht nach " + variables.actualhabour)
    # Reisezeit berechnen
    variables.remainlength -= 14
    variables.currentlength += 14
    # Schiffshelfer bezahlen
    for helper in range(0, variables.shiphelper):
        if variables.money >= 200:
            variables.money -= 200
        else:
            variables.shiphelper -= 1
            messagebox.showinfo("- I N F O -",
                                "Ein Helfer hat gekündigt, nachdem du ihn\nnicht mehr bezahlen konntest")


# GUI ----------------------------------------
# Hauptfenster
Fenster = tkinter.Tk()
Fenster.title("SpiceWars")

# Gewürze-------------------------
LabelGewuerze = tkinter.Label(Fenster, width=30, height=15)
LabelGewuerze.grid(padx=5, pady=5, row=1, column=1, columnspan=1, rowspan=1)

UeberschriftListe = tkinter.Label(LabelGewuerze, width=20, height=1, text='<<<Gewuerze>>>')
UeberschriftListe.grid(padx=5, pady=1, row=1, column=1, columnspan=1, rowspan=1)

Liste = tkinter.Listbox(LabelGewuerze, width=30, height=10)
Liste.grid(padx=5, pady=5, row=2, column=1, columnspan=1, rowspan=3)
# Handel---------------------------
LabelHandel = tkinter.Label(Fenster, width=30, height=15)
LabelHandel.grid(padx=5, pady=5, row=1, column=2, columnspan=1, rowspan=1)

UeberschriftHandel = tkinter.Label(LabelHandel, width=20, height=1, text='<<<Handel>>>')
UeberschriftHandel.grid(padx=5, pady=5, row=1, column=1, columnspan=2, rowspan=1)

LabelMenge = tkinter.Label(LabelHandel, text='Menge: ')
LabelMenge.grid(padx=5, pady=5, row=2, column=1, columnspan=1, rowspan=1)

EingabeMenge = tkinter.Entry(LabelHandel, width=4)
EingabeMenge.grid(padx=5, pady=5, row=2, column=2, columnspan=1, rowspan=1)

LabelError = tkinter.Label(LabelHandel, width=20, text='ERROR')
LabelError.grid(padx=5, pady=5, row=3, column=1)

ButtonKaufen = tkinter.Button(LabelHandel, text=' kaufen >>> ', command=kaufen)
ButtonKaufen.grid(padx=5, pady=5, row=4, column=1, columnspan=2, sticky=tkinter.W + tkinter.E)

ButtonVerkaufen = tkinter.Button(LabelHandel, text=' <<< verkaufen ', command=verkaufen)
ButtonVerkaufen.grid(padx=5, pady=5, row=5, column=1, columnspan=2, sticky=tkinter.W + tkinter.E)

# Laderaum--------------------------
LabelLaderaum = tkinter.Label(Fenster, width=30, height=10)
LabelLaderaum.grid(padx=5, pady=5, row=1, column=3, columnspan=1, rowspan=1)

UeberschriftLaderaum = tkinter.Label(LabelLaderaum, width=20, height=1, text='<<<Laderaum>>>')
UeberschriftLaderaum.grid(padx=5, pady=1, row=1, column=5, columnspan=2, rowspan=1)

ListeLaderaum = tkinter.Listbox(LabelLaderaum, width=30, height=10)
ListeLaderaum.grid(padx=5, pady=5, row=2, column=5, columnspan=2, rowspan=3)

# Schiffsstatus-----------
LabelSchiffsstatus = tkinter.Label(Fenster, width=30, height=10)
LabelSchiffsstatus.grid(padx=5, pady=5, row=1, column=4, columnspan=1, rowspan=1)

UeberschriftSchiffsstatus = tkinter.Label(LabelSchiffsstatus, width=20, height=1, text='<<<Status>>>')
UeberschriftSchiffsstatus.grid(padx=5, pady=1, row=1, column=1, columnspan=1, rowspan=1)

Schiffsstatus = tkinter.Listbox(LabelSchiffsstatus, width=30, height=10)
Schiffsstatus.grid(padx=5, pady=5, row=2, column=1, columnspan=1, rowspan=1)

# Spielzeit------------------------- #Evtl 30sec=1 Tag und die Reisezeit wird trotzdem hinzugefügt
# TODO: Die Spielzeit musst du noch einbauen und die übrige berechnen lassen
LabelSpielzeit = tkinter.Label(Fenster, width=30, height=10)
LabelSpielzeit.grid(padx=5, pady=5, row=1, column=5, columnspan=1, rowspan=1)

UeberschriftSpielzeit = tkinter.Label(LabelSpielzeit, width=20, height=5, text='<<<Zeit>>>')
UeberschriftSpielzeit.grid(padx=5, pady=1, row=1, column=1, columnspan=1, rowspan=1)

LabelZeit = tkinter.Label(LabelSpielzeit, width=25, height=2, text='Spielzeit: \n')
LabelZeit.grid(padx=5, pady=5, row=2, column=1, columnspan=1, rowspan=1)

LabelRestzeit = tkinter.Label(LabelSpielzeit, width=25, height=2, text='Restzeit: \n ')
LabelRestzeit.grid(padx=5, pady=5, row=3, column=1, columnspan=1, rowspan=1)

# Bank----------------------------- #Eigenes Konto auf der Bank?
LabelBank = tkinter.Label(Fenster, width=30, height=10)
LabelBank.grid(padx=5, pady=5, row=2, column=1, columnspan=1, rowspan=1)

UeberschriftBank = tkinter.Label(LabelBank, width=20, height=1, text='<<<Bank>>>')
UeberschriftBank.grid(padx=5, pady=5, row=1, column=1, columnspan=2, rowspan=1)

LabelBetrag = tkinter.Label(LabelBank, text='Betrag: ')
LabelBetrag.grid(padx=5, pady=5, row=2, column=1, columnspan=1, sticky=tkinter.W)

EingabeBetrag = tkinter.Entry(LabelBank, width=4)
EingabeBetrag.grid(padx=5, pady=5, row=2, column=2, columnspan=1)

ButtonLeihen = tkinter.Button(LabelBank, text=' Leihen <<< ', command=leihen)
ButtonLeihen.grid(padx=5, pady=5, row=3, column=1, columnspan=1, rowspan=1, sticky=tkinter.W + tkinter.E)

ButtonZahlen = tkinter.Button(LabelBank, text=' >>> Zurückzahlen ', command=zurueckzahlen)
ButtonZahlen.grid(padx=5, pady=5, row=3, column=2, columnspan=1, rowspan=1, sticky=tkinter.W + tkinter.E)

# Events-----------------------------
LabelEvents = tkinter.Label(Fenster, width=30, height=10)
LabelEvents.grid(padx=5, pady=5, row=2, column=2, columnspan=1, rowspan=1)

UeberschriftEvents = tkinter.Label(LabelEvents, width=20, height=5, text='<<<Events>>>')
UeberschriftEvents.grid(padx=5, pady=5, row=1, column=1, columnspan=2, rowspan=1)

# Segeln ---------------------------
LabelSegeln = tkinter.Label(Fenster, width=30, height=10)
LabelSegeln.grid(padx=5, pady=5, row=2, column=3, columnspan=1, rowspan=1)

UeberschriftStaedte = tkinter.Label(LabelSegeln, width=20, height=1, text='<<<Reiseziele>>')
UeberschriftStaedte.grid(padx=5, pady=5, row=1, column=1, columnspan=2, rowspan=1)

ListeStaedte = tkinter.Listbox(LabelSegeln, width=30, height=8)
ListeStaedte.grid(padx=5, pady=5, row=2, column=1, columnspan=2, rowspan=1)

ButtonSegeln = tkinter.Button(LabelSegeln, text=' weitersegeln ... ', command=Weitersegeln)
ButtonSegeln.grid(padx=5, pady=5, row=3, column=1, columnspan=2, sticky=tkinter.W + tkinter.E)

# Upgrades ------------------------
LabelUpgrades = tkinter.Label(Fenster, width=30, height=10)
LabelUpgrades.grid(padx=5, pady=5, row=2, column=4, columnspan=1, rowspan=1)

UeberschriftUpgrades = tkinter.Label(LabelUpgrades, width=20, height=1, text='<<<Verbesserungen>>>')
UeberschriftUpgrades.grid(padx=5, pady=5, row=1, column=1, columnspan=2, rowspan=1)

ListeUpgrades = tkinter.Listbox(LabelUpgrades, width=30, height=8)
ListeUpgrades.grid(padx=5, pady=5, row=2, column=1, columnspan=2, rowspan=1)

UpgradeButton = tkinter.Button(LabelUpgrades, text='Upgrade', command=Upgrade)
UpgradeButton.grid(padx=5, pady=5, row=3, column=1, columnspan=1, rowspan=1)

DowngradeButton = tkinter.Button(LabelUpgrades, text='Downgrade', command=Downgrade)
DowngradeButton.grid(padx=5, pady=5, row=3, column=2, columnspan=1, rowspan=1)
# ------------------------


# Neues Spiel-----------------------
ButtonNeustart = tkinter.Button(Fenster, text=' neues Spiel ', command=NeuesSpiel)
ButtonNeustart.grid(row=2, column=5, padx=35, pady=25, sticky=tkinter.W + tkinter.E)

# ---------------------
NeuesSpiel()
# ---------------------
Fenster.mainloop()
