FROM python:3.12-slim-trixie

LABEL maintainer="MrClock"
LABEL name="GeoComPy Python 3.12 testing container"
LABEL description="Python 3.12 testing container with preinstalled packages for the GeoComPy package"

RUN apt-get update && apt-get install socat -y
RUN python -m pip install --upgrade pip
