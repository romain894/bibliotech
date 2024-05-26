import os
import logging

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import pandas as pd
from multiprocessing import Pool

# load environment variables from .env file
load_dotenv()

documents_path = os.getenv('DOCUMENTS_PATH')
parquet_compression = os.getenv('PARQUET_COMPRESSION')
# get the environment variable with the elastic user password
elasticsearch_url = os.getenv('ELASTICSEARCH_URL')
elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
elastic_password = os.getenv('ELASTIC_PASSWORD')
# get the path of the elastic certificates
elastic_ca_certs_path = os.getenv('CA_CERTS_PATH')

new_enriched_documents_path = os.path.join(documents_path, 'new_enriched_documents.parquet')
ingested_documents_path = os.path.join(documents_path, 'ingested_documents.parquet')

# Create the client instance
client = Elasticsearch(
    "elasticsearch_url",
    ca_certs=os.path.join(elastic_ca_certs_path, "ca/ca.crt"),
    basic_auth=("elastic", elastic_password)
)


def ingest_documents():
    if not os.path.exists(new_enriched_documents_path):
        return

    df_new = pd.read_parquet(new_enriched_documents_path)
    logging.info(f"Ingesting {len(df_new.index)} new documents")

    # # Successful response!
    # print(client.info())

    # create an index for the documents (articles paragraphs) if it doesn't already exist
    if not client.indices.exists(index=elasticsearch_index):
        client.indices.create(index=elasticsearch_index)

    def ingest_document(iterator):
        index = iterator[0]
        row = iterator[1]
        client.index(
            index=elasticsearch_index,
            id=str(index),
            document={
                'pdf': row['pdf'],
                'doi': row['doi'],
                'year': row['year'],
                'title': row['title'],
                'authors': row['authors'],
                'paragraph': row['paragraph'],
            }
        )

    print("indexing documents....")
    # TODO: re-implement the loading bar to be compatible with container and file logging
    with Pool(processes=int((os.cpu_count() + 1) / 2)) as pool:
        # results = tqdm(pool.imap(ingest_document, df_new.iterrows()), total=df_new.shape[0])
        results = pool.imap(ingest_document, df_new.iterrows())
        tuple(results)  # fetch the lazy results

    logging.info("Adding the new documents in the parquet file with the already ingested documents")
    df_ingested = pd.read_parquet(ingested_documents_path)
    df_ingested = pd.concat([df_ingested, df_new])
    df_ingested.to_parquet(ingested_documents_path)
    os.remove(new_enriched_documents_path)


def delete_documents():
    # purge the index
    try:
        client.indices.delete(index=elasticsearch_index)
    except Exception as e:
        logging.warning("Failed to delete index, it may because no document were previously ingested")
        logging.warning(e)


if __name__ == '__main__':
    ingest_documents()
