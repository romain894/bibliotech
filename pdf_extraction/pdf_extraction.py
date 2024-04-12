from grobid_client.grobid_client import GrobidClient
from bs4 import BeautifulSoup

client = GrobidClient(config_path="./grobid_config.json")
client.process("processFulltextDocument", "../data/pdf_new", n=10)