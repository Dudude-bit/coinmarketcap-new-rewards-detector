FROM python:3.9

WORKDIR /main

COPY requirements.txt ./

RUN apt update -y

RUN apt install -y python3-pip

RUN pip3 install -r requirements.txt

COPY docker-entrypoint.sh ./

COPY src ./

CMD ./docker-entrypoint.sh