#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 1 12:11:30 2021
@author: Bernardo Carvalho
"""

import sys
import numpy as np
import MySQLdb

if len(sys.argv) > 1:
    Ensaio= sys.argv[1]
#else:

print("Ensaio %s" %Ensaio)

mydb = MySQLdb.connect(host='epics.ipfn.tecnico.ulisboa.pt',
        user='pzoio',
        passwd='123456',
        db='miniNirDB')

# prepare a cursor object
cursor = mydb.cursor()

sql = 'SELECT filename from tabelaEnsaios where Ensaio = %s'
sql1= sql %Ensaio
print(sql1)
record = (Ensaio)
cursor.execute(sql1)
result = cursor.fetchone()
filename = "dados/" + result[0]

print(filename)
d = np.genfromtxt(filename, delimiter=',')
NSAMP=600
line=0
sql = """INSERT INTO dadosPLS (EnsaioId, line, initTime, LED1_avg, LED1_std, LED2_avg, LED2_std, LED3_avg, LED3_std, LED4_avg, LED4_std, LED5_avg, LED5_std, LED6_avg, LED6_std) VALUES (%s, %s, %f, 
%s, %s, %s, %s, %s, %s,
%s, %s, %s, %s, %s, %s)"""
line = 0
for i in range(0, d.shape[0], NSAMP):
#for i in range(0, 2):
    a = np.average(d[i:i+NSAMP,:], axis=0)
    s = np.std(d[i:i+NSAMP,:], axis=0)
    record = (Ensaio, line, d[i,0],a[1],s[1],a[2],s[2],a[3],s[3],a[4],s[4],a[5],s[5],a[6],s[6])
    sql2=sql%record
    print(sql2)
    try:
   # Executing the SQL command
        cursor.execute(sql2)
        #cursor.execute(sql,record)

   # Commit your changes in the database
        mydb.commit()
    except:
   # Rolling back in case of error
        print('Data not saved.')
        mydb.rollback()
    line = line + 1 

# disconnect from server

mydb.close()
