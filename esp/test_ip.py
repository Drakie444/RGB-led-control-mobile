import network
import time
from config import WIFI_PASS, WIFI_SSID

wifi = network.WLAN(network.STA_IF)
wifi.active(False)
time.sleep(1)
wifi.active(True)

wifi.connect(WIFI_SSID, WIFI_PASS)

for _ in range(10):
    if not wifi.isconnected():
        time.sleep(1)

if wifi.isconnected():
    print("IP ESP32:", wifi.ifconfig()[0])
else:
    print("Could not connect to wifi")