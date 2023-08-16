"""
Library to use the BirdBrain Hummingbird bit with MicroPython on the micro:bit v2.
Source: https://github.com/CodeJoyEducation/microbit-hummingbird-python

Refactored from the MakeCode library for MicroPython on the micro:bit v2 by CodeJoy (codejoy.org)
Original MakeCode library: https://github.com/BirdBrainTechnologies/pxt-hummingbird-bit (MIT License)

Note: I tried to be as true as possible to the original MakeCode library during the refactor.

IMPORTANT: This library was built and tested using the micro:bit v2. It is unlikely to 
            function properly on the micro:bit v1 due to memory constraints.

Copyright 2023 CodeJoy

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in the
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
"""

from microbit import *
from time import sleep_us

class hummingbird:
    readyToSend = False
    waitTime_1 = 4 # microseconds
    waitTime_2 = 100 # microseconds
    waitTime_Initial = 500 # microseconds
    waitTime_Start = 2000

    # Sensor ID List
    sensor_light = 1
    sensor_dial = 2
    sensor_distance = 3
    sensor_sound = 4
    sensor_other = 5

    @staticmethod
    def startHummingbird():
        """Must be run before any other Hummingbird commands. This initializes the Hummingbird bit.
        """

        # ********** Initialize and setup Hummingbird bit
        pin0.write_analog(0)
        sleep(hummingbird.waitTime_Start)
        pin16.write_digital(1)
        spi.init(baudrate=1000000, bits=8, mode=0, sclk=pin13, mosi=pin15, miso=pin14)
        sleep_us(hummingbird.waitTime_Initial)
        pin16.write_digital(0)
        sleep_us(hummingbird.waitTime_1)
        spi.write(b'\xCB')
        sleep_us(hummingbird.waitTime_2)
        spi.write(b'\xFF')
        sleep_us(hummingbird.waitTime_2)
        spi.write(b'\xFF')
        sleep_us(hummingbird.waitTime_2)
        spi.write(b'\xFF')
        sleep_us(hummingbird.waitTime_1)
        pin16.write_digital(1)
        hummingbird.readyToSend = True
        
        # Set LEDs 2 and 3 to 0
        pin2.write_analog(0)
        pin8.write_analog(0)
    
        print('Hummingbird READY')
        display.show(Image.FABULOUS)
        
    @staticmethod
    def setLED(port: int, intensity: int):
        """Controls the status and brightness of an LED attached to one of the LED ports

        :param port: the port number (1-3) to control (Integer)
        :param intensity: the brightness as a percentage (0 - 100) (Integer) [0 = Off]
        """
 
        # LED Control
        timeout = 0
        while (not hummingbird.readyToSend and timeout < 25):
            sleep(10)
            timeout += 1
            
        if (port >= 1 and port <= 3 and hummingbird.readyToSend):
            intensityScaled = 0
            if (intensity > 100):
                intensity = 100
            if (intensity < 0):
                intensity = 0
            intensityScaled = int((intensity * 255) / 100)
        
            while (not hummingbird.readyToSend): # Wait for other functions in other threads
                sleep_us(10)

            hummingbird.readyToSend = False
            if (port == 1):
                display.scroll(1)
                sleep_us(hummingbird.waitTime_Initial)
                pin16.write_digital(0)
                sleep_us(hummingbird.waitTime_1)
                spi.write(b'\xC0')
                sleep_us(hummingbird.waitTime_2)
                spi.write(bytes([intensityScaled]))
                sleep_us(hummingbird.waitTime_2)
                spi.write(b'\xFF')
                sleep_us(hummingbird.waitTime_2)
                spi.write(b'\xFF')
                sleep_us(hummingbird.waitTime_1)
                pin16.write_digital(1)
            elif (port == 2):
                display.scroll(2)
                pin2.write_analog(intensityScaled * 4)
            elif (port == 3):
                display.scroll(3)
                pin8.write_analog(intensityScaled * 4)
            
            hummingbird.readyToSend = True
    
    @staticmethod
    def setTriLED(port, red = 50, green = 0, blue = 50):
        """Controls the status and brightness of a Tri-Color (RGB) LED attached to one of the Tri-Color ports. 
            Mixing color brightnesses can produce a variety of colors.

        :param port: the port number (1-2) to control (Integer)
        :param red: the brightness as a percentage (0 - 100) for the color red (Integer) [0 = Off]
        :param green: the brightness as a percentage (0 - 100) for the color green (Integer) [0 = Off]
        :param blue: the brightness as a percentage (0 - 100) for the color blue (Integer) [0 = Off]
        """

        timeout = 0
        while (not hummingbird.readyToSend and timeout < 25):
            sleep(10)
            timeout += 1
            
        if (port >= 1 and port <= 2 and hummingbird.readyToSend):
            red = max(0, min(red, 100))
            green = max(0, min(green, 100))
            blue = max(0, min(blue, 100))
            port_val = 0xC3 + port
            red = int(red * 255 / 100)
            green = int(green * 255 / 100)
            blue = int(blue * 255 / 100)
    
            while (not hummingbird.readyToSend):
                sleep_us(10)
            hummingbird.readyToSend = False
            sleep_us(hummingbird.waitTime_Initial)
            pin16.write_digital(0)
            sleep_us(hummingbird.waitTime_1)
            spi.write(bytes([port_val]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([red]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([green]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([blue]))
            sleep_us(hummingbird.waitTime_1)
            pin16.write_digital(1)
            hummingbird.readyToSend = True
    
    @staticmethod
    def setPositionServo(port:int, angle:int = 90):
        """Sets the angle of a position servo attached to one of the servo ports.

        :param port: the port number (1-3) to control (Integer)
        :param angle: the angle to which to move the servo (0 - 180) (Integer)
        """
        timeout = 0
        while (not hummingbird.readyToSend and timeout < 25):
            sleep(10)
            timeout += 1
        if (port >= 1 and port <= 4 and hummingbird.readyToSend):
            angle_conv = 0
            angle = max(0, min(angle, 180))
    
            angle_conv = int((angle * 254) / 180)
            port_val = 0xC5 + port
            # print("servo {} ({}) - {}".format(port, port_val, angle))
            while (not hummingbird.readyToSend):
                sleep_us(10)
            hummingbird.readyToSend = False
            sleep_us(hummingbird.waitTime_Initial)
            pin16.write_digital(0)
            sleep_us(hummingbird.waitTime_1)
            spi.write(bytes([port_val]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([angle_conv]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([0xFF]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([0xFF]))
            sleep_us(hummingbird.waitTime_1)
            pin16.write_digital(1)
            hummingbird.readyToSend = True
    
    @staticmethod
    def setRotationServo(port:int, speed:int = 0):
        """Sets rotation speed of a rotation servo attached to one of the servo ports.

        :param port: the port number (1-3) to control (Integer)
        :param speed: the percentage based speed at which to spin the servo (-100 - 100) (Integer) [0 = Stop]
        """

        timeout = 0
        while (not hummingbird.readyToSend and timeout < 25):
            sleep(10)
            timeout += 1
        
        if (port >= 1 and port <= 4 and hummingbird.readyToSend):
            speed_conv = 0
            speed = max(-100, min(speed, 100))
            
            # Send the off command if the speed is close to zero. Otherwise,
            # convert the speed to a range from 104 to 144 (found experimentally to
            # be the command range for the rotation servo)
            if (speed > -10 and speed < 10):
                speed_conv = 255
            else:
                speed_conv = int((speed * 23 / 100) + 122)
    
            port_val = 0XC5 + port
    
            while (not hummingbird.readyToSend):
                sleep_us(10)
            hummingbird.readyToSend = False
            sleep_us(hummingbird.waitTime_Initial)
            pin16.write_digital(0)
            sleep_us(hummingbird.waitTime_1)
            spi.write(bytes([port_val]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([speed_conv]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([0xFF]))
            sleep_us(hummingbird.waitTime_2)
            spi.write(bytes([0xFF]))
            sleep_us(hummingbird.waitTime_1)
            pin16.write_digital(1)
            hummingbird.readyToSend = True
    
    @staticmethod
    def getSensor(sensor:int, port:int):
        """Returns the value of the sensor attached to one of the sensor ports
            Sensor list:
                Light (hummingbird.sensor_light or 1):
                    Returns an integer value 0 - 100 based on the intensity of the light (No units)
                Dial (hummingbird.sensor_dial or 2):
                    Returns an Returns an integer value 0 - 100 based on where the dial (potentiometer) is in it's available rotation range (No units)
                Distance (hummingbird.sensor_distance or 3):
                    Returns the approximate distance from the sensor in centimeters (cm)
                Sound (hummingbird.sensor_sound or 4):
                    Returns an integer value 0 - 100 based on the intensity/volume of the sound detected (No units)
                Other (hummingbird.sensor_other or 5):
                    This one is very dependant on what you attach, but will generally return an integer value 0 - 100 based on the intensity of whatever it is detecting (No units)
        
        :param sensor: the type of sensor attached to the port (Integer) \
            [ hummingbird.sensor_light | \
            hummingbird.sensor_dial | \
            hummingbird.sensor_distance | \
            hummingbird.sensor_sound | \
            hummingbird.sensor_other ]
            
        :param port: the port number (1-3) to control (Integer)
        """
 
        timeout = 0
        while (not hummingbird.readyToSend and timeout < 25):
            sleep(10)
            timeout += 1
        
        if (port >= 1 and port <= 3 and hummingbird.readyToSend):
            vals = [bytearray(1), bytearray(1), bytearray(1), bytearray(1)]
            while (not hummingbird.readyToSend):
                sleep_us(10)
            hummingbird.readyToSend = False
            # Need to read all three sensor values and the battery (vals[3]) to complete the communication protocol.
            sleep_us(hummingbird.waitTime_Initial)
            pin16.write_digital(0)
            sleep_us(hummingbird.waitTime_1)
            spi.write_readinto(bytearray(b'\xCC'), vals[0])
            sleep_us(hummingbird.waitTime_2)
            spi.write_readinto(bytearray(b'\x66'), vals[1])
            sleep_us(hummingbird.waitTime_2)
            spi.write_readinto(bytearray(b'\x77'), vals[2])
            sleep_us(hummingbird.waitTime_2)
            spi.write_readinto(bytearray(b'\x88'), vals[3])
            sleep_us(hummingbird.waitTime_1)
            spi.write_readinto(bytearray(b'\x55'), vals[0])
            sleep_us(hummingbird.waitTime_1)
            spi.write_readinto(bytearray(b'\x66'), vals[1])
            sleep_us(hummingbird.waitTime_1)
            pin16.write_digital(1)
            hummingbird.readyToSend = True
            if sensor == 3: # Distance
                return round(int.from_bytes(vals[port - 1], 'big') * 117 / 100)
            elif sensor == 4: # Sound
                return round(int.from_bytes(vals[port - 1],'big') * 200 / 255)
            elif sensor == 2: # Dial
                return min(round(int.from_bytes(vals[port - 1], 'big') * 100 / 230), 100)
            else:
                return round((int.from_bytes(vals[port - 1], 'big') * 100) / 255)
                
        return 0
    
    @staticmethod
    def getBattery():
        """Returns the voltage of the battery in millivolts. The device my start experiencing difficulty at a reading of about 4630 mV.
        """
        timeout = 0
        while (not hummingbird.readyToSend and timeout < 25):
            sleep(10)
            timeout += 1
        if hummingbird.readyToSend:
            while (not hummingbird.readyToSend):
                sleep_us(10)
            hummingbird.readyToSend = False
    
            batt = bytearray(1)
            junk = bytearray(1)
            sleep_us(hummingbird.waitTime_Initial)
            pin16.write_digital(0)
            sleep_us(hummingbird.waitTime_1)
            # spi.write(bytearray(b'\x55'))
            spi.write_readinto(bytearray(b'\x55'), junk)
            sleep_us(hummingbird.waitTime_2)
            spi.write_readinto(bytearray(b'\x66'), junk)
            sleep_us(hummingbird.waitTime_2)
            spi.write_readinto(bytearray(b'\x77'), junk)
            sleep_us(hummingbird.waitTime_2)
            spi.write_readinto(bytearray(b'\x88'), batt)
            sleep_us(hummingbird.waitTime_1)
            pin16.write_digital(1)
            hummingbird.readyToSend = True
            return round(int.from_bytes(batt, 'big') * 406 / 10)
                
        return 0
