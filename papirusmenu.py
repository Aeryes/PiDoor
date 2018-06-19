#!/usr/bin/python   

import csv, os, time, datetime
from papirus import *

import counterfunc as cf
import RPi.GPIO as GPIO

#This class can be global scope but for the sake of readability will be class.
#This class controls current menu state.
class Control():
    def __init__(self):
        self.done = False
        
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update()

    def event_loop(self):
        self.state.get_event()
    
    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
        
#This class switches between states and contains variables carried  by,
#All classes.
class States():
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
    
#Main menu class. Displays other menu options and general inforamation.
class MainMenu(States):
    def __init__(self):
        States.__init__(self)
        self.next = ''

        self.screen = Papirus()
        self.text = PapirusTextPos()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(cf.SW1, GPIO.IN)
        GPIO.setup(cf.SW2, GPIO.IN)
        GPIO.setup(cf.SW3, GPIO.IN)
        GPIO.setup(cf.SW4, GPIO.IN)
        if cf.SW5 != -1:
            GPIO.setup(cf.SW5, GPIO.IN)
            
    def cleanup(self):
        print 'Cleaning up Main Menu'

    def startup(self):
        print 'Starting Main Menu'

    def button_control(self):
        self.text.AddText('1. Traffic Tracker',0, 25, size = 16, Id = 'One')
        if GPIO.input(cf.SW1) == False:
            print 'Changing menu now...'
            self.text.Clear()
            self.next = 'csvmenu'
            self.done = True
            print 'Menu changed...'
    
    #This func acts as menu main loop.
    def get_event(self):
        self.text.AddText('Main Menu', 40, 0, Id = 'Top')
        self.button_control()
        
    #Functionality that needs to be updated occassionaly goes here.
    def update(self):
        self.screen.partial_update()

#This class displays info related to CSV files based on todays date.
class CSV_Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = ''
            
    def cleanup(self):
        print 'Cleaning up CSV Menu'

    def startup(self):
        print 'Starting CSV Menu'
        self.screen = Papirus()
        self.text = PapirusTextPos()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
      
        GPIO.setup(cf.SW1, GPIO.IN)
        GPIO.setup(cf.SW2, GPIO.IN)
        GPIO.setup(cf.SW3, GPIO.IN)
        GPIO.setup(cf.SW4, GPIO.IN)
        if cf.SW5 != -1:
            GPIO.setup(cf.SW5, GPIO.IN)
        
    def button_control(self):
        self.text.AddText('1. Return to Menu 2. Todays Info',0, 25, size=16, Id='One')
        if GPIO.input(cf.SW1) == False:
            self.text.Clear()
            self.next = 'mainmenu'
            self.done = True
        if GPIO.input(cf.SW2) == False:
            self.text.Clear()
            self.next = 'csvdisplay'
            self.done = True
                                 
    #This func acts as menu main loop.
    def get_event(self):
        self.text.AddText('CSV Menu', 45, 0, Id = 'Top')
        self.button_control()
        
    #Functionality that needs to be updated occassionaly goes here.
    def update(self):
        self.screen.partial_update()

#This class displays counts from CSV files based on dates.
class CSV_Display(States):
    def __init__(self):
        States.__init__(self)
        self.next = ''
            
    def cleanup(self):
        print 'Cleaning up CSV_Display Menu'

    def startup(self):
        print 'Starting CSV_Display Menu'
        self.screen = Papirus()
        self.text = PapirusTextPos()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
      
        GPIO.setup(cf.SW1, GPIO.IN)
        GPIO.setup(cf.SW2, GPIO.IN)
        GPIO.setup(cf.SW3, GPIO.IN)
        GPIO.setup(cf.SW4, GPIO.IN)
        if cf.SW5 != -1:
            GPIO.setup(cf.SW5, GPIO.IN)
               
    def button_control(self):
        self.text.AddText('1. Return to Menu',0, 25, size=16, Id='Two')

        current_day = datetime.datetime.now()
        record_date = current_day.strftime('%Y-%m-%d')
  
        with open(record_date, 'r') as file_object:
            read = csv.reader(file_object)
            for row in read:
                count = row[0]
                self.text.AddText(count, 95, 45, size = 16, Id = 'Rows')

        if GPIO.input(cf.SW1) == False:
            self.text.Clear()
            self.next = 'mainmenu'
            self.done = True
                                 
    #This func acts as menu main loop.
    def get_event(self):
        self.text.AddText('CSV Display', 35, 0, Id = 'Top')
        self.button_control()
        
    #Functionality that needs to be updated occassionaly goes here.
    def update(self):
        self.screen.partial_update()
    
app = Control()

#State dict.
state_dict = {'mainmenu' : MainMenu(),
              'csvmenu' : CSV_Menu(),
              'csvdisplay' : CSV_Display()}

#Setup state is called and sets the initial state of the program.
app.setup_states(state_dict, 'mainmenu')

#Call main loop to run the program.
app.main_loop()
    
sys.exit()
