# Based on Stefan Schulze Frielinghaus' dotnet-cloud-init.
# Use old Ubuntu for RHEL compatibility.

FROM ubuntu:18.04 as cmake
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
        curl \
        g++ \
        gcc \
        git \
        libssl-dev \
        make
# v3.14.5+
RUN curl -L https://github.com/Kitware/CMake/releases/download/v3.23.2/cmake-3.23.2.tar.gz | tar -xz
RUN cd cmake-3.23.2 && ./bootstrap --parallel="$(nproc)"
RUN cd cmake-3.23.2 && make -j"$(nproc)" install DESTDIR=/cmake

FROM ubuntu:18.04 as gh
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
        curl \
        gcc \
        git \
        make
RUN curl -L https://go.dev/dl/go1.18.3.linux-$(dpkg --print-architecture).tar.gz | tar -xz
RUN git clone --branch=v2.13.0 --depth=1 https://github.com/cli/cli.git
RUN cd cli && PATH=/go/bin:$PATH make

FROM ubuntu:18.04 as gdb
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
        bison \
        flex \
        g++ \
        gcc \
        git \
        libexpat1-dev \
        libgmp-dev \
        libncurses5-dev \
        libpython3-dev \
        make \
        python3 \
        python3-distutils \
        texinfo
RUN git clone \
        --branch=section-map-20220801 \
        --depth=1 \
        https://github.com/iii-i/binutils-gdb.git
RUN cd binutils-gdb && ./configure --with-python=python3
RUN cd binutils-gdb && make -j"$(nproc)"
RUN cd binutils-gdb && make -j"$(nproc)" install DESTDIR=/gdb

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
        less \
        libgcc-8-dev \
        libgcc-8-dev-s390x-cross \
        libicu-dev:s390x \
        libkrb5-dev \
        libkrb5-dev:s390x \
        liblttng-ust-dev \
        liblttng-ust-dev:s390x \
        liblttng-ust0 \
        libssl-dev \
        libssl-dev:s390x \
        libstdc++-8-dev \
        libstdc++-8-dev-s390x-cross \
        libxml2-utils \
        llvm-$llvm_version \
        locales \
        lttng-modules-dkms \
        lttng-tools \
        mono-devel \
        ninja-build \
        nodejs \
        psmisc \
        python3 \
        quilt \
        ssh \
        strace \
        tmux \
        unzip \
        vim \
        wget \
        yarn \
        zlib1g-dev \
        zlib1g-dev:s390x \
        zsh
# libicu-dev conflicts with libicu-dev:s390x because of /usr/bin/icu-config
# (fixed in focal). Install libicu-dev:s390x first and then force overwrite.
RUN apt-get update && \
    apt-get install -y libiculx60 libicu-le-hb-dev && \
    apt-get download libicu-dev && \
    dpkg --force-conflicts -i libicu-dev*.deb && \
    rm libicu-dev*.deb
ENV PATH=/usr/lib/llvm-$llvm_version/bin:$PATH
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
COPY --from=cmake /cmake/ /
COPY --from=gh /cli/bin/gh /usr/bin/
COPY --from=gdb /gdb/ /
