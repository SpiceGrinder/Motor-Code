FROM python:3

ADD ./src .

RUN pip install json-rpc

RUN pip install Werkzeug

#RUN pip install grpcio

EXPOSE 4000:4000

CMD [ "python", "./app.py" ]

