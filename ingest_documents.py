import json
import os

from elasticsearch import Elasticsearch
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# load environment variables from .env file
load_dotenv()

# get the environment variable with the elastic user password
elastic_password = os.getenv('ELASTIC_PASSWORD')
# get the path of the elastic certificates
elastic_ca_certs_path = os.getenv('CA_CERTS_PATH')

# load config
with open("config.json", "r") as f:
    config = json.load(f)

df = pd.read_parquet(config['documents_path'])

print(df.columns)

# Create the client instance
client = Elasticsearch(
    "https://localhost:9200",
    ca_certs=os.path.join(elastic_ca_certs_path, "ca/ca.crt"),
    basic_auth=("elastic", elastic_password)
)

# Successful response!
print(client.info())

# purge the index
try:
    client.indices.delete(index="src_articles")
except Exception as e:
    print(e)
# create an index for the documents (SRC's articles paragraphs)
client.indices.create(index="src_articles")

print("indexing documents....")
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    client.index(
        index="src_articles",
        id=str(index),
        document={
            'pdf': row['pdf'],
            'doi': row['doi'],
            'title': row['title'],
            'authors': row['authors'],
            'paragraph': row['paragraph'],
        }
    )
