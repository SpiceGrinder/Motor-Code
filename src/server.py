from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep
import threading

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def grind_spices():
    threads = []
    content = request.get_json(force=True)

    print content

    for spice in content['spices']:
        spiceThread = grindThread(spice['grinder'], spice['amount'])
        spiceThread.start()
        threads.append(spiceThread)

    for t in threads:
        t.join()

    return 'finished'

#setting up pins
########THESE LINE WILL NEED TO BE ADDED TO THE MAIN CODE TO SETUP GPIO PINS########
Motor1 = 2 #set GPIO pin thats connected to first motor
Scale1 = [15,17]
Motor2 = 3 #set GPIO pin thats connected to second motor
Scale2 = [18, 27]
Motor3 = 4 #set GPIO pin thats connected to third motor
Scale3 = [22, 23]
Motor4 = 5 #set GPIO pin thats connected to fourth motor
Scale4 = [24, 25]
Motor5 = 6 #set GPIO pin thats connected to fifth motor
Scale5 = [19, 16]
Motor6 = 7 #set GPIO pin thats connected to sixth motor
Scale6 = [26, 20]
Sleep = 12 #set GPIO pin thats connected to Sleep
Step = 13 #set GPIO pin thats connected to Step
Dir = 14 #set GPIO pin thats connected to Dir
CW = 1 #used for clockwise direction
CCW = 0 #used for counter clockwise direction

#setting up GPIO pins
GPIO.setmode(GPIO.BCM)
Outs = (Motor1,Motor2,Motor3,Motor4,Motor5,Motor6,Sleep,Step,Dir,Scale1[1],Scale2[1],Scale3[1],Scale4[1],Scale5[1],Scale6[1])
Ins = (Scale1[0],Scale2[0],Scale3[0],Scale4[0],Scale5[0],Scale6[0])
GPIO.setup(Outs, GPIO.OUT)
GPIO.setup(Ins, GPIO.IN)
###################################################################################

# maping the motor with the scale
motorDict = {
        '0': {
            'motor': Motor1,
            'scale': Scale1,
            'reference': 6659
            },
        '1': {
            'motor': Motor2,
            'scale': Scale2,
            'reference': 6659
            },
        '2': {
            'motor': Motor3,
            'scale': Scale3,
            'reference': 6921
            },
        '3': {
            'motor': Motor4,
            'scale': Scale4,
            'reference': 6659
            },
        '4': {
            'motor': Motor5,
            'scale': Scale5,
            'reference': 6659
            },
        '5': {
            'motor': Motor6,
            'scale': Scale6,
            'reference': 6659
            },
        }

#motor function triggers motor on or off. E.I motor(ON,Motor1) will turn on motor 1
def toggle_motor(toggle,motor):
    if toggle == 1:
        GPIO.output(motor, GPIO.HIGH)
    if toggle == 0:
        GPIO.output(motor, GPIO.LOW)

def wiggle(amount):
    delay = .00055 #preset time
    SPR = 200 #preset Steps per Revolution
    step_count = SPR * 1 #calculating how far the motor will spin
    GPIO.output(Sleep, GPIO.HIGH)  #turning on stepper motor controller
    GPIO.output(Dir,1)  #telling controller what direction to move
    
    #rotating stepper motor
    for y in range(int(amount)):
        GPIO.output(Dir,y%2)
        for x in range(int(step_count)):
            GPIO.output(Step, GPIO.HIGH)
            sleep(delay)
            GPIO.output(Step, GPIO.LOW)
            sleep(delay)
    
    sleep(2) #making sure motor fully stops before turning off stepper motor controller
    GPIO.output(Sleep, GPIO.LOW)  #turning off stepper motor controller
 

def grindSpice(motor, amount):
    # Setting up scales
    ### first param a GPIO number?
    print "setting up scale"
    hx = HX711(motorDict[motor]['scale'][0], motorDict[motor]['scale'][1])
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(motorDict[motor]['reference'])
    

    hx.reset()
    hx.tare()

    # start the motor
    print "starting motor"
    toggle_motor(1, motorDict[motor]['motor'])

    while True:
        try:
            val_A = hx.get_weight_A(1)
            #val_B = hx.get_weight_B(5)
            print "A: %s" % ( val_A)

            hx.power_down()
            hx.power_up()
            #time.sleep(0.01)

            if val_A >= amount:
                #toggle_motor(0, motorDict[motor]['motor'])
                break

        except (KeyboardInterrupt, SystemExit):
            print("error with the scale")
    # stop the motor
    print "stopping motor"
    toggle_motor(0, motorDict[motor]['motor'])

    wiggle(4)
    sleep(1)
    wiggle(4)


class grindThread(threading.Thread):
    def __init__(self, motor, amount):
        threading.Thread.__init__(self)
        self.motor = motor
        self.amount = amount
    def run(self):
        grindSpice(self.motor, self.amount)



if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)

