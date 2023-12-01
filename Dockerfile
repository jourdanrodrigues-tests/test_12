FROM python:3.10.13-alpine
LABEL maintainer="Jourdan Rodrigues <thiagojourdan@gmail.com>"

WORKDIR /server/

RUN apk add -qU --no-cache postgresql-libs && \
    apk add -q --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev jpeg-dev zlib-dev

COPY requirements.txt ./

RUN pip install --no-cache --upgrade pip setuptools -r requirements.txt && \
    apk --purge del .build-deps

COPY . .

RUN SECRET_KEY=dummy ./manage.py collectstatic --no-input
