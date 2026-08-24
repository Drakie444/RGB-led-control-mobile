from machine import Pin, PWM
import time
import network
import socket
from config import WIFI_PASS, WIFI_SSID

wlan = network.WLAN(network.STA_IF)

r1 = PWM(Pin(16), freq=1000)
g1 = PWM(Pin(17), freq=1000)
b1 = PWM(Pin(18), freq=1000)

r2 = PWM(Pin(19), freq=1000)
g2 = PWM(Pin(21), freq=1000)
b2 = PWM(Pin(22), freq=1000)

r3 = PWM(Pin(25), freq=1000)
g3 = PWM(Pin(26), freq=1000)
b3 = PWM(Pin(27), freq=1000)

r_leds = [r1, r2, r3]
g_leds = [g1, g2, g3]
b_leds = [b1, b2, b3] 

def wifi_connect():
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    print("Connecting to wifi...")
    for _ in range(20):
        if wlan.isconnected():
            print("Connected to wifi.")
            print(f"ESP32 IP address: {wlan.ifconfig()[0]}")
            return 
        time.sleep(0.5)

    print("Error, couldn't connect to the wifi.")
    return

def set_color(r_val, g_val, b_val):
    r_ns = int((r_val / 255) * 1_000_000)
    g_ns = int((g_val / 255) * 1_000_000)
    b_ns = int((b_val / 255) * 1_000_000)

    for led in r_leds: led.duty_ns(r_ns)
    for led in g_leds: led.duty_ns(g_ns)
    for led in b_leds: led.duty_ns(b_ns)

wifi_connect()
set_color(0, 0, 0)

# --- setting up the http server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 80))
server.listen(5)

print("Server HTTP is listening...")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024).decode('utf-8')

    if 'GET /set?' in request:
        try:
            params = request.split('GET /set?')[1].split(' ')[0]
            r, g, b = params.split('&')
            r = int(r[2:])
            g = int(g[2:])
            b = int(b[2:])
            print(r, g, b) 

            set_color(r, g, b)
            
        except Exception as e:
            print("Error receiving the data:", e)

    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK"
    conn.send(response)
    conn.close()
