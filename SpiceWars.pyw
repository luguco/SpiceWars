# -*- coding: cp1252 -*-

import pymysql, tkinter, random, json
from tkinter import messagebox

config_file = open("config.json", "r")
config = json.load(config_file)

Geld = config['general']['startmoney']
Laderaum = config['general']['holdspace']

Gewuerze = []
aktKosten = {}
KostenMin = {}
KostenMax = {}
EigeneLadung = {}
Haefen = []
Error = ''

# TODO: Vairableninziierung in eigene Funktion
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
    ListeLaderaum.insert("end", "Platz im Laderaum: " + str(Laderaum))

    ListeStaedte.delete("0", "end")
    for item in Haefen:
        ListeStaedte.insert("end", item)


def NeuesSpiel():
    global aktKosten
    global EigeneLadung
    global Geld
    global Laderaum
    # aktKosten = [100, 30, 50, 20, 10]
    # EigeneLadung = [0, 0, 0, 0, 0]
    # Geld = 1000
    # Laderaum = 100
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
ButtonKaufen.grid(padx=5, pady=5, row=3, column=2, columnspan=2)
ButtonVerkaufen = tkinter.Button(Fenster, text=' <<< verkaufen ', command=verkaufen)
ButtonVerkaufen.grid(padx=5, pady=5, row=4, column=2, columnspan=2)

ListeLaderaum = tkinter.Listbox(width=30, height=10)
ListeLaderaum.grid(padx=5, pady=5, row=1, column=5, columnspan=2, rowspan=3)

# -----------------------
ListeStaedte = tkinter.Listbox(width=30, height=6)
ListeStaedte.grid(padx=5, pady=20, row=4, column=1, columnspan=1, rowspan=3)

ButtonBewegen = tkinter.Button(Fenster, text=' weitersegeln ... ', command=Weitersegeln)
ButtonBewegen.grid(row=5, column=2, padx=5, pady=25, columnspan=2)

ButtonNeustart = tkinter.Button(Fenster, text=' neues Spiel ', command=NeuesSpiel)
ButtonNeustart.grid(row=5, column=5, padx=5, pady=25)

NeuesSpiel()
# ---------------------
Fenster.mainloop()
