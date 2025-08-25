FROM python:3.11-slim-trixie

LABEL maintainer="MrClock"
LABEL name="GeoComPy Python 3.11 testing container"
LABEL description="Python 3.11 testing container for the GeoComPy package"

RUN apt-get update & apt-get install socat -y

WORKDIR /usr/src/build

COPY ./pyproject.toml ./pyproject.toml

RUN python -m pip install pip-tools
RUN python -m piptools compile -o tests/requirements.txt pyproject.toml --pip-args "--group testing"
RUN python -m pip install -r test/requirements.txt
