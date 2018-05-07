# import the buzzer file to be used
import buzzer as buzzer

#import RPi library to control IO through GPIO pins
import RPi.GPIO as GPIO

# import time library for sleep function 
import time
 
# import library for customisable date and time formats 
import datetime

# initialise the database with the firebase library
from firebase import firebase
firebase = firebase.FirebaseApplication('https://internetworking-project-c8b1f.firebaseio.com/')

# function to poll the lock status from the database and trigger the alarm accordingly 
def fetch():
	# retrieve the Current Status node from the database
	fetchData = firebase.get('/LockStatus/Current Status', None)
	a = str(fetchData)
	# if the Current Status is "Locked", then stop the alarm
	if "Locked" in a:
		buzzer.stopSound()

	# if the Current Status is "Unlocked", then start the alarm
	elif "Unlocked" in a:
		buzzer.buzzSound()
		
	GPIO.cleanup()
	time.sleep(1)
	
while True:
	fetch()
