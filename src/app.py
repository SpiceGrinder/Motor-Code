from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import RPi.GPIO as GPIO
from jsonrpc import JSONRPCResponseManager, dispatcher
from hx711 import HX711
import threading

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
Scale5 = [26, 20]
Motor6 = 7 #set GPIO pin thats connected to sixth motor
Sleep = 12 #set GPIO pin thats connected to Sleep
Step = 13 #set GPIO pin thats connected to Step
Dir = 14 #set GPIO pin thats connected to Dir
CW = 1 #used for clockwise direction
CCW = 0 #used for counter clockwise direction

#setting up GPIO pins
GPIO.setmode(GPIO.BCM)
Outs = (Motor1,Motor2,Motor3,Motor4,Motor5,Motor6,Sleep,Step,Dir)
GPIO.setup(Outs, GPIO.OUT)
###################################################################################

# maping the motor with the scale
motorDict = {
        '0': {
            'motor': 2,
            'scale': [15, 17]
            },
        '1': {
            'motor': 3,
            'scale': [18, 27]
            },
        '2': {
            'motor': 4,
            'scale': [22, 23]
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
        GPIO.output(motorDict[motor]['motor'], GPIO.HIGH)
    if toggle == 0:
        GPIO.output(motorDict[motor]['motor'], GPIO.LOW)

def grindSpice(motor, amount):
    # start the motor
    toggle_motor(motorDict[motor]['motor'], 1)

    # Setting up scales
    ### first param a GPIO number?
    hx = HX711(motorDict[motor]['scale'][0], motorDict[motor]['scale'][1])
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(920)

    hx.reset()
    hx.tare()

    while True:
        try:
            val = hx.get_weight(5)
            val = hx.read_long()
            print "Grinder #", motor, " grinded ", val

            if val >= amount:
                break

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            print("error with the scale")

        # stop the motor
        toggle_motor(motorDict[motor]['motor'], 0)

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
        threads.append(grindThread(spice['grinder'], spice['amount']))

    for t in threads:
        t.join()

    return "finished"

@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
