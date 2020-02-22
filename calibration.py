#!/usr/bin/env python
#  -*- coding: utf-8 -*-

ph7voltage = input("Put in the measured voltage while producing a shortcut between inner pole and outer area of the "
                   "BNC. This presents voltage at pH 7. Format x.xxx:  ")
ph401voltage = input("Put in the measured voltage while measuring the buffer pH 4.01. Format x.xxx:  ")
VoltageperPH = round((ph7voltage-ph401voltage)/2.99, 5)
print ("The Voltage per pH Factor is " + str(VoltageperPH))
print ("put it in the Formula in Line 114 of __init__.py")
print ("(7 + ((" + str(ph7voltage) + "- voltage) / " + str(-1*VoltageperPH) + "))")
