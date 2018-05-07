# import the fetchData file to be used
import fetchData as fetchData

# import RPi library to control IO through GPIO pins
import RPi.GPIO as GPIO

# import library for customisable date and time formats
import datetime

#import time library for sleep function
import time

# initialise the database with the firebase library
from firebase import firebase
firebase = firebase.FirebaseApplication('https://internetworking-project-c8b1f.firebaseio.com/')

# declare GPIO pin 7 as the channel for IO
channel = 7 

# set the GPIO pin numbering scheme to BOARD 
GPIO.setmode(GPIO.BOARD)

# set the channel to provide input 
GPIO.setup(channel, GPIO.IN)

# function to generate a date in the following format: DD/MM/YY HH:MM pm/am
def printDateTime():
	currentDateTime = datetime.datetime.now().strftime("%d/%m/%y %I:%M %P")
	print(currentDateTime)

# function to send data to the database when input is detected from a sensor
def sound(channel):
	if GPIO.input(channel):
		pushToFirebase()

# call the function to get data from the database
def fetchCommand():
	fetchData.fetch()
	
# set interval between two callbacks to 300ms
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, sound)


# function to update a database node with a status and the current time
def pushToFirebase():
	currentDateTime = datetime.datetime.now().strftime("%d/%m/%y %I:%M %P")
	printDateTime()
	result = firebase.post('/Lock', {'status':'Unlocked', 'time':currentDateTime})
	print(result) 

while True:
	time.sleep(1)
