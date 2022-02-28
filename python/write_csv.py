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
    filename = 'dados.csv'


REF = 5.22          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

NUM_SAMPLES = 1000
NUM_CHANNELS = 6


try:
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0)

    # rate test
    time_start = time.time()
    ADC_Value = np.zeros((NUM_SAMPLES, NUM_CHANNELS + 1))

#        isSingleChannel = False
#        if isSingleChannel:
    for i in range(NUM_SAMPLES):
        for c in range(NUM_CHANNELS):
        #ADC_Value.append(ADC.ADS1263_GetAll())
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
    # ADC.ADS1263_DAC_Test(1, 1)      # Open IN6
    # ADC.ADS1263_DAC_Test(0, 1)      # Open IN7
    
        
    ADC.ADS1263_Exit()

# colocar aqui funcao para guardar ADC_Value em fich  .csv    
    np.savetxt(filename, ADC_Value, fmt='%.5f', delimiter=',')

except IOError as e:
    print(e)
   
except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()
   
