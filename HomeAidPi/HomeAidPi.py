import RPi.GPIO as gpio
from TextToSpeech import *
from flask import Flask
from flask import render_template
from flask import request
from bluetooth import *
import sys
from subprocess import call
import time
import threading

INTRUDER = False

# class definitions ---------------------------------------------------------------------------------------------

class Occupant:
	def __init__(self, name, btID, id, iphoneName, present, greeted):
		self.name = name
		self.btID = btID
		self.id = id
		self.present = present
		self.greeted = greeted
		self.iphoneName = iphoneName
		
class Room:

	occupants = []
	
	def __init__(self, numOfOccupants, matEnabled):
		self.numOfOccupants = numOfOccupants
		self.matEnabled = matEnabled
		gpio.setmode(gpio.BCM)
		gpio.setup(25, gpio.OUT)
		gpio.output(25, gpio.HIGH)
		gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
	
	#def reactivateMat(self):
	#	self.matEnabled == True
	#	print 'mat re-activated'
	
	def floorMatActivated(self):
		if gpio.input(17) == gpio.HIGH:
			return True
		else:
			return False
			
	def greetPerson(self, o):
		if o.greeted == False:
			speakSpeechFromText('Hi '+o.name+'. Welcome back.')
			time.sleep(1)
			print 'hello '+o.name
			o.greeted = True
	
	def checkForNewOccupants(self, system):
		noNewOccupants = True
		print 'checking for new occupants'
	
		for occupant in self.occupants:
			if occupant.present == False: #for all occupants who arent present:
				if occupant.iphoneName == lookup_name(occupant.btID): #if you ping their phone and find that they are now present:
					noNewOccupants = False
					system.adjustOccupantsPresent(self, occupant, "add")
					#self.greetPerson(occupant)
					print occupant.name+' is now present'
			
		if noNewOccupants == True and self.numOfOccupants == 0: 		# no occupants present, and stranger
			INTRUDER = True
			print 'An unidentified person has entered while no one is here'
		elif noNewOccupants == True:   #no new occupants have arrived: one may have left, or an unidentified person may have entered.
			system.resetTime()
			print 'time from last ping has been reset'
	

class System:
	
	def __init__(self, lastPing):
		self.lastPing = lastPing
		#call(["voicecommand"])  #turns on PiAUISuite
		print 'voicecommand start'
		
	def resetTime(self):
		self.lastPing = time.time() 
	
	def fiveMinutesHavePassed(self):
		if time.time() - self.lastPing >= PING_INTERVAL: 
			return True
		else:
			return False
	
	def pingBluetooth(self, fr):
		for occupant in fr.occupants: #go through occupants array
			if occupant.present == True:   #for all occupants present:
				if occupant.iphoneName != lookup_name(occupant.btID):  #pinged and got no response from the address sent to lookup_name
					self.adjustOccupantsPresent(fr, occupant, "remove")
					print occupant.name+' is no longer here'
					
	def adjustOccupantsPresent(self, fr, o, type):
		if type == "add":
			o.greeted = False
			fr.greetPerson(o)
			fr.occupants[o.id].present = True
			fr.numOfOccupants += 1
			print 'Just added '+o.name+' to occupants present'
		elif type == "remove":
			fr.occupants[o.id].present = False
			fr.numOfOccupants -= 1
			print 'Just removed'+o.name+' from occupants present'
					
	
#end class definitions -------------------------------------------------------------------------------------------
	

#main ------------------------------------------------------------------------------------------------------------

Steve = Occupant("Steven", "CC:78:5F:5B:57:29", 0, "PATTERSONSW1\xe2\x80\x99s iPhone", False, False)
JR = Occupant("JR", "FF:FF:FF:FF:FF:FF", 1, "JR's iPhone", False, False)
Josh = Occupant("Josh", "FF:FF:FF:FF:FF:FF", 2, "Josh's iPhone", False, False)
Ken = Occupant("Ken", "FF:FF:FF:FF:FF:FF", 3, "Ken's iPhone", False, False)
Pi = System(time.time())  
FamilyRoom = Room(0, True)     
FamilyRoom.occupants.append(Steve)
FamilyRoom.occupants.append(JR)
FamilyRoom.occupants.append(Josh)
FamilyRoom.occupants.append(Ken)
#INTRUDER = False
REMOVE_INTRUDER = False
PING_INTERVAL = 60
MAT_INTERVAL = 5



	#parse command line args to tell prog who is present when it was started-------
	
for arg in sys.argv:
	if str(arg) == "Steve":
		print 'Steve found in command line'
		Pi.adjustOccupantsPresent(FamilyRoom, Steve, "add")
	elif str(arg) == "JR":
		print 'JR found in command line'
		Pi.adjustOccupantsPresent(FamilyRoom, JR, "add")
	elif str(arg) == "Josh":
		print 'Josh found in command line'
		Pi.adjustOccupantsPresent(FamilyRoom, Josh, "add")
	elif str(arg) == "Ken":
		print 'Ken found in command line'
		Pi.adjustOccupantsPresent(FamilyRoom, Ken, "add")
		
	#end command line parsing-------------------------------------------------------
	
		
	#main logic loop----------------------------------------------------------------
	
while True:  #some number of occupants are present
	
	if FamilyRoom.floorMatActivated() == True:
		print 'floor mat has been activated'
		FamilyRoom.checkForNewOccupants(Pi)
		time.sleep(5)
	if Pi.fiveMinutesHavePassed() == True:
		Pi.pingBluetooth(FamilyRoom)
	
	if INTRUDER == True:
		#take picture
		print 'picture taken, notification sent'
		#send notification
		INTRUDER = False
	if REMOVE_INTRUDER == True:
		#record video
		print 'start recording, turn on music'
		#turn on music
		REMOVE_INTRUDER == False;
	
	time.sleep(.1)
	#end main loop-------------------------------------------------------------------
		

#end main ----------------------------------------------------------------------------------------------------------


