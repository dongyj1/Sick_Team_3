import xml.etree.ElementTree as ET
import fileinput


filename = 'production_xmldata.2017-07-04.xml'

data = ''
with open(filename, 'r') as f:
    data = f.read().replace('\n', '')
if (not data.startswith('<data>')):
    data = '<data>'+data+'</data>'

dictionary = {}
root = ET.fromstring(data)
# print(data)
print(root)
for child in root:
    # dictionary[child.tag] = child.attrib
    if(child.tag=='objectdata'):

"""
import csv
with open('object.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    object_feature = []
    for key in objects.keys():
        print(key)
        object_feature.append(objects.get(key))
 """
