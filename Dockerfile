FROM python:3.11-slim
SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN useradd --home-dir /app runner && chown -R runner:runner /app
USER runner

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/app/.local/bin:${PATH}"

COPY --chown=runner:runner . /app/
RUN python -m venv venv && source venv/bin/activate && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

ENTRYPOINT ["/app/start-server.bash"]
