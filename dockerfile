FROM python:3.10.10

ENV PORT 8080

WORKDIR /app

COPY server/src/ /app

RUN pip install Flask gunicorn pipenv

RUN pipenv install --deploy --system

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
