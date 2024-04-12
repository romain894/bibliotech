from bs4 import BeautifulSoup

test_file = "../data/tei_xml_collection/1-s2.0-S0025326X17306501-main.grobid.tei.xml"


def get_paragraphs_from_xml(xml_file_path):
    with open(xml_file_path, 'r') as tei:
        soup = BeautifulSoup(tei, 'lxml-xml')

    full_text = soup.body.find_all('p')
    paragraphs = [None] * len(full_text)

    for i, paragraph in enumerate(full_text):
        paragraphs[i] = paragraph.text

    return paragraphs


print(get_paragraphs_from_xml(test_file))
