import sys
import RPi.GPIO as GPIO
import time

# Pin configuration
SENSOR_ECHO = 7
SENSOR_TRIGGER = 11
LED_PIN = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_ECHO, GPIO.IN)
GPIO.setup(SENSOR_TRIGGER, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

led = GPIO.PWM(LED_PIN, 100)

def getdistance():
    GPIO.output(SENSOR_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)
    GPIO.output(SENSOR_TRIGGER, GPIO.LOW)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(SENSOR_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(SENSOR_ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance

led.start(0)

try:
    while True:
        distance = getdistance()
        led_brightness = 100 - (distance / 30) * 100

        # Clamp if below 0%
        if led_brightness < 0:
            led_brightness = 0
        
        led.ChangeDutyCycle(led_brightness)
        print(distance, " ", led_brightness)

except KeyboardInterrupt:
    GPIO.cleanup()
