import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from log_config import log

# load environment variables from .env file
load_dotenv()

documents_path = os.getenv('DOCUMENTS_PATH')
pdf_collection_path = os.getenv('PDF_COLLECTION_PATH')
tei_xml_collection_path = os.getenv('TEI_XML_COLLECTION_PATH')
# get the environment variable with the elastic user password
elasticsearch_url = os.getenv('ELASTICSEARCH_URL')
elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
elastic_password = os.getenv('ELASTIC_PASSWORD')
# get the path of the elastic certificates
elastic_ca_certs_path = os.getenv('CA_CERTS_PATH')

ingested_documents_path = os.path.join(documents_path, 'ingested_documents.parquet')

# Create the client instance
client = Elasticsearch(
    elasticsearch_url,
    ca_certs=os.path.join(elastic_ca_certs_path, "ca/ca.crt"),
    basic_auth=("elastic", elastic_password)
)


def delete_documents():
    # purge the index
    try:
        client.indices.delete(index=elasticsearch_index)
    except Exception as e:
        log.warning("Failed to delete index, it may because no document were previously ingested")
        log.warning(e)
    # delete parquet file
    try:
        os.remove(ingested_documents_path)
    except Exception as e:
        log.warning("Failed to delete ingested documents parquet file, it may because no document were previously "
                    "ingested")
        log.warning(e)
    # delete XML files
    try:
        for f in os.listdir(tei_xml_collection_path):
            if ".grobid.tei.xml" == f[-15:]:
                os.remove(os.path.join(tei_xml_collection_path, f))
    except Exception as e:
        log.warning("Failed to delete ingested XML TEI files, it may because no document were previously ingested")
        log.warning(e)
    # delete PDF files
    try:
        for f in os.listdir(pdf_collection_path):
            if ".pdf" == f[-4:]:
                os.remove(os.path.join(pdf_collection_path, f))
    except Exception as e:
        log.warning("Failed to delete ingested PDF files, it may because no document were previously ingested")
        log.warning(e)


if __name__ == '__main__':
    delete_documents()
