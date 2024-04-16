import os
import shutil

from dotenv import load_dotenv
from grobid_client.grobid_client import GrobidClient

# load environment variables from .env file
load_dotenv()

pdf_new_path = os.getenv('PDF_NEW_PATH')
pdf_collection_path = os.getenv('PDF_COLLECTION_PATH')
tei_xml_collection_path = os.getenv('TEI_XML_COLLECTION_PATH')
documents_path = os.getenv('DOCUMENTS_PATH')

client = GrobidClient(config_path="grobid_config.json")

# process all the PDF in the directory data/pdf_new
client.process("processFulltextDocument", pdf_new_path, n=20)

# move the processed files
for filename in os.listdir(pdf_new_path):
    if ".grobid.tei.xml" == filename[-15:]:
        shutil.move(os.path.join(pdf_new_path, filename), tei_xml_collection_path)
        shutil.move(os.path.join(pdf_new_path, filename[:-15]+".pdf"), pdf_collection_path)

print("Done.")