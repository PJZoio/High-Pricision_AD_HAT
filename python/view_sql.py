#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 09 12:11:30 2021
@author: Bernardo Carvalho
"""

import sys
import numpy as np
import MySQLdb

mydb = MySQLdb.connect(host='epics.ipfn.tecnico.ulisboa.pt',
        user='pzoio',
        passwd='123456',
        db='miniNirDB')
cursor = mydb.cursor()
