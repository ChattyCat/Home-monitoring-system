#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# See https://docs.pycom.io for more information regarding library specifics

import time
import pycom
from pysense import Pysense
import machine
import os
import ubinascii
import hashlib
from mqtt import MQTTClient
import micropython

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

py = Pysense()

si = SI7006A20(py)
lt = LTR329ALS01(py)

topic_pub = config['topic_pub']
topic_sub = config['topic_sub']
broker_url = config['broker']
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac

c = MQTTClient(client_name,broker_url,user=config['user_mqtt'],password=config['pass_mqtt'])
#c.set_callback(sub_cb)
c.connect()
#c.subscribe(topic_sub)

#def sub_cb(topic, msg):
#    print((topic, msg))

#def interval_send(t_):
#    while True:
#        send_value()
#        time.sleep(t_)

#def listen_command(i_):
#    while True:
#        c.check_msg()
#        time.sleep(i_)

#def send_value(t_):
#    try:
#        temper = si.temperature()
#        dew = si.dew_point()
#        light = lt.light()
#        print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
#        print("Dew point: "+ str(si.dew_point()) + " deg C")
#        t_ambient = 24.4
#        print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")
#        print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
#        c.publish(topic_pub,'{"home_sensor": {"co2":' + str(temper) +
#        ',"voc":'+ str(dew) +
#        ',"temperature":' + str(light) +
#        '}}')
t_ambient = 24.4

while True:
    temper = si.temperature()
    dew = si.dew_point()
    light = lt.light()
    print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
    print("Dew point: "+ str(si.dew_point()) + " deg C")

    print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")
    print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
    c.publish(topic_pub,'{"home_sensor_pysense": {"temperature":' + str(temper) +
            ',"dew":'+ str(dew) +
            ',"light":' + str(light) +
            '}}')
    pycom.rgbled(0)
    time.sleep(5)
    py.setup_sleep(10)
    py.go_to_sleep()

#_thread.start_new_thread(_thread, ())
#_thread.start_new_thread(interval_send,[10])
#_thread.start_new_thread(listen_command,[0.1])
