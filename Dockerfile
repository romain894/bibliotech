FROM python:3.12

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY grobid_config_docker.json grobid_config.json
COPY .env_docker .env
COPY *.py .

LABEL authors="Romain Thomas"
LABEL org.opencontainers.image.source="https://github.com/romain894/bibliotech"

ENTRYPOINT ["python3", "bibliotech_main.py"]