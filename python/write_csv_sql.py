#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
import sys
import ADS1263
#import RPi.GPIO as GPIO
import numpy as np
import MySQLdb

if len(sys.argv) > 1:
    desc = str(sys.argv[1])
else:
    desc = 'Descricao'

if len(sys.argv) > 2:
    filename = str(sys.argv[2])
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

    # rate test
    time_start = time.time()
    ADC_Value = np.zeros((NUM_SAMPLES, NUM_CHANNELS + 1))

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

    print('frequency = ', NUM_SAMPLES / (time_end - time_start))
    print ('Acquisition Done. Saving Data to ', filename)

# colocar aqui funcao para guardar ADC_Value em SQL
    a = np.average(ADC_Value, axis=0)
# Compute the standard deviation along the specified axis
    s = np.std(ADC_Value, axis=0)

    mydb = MySQLdb.connect(host='epics.ipfn.tecnico.ulisboa.pt',
        user='pzoio',
        passwd='123456',
        db='miniNirDB')

# prepare a cursor object
    cursor = mydb.cursor()

#sql = 'INSERT INTO tabelaEnsaios Ensaio, Descricao, dateTime, VALUES (NULL, )'
    sql = """INSERT INTO tabelaEnsaios ( Descricao, dateTime, filename, ensaioRef, LED1_avg, LED1_std, LED2_avg, LED2_std, LED3_avg, LED3_std, LED4_avg, LED4_std, LED5_avg, LED5_std, LED6_avg, LED6_std) VALUES (%s, current_timestamp(), %s, %s, 
%s, %s, %s, %s, %s, %s,
%s, %s, %s, %s, %s, %s)"""
    record = (desc,filename[6:],1,a[1],s[1],a[2],s[2],a[3],s[3],a[4],s[4],a[5],s[5],a[6],s[6])

# execute SQL query using execute() method.
    try:
    # Executing the SQL command
        cursor.execute(sql, record)
   # Commit your changes in the database
        mydb.commit()
        print ('Data Stored in DB')
    except:
   # Rolling back in case of error
        print('Data not stored....')
        mydb.rollback()

# disconnect from server
    mydb.close()

#colocar aqui funcao para guardar ADC_Value em fich  .csv    
    np.savetxt(filename, ADC_Value, fmt='%.5f', delimiter=',')

except IOError as e:
    print(e)
   
except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()
   
