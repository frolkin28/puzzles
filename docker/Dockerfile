FROM python:3.12.4-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ========= install and configure pdm
ENV PIP_VERSION=24.1.2
ENV PDM_VERSION=2.17.1
ENV PDM_USE_VENV=no
ENV PYTHONPATH=/work/__pypackages__/3.12/lib

RUN pip install --upgrade pip==${PIP_VERSION} && \
    pip install pdm==${PDM_VERSION} && \
    pdm config cache_dir /pdm_cache && \
    pdm config check_update false

WORKDIR /app

COPY pyproject.toml .
COPY pdm.lock .
RUN pdm install --no-lock --no-editable --prod


# ==== dev backend build (don`t need to copy, because of mounting)
FROM base AS dev

ENTRYPOINT ["pdm", "run"]
