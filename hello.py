#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time
from array import *
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.motor import 


# state constants
ON = True
OFF = False


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)
def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')
def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')
def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)

def Selector():

class StorageUnit():
    storage = array('i', [0,0,0,0,0,0])

    def addBlock(self, blockType):
        """
        docstring
        """
        i = 0
        while(i < len(self.storage)):
            if (i == blockType and i < 3):
                self.storage[i] += 1
            elif(i== blockType and i > 2):
                self.storage[i] += 2
            i+=1



def SortBlock():
#Read Color
#Run Belt
#Read Length
#Run Feed-Bar


def OrderBlock():


def HMI():
    mode = 1



    return mode

def 

def main():
    running = True
    modeSelect = 0
    storage = StorageUnit()

    while running:
        while(modeSelect = 0):
            modeSelect = HMI()
            if (modeSelect = 1):
                SortBlock()
            elif (modeSelect = 2):
                OrderBlock()
        

    











    '''    Test Code:
    ''' '''The main function of our program''' '''
    my_led = Leds()
    i = 0
    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # print something to the screen of the device
    print('Hello World!')

    # print something to the output panel in VS Code
    debug_print('Hello VS Code!')
    while (i < 10):
        my_led.set_color('LEFT','RED')
        my_led.set_color('RIGHT','RED')
        time.sleep(1)
        
        my_led.set_color('LEFT' ,'GREEN')
        my_led.set_color('RIGHT','GREEN')
        time.sleep(1)
        i += 1
    
    # wait a bit so you have time to look at the display before the program
    # exits
    time.sleep(5)
    '''

if __name__ == '__main__':
    main()
