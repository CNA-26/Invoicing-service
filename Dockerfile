FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

RUN mkdir -p /code/app/pdfs && chmod 777 /code/app/pdfs

ENV PORT=8080
ENV PDF_FOLDER=/code/app/pdfs

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
