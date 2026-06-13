# syntax=docker/dockerfile:1
# Slim multi-stage build: install in a builder, ship only /usr/local. Cuts the
# pushed image ~43% (no default-jre/dev-tools/source) so layer pushes finish well
# inside the registry's blob-upload window even under concurrency.
FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_SYSTEM_PYTHON=1 \
    UV_HTTP_TIMEOUT=3600
# Some [all] deps (e.g. hnswlib, an agent-utilities transitive) ship no manylinux
# wheel and build from sdist, needing a C++ toolchain. Install it in the builder
# only — the final stage copies just /usr/local, so no compiler ships.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --upgrade --break-system-packages --prerelease=allow listmonk-api[all]>=0.24.0

FROM python:3.11-slim

ARG HOST=0.0.0.0
ARG PORT=8000
ARG TRANSPORT="http"
ARG AUTH_TYPE="none"
ARG TOKEN_JWKS_URI=""
ARG TOKEN_ISSUER=""
ARG TOKEN_AUDIENCE=""
ARG OAUTH_UPSTREAM_AUTH_ENDPOINT=""
ARG OAUTH_UPSTREAM_TOKEN_ENDPOINT=""
ARG OAUTH_UPSTREAM_CLIENT_ID=""
ARG OAUTH_UPSTREAM_CLIENT_SECRET=""
ARG OAUTH_BASE_URL=""
ARG OIDC_CONFIG_URL=""
ARG OIDC_CLIENT_ID=""
ARG OIDC_CLIENT_SECRET=""
ARG OIDC_BASE_URL=""
ARG REMOTE_AUTH_SERVERS=""
ARG REMOTE_BASE_URL=""
ARG ALLOWED_CLIENT_REDIRECT_URIS=""
ARG EUNOMIA_TYPE="none"
ARG EUNOMIA_POLICY_FILE="mcp_policies.json"
ARG EUNOMIA_REMOTE_URL=""

ENV HOST=${HOST} \
    PORT=${PORT} \
    TRANSPORT=${TRANSPORT} \
    AUTH_TYPE=${AUTH_TYPE} \
    TOKEN_JWKS_URI=${TOKEN_JWKS_URI} \
    TOKEN_ISSUER=${TOKEN_ISSUER} \
    TOKEN_AUDIENCE=${TOKEN_AUDIENCE} \
    OAUTH_UPSTREAM_AUTH_ENDPOINT=${OAUTH_UPSTREAM_AUTH_ENDPOINT} \
    OAUTH_UPSTREAM_TOKEN_ENDPOINT=${OAUTH_UPSTREAM_TOKEN_ENDPOINT} \
    OAUTH_UPSTREAM_CLIENT_ID=${OAUTH_UPSTREAM_CLIENT_ID} \
    OAUTH_UPSTREAM_CLIENT_SECRET=${OAUTH_UPSTREAM_CLIENT_SECRET} \
    OAUTH_BASE_URL=${OAUTH_BASE_URL} \
    OIDC_CONFIG_URL=${OIDC_CONFIG_URL} \
    OIDC_CLIENT_ID=${OIDC_CLIENT_ID} \
    OIDC_CLIENT_SECRET=${OIDC_CLIENT_SECRET} \
    OIDC_BASE_URL=${OIDC_BASE_URL} \
    REMOTE_AUTH_SERVERS=${REMOTE_AUTH_SERVERS} \
    REMOTE_BASE_URL=${REMOTE_BASE_URL} \
    ALLOWED_CLIENT_REDIRECT_URIS=${ALLOWED_CLIENT_REDIRECT_URIS} \
    EUNOMIA_TYPE=${EUNOMIA_TYPE} \
    EUNOMIA_POLICY_FILE=${EUNOMIA_POLICY_FILE} \
    EUNOMIA_REMOTE_URL=${EUNOMIA_REMOTE_URL} \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:/usr/local/bin:${PATH}" \
    UV_HTTP_TIMEOUT=3600 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1
COPY --from=builder /usr/local /usr/local

CMD ["listmonk-mcp"]
