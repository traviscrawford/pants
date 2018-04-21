# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

FROM centos:7

RUN yum -y update
RUN yum install -y centos-release-scl
RUN yum install -y \
  devtoolset-7 \
  git \
  java-1.8.0-openjdk-devel \
  libffi \
  libffi-devel \
  python27 \
  openssl \
  openssl-devel \
  which

# By default, execute in an environment with python27 enabled.
ENTRYPOINT ["/usr/bin/scl", "enable", "python27", "devtoolset-7", "--"]
