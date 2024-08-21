FROM python:3.10-alpine AS Builder
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev linux-headers

ENV PYTHONNUMBUFFERED 1

RUN mkdir /code

WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x ./entry.sh
