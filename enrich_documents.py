import os
import logging

from dotenv import load_dotenv
import pandas as pd
from openalex_analysis.analysis import get_multiple_works_from_doi

# load environment variables from .env file
load_dotenv()

pdf_new_path = os.getenv('PDF_NEW_PATH')
pdf_collection_path = os.getenv('PDF_COLLECTION_PATH')
tei_xml_collection_path = os.getenv('TEI_XML_COLLECTION_PATH')
documents_path = os.getenv('DOCUMENTS_PATH')

new_documents_path = os.path.join(documents_path, "new_documents.parquet")
new_enriched_documents_path = os.path.join(documents_path, 'new_enriched_documents.parquet')


def enrich_documents():
    """
    Enrich the documents with OpenAlex data
    """
    if not os.path.exists(new_documents_path):
        return
    if os.path.exists(new_enriched_documents_path):
        logging.error("The enriched documents file already exists and is going to be overwritten, you may not ingest "
                      "all of your documents.")

    df = pd.read_parquet(new_documents_path)
    dois = df['doi'].dropna().unique().tolist()

    # ignore dois with problematic characters (usually because of the errors in the pdf extraction)
    nb_dois = len(dois)
    dois = [doi for doi in dois if "," not in doi and "?" not in doi]
    nb_dois_enriched = len(dois)
    if len(dois) != nb_dois:
        logging.warning(f"Ignoring {nb_dois - nb_dois_enriched} DOI(s) because of problematic characters (pdf "
                        "extraction errors)")
    logging.info(f"Enriching {nb_dois_enriched} articles with OpenAlex data...")
    # get the metadata from OpenAlex
    works = get_multiple_works_from_doi(dois)

    # organize the works in a dictionary
    works = {work['doi']: work for work in works if work is not None}

    for i in range(len(df.index)):
        doi = df.at[i, 'doi']
        if doi in works.keys():
            df.at[i, 'title'] = works[doi]['display_name']

    df.to_parquet(new_enriched_documents_path)
    os.remove(new_documents_path)
    logging.info(f"Enriched {nb_dois_enriched} articles with OpenAlex data")


if __name__ == '__main__':
    enrich_documents()
