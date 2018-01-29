# -*- coding: cp1252 -*-

import pymysql, tkinter, random, json
from tkinter import messagebox

config_file = open("config.json", "r")
config = json.load(config_file)

Geld = 0
Schulden = 0
Laderaum = 0
MaxSchulden = 0
Zinsen = 0

Gewuerze = []
aktKosten = {}
KostenMin = {}
KostenMax = {}
EigeneLadung = {}
Haefen = []
Error = ''


# TODO: Vairableninziierung in eigene Funktion
def variableinitiation():
    global Geld
    global Laderaum
    global Schulden
    global MaxSchulden
    global Zinsen

    Geld = config['general']['startmoney']
    Schulden = config['general']['startdebts']
    MaxSchulden = config['general']['maxdebts']
    Laderaum = config['general']['holdspace']
    Zinsen = config['general']['interest']

    for spice, values in config['spices'].items():
        Gewuerze.append(spice)
        KostenMin[spice] = values['pricemin']
        KostenMax[spice] = values['pricemax']
        EigeneLadung[spice] = values['startvolume']
        aktKosten[spice] = values['startprice']

    for harbour in config['harbours']:
        Haefen.append(harbour)


def DisplayAktualisieren():
    global Gewuerze
    global aktKosten
    global EigeneLadung
    global Geld
    global Schulden
    global Laderaum
    global Haefen
    global Error

    LabelError.configure(text=Error)
    Error = ''

    Liste.delete("0", "end")
    for item in Gewuerze:
        Liste.insert("end", item + " " + str(aktKosten[item]))

    ListeLaderaum.delete("0", "end")
    for item in Gewuerze:
        ListeLaderaum.insert("end", str(EigeneLadung[item]) + " Einheiten: " + item)

    ListeLaderaum.insert("end", "-------")
    ListeLaderaum.insert("end", "Goldtaler: " + str(Geld))
    ListeLaderaum.insert("end", "Schulden: " + str(Schulden))
    ListeLaderaum.insert("end", "Platz im Laderaum: " + str(Laderaum))

    ListeStaedte.delete("0", "end")
    for item in Haefen:
        ListeStaedte.insert("end", item)


def NeuesSpiel():
    global aktKosten
    global EigeneLadung
    global Geld
    global Laderaum
    variableinitiation()
    DisplayAktualisieren()


# ERROR: Keine Auswahl von Gewürzen = Error
# FIXME: Besseres Errorhandling
def kaufen():
    global Geld
    global Gewuerze
    global aktKosten
    global EigeneLadung
    global Laderaum
    global Error

    anzahl = 0
    nummer = 0
    try:
        anzahl = int(EingabeMenge.get())
    except:
        Error = 'Keine Eingabemenge'

    try:
        nummer = int(Liste.curselection()[0])
    except:
        Error = 'Kein Gewürz'

    if (Laderaum >= anzahl) and (Geld >= aktKosten[Gewuerze[nummer]] * anzahl):
        Laderaum = Laderaum - anzahl
        Geld = Geld - int(aktKosten[Gewuerze[nummer]]) * anzahl
        EigeneLadung[Gewuerze[nummer]] = EigeneLadung[Gewuerze[nummer]] + anzahl
    EingabeMenge.delete(0, 'end')
    DisplayAktualisieren()


# ERROR Kein Errorhandling
def verkaufen():
    global Geld
    global Gewuerze
    global aktKosten
    global EigeneLadung
    global ListeLaderaum
    global Laderaum
    anzahl = 0
    nummer = 0
    anzahl = int(EingabeMenge.get())
    nummer = int(ListeLaderaum.curselection()[0])

    if anzahl <= EigeneLadung[Gewuerze[nummer]]:
        Laderaum = Laderaum + anzahl
        Geld = Geld + int(aktKosten[Gewuerze[nummer]]) * anzahl
        EigeneLadung[Gewuerze[nummer]] = EigeneLadung[Gewuerze[nummer]] - anzahl
    EingabeMenge.delete(0, 'end')
    DisplayAktualisieren()

# ERROR Kein Errorhandling
# TODO Zufaellige Kreditverweigerung

def leihen():
    global Geld
    global Schulden
    global MaxSchulden

    menge = int(EingabeBetrag.get())
    if Schulden < MaxSchulden:
        if menge + Schulden <= MaxSchulden:
            Geld = Geld + menge
            Schulden = Schulden + menge
            EingabeBetrag.delete(0, 'end')
        else:
            messagebox.showinfo("Fehler", "Leihsumme zu gross")
    else:
        messagebox.showinfo("Fehler", "Maximale Schulden erreicht")
    DisplayAktualisieren()


def zurueckzahlen():
    global Geld
    global Schulden
    global Zinsen

    menge = int(EingabeBetrag.get())
    zuzahlen = menge + menge * (Zinsen / 100)
    zuzahlen = int(zuzahlen)

    if Geld - zuzahlen >= 0:
        Geld = Geld - zuzahlen
        Schulden = Schulden - menge
        EingabeBetrag.delete(0, 'end')
        DisplayAktualisieren()
    else:
        messagebox.showinfo("Fehler", "Nicht genuegend Geld")


# ERROR Kein Errorhandling
def Weitersegeln():
    global ListeStaedte
    global Gewuerze
    global aktKosten
    global KostenMin
    global KostenMax
    nummer = int(ListeStaedte.curselection()[0])
    stadt = ListeStaedte.get(nummer)
    messagebox.showinfo("- R E I S E I N F O -",
                        "Ihre Reise geht nach " + stadt + ".\n Der Wind steht gut.\n Sie brauchen 2 Wochen")

    for spice in Gewuerze:
        # KostenDifferenz = KostenMax[i]-KostenMin[i]
        aktKosten[spice] = random.randint(KostenMin[spice], KostenMax[spice])
    DisplayAktualisieren()


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

NeuesSpiel()
# ---------------------
Fenster.mainloop()
