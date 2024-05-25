import logging
import os

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from multiprocessing import Pool

import pandas as pd

# load environment variables from .env file
load_dotenv()

tei_xml_collection_path = os.getenv('TEI_XML_COLLECTION_PATH')
documents_path = os.getenv('DOCUMENTS_PATH')
parquet_compression = os.getenv('PARQUET_COMPRESSION')

new_documents_path = os.path.join(documents_path, 'new_documents.parquet')


def get_documents_from_xml_file(file_name: str) -> list[dict]:
    xml_file_path = os.path.join(tei_xml_collection_path, file_name)
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

    if soup.publicationStmt.date and soup.publicationStmt.date.get("when"):
        year = soup.publicationStmt.date.get("when")[:4]
    else:
        year = ""

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
            'year': year,
            'title': get_text(soup.title),
            'authors': authors,
            'paragraph': p
            } for p in paragraphs]


def generate_documents():
    xml_filenames = [f for f in os.listdir(tei_xml_collection_path) if ".grobid.tei.xml" == f[-15:]]

    if not xml_filenames:
        return

    nb_xml_files = len(xml_filenames)
    logging.info(f"Creating the documents for {nb_xml_files} pdfs...")
    # TODO: re-implement the loading bar to be compatible with container and file logging
    with Pool(processes=int((os.cpu_count() + 1) / 2)) as pool:
        # docs = tqdm(pool.imap(get_documents_from_xml_file, xml_filenames), total=len(xml_filenames))
        docs = pool.imap(get_documents_from_xml_file, xml_filenames)
        docs = list(docs)  # fetch the lazy results
    logging.info("Unpacking documents...")
    docs = [doc for doc_group in docs for doc in doc_group]
    logging.info(f"{len(docs)} documents (paragraphs) extracted from the xml files (pdfs)")

    logging.info("Saving documents...")
    df = pd.DataFrame(docs)
    df.to_parquet(new_documents_path, compression=parquet_compression)

    logging.info(f"Document extraction complete and saved in {new_documents_path}...")


if __name__ == '__main__':
    generate_documents()
