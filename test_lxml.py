#=-= coding=utf-8 =-=
from lxml import etree

open_path='..\\data\\0007_gs.xml'
open_path='./dict1.txt'

xml = etree.parse(open_path)
bupd = xml.xpath("RDoC/TEXT")
print bupd
