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
    ensaio = str(sys.argv[1])
else:
    ensaio = 20

#if len(sys.argv) > 2:
#    desc = str(sys.argv[2])
#else:
#    desc = 'Descricao'

mydb = MySQLdb.connect(host='epics.ipfn.tecnico.ulisboa.pt',
        user='pzoio',
        passwd='123456',
        db='miniNirDB')

# prepare a cursor object
cursor = mydb.cursor(MySQLdb.cursors.DictCursor)

stmt = "SELECT * FROM tabelaEnsaios WHERE Ensaio = %s"
record = (ensaio,)
cursor.execute(stmt, record)
data = cursor.fetchone()

print(data)

try:
   # Executing the SQL command
#   cursor.execute(sql, record)

   # Commit your changes in the database
   mydb.commit()

except:
   # Rolling back in case of error
   print('Data not get.')
   #mydb.rollback()

# Fetch a single row using fetchone() method.
#data = cursor.fetchone()
#if data:
#   print('Version available: ', data)
#else:
#   print('Versioyyn not retrieved.')

# disconnect from server
mydb.close()
