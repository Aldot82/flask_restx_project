FROM python:3.8

LABEL Author="Alejandro Dotor"
LABEL E-mail="alexdotordp@gmail.com"

RUN mkdir /app
ADD . app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000