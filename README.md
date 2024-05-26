# Bibliotech platform by Romain

Bibliographic analysis framework using full text articles with topic modeling browsable thought a search engine.

The following libraries or docker images are used in this project:

  - [GROBID](https://github.com/kermitt2/grobid): metadata (title, authors...) and full text extraction from the PDF (used with `grobid_client_python`)
  - [OpenAlex analysis](https://github.com/romain894/openalex-analysis): data enrichment (adding institutions details, ORCID...)
  - [BERTopic](https://github.com/MaartenGr/BERTopic): topic modeling (separate deployment)
  - [Elasticsearch](https://www.elastic.co/elasticsearch): internal search engine
  - [Kibana](https://www.elastic.co/kibana): web user interface for data exploration

This project code is under AGPLv3 license.

## PDF to documents

From the PDF, extract metadata and full text, and create the documents

Process the full text TEI XML from GROBID to extract metadata the paragraph and store them in `data/documents.parquet` (each row is a paragraph/document and contains the text + the metadata).

## How to run

Clone the git repository, configure the `.env.template` and rename it to `.env`

Before running docker compose, you need to run the following command on the host (at each reboot):
```bash
sudo sysctl -w vm.max_map_count=262144
```

You need to build the container the first time
```bash
sudo docker compose build
```

Then you can run the containers:
```bash
sudo docker compose up
```


## TODO

  - Automatize file system ownership and mode, for now use `chmod 777 elasticsearch_data/es/ kibana_data/` 


Romain THOMAS 2024