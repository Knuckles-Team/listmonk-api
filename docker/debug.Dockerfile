FROM python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6
COPY --from=ghcr.io/astral-sh/uv:0.11.7@sha256:240fb85ab0f263ef12f492d8476aa3a2e4e1e333f7d67fbdd923d00a506a516a /uv /uvx /bin/

ARG HOST=127.0.0.1
ARG PORT=8000
ARG TRANSPORT="http"
ARG AUTH_TYPE="none"
ARG TOKEN_JWKS_URI=""
ARG TOKEN_ISSUER=""
ARG TOKEN_AUDIENCE=""
ARG OAUTH_UPSTREAM_AUTH_ENDPOINT=""
ARG OAUTH_UPSTREAM_TOKEN_ENDPOINT=""
ARG OAUTH_UPSTREAM_CLIENT_ID=""
ARG OAUTH_BASE_URL=""
ARG OIDC_CONFIG_URL=""
ARG OIDC_CLIENT_ID=""
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
    OAUTH_BASE_URL=${OAUTH_BASE_URL} \
    OIDC_CONFIG_URL=${OIDC_CONFIG_URL} \
    OIDC_CLIENT_ID=${OIDC_CLIENT_ID} \
    OIDC_BASE_URL=${OIDC_BASE_URL} \
    REMOTE_AUTH_SERVERS=${REMOTE_AUTH_SERVERS} \
    REMOTE_BASE_URL=${REMOTE_BASE_URL} \
    ALLOWED_CLIENT_REDIRECT_URIS=${ALLOWED_CLIENT_REDIRECT_URIS} \
    EUNOMIA_TYPE=${EUNOMIA_TYPE} \
    EUNOMIA_POLICY_FILE=${EUNOMIA_POLICY_FILE} \
    EUNOMIA_REMOTE_URL=${EUNOMIA_REMOTE_URL} \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/cargo/bin:/usr/local/bin:${PATH}" \
    UV_HTTP_TIMEOUT=3600 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app
COPY . /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-jre ripgrep tree fd-find curl nano build-essential cmake libssl-dev libcurl4-openssl-dev pkg-config cargo rustc \
    && uv pip install --system --no-cache --break-system-packages .[agent] \
    && rm -rf /var/lib/apt/lists/*


# Debug tooling is installed at build time; the running service stays unprivileged.
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid 10001 --no-create-home \
        --home-dir /tmp --shell /usr/sbin/nologin app \
    && chown -R 10001:10001 /app
ENV HOME=/tmp \
    XDG_CONFIG_HOME=/tmp/.config \
    XDG_CACHE_HOME=/tmp/.cache
USER 10001:10001

CMD ["listmonk-mcp"]
