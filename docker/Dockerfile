FROM python:3.7.4

RUN useradd --no-user-group --create-home --shell /bin/bash gentex
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF="Dev"

# Use specific environment file for docker
COPY ["requirements.txt", "/opt/requirements.txt"]
COPY [".", "/src/gentex"]

RUN apt-get update -qq \
    && pip install -r /opt/requirements.txt \
    && cd /src/gentex \
    && python setup.py build_ext -i \
    && python setup.py install \
    && chown -R gentex /src/gentex

USER gentex

WORKDIR /src/gentex
