import json
import os

from bs4 import BeautifulSoup
import pandas as pd

# load config
with open("config.json", "r") as f:
    config = json.load(f)


def get_documents_from_xml_file(xml_file_path: str) -> list[dict]:
    def get_text(element) -> str:
        if element:
            return element.text
        else:
            return ""

    def get_doi(element) -> str:
        if element:
            return "https://doi.org/"+element.text
        else:
            return ""

    with open(xml_file_path, 'r') as tei:
        soup = BeautifulSoup(tei, 'lxml-xml')

    full_text = soup.body.find_all('p')
    paragraphs = [p.text for p in full_text]

    authors = []
    for author in soup.analytic.find_all('author'):
        author_name = ""
        if author.persName:
            if author.persName.find("forename", type="first"):
                author_name += author.persName.find("forename", type="first").text + " "
            if author.persName.find("forename", type="middle"):
                author_name += author.persName.find("forename", type="middle").text + " "
            if author.persName.surname:
                author_name += author.persName.surname.text
            if author_name[-1] == " ":
                author_name = author_name[:-1]
        authors.append({
            'name': author_name,
            'institutions': [get_text(i.find("orgName", type="institution")) for i in author.find_all('affiliation')],
        })

    return [{
            'pdf': os.path.basename(xml_file_path)[:-15]+".pdf",
            'doi': get_doi(soup.find("idno", type="DOI")),
            'title': get_text(soup.title),
            'authors': authors,
            'paragraph': p
            } for p in paragraphs]


docs = []
for filename in os.listdir(config['tei_xml_collection_path']):
    if ".grobid.tei.xml" == filename[-15:]:
        docs.append(get_documents_from_xml_file(os.path.join(config['tei_xml_collection_path'], filename)))
docs = [doc for doc_group in docs for doc in doc_group]

df = pd.DataFrame(docs)
df.to_parquet(config['documents_path'], compression=config['parquet_compression'])
