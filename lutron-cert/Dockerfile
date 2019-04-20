ARG BUILD_FROM=hassioaddons/base-python:1.1.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

# Copy Python requirements file
COPY requirements.txt /tmp/

# Setup base
RUN \
    apk add --no-cache --virtual .build-dependencies \
        gcc=8.3.0-r0 \
        libc-dev=0.7.1-r0 \
        libffi-dev=3.2.1-r6 \
        openssl-dev=1.1.1b-r1 \
    \
    && apk add --no-cache \
        dbus=1.10.24-r1 \
    \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt \
    \
    && find /usr/local \
        \( -type d -a -name test -o -name tests -o -name '__pycache__' \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    \
    && apk del --purge .build-dependencies


# Build arugments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="Lutron Certificate" \
    io.hass.description="Generate certificate to control Lutron Caseta bridge locally" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Dale Higgs <dale3h@addons.community>" \
    org.label-schema.description="Generate certificate to control Lutron Caseta bridge locally" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="Lutron Certificate" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.url="https://community.home-assistant.io/" \
    org.label-schema.usage="https://github.com/hassio-addons/addon-lutron-cert/tree/master/README.md" \
    org.label-schema.vcs-ref=${BUILD_REF} \
    org.label-schema.vcs-url="https://github.com/hassio-addons/addon-lutron-cert" \
    org.label-schema.vendor="Community Hass.io Addons"
