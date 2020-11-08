from time import sleep

from gpiozero import LEDBoard, LEDBarGraph, Button, LED

testled = LED(25)

while True:
    testled.on()
    sleep(1)
    testled.off()
    sleep(1)