#  -*- coding: utf-8 -*-
# ADS1115 lib from Adafruit, author Toni DiCola, Licence Public Domain
# this is a addon for CraftbeerPi 3
# is should measure pH in the worth of a beer
# can be easily used for other analog sensor
# you can get the ADS1x115.py from the following page
# http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-ADS1115/ADS1x15.zip
# please put the following file of the Adafruit Lib in the home/pi/PHMeasureADS1115 folder:
# ADS1x15.py
# additionaly you can put the example file to the folder
# /home/pi/craftbeerpi3/modules/plugins/PHMeasureADS1115
# Comparator.py
# continious.py
# differential.py
# simpletest.py
# assembled by JamFfm
# Version 0.0.0.4

DEBUG = True
from ADS1x15 import ADS1115
from modules import cbpi
from modules.core.hardware import SensorActive
from modules.core.props import Property

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
# GAIN = 1
VOLTAGEDIFFERENZ = 0.009

@cbpi.sensor
class PHSensorADS1x15(SensorActive):
    ADS1x15channel = Property.Select("ADS1x15 Channel", options=["0", "1", "2", "3"],
                                     description="Select hardware channel-number of ADS1x15, default is 0")
    ADS1x15address = Property.Select("ADS1x15 Address", options=["0x48", "0x49", "0x4A", "0x4B"],
                                     description="Select hardware address-number of ADS1x15, default is 0x48")
    sensorType = Property.Select("Data Type", options=["pH Value", "Voltage", "Digits"],
                                 description="Select which type of data to register for this sensor, hint: add the "
                                             "same sensor several times with different units")
    ADS1x15gain = Property.Select("ADS1x15 Gain", options=["0", "1", "2", "4", "8", "16"],
                                  description="Select gain of pH ADS1x15, default = 1, hint 2/3 can be selected "
                                              "by 0")

    # Use Data Types Voltage and Digits (ADS1x15) for calibration

    def get_unit(self):
        """
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        """
        if self.sensorType == "pH Value":
            return " pH"
        elif self.sensorType == "Voltage":
            return " V"
        elif self.sensorType == "Digits":
            return " Bit"
        else:
            return "select Data Type"

    def stop(self):
        """
        Stop the sensor. Is called when the sensor config is updated or the sensor is deleted
        :return:
        """
        pass

    def execute(self):
        """
        Active sensor has to handle its own loop
        :return:
        """
        while self.is_running():

            ch = int(str(self.ADS1x15channel))
            gain = int(str(self.ADS1x15gain))
            address = int(str(self.ADS1x15address), 16)
            adc = ADS1115(address=address, busnum=1)
            # adc = ADS1115(address=0x48, busnum=1)                                               # change Address here

            if DEBUG: cbpi.app.logger.info('PH Sensor ADS1x115 channel    %s' % ch)               # debug channel
            if DEBUG: cbpi.app.logger.info('PH Sensor ADS1x115 self.ADS1x15address   %s' % self.ADS1x15address)  # debug
            value = adc.read_adc(ch, gain=gain)
            if DEBUG: cbpi.app.logger.info('PH Sensor ADS1x115 value     %s' % value)             # debug or calibration

            voltage = ((float(value)*4.096 / 32767) - VOLTAGEDIFFERENZ)
            if DEBUG: cbpi.app.logger.info('PH Sensor ADS1x115 voltage %.3f'   % voltage)         # debug or calibration

            # phvalue = ("%.2f" % (7 + ((2.564 - voltage) / 0.1839)))                         # better around pH 7 and 6
            phvalue = ("%.2f" % (7 + ((2.548 - voltage) / 0.17826)))                          # better around pH 5
            if DEBUG: cbpi.app.logger.info("PH Sensor ADS1x115 phvalue   %s%s" % (phvalue, "0"))  # debug or calibration

            if self.sensorType == "pH Value":
                reading = phvalue
            elif self.sensorType == "Voltage":
                reading = "%.3f" % voltage
            elif self.sensorType == "Digits":
                reading = value
            else:
                reading = 0.00

            self.data_received(reading)

            self.api.socketio.sleep(3)


@cbpi.initalizer()
def init(cbpi):
    pass

