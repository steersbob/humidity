FROM python:3.7 as base

ENV PIP_EXTRA_INDEX_URL=https://www.piwheels.org/simple

RUN set -ex \
    && pip3 install wheel \
    && pip3 wheel --wheel-dir=/wheeley paho-mqtt adafruit-DHT

FROM python:3.7-slim
WORKDIR /app

COPY --from=base /wheeley /wheeley
RUN pip3 install --no-index --find-links=/wheeley paho-mqtt adafruit-DHT

COPY script.py /app/script.py

CMD ["python3", "-u", "/app/script.py"]
