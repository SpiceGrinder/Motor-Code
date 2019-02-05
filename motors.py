from time import sleep
import RPI.GPIO as GPIO

#setting up pins
########THESE LINE WILL NEED TO BE ADDED TO THE MAIN CODE TO SETUP GPIO PINS########
Motor1 = 5 #set GPIO pin thats connected to first motor
Motor2 = 6 #set GPIO pin thats connected to second motor
Motor3 = 13 #set GPIO pin thats connected to third motor
Motor4 = 19 #set GPIO pin thats connected to fourth motor
Motor5 = 26 #set GPIO pin thats connected to fifth motor
Motor6 = 12 #set GPIO pin thats connected to sixth motor
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
    if toggle == ON:
        GPIO.output(motor, GPIO.HIGH)
    if toggle == OFF:
        GPIO.output(motor, GPIO.LOW)

#function that spins the stepper motor in a certain direction for x number of
#rotations. E.I steppermotor(.5,CW) will spin stepper motor half a rotation clockwise
def steppermotor(rotation, direction):
    #setting up stepper motor controller
    Sleep = 16 #set GPIO pin thats connected to Sleep
    Step = 20 #set GPIO pin thats connected to Step
    Dir = 21 #set GPIO pin thats connected to Dir
    
    delay = .003 #preset time
    SPR = 1600 #preset Steps per Revolution
    step_count = SPR * rotation #calculating how far the motor will spin
    GPIO.output(Sleep, GPIO.HIGH)  #turning on stepper motor controller
    GPIO.output(Dir,direction)  #telling controller what direction to move

    #rotating stepper motor
    for x in range(step_count):
        GPIO.output(Step, GPIO.HIGH)
        sleep(delay)
        GPIO.output(Step, GPIO.LOW)
        sleep(delay)

    delay(2) #making sure motor fully stops before turning off stepper motor controller
    GPIO.output(Sleep, GPIO.LOW)  #turning off stepper motor controller
    GPIO.cleanup()




