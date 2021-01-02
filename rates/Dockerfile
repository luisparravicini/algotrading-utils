FROM python:alpine as base


FROM base as builder

RUN apk --no-cache add gcc musl-dev libffi-dev openssl-dev
RUN mkdir /deps_install

WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/deps_install -r requirements.txt


FROM base

COPY --from=builder /deps_install /usr/local

WORKDIR /app

COPY bin/updater.sh bin/
COPY updater updater

RUN mkdir data


CMD [ "/app/bin/updater.sh", "kraken", "BTC/USD", "/app/data" ]
