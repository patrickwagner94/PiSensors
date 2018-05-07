# import the fetchData file to be used
#import fetchData as fetchData

# import RPi library to control IO through GPIO pins
import RPi.GPIO as GPIO

# import library for customisable date and time formats
#import datetime

#import time library for sleep function
import time

# initialise the database with the firebase library
from firebase import firebase
firebase = firebase.FirebaseApplication('https://internetworking-project-c8b1f.firebaseio.com/')

# declare GPIO pins as the channels for IO
sensor = 16
buzzer = 18

# set the GPIO pin numbering scheme to BOARD 
GPIO.setmode(GPIO.BOARD)

# set the channel to provide input and output
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)

# function to generate a date in the following format: DD/MM/YY HH:MM pm/am
def printDateTime():
	currentDate = datetime.datetime.now().strftime("%d/%m/%y")
	currentTime = datetime.datetime.now().strftime("%I:%M %P")
	return currentDate, currentTime

def pushToFirebase():
	currentDate, currentTime = printDateTime()
	result = firebase.post('/Smoke_Kitchen', {'date':currentDate, 'status':'Active', 'time':currentTime})
	print(result)

GPIO.output(buzzer,False)
print ("Initialising PIR Sensor.....")
time.sleep(5)
print ("PIR Ready")

try:
	while True:
		if GPIO.input(sensor):
			pushToFirebase()
			GPIO.output(buzzer,True)
			print "Motion Detected"
			while GPIO.input(sensor):
				time.sleep(0.2)
		else:
			GPIO.output(buzzer,False)

except KeyboardInterrupt:
    GPIO.cleanup()
