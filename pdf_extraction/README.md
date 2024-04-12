# Code for the PDF data extraction

From the PDF, extract metadata and full text.

Process the full text TEI XML from GROBID to extract metadata the paragraph and store them in `data/documents.parquet` (each row is a paragraph/document and contains the text + the metadata).
