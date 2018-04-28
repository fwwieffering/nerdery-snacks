FROM python:3.6-alpine

MAINTAINER fwieffering@gmail.com

RUN apk add gcc g++ make libffi-dev openssl-dev postgresql-dev python3-dev musl-dev bash --no-cache

RUN mkdir /build
COPY requirements.txt /build
RUN cd /build &&  pip install -r requirements.txt

RUN mkdir -p /work
COPY ./snacks/ /work/snacks
COPY ./setup.py /work/
RUN cd /work && pip install -e .


WORKDIR /work



ENTRYPOINT ["gunicorn", "--reload", "-b", "0.0.0.0:5050", "snacks.api:app"]
