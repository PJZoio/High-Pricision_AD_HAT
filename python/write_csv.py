#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
import sys
import ADS1263
import RPi.GPIO as GPIO
import numpy as np

if len(sys.argv) > 1:
    filename = str(sys.argv[1])
else:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'dados/BIODBR_' + timestr + '.csv'


REF = 5.22          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

NUM_SAMPLES = 6000
NUM_CHANNELS = 6

try:
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0)

    time_start = time.time()
    ADC_Value = np.zeros((NUM_SAMPLES, NUM_CHANNELS + 1))

    for i in range(NUM_SAMPLES):
        for c in range(NUM_CHANNELS):
            raw = ADC.ADS1263_GetChannalValue(c)
            if(raw>>31 ==1):
                adcval = REF*2 - raw * REF / 0x80000000
                # print("ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))
            else:
                # adcval = REF*2 - raw * REF / 0x7fffffff
                # print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
                adcval = raw * REF / 0x7fffffff   # 32bit
            ADC_Value[i, c + 1] = adcval

        ADC_Value[i, 0] = time.time() - time_start

    time_end = time.time()
        
    ADC.ADS1263_Exit()

    print('frequency = ', NUM_SAMPLES / (time_end - time_start))
    print ('Acquisition Done. Saving Data to ', filename)
    np.savetxt(filename, ADC_Value, fmt='%.5f', delimiter=',')

except IOError as e:
    print(e)
   
except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()
   
