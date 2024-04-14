import json
import os

from elasticsearch import Elasticsearch
import pandas as pd
from dotenv import load_dotenv


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
