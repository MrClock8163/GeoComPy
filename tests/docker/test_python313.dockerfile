FROM python:3.13-slim-trixie

LABEL maintainer="MrClock"
LABEL name="GeoComPy Python 3.13 testing container"
LABEL description="Python 3.13 testing container with preinstalled packages for the GeoComPy package"

RUN apt-get update && apt-get install socat -y
