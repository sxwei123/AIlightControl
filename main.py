#!/usr/bin/python
# -*- coding: UTF-8 -*-
from random import randint
import ssdp
import yeelight
from time import sleep
yeelight_master = ssdp.discover(":yeelink:yeebox")

yeeIP = yeelight_master[0].location
print 'IP of gateway: ',yeeIP
yee = yeelight.yeelight(yeeIP)
yee.start()

try:
    for i in range(0,1000):
        #yee.changeColor('0001',randint(0,255),randint(0,255),randint(0,255))
        yee.control('0001',randint(0,255),randint(0,255),randint(0,255),randint(0,255))
        sleep(1)
        print '>>> ',yee.readBuf()
finally:
    yee.close()
