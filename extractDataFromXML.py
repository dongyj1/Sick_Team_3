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


