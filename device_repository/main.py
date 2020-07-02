import i2c_read
import json
import time
import read_dht
import pycom
import _thread
from mqtt import MQTTClient
import ubinascii
import hashlib
import machine

with open('config.json') as f:
    config = json.load(f)

def sub_cb(topic, msg):
    if msg == b'{"alert":1}': pycom.rgbled(0x00ff04)
    if msg == b'{"alert":2}': pycom.rgbled(0xe5ff00)
    if msg == b'{"alert":3}': pycom.rgbled(0xff0000)
    #if msg == b'{"Command":"Blue"}': pycom.rgbled(0x0004ff)
    if msg == b'{"alert":0}': pycom.rgbled(0xe5ff00)
    #if msg == b'{"Command":"Off"}': pycom.rgbled(0x000000)
    print((topic, msg))

def interval_send(t_):
    while True:
        send_value()
        time.sleep(t_)

def blink_led():
    for n in range(1):
        pycom.rgbled(0xfcfc03)
        time.sleep(0.5)
        pycom.rgbled(0x000000)
        time.sleep(0.2)

def send_value():
    try:
        co2, voc = i2c_read.value()
        dht_T, dht_RH = read_dht.value()
        print('co2: ', co2) # two bytes
        print('voc: ', voc) # two bytes
        print('dht temp: ', dht_T) # one byte
        print('dht RH: ', dht_RH) # one byte
        c.publish(topic_pub,'{"home_sensor": {"co2":' + str(co2) +
                          ',"voc":'+ str(voc) +
                          ',"temperature":' + str(dht_T) +
                          ',"humidity":' + str(dht_RH) +
                          '}}')
        blink_led()

    except (NameError, ValueError, TypeError):
        pass


# topic = 'testtopic7891/1'
# broker_url = 'broker.hivemq.com' # HiveMQ can be used for testing, open broker
topic_pub = 'topic_pub' #Need to be changed
topic_sub = 'topic_sub' #Need to be changed
broker_url = 'broker_url' #Need to be changed
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac

c = MQTTClient(client_name,broker_url,user=config['user_mqtt'],password=config['pass_mqtt'])
c.set_callback(sub_cb)
c.connect()
c.subscribe(topic_sub)

# not used at the moment in this code. But - if you want to have something sent
# back to the device run this function in a loop (or in a thread)

# def listen_command():
#     while True:
#         if True:
#             # Blocking wait for message
#             c.wait_msg()
#         else:
#             # Non-blocking wait for message
#             c.check_msg()
#             # Then need to sleep to avoid 100% CPU usage (in a real
#             # app other useful actions would be performed instead)
#             time.sleep(2)

def listen_command(i_):
    while True:
        c.check_msg()
        time.sleep(i_)

_thread.start_new_thread(interval_send,[10])
_thread.start_new_thread(listen_command,[0.1])
