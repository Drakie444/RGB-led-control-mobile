from machine import Pin, PWM
import time
import network
import socket
from config import WIFI_PASS, WIFI_SSID

wlan = network.WLAN(network.STA_IF)

r1 = PWM(Pin(16), freq=1000)
g1 = PWM(Pin(17), freq=1000)
b1 = PWM(Pin(18), freq=1000)

led1 = [r1, g1, b1]

r2 = Pin(19, Pin.OUT)
g2 = Pin(21, Pin.OUT)
b2 = Pin(22, Pin.OUT)

led2 = [r2, g2, b2]

r3 = Pin(25, Pin.OUT)
g3 = Pin(26, Pin.OUT)
b3 = Pin(27, Pin.OUT)

led3 = [r3, g3, b3]

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

def set_color_led1(r_val, g_val, b_val):
    r_ns = int((r_val / 255) * 1_000_000)
    g_ns = int((g_val / 255) * 1_000_000)
    b_ns = int((b_val / 255) * 1_000_000)

    r1.duty_ns(r_ns)
    g1.duty_ns(g_ns)
    b1.duty_ns(b_ns)

wifi_connect()
set_color_led1(0, 0, 0)

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

            set_color_led1(r, g, b)
            
        except Exception as e:
            print("Error receiving the data:", e)

    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK"
    conn.send(response)
    conn.close()
