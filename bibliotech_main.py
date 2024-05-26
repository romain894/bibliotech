import os
import time

from dotenv import load_dotenv

from extract_pdf import extract_pdf
from generate_documents import generate_documents
from enrich_documents import enrich_documents
from ingest_documents import ingest_documents
from log_config import log

load_dotenv()

scan_refresh_rate = int(os.getenv('SCAN_REFRESH_RATE'))


def bibliotech_main_tasks():
    # reverse order so we make sure to not lose data if the program was interrupted
    ingest_documents()
    enrich_documents()
    generate_documents()
    extract_pdf()


def bibliotech_main_loop():
    log.info("Checking for new documents...")
    bibliotech_main_tasks()
    print("Idle for "+str(scan_refresh_rate)+" second(s)...")
    time.sleep(scan_refresh_rate) # refresh rate of one second


if __name__ == '__main__':
    bibliotech_main_loop()