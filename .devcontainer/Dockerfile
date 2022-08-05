# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.241.1/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use ubuntu-22.04 or ubuntu-18.04 on local arm64/Apple Silicon): ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="jammy"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

ENV DEBIAN_FRONTEND=noninteractive

# Install basic apt packages
RUN apt-get update && apt-get install gettext-base && rm -rf /var/lib/apt/lists/*

# Install apt packages
COPY apt.txt /tmp/
RUN echo $(cat /tmp/apt.txt | cut -d# -f1 | envsubst)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends $(cat /tmp/apt.txt | cut -d# -f1 | envsubst) \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
