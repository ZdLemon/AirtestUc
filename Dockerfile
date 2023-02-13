FROM python:3.10-slim as base

FROM base as builder
RUN apt-get update && apt-get install -y git
# there are no wheels for some packages (geventhttpclient?) for arm64/aarch64, so we need some build dependencies there
RUN if [ -n "$(arch | grep 'arm64\|aarch64')" ]; then apt install -y --no-install-recommends gcc python3-dev; fi
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# COPY requirements.txt /build/requirements.txt
RUN python3 -m pip install --upgrade pip \
    && pip install airtest \
    && pip install pocoui \
    && pip install pytest \
    && pip install allure-pytest \
    && pip install loguru \
    && pip install opencv-python-headless

FROM base
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# turn off python output buffering
ENV PYTHONUNBUFFERED=1
RUN useradd --create-home uc
# ensure correct permissions
RUN chown -R uc /opt/venv \
    && chown -R uc /home/uc
USER uc
WORKDIR /home/uc
