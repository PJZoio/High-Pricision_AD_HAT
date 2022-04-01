#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 09 12:11:30 2021
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
#sql = 'SELECT filename from tabelaEnsaios'
record = (Ensaio)
cursor.execute(sql1)
result = cursor.fetchone()
filename = "dados/" + result[0]

#sql = 'INSERT INTO tabelaEnsaios Ensaio, Descricao, dateTime, VALUES (NULL, )'
#record = (desc,filename[6:],1,a[1],s[1],a[2],s[2],a[3],s[3],a[4],s[4],a[5],s[5],a[6],s[6])
# execute SQL query using execute() method.
#cursor.execute(sql)
#try:
#   # Executing the SQL command
#    cursor.execute(sql, record)
#    filename = cursor.fetchone()

   # Commit your changes in the database
   #mydb.commit()

#except:
   # Rolling back in case of error
#   print('Data not saved.')
   #mydb.rollback()
print(filename)
d = np.genfromtxt(filename, delimiter=',')
a = np.average(d, axis=0)
# Compute the standard deviation along the specified axis
s = np.std(d, axis=0)
NSAMP=600
line=0
mydb.close()
mydb = MySQLdb.connect(host='epics.ipfn.tecnico.ulisboa.pt',
        user='pzoio',
        passwd='123456',
        db='miniNirDB')
curs = mydb.cursor()
sql = """INSERT INTO dadosPLS (EnsaioId, line, initTime, LED1_avg, LED1_std, LED2_avg, LED2_std, LED3_avg, LED3_std, LED4_avg, LED4_std, LED5_avg, LED5_std, LED6_avg, LED6_std) VALUES (%s, %s, %f, 
%s, %s, %s, %s, %s, %s,
%s, %s, %s, %s, %s, %s)"""
sql0 = """INSERT INTO dadosPLS (EnsaioId, line, initTime, LED1_avg, LED1_std, LED2_avg, LED2_std, LED3_avg, LED3_std, LED4_avg, LED4_std, LED5_avg, LED5_std, LED6_avg, LED6_std) VALUES (%s, %s, %f, 
%s, %s, %s, %s, %s, %s,
%s, %s, %s, %s, %s, %s)"""
for i in range(0, d.shape[0], NSAMP):
    print(i)
    a = np.average(d[i:i+NSAMP,:], axis=0)
    s = np.std(d[i:i+NSAMP,:], axis=0)
    #print(a)
#sql = """INSERT INTO tabelaEnsaios ( Descricao, dateTime, filename, ensaioRef, LED1_avg, LED1_std, LED2_avg, LED2_std, LED3_avg, LED3_std, LED4_avg, LED4_std, LED5_avg, LED5_std, LED6_avg, LED6_std) VALUES (%s, current_timestamp(), %s, %s, 
#%s, %s, %s, %s, %s, %s,
#%s, %s, %s, %s, %s, %s)"""
    record = (Ensaio, line, d[i,0],a[1],s[1],a[2],s[2],a[3],s[3],a[4],s[4],a[5],s[5],a[6],s[6])
    #print(sql%record)
# execute SQL query using execute() method.
    sql1=sql%record
    print(sql1)
    curs.execute(sql1)
    try:
#    Executing the SQL command
        curs.execute(sql, record)
   # Commit your changes in the database
        mydb.commit()

    except:
   # Rolling back in case of error
        print('Data not saved.')
        mydb.rollback()
    line +=1


# Fetch a single row using fetchone() method.
#data = cursor.fetchone()
#if data:
#   print('Version available: ', data)
#else:
#   print('Versioyyn not retrieved.')

# disconnect from server
mydb.close()
