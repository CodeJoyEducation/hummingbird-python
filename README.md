# Hummingbird bit Library for micro:bit v2

Library to use the [BirdBrain](https://www.birdbraintechnologies.com/) [Hummingbird bit](https://www.birdbraintechnologies.com/products/hummingbird-bit-robotics-kit/) with [MicroPython on the micro:bit v2](https://python.microbit.org/v/3).

**Refactored from the MakeCode library for MicroPython on the micro:bit v2 by CodeJoy (codejoy.org)**

_____

## Important notes:
* We attempted to be as true as possible to the original MakeCode library during the refactor with regard to method names and arguments, but there are some differences due to syntactical differences between the languages
   * [Original Birdbrain MakeCode library for Hummingbird bit](https://github.com/BirdBrainTechnologies/pxt-hummingbird-bit) (MIT License)
* **IMPORTANT**: This library was built and tested using the micro:bit v2. It is unlikely to function properly on the micro:bit v1 due to memory constraints.**
_____
## Adding the library

In the [micro:bit Python Editor](https://python.microbit.org/):
1. Select the "Project" tab on the menu on the left side of interface
2. Click the "Create file" button
3. Name the file "hummingbird.py" and click the "Create" button
4. Copy the content of the [hummingbird.py file from this github repo](https://github.com/CodeJoyEducation/hummingbird-python/blob/main/hummingbird.py)
7. Click back over to the main.py and import the new library by adding the line below under the `from microbit import *` line:
  * `from hummingbird import hummingbird`

Now just check out the documentation below to see how to use the library in your code!

_____
## API Reference
---
### startHummingbird()
This initialization method must be run after all your imports at the top of your python script and after your have imported the Hummingbird library.
```
    from microbit import *
    from hummingbird import hummingbird
    # ... any other needed libraries ...

    hummingbird.startHummingbird()

    # ... the rest of your code ...
```
---

### setLED(port, intensity)
Controls LEDs attached to the LED ports on the Hummingbird.

`hummingbird.setLED(port, intensity)`

This method has 2 arguments:
* `port`: This is an integer that represent the port number you wish to control (1 - 3)
* `intensity`: The brightness to set for the LED as a percentage (0 - 100) (Integer) [0 = Off]

```
    # Sets the LED in LED port 3 to 80% brightness
    hummingbird.setLED(3, 80)
```

---

### setTriLED(port, red, green, blue)
Controls the status and brightness of a Tri-Color (RGB) LED attached to one of the Tri-Color ports. Mixing color brightnesses can produce a variety of colors.

`hummingbird.setTriLED(port, red, green, blue)`

This method has 4 arguments:
* `port`: This is an integer that represent the port number you wish to control (1 - 2)
* `red`: The brightness to set for the red color of the LED as a percentage (0 - 100) (Integer) [0 = Off]
* `green`: The brightness to set for the green color of the LED as a percentage (0 - 100) (Integer) [0 = Off]
* `blue`: The brightness to set for the blue color of the LED as a percentage (0 - 100) (Integer) [0 = Off]

```
    # Sets the Tri-color LED in Tri-color port 1 80% red, 0% green and 10% blue
    hummingbird.setLED(1, 80, 0, 10)
```

---

### setPositionServo(port, angle)
Sets the angle of a position servo attached to one of the servo ports on the Hummingbird.

`hummingbird.setPositionServo(port, angle)`

This method has 2 arguments:
* `port`: This is an integer that represent the port number you wish to control (1 - 4)
* `angle`: The angle to which to move the servo (0 - 180) (Integer)

```
    # Sets the position servo in servo port 2 to 75 degrees
    hummingbird.setPositionServo(2, 75)
```

---

### setRotationServo(port, speed)
Sets rotation speed of a rotation servo attached to one of the servo ports on the Hummingbird.

`hummingbird.setRotationServo(port, speed)`

This method has 2 arguments:
* `port`: This is an integer that represent the port number you wish to control (1 - 4)
* `speed`: the percentage based speed at which to spin the servo (-100 - 100) (Integer) [0 = Stop]
    * When looked at from the top of the servo (the part with the horn or connector) the servo should rotate counter clockwise with positive number and clockwise with negative numbers
    * The max speed of will vary a bit from servo to servo and between positive and negative numbers on the same servo

```
    # Sets the rotation servo in servo port 3 to rotate at -60% (clockwise)
    hummingbird.setRotationServo(3, -60)
```

---

### getSensor(sensor_type, port)
Returns the value of the sensor attached to one of the sensor ports on the Hummingbird.

`hummingbird.getSensor(sensor_type, port)`

**Sensor list:**
* Light (hummingbird.sensor_light or 1)
    * Returns an integer value 0 - 100 based on the intensity of the light (No units)
* Dial (hummingbird.sensor_dial or 2)
    * Returns an Returns an integer value 0 - 100 based on where the dial (potentiometer) is in it's available rotation range (No units)
* Distance (hummingbird.sensor_distance or 3)
    * Returns the approximate distance from the sensor in centimeters (cm)
* Sound (hummingbird.sensor_sound or 4)
    * Returns an integer value 0 - 100 based on the intensity/volume of the sound detected (No units)
* Other (hummingbird.sensor_other or 5):
    * This one is very dependant on what you attach, but will generally return an integer value 0 - 100 based on the intensity of whatever it is detecting (No units)

This method has 2 arguments:
* `sensor`: the type of sensor attached to the port (Integer)
    * `hummingbird.sensor_light` or `1`
    * `hummingbird.sensor_dial` or `2`
    * `hummingbird.sensor_distance` or `3`
    * `hummingbird.sensor_sound` or `4`
    * `hummingbird.sensor_other` or `5`
* `port`: This is an integer that represent the port number you wish to control (1 - 3)

```
    # Get the current value from the Distance sensor attached to sensor port 2
    hummingbird.getSensor(hummingbird.sensor_distance, 2)
```

---

### getBattery()
Returns the voltage of the battery in millivolts. 

___Note: The device my start experiencing difficulty at a reading of about 4630 mV.~___

`hummingbird.getBattery()`

```
    # Get the current voltage from the battery in milliVolts
    hummingbird.getBattery()
```
_____

## Sample Code:

Below are some basic sample code projects to test out python on your micro:bit v2

Notes:
* Before running this code you must add the hummingbird.py file to your python project.

---

### Code 1: Controlling rotation servos with micro:bit buttons

What the code does:
* When the program starts the rotation servos in servo ports 3 and 4 are stopped
* When button A is pressed the rotation servos in servo ports 3 and 4 are set to -50% and the `-` character is displayed on the 5x5 LED matrix.
* When button B is pressed the rotation servos in servo ports 3 and 4 are set to 50% and the `+` character is displayed on the 5x5 LED matrix.
* When both button and and B have been pressed the rotation servos in servo ports 3 and 4 are stopped and the letter "S" is displayed on the 5x5 LED matrix.
* The program sleeps (pauses) for 100 milliseconds at the end of each loop

```
from microbit import *
from hummingbird import hummingbird

hummingbird.startHummingbird()

rSpeed = 0

while True:
    hummingbird.setRotationServo(3, rSpeed)
    hummingbird.setRotationServo(4, rSpeed)
    ba = button_a.was_pressed()
    bb = button_b.was_pressed()
    if ba and bb:
        display.show("S")
        rSpeed = 0    
    elif ba:
        display.show("-")
        rSpeed = -50
    elif bb:
        display.show("+")
        rSpeed = 50
    sleep(100)
```

### Code 2: Controlling Tri-color LEDs with the distance sensor and the position servo with the dial sensor

What the code does: controlling the 
* Displays the value of the distance and dial sensors on the serial console
* The distance sensor in sensor port 1 is used to control the color of the tri-color LED in tricolor port 1
  * The LED is green if the distance sensor reads further than or equal to 40cm
  * The LED is yellow if the distance sensor reads closer than 40cm, but further than 20 cm
  * The LED is red if the distance sensor reads further than or equal to 20cm
* The dial sensor in sensor port 2 is used to control the angle of the position servo attached to servo port 1

```
    from microbit import *
    from hummingbird import hummingbird

    hummingbird.startHummingbird()

    last_angle = -1
    dial = 0
    distance = 0

    while True:
        distance = hummingbird.getSensor(hummingbird.sensor_distance, 1)
        dial = hummingbird.getSensor(hummingbird.sensor_dial, 2)

        print("Distance: {}cm".format(distance))
        print("Dial: {}".format(dial))

        # Control Tri-color LED in tri-color port 1 based on distance sensor
        if distance >= 40:
            hummingbird.setTriLED(1, 0, 100, 0)
        elif distance < 40 and distance > 20:
            hummingbird.setTriLED(1, 100, 80, 0)
        elif distance <= 20:
            hummingbird.setTriLED(1, 100, 0, 0)

        # Control the postion servo in servo port 1 based on the value of the dial sensor
        # The angle formula is simplified from dial * 180 / 100
        angle = round(dial * 1.8)
        if last_angle != angle:
            hummingbird.setPositionServo(1, angle)
            last_angle = angle

        sleep(100)
```

### Code 3: Show a beating heart on the micro:bit and move the position servo from 180 to 0 degrees and back

```
# Imports go at the top
from microbit import *
from hummingbird import *

hummingbird.startHummingbird()

while True:
    hummingbird.setPositionServo(1, 180)
    display.show(Image.HEART)
    sleep(1000)
    hummingbird.setPositionServo(1, 0)
    display.show(Image.HEART_SMALL)
    sleep(1000)
```
_____

## License

Copyright 2023 CodeJoy

Permission is hereby granted, free of charge, to any person obtaining a copy ofthis software and associated documentation files (the “Software”), to deal in the
Software without restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
