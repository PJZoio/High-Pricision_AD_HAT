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
    filename = str(sys.argv[1])
else:
    filename = 'dados/BIODBR_20220315-163306.csv'

if len(sys.argv) > 2:
    desc = str(sys.argv[2])
else:
    desc = 'Descricao'

d = np.genfromtxt(filename, delimiter=',')
a = np.average(d, axis=0)
# Compute the standard deviation along the specified axis
s = np.std(d, axis=0)

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
#cursor.execute(sql)
try:
   # Executing the SQL command
   cursor.execute(sql, record)

   # Commit your changes in the database
   mydb.commit()

except:
   # Rolling back in case of error
   print('Data not saved.')
   mydb.rollback()

# Fetch a single row using fetchone() method.
#data = cursor.fetchone()
#if data:
#   print('Version available: ', data)
#else:
#   print('Versioyyn not retrieved.')

# disconnect from server
mydb.close()
