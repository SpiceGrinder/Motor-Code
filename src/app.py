from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import RPi.GPIO as GPIO
from jsonrpc import JSONRPCResponseManager, dispatcher

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



@dispatcher.add_method
def hello(**kwargs):
    return 'Hello ' + kwargs['name']

@dispatcher.add_method
def toggle(**kwargs):
    motor(kwargs['toggle'], kwargs['motor'])
    return True



@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
