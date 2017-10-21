import xml.etree.ElementTree as etree
data = etree.parse('production_xmldata.2017-07-04.xml')
for a in list(data.getroot()):
	# if (a.tag == 'objectdata'):
	print(a)
