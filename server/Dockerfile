FROM python:3.8

WORKDIR /server

ENV HOME /server

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]
