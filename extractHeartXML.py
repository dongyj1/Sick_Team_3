# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 19:22:03 2017

@author: suyux
"""

import xml.etree.ElementTree as ET
import csv

###################################################### 
#    get the data we want to analyze from xml file   #
#    all the data under pass_tag would be dropped    #
###################################################### 

def find_heart_element(dictionary, child):
    #pass_tag = []
    pass_tag = ["devicename","deviceid","general","sortstate"]
    if (len(child.getchildren()) != 0):
        for i in range(len(child.getchildren())):
            if(child.tag == "sorterstate"):
                dictionary['state'] = child.attrib.get('state')
                if(child.getchildren()[0].tag == 'speed'):
                    dictionary[child.getchildren()[0].tag] = float(child.getchildren()[0].getchildren()[0].text)
                    dictionary[str(child.getchildren()[0].tag + "_Unit")] = child.getchildren()[0].attrib.get('unit')
                else:
                    pass
            elif(child.getchildren()[i].tag == 'timestamp'):
                dictionary['timestamp'] = child.getchildren()[i].text
            elif(child.tag == "systemstate"):
                for j in range(len(child.getchildren())):
                    #print(len(child.getchildren()))
                    device_n = child.getchildren()[j].attrib.get("extinfo")
                    #dictionary["warning" + str(j) + "extinfo"] = child.getchildren()[j].attrib.get("extinfo")
                    dictionary[device_n + "numberoccur"] = child.getchildren()[j].attrib.get('numberoccurance')
                    dictionary[device_n + "errid"] = child.getchildren()[j].attrib.get('errorid')
                    #print(child.getchildren()[j])
                    dictionary[device_n + "firsttime"] = child.getchildren()[j].getchildren()[0].text
                    dictionary[device_n + "lasttime"] = child.getchildren()[j].getchildren()[1].text



            else:
                find_heart_element(dictionary, child.getchildren()[i])
        return
    else:
        #print("tag:",child.tag, "text:",child.text,"attri:",child.attrib)
        if(child.tag in pass_tag):
            pass
        else:
            try:
                dictionary[child.tag] = float(child.text)
            except:
                dictionary[child.tag] = child.text
        return
def extract_condition(child):
    pass
#----------main-----------
filename = ['Dataset_MachineLearning/production_xmldata.2017-07-04.xml',
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
            'Dataset_MachineLearning/production_xmldata.2017-08-01.xml',
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
mon = 7
day = 4

for file in filename:
    flag = True
    if (day > 31):
        mon = 8
        day = 1
    csv_name = "heartbeat" + str(mon) + "." + str(day) + ".csv"
    print("the date we are processing is "+ str(mon) + "." + str(day))
    #print(file)
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
            #hashset = [all header]
            header = set()
            object_feature = []
            object_feature_name = []
            for child in root:
                # dictionary[child.tag] = child.attrib
                if(child.tag=='heartbeatdata'):
                    dictionary = {}
                    #print(len(child.getchildren()))
                    for i in child.getchildren():
                        find_heart_element(dictionary, child)

                    #------write in csv--------------

                    #owe data may be missed in some data
                    #if no owe data in the dict, here just add "-1" value to owe
                    #to make sure all the features have same length
                    #----
                    if (count == 0):
                        for key in dictionary.keys():
                            header.add(key)
                            object_feature_name.append(key)
                        filewriter.writerow(object_feature_name)
                    #------
                    object_value = []
                    for head in object_feature_name:
                        if(head not in dictionary.keys()):
                            object_value.append(-1)
                        else:
                            object_value.append(dictionary.get(head))
                    filewriter.writerow(object_value)
                    #for all header set, write getvalue(header[i])
                    count +=1
                    #print("Now is processing #",count," line of data")
    day += 1
