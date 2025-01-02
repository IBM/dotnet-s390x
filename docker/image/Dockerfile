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

FROM ubuntu:18.04
LABEL org.opencontainers.image.source https://github.com/ibm/dotnet-s390x
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y ca-certificates curl
COPY fs/ /
ARG llvm_version=11
RUN apt-get update && \
    apt-get install --no-install-recommends --yes \
        binutils-multiarch \
        clang-$llvm_version \
        cpio \
        gawk \
        git \
        jq \
        less \
        liblttng-ust0 \
        libssl-dev \
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
        zsh
ARG deb_arch
ARG gnu_arch
RUN if [ "$deb_arch" = "" ]; then \
        apt-get update && \
        apt-get install --no-install-recommends --yes \
            libgcc-8-dev \
            libicu-dev \
            libkrb5-dev \
            liblttng-ust-dev \
            libstdc++-8-dev \
            zlib1g-dev; \
    else \
        dpkg --add-architecture "$deb_arch" && \
        apt-get update && \
        apt-get install --no-install-recommends --yes \
            binutils-"$gnu_arch"-linux-gnu \
            libgcc-8-dev-"$deb_arch"-cross \
            libicu-dev:"$deb_arch" \
            libkrb5-dev:"$deb_arch" \
            liblttng-ust-dev:"$deb_arch" \
            libssl-dev:"$deb_arch" \
            libstdc++-8-dev-"$deb_arch"-cross \
            zlib1g-dev:"$deb_arch"; \
    fi
ENV PATH=/usr/lib/llvm-$llvm_version/bin:$PATH
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
COPY --from=cmake /cmake/ /
COPY --from=gh /cli/bin/gh /usr/bin/
# Prevent qemu-user guests from reading the host ld.so.cache and crashing.
ENV QEMU_LD_PREFIX=/usr/"$deb_arch"-linux-gnu
RUN mkdir -p "$QEMU_LD_PREFIX"/etc
RUN touch "$QEMU_LD_PREFIX"/etc/ld.so.cache
