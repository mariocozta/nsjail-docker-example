FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    clang \
    pkg-config \
    protobuf-compiler \
    flex \
    bison \
    libtool \
    autoconf \
    automake \
    libnl-route-3-dev \
    libcap-dev \
    libseccomp-dev \
    libelf-dev \
    zlib1g-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail.git /opt/nsjail && \
    make -C /opt/nsjail && \
    cp /opt/nsjail/nsjail /usr/local/bin/nsjail && \
    rm -rf /opt/nsjail

RUN mkdir -p /sandbox /config

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app.py /app.py
COPY runner.py /sandbox/runner.py
COPY nsjail.cfg /config/nsjail.cfg

ENV USE_NSJAIL=false

EXPOSE 8080

WORKDIR /
CMD ["python", "app.py"]
