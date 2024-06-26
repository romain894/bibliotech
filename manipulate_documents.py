import os

from dotenv import load_dotenv
import pandas as pd

from log_config import log

# load environment variables from .env file
load_dotenv()

pdf_new_path = os.getenv('PDF_NEW_PATH')
pdf_collection_path = os.getenv('PDF_COLLECTION_PATH')
tei_xml_collection_path = os.getenv('TEI_XML_COLLECTION_PATH')
documents_path = os.getenv('DOCUMENTS_PATH')


def get_articles_list() -> list[str]:
    """
    Get the list of the articles in the PDF collection and parquet file.
    Raises a warning is the PDF collection and parquet file are incoherent.
    :return: The list of the articles (file names)
    :rtype: list[str]
    """
    pdfs = os.listdir(pdf_collection_path)
    pdfs.sort()

    # TODO: check if warning is working and add more details in logs
    # df = pd.read_parquet(documents_path, columns=['pdf'])
    # documents = df['pdf'].unique().tolist()
    # documents.sort()
    #
    # if pdfs != documents:
    #     log.warning("Incoherence between the PDFs in the collection directory and the PDFs listed in the documents "
    #                 "parquet file")

    return pdfs
