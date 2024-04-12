from bs4 import BeautifulSoup

test_file = "../data/tei_xml_collection/1-s2.0-S0025326X17306501-main.grobid.tei.xml"

with open(test_file, 'r') as tei:
    soup = BeautifulSoup(tei, 'lxml-xml')

print(soup.title.getText())