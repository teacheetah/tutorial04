# ARG DISTRO=python:3.8-alpine3.14
# FROM python:3.8-slim
ARG DISTRO=python:3.8
FROM $DISTRO

RUN mkdir -p /teacheetah

COPY . /teacheetah

WORKDIR /teacheetah

RUN pip install -r config/requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:init_app", "--worker-class", "aiohttp.GunicornWebWorker", "--access-logfile", "-"]

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1
