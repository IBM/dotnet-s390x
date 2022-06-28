# Based on Stefan Schulze Frielinghaus' dotnet-cloud-init.
# Use old Ubuntu for RHEL compatibility.
FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
COPY fs/ /
RUN dpkg --add-architecture s390x && \
    apt-get update && \
    apt-get install --no-install-recommends --yes \
        binutils-multiarch \
        binutils-s390x-linux-gnu \
        clang \
        gawk \
        git \
        libgcc-8-dev-s390x-cross \
        libicu-dev:s390x \
        libkrb5-dev:s390x \
        liblttng-ust-dev:s390x \
        liblttng-ust0 \
        libssl-dev:s390x \
        libstdc++-8-dev-s390x-cross \
        libxml2-utils \
        llvm \
        locales \
        lttng-modules-dkms \
        lttng-tools \
        mono-devel \
        ninja-build \
        nodejs \
        python3 \
        python3-pip \
        quilt \
        tmux \
        vim \
        wget \
        yarn \
        zlib1g-dev:s390x \
        zsh
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
# v3.14.5+
RUN python3 -m pip install cmake
