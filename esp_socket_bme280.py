from machine import Pin, I2C
import bme280
import socket
import network
import ure
from utime import sleep

i2c = I2C(sda=Pin(4), scl=Pin(5))
bme = bme280.BME280(i2c=i2c)

ap_if = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
    
sta.active(False)
ap_if.active(True)   

ap_if.config(
            essid="First",
            hidden=0,
            authmode=4,
            channel=5,
            password="12345678"
            )

ap_if.ifconfig((
                '192.168.3.1', 
                '255.255.255.0', 
                '192.168.3.2', 
                '8.8.8.8'))


s = socket.socket()
s.bind(('192.168.3.1', 9090))
s.listen(1)

def value_bme():
    return b'%s|%s|%s' % (bme.values[0], bme.values[2], bme.values[1])


    

while True:
    cl, addr = s.accept()
    data = cl.recv(30)
    if data == b'bme':
        cl.send(value_bme())
    cl.close()
        



