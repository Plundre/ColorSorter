#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time
from array import *
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent, MoveTank

from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.led import Leds
#Errors/Return Constants
ERROR_NO_BLOCK_ON_BELT = 69

#Parameters
STRG_CTRL_THRESHOLD = 5
FEEDBELT_ONE_BLOCK_TO_DEG = 92

BAR_STATE_READY_TO_RETRACT = -1#80
BAR_STATE_READY_TO_EXTEND = -7#20

legalColor1 = 2
legalColor2 = 4
legalColor3 = 5

POS_CHAMBER1 = (170*6)
POS_CHAMBER2 = (170*5)
POS_CHAMBER3 = (170*4)
POS_CHAMBER4 = (170*3)
POS_CHAMBER5 = (170*2)
POS_CHAMBER6 = 170
POS_TRASH = 0

# state constants
ON = True
OFF = False
SPEED = 50

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


class StorageUnit():
    storage = array('i', [0,0,0,0,0,0])
    countyBoi = 0
    trashCounter = 0
    color = 4
    def addBlock(self, blockType):

        """
        docstring
        """
        i = 0
        while(i < len(self.storage)):
            if (i == (blockType-1) and i < 3):
                self.storage[i] += 1
            elif(i== (blockType-1) and i > 2):
                self.storage[i] += 2
            i+=1

    def countTrash(self):
        self.trashCounter += 1

    def RunStorageUnit(self,deg):
        storageMotor = LargeMotor(OUTPUT_A)
        storageMotor.on_for_degrees(speed=SPEED, degrees=deg)

    def GetPos_StorageUnit(self):
        storageEncoder = LargeMotor(OUTPUT_A).position
        return storageEncoder

    def Sorting_A_Block(self, legalColor1, legalColor2, legalColor3):
        feedBelt = FeedBelt()
        pushBar = PushBar()
        sensors = SensorArray()
        #print('Hyll Satan')
        blockUnderSorting = True
        
        #If colorSensor doesnt see anything, run FeedBelt until it sees something or it has run 2 Turns
        
        if(sensors.ReadColor(legalColor1,legalColor2,legalColor3) > 0):
        
            while(blockUnderSorting == True):
            
                self.color = sensors.ReadColor(legalColor1, legalColor2, legalColor3)
                        
                #setVal = Color_To_SetVal(color, legalColor1, legalColor2, legalColor3)
                #print('Hail Cthulu')
                if(self.color > 0 and self.color < 4):
                    pushBar.RunBar(BAR_STATE_READY_TO_RETRACT)
                    print('Hail Asmoduus')
                    feedBelt.RunBelt(FEEDBELT_ONE_BLOCK_TO_DEG)
                    time.sleep(0.5)

                    setValue = self.color + sensors.ReadLength(legal1=legalColor1, legal2=legalColor2, legal3=legalColor3)
                    time.sleep(0.5)

                    self.StorageControl(setValue)

                    pushBar.RunBar(0-BAR_STATE_READY_TO_RETRACT)
                    time.sleep(0.5)

                    pushBar.RunBar(BAR_STATE_READY_TO_RETRACT + BAR_STATE_READY_TO_EXTEND - ( (self.storage[setValue-1] + 1) * 102))

                    pushBar.RunBar(0 - (BAR_STATE_READY_TO_RETRACT + BAR_STATE_READY_TO_EXTEND - ((self.storage[setValue-1]+1)*102) ) )

                    self.addBlock(setValue)

                    blockUnderSorting = False
            
                elif(self.color == 4):
                    pushBar.RunBar(BAR_STATE_READY_TO_RETRACT)
                    feedBelt.RunBelt(FEEDBELT_ONE_BLOCK_TO_DEG)
                    time.sleep(0.5)
                    #print('Beelzebub')
                    print(self.countyBoi)

                    self.countyBoi = self.countyBoi + 1
                    #if(countyBoi == 2 or countyBoi == 4 or countyBoi == 6 or countyBoi == 8 or countyBoi == 10 or countyBoi == 12):
                    #    print('Fytti Katta og hutti tu')
                    #    print(countyBoi)
                    setValue = 7 #Dvs utenfor array-et
                    time.sleep(0.5)

                    self.StorageControl(setValue)

                    pushBar.RunBar(0-BAR_STATE_READY_TO_RETRACT)
                    time.sleep(0.5)

                    pushBar.RunBar(BAR_STATE_READY_TO_RETRACT + BAR_STATE_READY_TO_EXTEND)

                    pushBar.RunBar(0 - BAR_STATE_READY_TO_EXTEND)

                    self.countTrash()

                    blockUnderSorting = False
                else:
                    blockUnderSorting = False
                    #If end up here, something went wrong (Might not need elif, just use else instead)                        
        else:
            #What To do when there is no block seen
            
            return ERROR_NO_BLOCK_ON_BELT

    def SortingProtocoll(self):
        numOfBlocks = 12
        while(numOfBlocks > 0):
            
            self.Sorting_A_Block(legalColor1,legalColor2,legalColor3)
            #print('naere no')
            numOfBlocks= numOfBlocks - 1
    
    def SetVal_To_SetDeg(self,setVal):
        if(setVal == 1):    
            return POS_CHAMBER1
        elif(setVal == 2):
            return POS_CHAMBER2
        elif(setVal == 3):
            return POS_CHAMBER3
        elif(setVal == 4):
            return POS_CHAMBER4
        elif(setVal == 5):
            return POS_CHAMBER5
        elif(setVal == 6):
            return POS_CHAMBER6
        elif(setVal == 7):
            return POS_TRASH            
    
    def StorageControl(self,setValue):
        setDeg = self.SetVal_To_SetDeg(setVal=setValue)
        if((setDeg - self.GetPos_StorageUnit()) > STRG_CTRL_THRESHOLD):
            self.RunStorageUnit(2)
        elif(self.GetPos_StorageUnit() - setDeg > STRG_CTRL_THRESHOLD):
            self.RunStorageUnit(-2)
        else:
            self.RunStorageUnit(0)


