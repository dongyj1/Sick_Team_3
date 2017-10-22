#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 11:13:11 2017

@author: xogoss
"""


import xml.etree.ElementTree as ET
import csv
import fileinput

def find_element(dictionary, child):
    pass_tag = []
    pass_tag = ['udi','uds','usertag1','usertag2','dcs','norca','due','ss','sw','st','wud','rxoffset','rxstring','sortstate','hostmessage','polygon']
    if (len(child.getchildren()) != 0):
        for i in range(len(child.getchildren())):
            if(child.getchildren()[i].tag == 'value'):
                dictionary[child.tag] = child.getchildren()[i].text
            elif(child.tag == 'general' and child.getchildren()[i].tag == 'timestamp'):
                dictionary['timestamp1'] = child.getchildren()[i].text
            elif(child.tag == 'codevalid'):
                pass
            elif(child.tag != 'objectdata' and child.getchildren()[i].tag == 'condition'):
                pass
            else:
                find_element(dictionary, child.getchildren()[i])
        return
    else:
        print("tag:",child.tag, "text:",child.text,"attri:",child.attrib)
        if(child.tag in pass_tag):
            pass
        elif(child.tag == 'size'):
            for att in child.attrib.keys():
                if(att == 'unit'):
                    pass
                else:
                    dictionary[att] = child.attrib.get(att)
        else:
            dictionary[child.tag] = child.text
        return

#----------main-----------

filename = 'production_xmldata.2017-07-04.xml'

data = ''
with open(filename, 'r') as f:
    data = f.read().replace('\n', '')
if (not data.startswith('<data>')):
    data = '<data>'+data+'</data>'
with open('object.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

    #dictionary = {}
    root = ET.fromstring(data)
    # print(data)
    print(root)
    #child = root[0]
    for child in root[:60]:
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
            print(con)
            all_conditions = ['TooBig','NoRead','NotLFT','LFT','MultiRead','Irreg','TooSmall']
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
            for key in dictionary.keys():
                object_feature.append(key)
                object_feature.append(dictionary.get(key))
            filewriter.writerow(object_feature)
    
