FROM python:3.12-slim AS builder

ARG INSTALL_DEV=false

ENV POETRY_VERSION=2.0.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PATH=${POETRY_HOME}/bin:${PATH}

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN if [ "${INSTALL_DEV}" = "true" ]; then poetry install --no-root --with dev; else poetry install --no-root --only main; fi
COPY . .

EXPOSE 8000


