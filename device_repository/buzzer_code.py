import time
from machine import Pin,  PWM


def buzz(pwm_channel, pwm):
    tones = [2000, 3000, 2000, 3000, 0]

    for i in tones:
        if i == 0:
            pwm_channel.duty_cycle(0)
        else:
            pwm=PWM(0, frequency=i)
            pwm_channel.duty_cycle(0.45)
        time.sleep(0.10)

def buzzOff():
    buz = Pin("P7")
    buz = 0

#def battery():
#    adc = ADC(0)
#    adc_c = adc.channel(pin='P13')
#    value = adc_c.voltage()
#    print("ADC value:" + str(value))
#    return(value)
