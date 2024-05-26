import os

from dotenv import load_dotenv
import pandas as pd
from openalex_analysis.analysis import get_multiple_works_from_doi

from log_config import log

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
        log.error("The enriched documents file already exists and is going to be overwritten, you may not ingest all "
                  "of your documents.")

    df = pd.read_parquet(new_documents_path)
    dois = df['doi'].dropna().unique().tolist()

    # ignore dois with problematic characters (usually because of the errors in the pdf extraction)
    nb_dois = len(dois)
    dois = [doi for doi in dois if "," not in doi and "?" not in doi]
    nb_dois_enriched = len(dois)
    if len(dois) != nb_dois:
        log.warning(f"Ignoring {nb_dois - nb_dois_enriched} DOI(s) because of problematic characters (pdf extraction "
                    "errors)")
    log.info(f"Enriching {nb_dois_enriched} articles with OpenAlex data...")
    log.info("Downloading the metadata from OpenAlex...")
    works = get_multiple_works_from_doi(dois)

    log.info("Adding the metadata to the documents")
    # organize the works in a dictionary
    works = {work['doi']: work for work in works if work is not None}

    # authorships removed as authors already contains authors + universities. Needs some formating in data to merge
    # PDF metadata and OpenAlex metadata
    df['date'] = None
    # df['authorships'] = None
    df['is_open_access'] = None
    df['article_topics'] = None
    for i in range(len(df.index)):
        doi = df.at[i, 'doi']
        if doi in works.keys():
            df.at[i, 'title'] = works[doi]['display_name']
            df.at[i, 'year'] = str(works[doi]['publication_year'])
            df.at[i, 'date'] = works[doi]['publication_date']
            # df.at[i, 'authors'] = [a['author'].get('display_name') if a.get('author') is not None else None
            #                        for a in works[doi]['authorships']]
            # df.at[i, 'authorships'] = works[doi]['authorships']
            df.at[i, 'is_open_access'] = works[doi]['open_access']['is_oa']
            df.at[i, 'article_topics'] = [t['display_name'] for t in works[doi]['topics']]

    log.info(f"Saving the enriched documents to {new_enriched_documents_path}")
    df.to_parquet(new_enriched_documents_path)
    os.remove(new_documents_path)
    log.info(f"Enriched {nb_dois_enriched} articles with OpenAlex data")


if __name__ == '__main__':
    enrich_documents()
