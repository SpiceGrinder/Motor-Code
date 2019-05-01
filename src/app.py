from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import RPi.GPIO as GPIO
from jsonrpc import JSONRPCResponseManager, dispatcher
from hx711 import HX711
import threading
import time

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
            'motor': 2,
            'scale': [15, 17],
            'reference': 6659
            },
        '1': {
            'motor': 3,
            'scale': [18, 27]
            },
        '2': {
            'motor': 4,
            'scale': [22, 23],
            'reference': 6921
            },
        '3': {
            'motor': 5,
            'scale': [24, 25]
            },
        '4': {
            'motor': 6,
            'scale': [19, 16]
            },
        '5': {
            'motor': 7,
            'scale': [26, 20]
            },
        }

#motor function triggers motor on or off. E.I motor(ON,Motor1) will turn on motor 1
def toggle_motor(toggle,motor):
    if toggle == 1:
        GPIO.output(motor, GPIO.HIGH)
    if toggle == 0:
        GPIO.output(motor, GPIO.LOW)

def grindSpice(motor, amount):
<<<<<<< HEAD
    # start the motor
    print "starting motor #", motor
    toggle_motor(0, motorDict[motor]['motor'])

=======
>>>>>>> 97f8071d3b9ea2e0b999f2d18da74dd60a7391f4
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

<<<<<<< HEAD
        # stop the motor
    print "stopping motor #", motor
=======
    # stop the motor
    print "stopping motor"
>>>>>>> 97f8071d3b9ea2e0b999f2d18da74dd60a7391f4
    toggle_motor(0, motorDict[motor]['motor'])

class grindThread(threading.Thread):
    def __init__(self, motor, amount):
        threading.Thread.__init__(self)
        self.motor = motor
        self.amount = amount
    def run(self):
        grindSpice(self.motor, self.amount)


@dispatcher.add_method
def hello(**kwargs):
    return 'Hello ' + kwargs['name'][1]

@dispatcher.add_method
def toggle(**kwargs):
    toggle_motor(kwargs['toggle'], kwargs['motor'])
    return True

@dispatcher.add_method
def grindSpices(**kwargs):
    threads = []
    for spice in kwargs['spices']:
        spiceThread = grindThread(spice['grinder'], spice['amount'])
        spiceThread.start()
        threads.append(spiceThread)

    for t in threads:
        t.join()

    return "finished"

@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()


if __name__ == '__main__':
    run_simple('0.0.0.0', 4000, application)
    #except (KeyboardInterrupt, SystemExit):
    #    cleanAndExit()
