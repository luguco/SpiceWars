# -*- coding: cp1252 -*-

import sqlite3, tkinter, random
from tkinter import messagebox

Geld = 1000
Laderaum = 100
Gewuerze = ["Pfeffer", "Muskat", "Nelken", "Vanille", "Zimt"]
aktKosten = [100, 30, 50, 20, 10]
KostenMin = [50, 5, 20, 100, 60]
KostenMax = [150, 35, 170, 450, 300]
EigeneLadung = [0, 0, 0, 0, 0]


def DisplayAktualisieren():
    global Gewuerze
    global aktKosten
    global EigeneLadung
    global Geld
    global Laderaum
    Liste.delete("0", "end")
    Liste.insert("end", Gewuerze[0] + "  " + str(aktKosten[0]))
    Liste.insert("end", Gewuerze[1] + "  " + str(aktKosten[1]))
    Liste.insert("end", Gewuerze[2] + "  " + str(aktKosten[2]))
    Liste.insert("end", Gewuerze[3] + "  " + str(aktKosten[3]))
    Liste.insert("end", Gewuerze[4] + "  " + str(aktKosten[4]))

    ListeLaderaum.delete("0", "end")
    ListeLaderaum.insert("end", str(EigeneLadung[0]) + " Einheiten: " + str(Gewuerze[0]))
    ListeLaderaum.insert("end", str(EigeneLadung[1]) + " Einheiten: " + str(Gewuerze[1]))
    ListeLaderaum.insert("end", str(EigeneLadung[2]) + " Einheiten: " + str(Gewuerze[2]))
    ListeLaderaum.insert("end", str(EigeneLadung[3]) + " Einheiten: " + str(Gewuerze[3]))
    ListeLaderaum.insert("end", str(EigeneLadung[4]) + " Einheiten: " + str(Gewuerze[4]))
    ListeLaderaum.insert("end", "-------")
    ListeLaderaum.insert("end", "Goldtaler: " + str(Geld))
    ListeLaderaum.insert("end", "Platz im Laderaum: " + str(Laderaum))

    ListeStaedte.delete("0", "end")
    ListeStaedte.insert("end", "Alexandria")
    ListeStaedte.insert("end", "Tunesien")
    ListeStaedte.insert("end", "Venedig")
    ListeStaedte.insert("end", "Rom")
    ListeStaedte.insert("end", "Barcelona")


def NeuesSpiel():
    global aktKosten
    global EigeneLadung
    global Geld
    global Laderaum
    aktKosten = [100, 30, 50, 20, 10]
    EigeneLadung = [0, 0, 0, 0, 0]
    Geld = 1000
    Laderaum = 100
    DisplayAktualisieren()


def kaufen():
    global Geld
    global aktKosten
    global EigeneLadung
    global Laderaum
    Anzahl = int(EingabeMenge.get())
    Nummer = int(Liste.curselection()[0])
    if (Laderaum >= Anzahl) and (Geld >= aktKosten[Nummer] * Anzahl):
        Laderaum = Laderaum - Anzahl
        Geld = Geld - int(aktKosten[Nummer]) * Anzahl
        EigeneLadung[Nummer] = EigeneLadung[Nummer] + Anzahl
    DisplayAktualisieren()


def verkaufen():
    global Geld
    global aktKosten
    global EigeneLadung
    global ListeLaderaum
    global Laderaum
    Anzahl = int(EingabeMenge.get())
    Nummer = int(ListeLaderaum.curselection()[0])
    if (Anzahl <= EigeneLadung[Nummer]):
        Laderaum = Laderaum + Anzahl
        Geld = Geld + int(aktKosten[Nummer]) * Anzahl
        EigeneLadung[Nummer] = EigeneLadung[Nummer] - Anzahl
    DisplayAktualisieren()


def Weitersegeln():
    global ListeStaedte
    global aktKosten
    global KostenMin
    global KostenMax
    Nummer = int(ListeStaedte.curselection()[0])
    Stadt = ListeStaedte.get(Nummer)
    messagebox.showinfo("- R E I S E I N F O -",
                        "Ihre Reise geht nach " + Stadt + ".\n Der Wind steht gut.\n Sie brauchen 2 Wochen")
    for i in range(5):
        # KostenDifferenz = KostenMax[i]-KostenMin[i]
        aktKosten[i] = random.randint(KostenMin[i], KostenMax[i])
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

ButtonKaufen = tkinter.Button(Fenster, text=' kaufen  >>> ', command=kaufen)
ButtonKaufen.grid(padx=5, pady=5, row=2, column=2, columnspan=2)
ButtonVerkaufen = tkinter.Button(Fenster, text=' <<< verkaufen ', command=verkaufen)
ButtonVerkaufen.grid(padx=5, pady=5, row=3, column=2, columnspan=2)

ListeLaderaum = tkinter.Listbox(width=30, height=10)
ListeLaderaum.grid(padx=5, pady=5, row=1, column=5, columnspan=2, rowspan=3)

# -----------------------
ListeStaedte = tkinter.Listbox(width=30, height=6)
ListeStaedte.grid(padx=5, pady=20, row=4, column=1, columnspan=1, rowspan=3)

ButtonBewegen = tkinter.Button(Fenster, text=' weitersegeln ... ', command=Weitersegeln)
ButtonBewegen.grid(row=4, column=2, padx=5, pady=25, columnspan=2)

ButtonNeustart = tkinter.Button(Fenster, text=' neues Spiel ', command=NeuesSpiel)
ButtonNeustart.grid(row=4, column=5, padx=5, pady=25)

NeuesSpiel()
# ---------------------
Fenster.mainloop()
