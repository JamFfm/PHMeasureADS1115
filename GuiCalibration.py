#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from Tkinter import *


# Die folgende Funktion soll ausgeführt werden, wenn
# der Benutzer den Button anklickt


def button_action():
    factor = round((float(ph7voltage_enter.get()) - float(ph401voltage_enter.get())) / 2.99, 5)
    result_label.config(text="The Voltage per pH factor is "+str(factor)+".\n\
    Put it in the formula in line 114 of the file __init__.py :\n\
    (7 + (("+str(float(ph7voltage_enter.get()))+"- voltage) / "+str(-1*factor)+"))")


# Ein Fenster erstellen
fenster = Tk()
# Den Fenstertitle erstellen
fenster.title("determine the factor")

# Buttons erstellen.
calculate_button = Button(fenster, text="Calculate", command=button_action)
exit_button = Button(fenster, text="Exit", command=fenster.quit)

# Label erstellen

info_label = Label(fenster, text="Please input the values to determine your Factor")

ph7voltage_label = Label(fenster,
                         text="Put in the measured voltage while producing a shortcut between inner pole and outer area of the "
                              "BNC. This presents voltage at pH 7. Format x.xxx:  ")

ph401voltage_label = Label(fenster, text="Put in the measured voltage while measuring the buffer pH 4.01. Format "
                                           "x.xxx:")

result_label = Label(fenster, text="press calculate")

space_label1 = Label(fenster)
space_label2 = Label(fenster)
space_label3 = Label(fenster)

# Eingabe erstellen
ph7voltage_enter = Entry(fenster, bd=5, width=5)

ph401voltage_enter = Entry(fenster, bd=5, width=5)


# Nun fügen wir die Komponenten unserem Fenster
# in der gwünschten Reihenfolge hinzu.
info_label.pack()
space_label1.pack()
ph7voltage_label.pack()
ph7voltage_enter.pack()
ph401voltage_label.pack()
ph401voltage_enter.pack()
space_label2.pack()
result_label.pack()
space_label3.pack()
calculate_button.pack()
exit_button.pack()
# In der Ereignisschleife auf Eingabe des Benutzers warten.
fenster.mainloop()