class FeedBelt():
    def RunBelt(self, deg):
        beltMotor = LargeMotor(OUTPUT_B)
        beltMotor.on_for_degrees(speed=SPEED, degrees=deg)
        
    
    def GetPos_Belt(self):
        beltEncoder = LargeMotor(OUTPUT_B)
        return beltEncoder.position

class PushBar():
    def RunBar(self, deg):
        barMotor = LargeMotor(OUTPUT_D)
        barMotor.on_for_degrees(degrees=deg, speed=SPEED)

    def GetPos_Bar(self):
        barEncoder = LargeMotor(OUTPUT_D)
        return barEncoder.position

class SensorArray():

    def ReadColor(self, legal1, legal2, legal3):
        colorSens = ColorSensor(INPUT_1)
        if(colorSens == legal1):
            return 1
        elif (colorSens == legal2):
            return 2
        elif (colorSens == legal3):
            return 3
        elif (colorSens == 0):
            return 0
        else:
            return 4
        #return  colorSens.color

    def ReadLength(self, legal1, legal2, legal3):
        LengthSens = ColorSensor(INPUT_2)
        readVal = LengthSens.color
        if(readVal == legal1 or readVal == legal2 or readVal == legal3):
            return 3
        else:
            return 0

    #def Color_To_SetVal(color, legal1, legal2, legal3):
    #    if(color == legal1):
    #        return 1
    #    elif (color == legal2):
    #        return 2
    #    elif (color == legal3):
    #        return 3
    #    else:
    #        return 0

    #Run Belt
    #Read Length
    #Run Feed-Bar

def OrderBlock():   
    return 0    


def HMI():
    mode = 1



    return mode



def main():
    running = True
    modeSelect = 1
    storage = StorageUnit()
    print('whaat')
    while running:
        while(modeSelect == 1):
            modeSelect = HMI()
            if (modeSelect == 1):
                print('Alyoo')
                storage.SortingProtocoll()
            elif (modeSelect == 2):
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
