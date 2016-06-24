#encoding:utf8
import libxml2
def parseXML(XMLPath) :
  doc = libxml2.parseFile(XMLPath)
  for text in doc.xpathEval('//RDoC/TEXT') :
        return text.content
  doc.freeDoc()

path = "C:\\Users\\310210774\\Desktop\\Tj_Train\\0006_gs.xml"
content = parseXML(path)
print type(content)