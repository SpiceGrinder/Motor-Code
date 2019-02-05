from time import sleep
import RPi.GPIO as GPIO

#setting up pins
########THESE LINE WILL NEED TO BE ADDED TO THE MAIN CODE TO SETUP GPIO PINS########
Motor1 = 5 #set GPIO pin thats connected to first motor
Motor2 = 12 #set GPIO pin thats connected to second motor
Motor3 = 6 #set GPIO pin thats connected to third motor
Motor4 = 13 #set GPIO pin thats connected to fourth motor
Motor5 = 19 #set GPIO pin thats connected to fifth motor
Motor6 = 26 #set GPIO pin thats connected to sixth motor
Sleep = 16 #set GPIO pin thats connected to Sleep
Step = 20 #set GPIO pin thats connected to Step
Dir = 21 #set GPIO pin thats connected to Dir
CW = 1 #used for clockwise direction
CCW = 0 #used for counter clockwise direction

#setting up GPIO pins
GPIO.setmode(GPIO.BCM)
Outs = (Motor1,Motor2,Motor3,Motor4,Motor5,Motor6,Sleep,Step,Dir)
GPIO.setup(Outs, GPIO.OUT)
###################################################################################


#motor function triggers motor on or off. E.I motor(ON,Motor1) will turn on motor 1
def motor(toggle,motor):
    if toggle == 1:
        GPIO.output(motor, GPIO.HIGH)
    if toggle == 0:
        GPIO.output(motor, GPIO.LOW)

#function that spins the stepper motor in a certain direction for x number of
#rotations. E.I steppermotor(.5,CW) will spin stepper motor half a rotation clockwise
def steppermotor(rotation, direction):
    #setting up stepper motor controller
    Sleep = 21 #set GPIO pin thats connected to Sleep
    Step = 20 #set GPIO pin thats connected to Step
    Dir = 16 #set GPIO pin thats connected to Dir
    
    delay = .0005 #preset time
    SPR = 200 #preset Steps per Revolution
    step_count = SPR * rotation #calculating how far the motor will spin
    GPIO.output(Sleep, GPIO.HIGH)  #turning on stepper motor controller
    GPIO.output(Dir,direction)  #telling controller what direction to move
    
    #rotating stepper motor
    for x in range(step_count):
        GPIO.output(Step, GPIO.HIGH)
        sleep(delay)
        GPIO.output(Step, GPIO.LOW)
        sleep(delay)
    
    sleep(2) #making sure motor fully stops before turning off stepper motor controller
    GPIO.output(Sleep, GPIO.LOW)  #turning off stepper motor controller

#this is a series of function calls that turns on the motors 1 by 1 until they are all turned on then turns them off to run the stepper motor for half a turn clockwise and a full turn counterclockwise

motor(1,Motor1)
sleep(1)
motor(1,Motor2)
sleep(1)
motor(1,Motor3)
sleep(1)
motor(1,Motor4)
sleep(1)
motor(1,Motor5)
sleep(1)
motor(1,Motor6)
sleep(1)
motor(0,Motor6)
motor(0,Motor1)
motor(0,Motor5)
motor(0,Motor4)
motor(0,Motor2)
motor(0,Motor3)


steppermotor(1,CW)
sleep(2)
steppermotor(1,CCW)













