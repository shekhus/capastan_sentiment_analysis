FROM python:3.11-slim

WORKDIR /app

COPY flask_app/ /app/
# COPY models/vectorizer.pkl /app/models/vectorizer.pkl
COPY models/vectorizer.pkl /models/vectorizer.pkl


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

CMD ["python", "app.py"]
