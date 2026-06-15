FROM ghcr.io/astral-sh/uv:0.9.17@sha256:5cb6b54d2bc3fe2eb9a8483db958a0b9eebf9edff68adedb369df8e7b98711a2 AS uv

FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm@sha256:b726eb94f42fcddb10056835f2c474c9f9e12e717ba2b2d2f9a8b1d78feeb68b

COPY --from=uv /uv /uvx /usr/local/bin/
