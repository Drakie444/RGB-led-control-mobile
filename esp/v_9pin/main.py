from machine import Pin
import time


r1 = Pin(16, Pin.OUT)
g1 = Pin(17, Pin.OUT)
b1 = Pin(18, Pin.OUT)

led1 = [r1, g1, b1]

r2 = Pin(19, Pin.OUT)
g2 = Pin(21, Pin.OUT)
b2 = Pin(22, Pin.OUT)

led2 = [r2, g2, b2]

r3 = Pin(25, Pin.OUT)
g3 = Pin(26, Pin.OUT)
b3 = Pin(27, Pin.OUT)

led3 = [r3, g3, b3]

for led in [led1, led2, led3]:
    for diode in led:
        diode.value(0)

for _ in range(100):
    r1.value(1)
    time.sleep(0.2)
    r1.value(0)
    r2.value(1)
    time.sleep(0.2)
    r2.value(0)
    r3.value(1)
    time.sleep(0.2)
    r3.value(0)

