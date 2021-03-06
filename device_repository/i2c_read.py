# Example for CCS811 sensor
from machine import I2C
import CCS811
import time

i2c = I2C(0)                         # create on bus 0
i2c = I2C(0, I2C.MASTER)             # create and init as a master
i2c = I2C(0, pins=('P9','P10'))      # PIN assignments (P9=SDA, P10=SCL) May need to be modified
i2c.init(I2C.MASTER, baudrate=10000) # init as a master

# https://github.com/Notthemarsian/CCS811

ccs = CCS811.CCS811(i2c=i2c,addr=91)
time.sleep(3) # Just to get it some slack starting up ...
time.sleep(1)


def value():
    ccs.data_ready() # Make a reading
    co2 = ccs.eCO2
    voc = ccs.tVOC
    #print(co2,voc)
    if co2 > 399:    # just to filter out faulty readings
        return(co2,voc)
