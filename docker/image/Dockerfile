# Based on Stefan Schulze Frielinghaus' dotnet-cloud-init.
# Use old Ubuntu for RHEL compatibility.
FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
COPY fs/ /
ARG llvm_version=7
RUN dpkg --add-architecture s390x && \
    apt-get update && \
    apt-get install --no-install-recommends --yes \
        binutils-multiarch \
        binutils-s390x-linux-gnu \
        clang-$llvm_version \
        gawk \
        git \
        jq \
        libgcc-8-dev-s390x-cross \
        libicu-dev:s390x \
        libkrb5-dev:s390x \
        liblttng-ust-dev:s390x \
        liblttng-ust0 \
        libssl-dev \
        libssl-dev:s390x \
        libstdc++-8-dev-s390x-cross \
        libxml2-utils \
        llvm-$llvm_version \
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
ENV PATH=/usr/lib/llvm-$llvm_version/bin:$PATH
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
# v3.14.5+
RUN cd /tmp && \
    curl -L https://github.com/Kitware/CMake/releases/download/v3.23.2/cmake-3.23.2.tar.gz | tar -xz && \
    cd cmake-3.23.2 && \
    ./bootstrap --parallel="$(nproc)" && \
    make -j"$(nproc)" install && \
    cd .. && \
    rm -r cmake-3.23.2 \
