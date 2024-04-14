# Bibliotech platform by Romain

Bibliographic analysis framework using full text articles with topic modeling browsable thought a search engine.

This framework uses opensource projects for the following steps:

  - [GROBID](https://github.com/kermitt2/grobid): metadata (title, authors...) and full text extraction from the PDF (used with `grobid_client_python`)
  - [BERTopic](https://github.com/MaartenGr/BERTopic): topic modeling
  - [Elasticsearch](https://www.elastic.co/elasticsearch): search engine

## PDF to documents

From the PDF, extract metadata and full text, and create the documents

Process the full text TEI XML from GROBID to extract metadata the paragraph and store them in `data/documents.parquet` (each row is a paragraph/document and contains the text + the metadata).

## Elastic

Before running docker compose, you need to run the following command on the host:
```bash
sudo sysctl -w vm.max_map_count=262144
```
Then you can run the elastic containers:
```bash
sudo docker compose -f elastic-docker-compose.yml up
```


Romain THOMAS 2024