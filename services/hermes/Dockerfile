FROM python:3.11-slim-bookworm@sha256:e2d3af735aff6eeee600b1933bedd99da6645fedf572cc12ef4cc1331f2ceebe

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 10001 hermes

COPY services/hermes/requirements.txt /tmp/hermes-requirements.txt

RUN mkdir -p /opt/data/personal /opt/data/work /workspace \
    && chown -R hermes:hermes /opt/data /workspace \
    && pip install --no-cache-dir -r /tmp/hermes-requirements.txt

USER hermes
WORKDIR /workspace

CMD ["hermes"]
