FROM python:3.13.0a6-slim-bookworm

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./main.py"]

