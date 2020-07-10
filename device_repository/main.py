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
import buzzer_code
import _thread
from machine import Pin,  PWM
from machine import ADC

co2High = False
numThread = 0
co2HighValue = 0
buzzer_unit = Pin("P7")

with open('config.json') as f:
    config = json.load(f)

def battery():
    adc = ADC(0)
    adc_c = adc.channel(pin='P16')
    mult = 1.64
    value = adc_c.voltage()
    bat_vdc = round((value*3/1000) * (mult), 2)

    print("ADC value:" + str(bat_vdc))
    return(bat_vdc)

def buzz(co2HighTest, tune):
    global numThread
    global buzzer_unit
    pwm = PWM(0, frequency=300)
    pwm_channel = pwm.channel(2, duty_cycle=0.5, pin=buzzer_unit)

    global co2High
    global co2HighValue
    while co2High == True:
            buzzer_code.buzz(pwm_channel, pwm)

    numThread = numThread - 1
    #buzzer_unit = 0

def sub_cb(topic, msg):
    global co2High
    global numThread
    print(co2High)
#    if msg == b'{"alert":1}':
#        pycom.rgbled(0x00ff04)
#        time.sleep(1)
#        pycom.rgbled(0x000000)
#        time.sleep(0.2)
#        co2High = False
#    if msg == b'{"alert":2}':
#        pycom.rgbled(0x00ff04)
#        time.sleep(1)
#        pycom.rgbled(0x000000)
#        time.sleep(0.2)
#        co2High = False
    if msg == b'{"alert":1}':
        pycom.rgbled(0xe5ff00)
        time.sleep(1)
        pycom.rgbled(0x000000)
        time.sleep(0.2)
        co2High = True
        numThread = numThread + 1
        if co2High == True and numThread <= 1:
            _thread.start_new_thread(buzz, (co2High, 1))
    if msg == b'{"alert":2}':
        pycom.rgbled(0xff0000)
        time.sleep(1)
        pycom.rgbled(0x000000)
        time.sleep(0.2)
        co2High = True
        numThread = numThread + 1
        numThread = numThread - 1
        if co2High == True and numThread <= 1:
            _thread.start_new_thread(buzz, (co2High, 2))
    if msg == b'{"alert":3}':
        pycom.rgbled(0xff0000)
        time.sleep(1)
        pycom.rgbled(0x000000)
        time.sleep(0.2)
        co2High = True
        numThread = numThread + 1
        if co2High == True and numThread <= 1:
            _thread.start_new_thread(buzz, (co2High, 2))
    #if msg == b'{"Command":"White"}': pycom.rgbled(0xe5ff00)
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
    global co2HighValue
    try:
        co2, voc = i2c_read.value()
        dht_T, dht_RH = read_dht.value()
        voltage = battery()
        co2HighValue = co2
        print('co2: ', co2) # two bytes
        print('voc: ', voc) # two bytes
        print('dht temp: ', dht_T) # one byte
        print('dht RH: ', dht_RH) # one byte
        c.publish(topic_pub,'{"home_sensor": {"co2":' + str(co2) +
                          ',"voc":'+ str(voc) +
                          ',"temperature":' + str(dht_T) +
                          ',"humidity":' + str(dht_RH) +
                          ',"voltage":' + str(voltage) +
                          '}}')
        #blink_led()

    except (NameError, ValueError, TypeError):
        pass


# topic = 'testtopic7891/1'
# broker_url = 'broker.hivemq.com' # HiveMQ can be used for testing, open broker
topic_pub = config['topic_pub']
topic_sub = config['topic_sub']
broker_url = config['broker']
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
