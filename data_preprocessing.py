#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 21:44:47 2017

@author: changlongjiang
"""
import xml.etree.ElementTree as etree

data = etree.parse('Dataset_MachineLearning/production_xmldata.2017-07-04.xml')
root = data.getroot()
data_set1=[]
data_con=[]
for i in range(len(root)):
    data_o=[]
    
    if root[i].tag == 'objectdata':
        data_o.append(root[i][6][3][0].text)
        data_o.append(root[i][9][0].attrib['ole'])
        data_o.append(root[i][9][0].attrib['owi'])
        data_o.append(root[i][9][0].attrib['ohe'])
        data_o.append(root[i][9][1][0].text)
        data_o.append(root[i][9][2][0].text)
        data_o.append(root[i][9][4][0].text)
        data_o.append(root[i][10][0][0].text)
        data_con.append(root[i][7].text)
        if root[i][7].text.find('TooBig') != -1:
            data_o.append(1)
        else:
            data_o.append(0)
        if root[i][7].text.find('ValidRead') != -1:
            data_o.append(1)
        else:
            data_o.append(0)
        if root[i][7].text.find('ValidDim') != -1:
            data_o.append(1)
        else:
            data_o.append(0)
        if root[i][7].text.find('MultiRead') != -1:
            data_o.append(1)
        else:
            data_o.append(0)
        if root[i][7].text.find('NotLFT') != -1:
            data_o.append(0)
        else:
            data_o.append(1)
            
        data_set1.append(data_o[0]+ ',' + data_o[1]+ ',' +data_o[2]+','+data_o[3]+','+data_o[4]+','+data_o[5]+','+data_o[6]+','+data_o[7]+','+str(data_o[8])+','+str(data_o[9])+','+str(data_o[10])+','+str(data_o[11])+','+str(data_o[12]))
            
thefile = open('data_test.txt', 'w')
thefile.write("Gap,O_Height,O_Width,O_Length,Angle,O_Box_Volume,O_Transport_Velocity,Speed_CB,TooBig,ValidRead,ValidDim,MultiRead,LFT\n")
for item in data_set1:
    thefile.write("%s\n" %(item))           
thatfile = open('NotLFT.txt', 'w')
thatfile.write("Gap,O_Height,O_Width,O_Length,Angle,O_Box_Volume,O_Transport_Velocity,Speed_CB,TooBig,ValidRead,ValidDim,MultiRead,LFT\n")
for item in data_set1:
    if item[-1] == '0':
        thatfile.write("%s\n" %(item))
theconfile = open('Condition.txt', 'w')
theconfile.write("Condition\n")
for item in data_con:
    theconfile.write("%s\n" %(item))
