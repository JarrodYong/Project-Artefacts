import paho.mqtt.client as mqtt         # Import the MQTT library
import time                 # The time library is useful for delays
import RPi.GPIO as GPIO

LED = 4
LEDSCAN = 21
LEDWARN = 20
LEDOK = 16

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED,GPIO.OUT)
GPIO.setup(LEDSCAN,GPIO.OUT)
GPIO.setup(LEDWARN,GPIO.OUT)
GPIO.setup(LEDOK,GPIO.OUT)

def warn():
     i=0
     while i<10:
       GPIO.output(LEDWARN,GPIO.HIGH)
       time.sleep(0.1)
       GPIO.output(LEDWARN,GPIO.LOW)
       time.sleep(0.1)
       i+= 1
       
def Scanning():
    GPIO.output(LEDSCAN,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LEDSCAN,GPIO.LOW)
    
def openDoor():
    i=0
    while i<10:
        GPIO.output(LEDOK,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(LEDOK,GPIO.LOW)
        time.sleep(0.1)
        i+= 1
        
    GPIO.output(LED,GPIO.HIGH)
    time.sleep(4)
    GPIO.output(LED,GPIO.LOW)
    time.sleep(0.5)
# Our "on message" event
def messageFunction (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    print(topic + message)
    if (message == "Card Scanned"):
        Scanning()
        print('Checking System and Temperature')
    if (message == "Open Lock"):
        openDoor()
        print('Everything is fine enjoy your day!')
    if (message == "Stay Locked"):
        warn()
        print('Your Temperature is unusually high please go get tested and head home for today.')
        
ourClient = mqtt.Client("Jarrods Raspberry Pi")     # Create a MQTT client object
ourClient.connect("test.mosquitto.org", 1883)   # Connect to the test MQTT broker
ourClient.subscribe("Security ")            # Subscribe to the topic AC_unit
ourClient.on_message = messageFunction      # Attach the messageFunction to subscription
ourClient.loop_start()              # Start the MQTT client

while(1):
 time.sleep(1)