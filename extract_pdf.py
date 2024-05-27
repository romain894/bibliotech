import os
import shutil

from dotenv import load_dotenv
from grobid_client.grobid_client import GrobidClient

from manipulate_documents import get_articles_list
from log_config import log

# load environment variables from .env file
load_dotenv()

pdf_new_path = os.getenv('PDF_NEW_PATH')
pdf_ingestion_failed_path = os.getenv('PDF_INGESTION_FAILED')
pdf_collection_path = os.getenv('PDF_COLLECTION_PATH')
tei_xml_to_ingest_path = os.getenv('TEI_XML_TO_INGEST_PATH')

pdf_being_extracted_path = os.path.join(pdf_new_path, "pdf_being_extracted")
os.makedirs(pdf_being_extracted_path, exist_ok=True)
pdf_ingestion_failed_already_exists_path = os.path.join(pdf_ingestion_failed_path, "pdf_already_ingested")
os.makedirs(pdf_ingestion_failed_already_exists_path, exist_ok=True)
pdf_ingestion_failed_grobid_extraction_failed_path = os.path.join(pdf_ingestion_failed_path, "grobid_extraction_failed")
os.makedirs(pdf_ingestion_failed_grobid_extraction_failed_path, exist_ok=True)

client = GrobidClient(config_path="grobid_config.json")


def extract_pdf():
    # check if the new file names are not already in the collection
    documents_in_collection = get_articles_list()
    for filename in os.listdir(pdf_new_path):
        if filename in documents_in_collection:
            log.error("A PDF file in the collection already exists with the same name: " + filename)
            shutil.move(
                os.path.join(pdf_new_path, filename),
                os.path.join(pdf_ingestion_failed_path, "pdf_already_ingested")
            )

    nb_pdf = 0
    # move pdf to be extracted in a dedicated directory
    for filename in os.listdir(pdf_new_path):
        if filename.lower().endswith(".pdf") and filename[-4:] != ".pdf":
            os.rename(os.path.join(pdf_new_path, filename), os.path.join(pdf_new_path, filename[-4:] + ".pdf"))
        if filename.endswith(".pdf"):
            nb_pdf += 1
            shutil.move(os.path.join(pdf_new_path, filename), pdf_being_extracted_path)

    # no PDF to extract
    if nb_pdf == 0:
        return

    # process all the PDF in the directory data/pdf_new
    client.process("processFulltextDocument", pdf_being_extracted_path, n=int((os.cpu_count() + 1) / 2))

    nb_pdf_success = 0
    # move the processed files
    for filename in os.listdir(pdf_being_extracted_path):
        if ".grobid.tei.xml" == filename[-15:]:
            nb_pdf_success += 1
            shutil.move(os.path.join(pdf_being_extracted_path, filename), tei_xml_to_ingest_path)
            shutil.move(os.path.join(pdf_being_extracted_path, filename[:-15] + ".pdf"), pdf_collection_path)

    nb_pdf_failed = 0
    # for all remaining pdf in pdf_being_extracted_path, aka pdf which experienced an error during the extraction
    for filename in os.listdir(pdf_being_extracted_path):
        nb_pdf_failed += 1
        log.error("The following PDF file experienced an error during the extraction with GROBID: " + filename)
        shutil.move(os.path.join(pdf_being_extracted_path, filename),
                    pdf_ingestion_failed_grobid_extraction_failed_path)

    log.info(f"The extraction of {nb_pdf} PDFs finished with {nb_pdf_success} successes and {nb_pdf_failed} failures.")


if __name__ == '__main__':
    extract_pdf()
