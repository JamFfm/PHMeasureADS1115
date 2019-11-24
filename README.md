![](https://img.shields.io/badge/CBPi%20beta%20addin-functionable_for_V3-green.svg)  ![](https://img.shields.io/github/license/JamFfm/PHMeasureADS1115.svg?style=flat) ![](https://img.shields.io/github/last-commit/JamFfm/PHMeasureADS1115.svg?style=flat) ![](https://img.shields.io/github/release-pre/JamFfm/PHMeasureADS1115.svg?style=flat)

# PHMeasureADS1115 add-on for CraftBeerPi 3

This is Beta Software

*Craftbeerpi3* sensor for measuring ph values.
Using the ADS115 A/D via I2C connection

The mash can be between 4.5pH and 5.8pH.

>**The target pH for the mash usually should be between 5.3pH and 5.7pH**

Therefore we should know the pH of the mash

German link to ph in Beer

- https://www.maischemalzundmehr.de/index.php?inhaltmitte=exp_maischph


 
# The probe and board for this Craftbeerpi 3 addon

at ebay
- https://www.ebay.de/i/322935814230?ul_noapp=true

but there are same in Aliexpress.
Search for this: "Liquid PH Value Erkennung Detect Modul +BNC Electrode Probe for Arduino"


![Test Graph](https://github.com/JamFfm/PHMeasure/blob/master/PHSet.jpg "set")

**The probe board is an analog sensor. RaspberryPi can read only digital sensors.
Therefore you need an analog/digital converter like the ADS1115 (16Bit)**

![Test Graph](https://github.com/JamFfm/PHMeasureADS1115/blob/master/ADS1115.jpg  "Pins of ADS1115")
  
# How to connect

![Test Graph](https://github.com/JamFfm/PHMeasure/blob/master/RaspberryPiPHSensorSteckplatine.png "Example wiring, not campatible with code. Have a look at Software SPI")
Be aware that you use the **connections below** if you don't change the code. Not use the MCP3008 connections in the picture!
**But use the Picture to wire the levelshifter and the probe-board. In this picture channel 0 is connected**

## Connect I2C

To connect the ADS1115 to the Raspberry Pi use the following connections:

- ADS GND   to RASPI GND 
- ADS VDD   to RASPI 5v 
- ADS SCL   to RASPI SCL (daisychain possible)
- ADS SCA   to RASPI SCA (daisychain possible)
- Address   have a look at the specs of ADS1115 for changing adress
- Alert     have a look at the specs of ADS1115 for Alert events
- A0        to Po of the PhMeasure Board. Put a level shifter 5v/3,3v inbetween because the Raspi pin can only stand 3.3v

![Test Graph](https://github.com/JamFfm/PHMeasureADS1115/blob/master/RaspiGPIOI2C.jpg "Example wiring, have a look at wireing I2C")


# How to Install

1. Load the NEXTIONDisplay addin from the CraftbeerPi3 addin section (not jet available).

    Workaround:

    Key in in the command box of Raspi

    ```python
    git clone https://github.com/JamFfm/PHMeasureADS1115.git -b master --single-branch /home/pi/craftbeerpi3/modules/plugins/PHMeasureADS1115
    ```
    
    A update is done by the following commands in the command box of the Raspi
    
    ```python
    cd /home/pi/craftbeerpi3/modules/plugins/PHMeasureADS1115
    git pull
    ```

3. Reboot at least CBPi3


# Board description

![Test Graph](https://github.com/JamFfm/PHMeasure/blob/master/1.0x0.jpg "powerampfilter")



* BNC plug: Where you put the probe. It seems to work with any probe with a calibration difference.

* Pin To: Should be the temperature but I can't make it works.
* Pin Do: High/Low 3.3v adjustable limit.
* Pin G/GND: Probe ground. It may be useful when the ground is not the same as your Raspi. In fact I use the ground of the Raspi.
  In some circumstances the ground voltage of the liquid to measure can be different.
* Pin G/GND: Power ground (ex. Raspi).
* Pin V+/VCC: Input power 5V DC (direct from Raspi).
* Blue potentiometer close to BNC: pH offset.
* Blue potentiometer close to pins: limit adjustment.
* Black component with 103 printed (not the one between potentiometers): thermistor for temperature compensation.

# Calibration: this section is invalid and has to be corrected

## The offset

The offset is the shifting of all pH values to a specific voltage range. If a pH 7 output a voltage of 2.2v and pH 8 a voltage of 2.1v, then a shift of +0.3v move the pH 7 to 2.5v and the pH 8 to 2.4v. 


This can be done on the board or via software but it's probably easyer on the board because it's probe independant and there are less programming to do.


Connect GND (both) to Raspi GND and and Vcc to Raspi 5v. Please use a levelshifter to avoid damage at the GPIO which only support 3.3v. 

Remove the probe and do a short circuit between the the small BNC hole and the external part of BNC. 

Put a voltmeter to measure the voltage between GND and Po. Adjust the pot (close BNC) until the output is 2.5v. 

Now the pH 7 have an exact value of 2.5v (511 with analogRead function) because the probe will output 0 millivolt.

## The steps

Now you need one or more buffer solutions depending the range and precision you want. Ideally you should know the range of the measure you want to do with your system. 

I use water (upcoming beer) between pH 5 and pH 7, then I choose the buffer 4.01 (and 6.86 to verify my stuff). If you usually measure pH between 8 and 10 choose buffer 9.18 (eventually 6.86 also).


Connect the (clean) probe and put it in the buffer then let it stabilize for a minute. You know it's stable when it goes up and down (3.04 then 3.05 then 3.03 then 3.04). Take note of the voltmeter value, in my example it's 3.05v.

## Unit per step

The PH_step calculation is quite simple. You take the difference between the two known voltage, in my example 2.5v@pH7 and 3.05v@pH4.01 which is -0.55v. 

It's the voltage range equivalent of the pH range from 7 to 4.01, which is 2.99 pH units. A small division of the voltage by pH units gives you a volts per pH number (0,1839... in my case).

The PH_probe is calculated by taking the known pH 7 voltage (2.5v) where we add some PH_step to match the probe voltage. This means that a pH of 8 have a voltage value of 2.5v (pH 7) + 0.1839 (1 unit/step); pH 9 then is 2.5v + 0.1839 + 0.1839 = 2.87v.

To determine the Unit per Step (=PH_step in formula) is important to know.

# Finally the code

16 Bit = 32767 possible values

voltage = 5 / 32767 * measure; //classic digital to voltage conversion

// PH_step = (voltage@PH7 - voltage@PH4) / (PH7 - PH4) = (2.5-3.05) / (7-4) = (-.55/2.99) = -0.1839....

// PH_probe = PH7 - ((voltage@PH7 - voltage@probe) / PH_step)

phvalue = 7 + ((2.5 - voltage) / *0.1839* )

# Usage

Use this sensor as any other sensor in Craftbeerpi 3.
The Digit and Voltage values can help to calibrate. They are not needed for pH measurement.
The main calibaration is already described above. 

Keep in mind that it takes several minutes to get the right pH value.

When using in the rotating mash no stable values are shown but in a probe of mash (ex. a glass) it was very stable.
Values matched with a other pH measurement tool.

Please do changes of the formula in the code of the file "__init__.py". 
It is situated in the folder

home/pi/craftbeerpi3/modules/plugins/PHMeasureADS1115/

According the parameters of the probe it can be situated in max 80°C liquid but not for longtime.
I never tryed that until now.

# Parameter

There are 3 parameter to select:

## Digit
This shows the value of the MCP 3008 and runs from 0-1024.
This is the basic of all measurement.


## Voltage
This shows the calculated value of the Voltage measurement.
Voltage = 5 / 1024.0 * Digit
5 is the basic voltage of the Board
This means 1024 digit is equal to 5V.


## pH Value
This shows the calculated value of the pH measurment.
phvalue = 7 + ((2.532 - voltage) / *0.1839* )
As discribed above the *0.1839* has to be adopted in the code.

Maybe the 2.532 has to be adopted to the voltage value you measure with the short circuit between the the small BNC hole and the external part of BNC.


# Hint

You can easily change the addon for different analog sensors.

There are only some lines to change. 

# Known Problems
- This is just to show how to use the ADS1115 to show values
- You hae to find out the right parameter to show the right voltage values and the right pH values
- When using in the rotating mash no stable values are shown 
- Wrong spelling
- no temperature calibration


# Support

Report issues either in this Git section or at Facebook at the [Craftbeerpi group](https://www.facebook.com/groups/craftbeerpi/)

# Most helpful links:
## All information on this side comes from the following links

I got all my knowledge from these links:


- http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-ADS1115/index.html
  
  Used this for the libs and classes
 

- https://forum.arduino.cc/index.php?topic=336012.0 

  last post first page, for understanding probe in general


- https://www.botshop.co.za/how-to-use-a-ph-probe-and-sensor/

  additional info
  
  
- https://raspberrypi.stackexchange.com/questions/96653/calibrate-ph-4502c-ph-meter
