FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /app/database

COPY mysite .

CMD ["gunicorn" "mysite.wsgi:application" "--bind" "0.0.0.0:8000"]