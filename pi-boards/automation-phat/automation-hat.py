#LCD : CN6 to CN2
#DHT11 : RM19 to RM2
#Ultrasonice : RM21 to RM4
#SoilMoisture: RM23 to RM6
#Relay : RM26 to RM27
#bUZZER: RM1 to RM7
#Stepomotor : CN7 to CN10
#LED: CN4 to CN9
import time
import Adafruit_DHT
import automationhat
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import subprocess
import lcdlib
from subprocess import PIPE
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
ECHO = 37
TRIG = 35
moisture = 38
Relay = 36
Buzzer = 5
StepPins = [33,7,31,29]


#moisture = 19
# Set all pins as output
for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
            
StepCount = len(Seq)
StepDir = 2 # Set to 1 or 2 for clockwise

# Read wait time from command line
WaitTime = 10/float(1000)
     
    # Initialise variables
#StepCounter = 0
    
  
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(Buzzer,GPIO.OUT)
GPIO.setup(Relay,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(moisture,GPIO.IN)
#GPIO.setup(33,GPIO.IN)
GPIO.output(3,False)
GPIO.output(5,False)


def readADC(channel):
    if channel == 1:
        humidity,adc_value = Adafruit_DHT.read_retry(11,4)
    elif channel == 2:
        adc_value, temperature = Adafruit_DHT.read_retry(11,4)
    elif channel == 3:
        spi_mods = subprocess.Popen(['sudo lsmod |grep spi_b*'], shell=True,stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, bufsize=1,
                               universal_newlines=True)
        output = spi_mods.communicate()[0]
        spi_mod_name = output.split()[0]
        #print("SPI MOD = ",spi_mod_name)
        result = subprocess.check_output(['sudo', 'rmmod', spi_mod_name])
        result = subprocess.check_output(['sudo', 'modprobe', spi_mod_name])

        SPI_PORT   = 0
        SPI_DEVICE = 0
        mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
        moisture_value = mcp.read_adc(0)
        adc_value = moisture_value
    elif channel == 4:
        lcdlib.lcd_init()
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        print("Waitng For Sensor To Settle")
        time.sleep(2)                            #Delay of 2 seconds

        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
          pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
          pulse_end = time.time()                #Saves the last known time of HIGH pulse 

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance)
        lcdlib.lcd_string("Distance : "+str(distance),0x80)
        adc_value = distance
    else:
        state = False
        print "Specified input channel is out of range."
    print(adc_value)
    return float(adc_value)

def writeOutput(channel, state):
    if channel == 1:
        if(state == True):
            run_motor()
        if(state == False):
            off_motor()
    elif channel == 2:
        GPIO.output(Buzzer,state)
    elif channel == 3:
        GPIO.output(3,state)
    return 0    
def writeRelay(channel, state):
    if channel == 1:
        GPIO.output(Relay,state)
    #elif channel == 2:
    #    GPIO.output(Relay,state)
    return 0        
def readInput(channel):
    if channel == 1:
        value = GPIO.input(moisture)
    print(value)
    return int(value)
    
def run_motor():
    # Set to -1 or -2 for anti-clockwise
     
    
    StepCounter = 0 
    # Start main loop
    for i in range(0,500):
      print StepCounter,
      print Seq[StepCounter]
     
      for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          print " Enable GPIO %i" %(xpin)
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
     
      StepCounter += StepDir
     
      # If we reach the end of the sequence
      # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
        StepCounter = StepCount+StepDir
     
      # Wait before moving on
      time.sleep(0.01)
def off_motor():
    StepCounter = 0
     
    # Start main loop
    for i in range(0,500):
      print StepCounter,
      print Seq[StepCounter]
     
      for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          print " Enable GPIO %i" %(xpin)
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
     
      StepCounter -= StepDir
     
      # If we reach the end of the sequence
      # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
        StepCounter = StepCount-StepDir
     
      # Wait before moving on
      time.sleep(0.01)
#writeOutput(2,0)
#readADC(3)
#readInput(1)
#writeOutput(1,0)
#readADC(1)
#readADC(2)
#readADC(4)
#readInput(1)
