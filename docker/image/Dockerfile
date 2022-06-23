# Based on Stefan Schulze Frielinghaus' dotnet-cloud-init.
FROM ubuntu:20.04
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
        cmake \
        gawk \
        git \
        libgcc-10-dev-s390x-cross \
        libicu-dev:s390x \
        libkrb5-dev:s390x \
        liblttng-ust-dev:s390x \
        liblttng-ust0 \
        libssl-dev:s390x \
        libstdc++-10-dev-s390x-cross \
        libxml2-utils \
        llvm \
        locales \
        lttng-modules-dkms \
        lttng-tools \
        mono-devel \
        ninja-build \
        nodejs \
        python3 \
        quilt \
        tmux \
        vim \
        wget \
        yarn \
        zlib1g-dev:s390x \
        zsh
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
