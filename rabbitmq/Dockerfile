FROM python:3.8

LABEL Author="Alejandro Dotor"
LABEL E-mail="alexdotordp@gmail.com"

RUN mkdir /worker
ADD . worker/
WORKDIR /worker
RUN pip install -r requirements.txt
CMD python worker.py