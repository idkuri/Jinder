FROM python:3.8.3-slim-buster

WORKDIR /server

ENV HOME /server

COPY . .

RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all \
    && rm -rf /var/lib/apt/lists/*
    
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]
