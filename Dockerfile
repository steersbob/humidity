FROM python:3.7 as base

ENV PIP_EXTRA_INDEX_URL=https://www.piwheels.org/simple
ENV PIP_FIND_LINKS=/wheeley

RUN set -ex \
    && pip3 install wheel \
    && pip3 wheel --wheel-dir/wheeley paho-mqtt adafruit-DHT

FROM python:3.7-slim
WORKDIR /app

COPY --from=base /wheeley /wheeley
COPY script.py /app/script.py

RUN pip3 install --no-index --find-links=/wheeley paho-mqtt adafruit-DHT

CMD ["python3", "/app/script.py"]
