import json
from grobid_client.grobid_client import GrobidClient
import os, re, shutil
from bs4 import BeautifulSoup

# load config
with open("config.json", "r") as f:
    config = json.load(f)

client = GrobidClient(config_path="./grobid_config.json")

# process all the PDF in the directory data/pdf_new
client.process("processFulltextDocument", config['pdf_new_path'], n=10)

# move the processed files
for filename in os.listdir(config['pdf_new_path']):
    # if re.match(r'.*\.tei\.xml$', filename):
    if ".grobid.tei.xml" == filename[-15:]:
        shutil.move(os.path.join(config['pdf_new_path'], filename), config['pdf_collection_path'])
        shutil.move(os.path.join(config['pdf_new_path'], filename[:-15]+".pdf"), config['tei_xml_collection_path'])
