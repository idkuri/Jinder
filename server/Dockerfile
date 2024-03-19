FROM python:3.8

WORKDIR /server

ENV HOME /server

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD python3 -u server.py
