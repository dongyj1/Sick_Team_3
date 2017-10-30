#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 11:13:11 2017
@author: xogoss
"""


import xml.etree.ElementTree as ET
import csv
import fileinput

###################################################### 
#    get the data we want to analyze from xml file   #
#    all the data under pass_tag would be dropped    #
###################################################### 

def find_element(dictionary, child):
    #pass_tag = []
    pass_tag = ['barcode','udi','uds','usertag1','usertag2','dcs','norca','due','ss','sw','st','wud','rxoffset','rxstring','sortstate','hostmessage','polygon']
    if (len(child.getchildren()) != 0):
        for i in range(len(child.getchildren())):
            if(child.getchildren()[i].tag == 'value'):
                dictionary[child.tag] = float(child.getchildren()[i].text)
                #dictionary[child.tag].append(child.attrib.get('unit'))
                #print("tag is : ", child.tag)
                #print("value in child is : ", float(child.getchildren()[i].text))
                #print("the attribute is unit is : ",child.attrib.get('unit'))
                dictionary[str(child.tag + "_Unit")] = child.attrib.get('unit')
            elif(child.tag == 'general' and child.getchildren()[i].tag == 'timestamp'):
                dictionary['timestamp1'] = child.getchildren()[i].text
            elif(child.tag == 'barcode'):
                pass
            elif(child.tag != 'objectdata' and child.getchildren()[i].tag == 'condition'):
                pass
            else:
                find_element(dictionary, child.getchildren()[i])
        return
    else:
        #print("tag:",child.tag, "text:",child.text,"attri:",child.attrib)
        if(child.tag in pass_tag):
            pass
        elif(child.tag == 'size'):
            for att in child.attrib.keys():
                #print("att is : ",att)
                if(att == 'unit'):
                    pass
                else:
                    dictionary[att] = float(child.attrib.get(att))
                    #print(dictionary[att])
                    #print(child.attrib.get('unit'))
                    #dict_tmp = {"unit": child.attrib.get('unit')}
                    dictionary[str(child.tag + "_Unit")] = child.attrib.get('unit')
                    #dictionary.update(dict_tmp)
        else:
            try:
                dictionary[child.tag] = float(child.text)
            except:
                dictionary[child.tag] = child.text
        return



#----------main-----------
"""filename = ['Dataset_MachineLearning/production_xmldata.2017-07-04.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-05.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-06.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-07.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-08.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-09.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-10.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-11.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-12.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-13.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-14.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-15.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-16.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-17.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-18.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-19.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-20.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-21.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-22.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-23.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-24.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-25.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-26.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-27.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-28.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-29.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-30.xml',
            'Dataset_MachineLearning/production_xmldata.2017-07-31.xml',
            """
filename = ['Dataset_MachineLearning/production_xmldata.2017-08-01.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-02.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-03.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-04.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-05.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-06.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-07.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-08.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-09.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-10.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-11.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-12.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-13.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-14.xml',
            'Dataset_MachineLearning/production_xmldata.2017-08-15.xml',
            ]
mon = 8
day = 1

for file in filename:
    flag = True
    if (day > 31):
        mon = 8
        day = 1
    csv_name = "object" + str(mon) + "." + str(day) + ".csv"
    print("the date we are processing is "+ str(mon) + "." + str(day))
    print(file)
    with open(csv_name, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,dialect='unix')
    
        data = ''
        with open(file, 'r') as f:
            data = f.read().replace('\n', '')
        if (not data.startswith('<data>')):
            data = '<data>'+data+'</data>'
    
        #dictionary = {}
        try:
            root = ET.fromstring(data)
        except:
            flag = False
        count = 0
        if(flag == True):
            for child in root:
                # dictionary[child.tag] = child.attrib
                if(child.tag=='objectdata'):
                    dictionary = {}
                    #print(len(child.getchildren()))
                    for i in child.getchildren():
                        find_element(dictionary, child)
                    #---trans conditon---
                    if('condition' not in dictionary.keys()):
                        raise Exception
                    con = dictionary.get('condition')
                    #print(con)
                    all_conditions = ['TooBig','NoRead','NotLFT','LFT','MultiRead','Irreg','TooSmall','Gap','ValidDim','ValidRead','Clipping','PeError']
                    for j in all_conditions:
                        if(j == 'NotLFT' and j in con):
                            dictionary['LFT'] = 0
                        elif(j == 'NotLFT' and j not in con):
                            pass
                        elif(j == 'LFT' and j in dictionary.keys()):
                            pass
                        else:
                            if(j in con):
                                dictionary[j] = 1
                            else:
                                dictionary[j] = 0
                    dictionary.pop('condition')
                #------write in csv--------------
                    object_feature = []
                    object_feature_name = []
                    for key in dictionary.keys():
                        object_feature_name.append(key)
                        object_feature.append(dictionary.get(key))
                    #owe data may be missed in some data
                    #if no owe data in the dict, here just add "-1" value to owe
                    #to make sure all the features have same length
                    if (count == 0):
                        filewriter.writerow(object_feature_name)
                    if "owe" not in object_feature_name:
                        #print(object_feature_name)
                        object_feature = object_feature[:28] + ['-1','LB'] + object_feature[28:]
                        #print(object_feature)
                    filewriter.writerow(object_feature)
                    count +=1
                    #print("Now is processing #",count," line of data")
    day += 1
