# Backing Platform — Listmonk

`listmonk-api` is a **client** of a [Listmonk](https://listmonk.app/) instance. This
page provides a Docker recipe for deploying one locally to serve as the target of
`LISTMONK_URL`. For production topologies, follow the upstream
[Listmonk documentation](https://listmonk.app/docs/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a `docs/platform.md`
    recipe for the system it integrates with, accompanied by a sample Compose stack that
    mirrors the system's official image. Systems offered only as a managed service have
    no local recipe; only connection configuration is required.

## Single-node deployment (Compose)

Listmonk publishes the `listmonk/listmonk` image and requires a PostgreSQL database. The
following stack runs Listmonk on `:9000` with a dedicated Postgres instance:

```yaml
# docker/listmonk-platform.compose.yml
services:
  listmonk-db:
    image: postgres:16-alpine
    container_name: listmonk-db
    hostname: listmonk-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=listmonk
      - POSTGRES_PASSWORD=listmonk
      - POSTGRES_DB=listmonk
    volumes:
      - listmonk_db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U listmonk"]
      interval: 10s
      timeout: 5s
      retries: 6

  listmonk:
    image: listmonk/listmonk@sha256:<digest>
    container_name: listmonk
    hostname: listmonk
    restart: unless-stopped
    depends_on:
      listmonk-db:
        condition: service_healthy
    ports:
      - "9000:9000"            # Listmonk admin + API (HTTP)
    environment:
      - LISTMONK_app__address=0.0.0.0:9000
      - LISTMONK_db__host=listmonk-db
      - LISTMONK_db__port=5432
      - LISTMONK_db__user=listmonk
      - LISTMONK_db__password=listmonk
      - LISTMONK_db__database=listmonk
    command: >
      sh -c "./listmonk --install --idempotent --yes && ./listmonk --upgrade --yes && ./listmonk"

volumes:
  listmonk_db:
```

```bash
docker compose -f docker/listmonk-platform.compose.yml up -d

# Wait for the API to answer
curl -s http://localhost:9000/api/health
```

After the first boot, sign in to the admin console at `http://localhost:9000/admin` and
create an **API user / token** (Settings → Users) to authenticate `listmonk-api`.

## Connect listmonk-api

```bash
export LISTMONK_URL=https://listmonk.example.invalid
export LISTMONK_TOKEN=your-api-token
# Or, with basic auth:
# export LISTMONK_USERNAME=admin
# export LISTMONK_PASSWORD=your-listmonk-password

listmonk-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places Listmonk, its database, and the MCP server on one Docker network,
so the server reaches Listmonk by container name:

```yaml
# docker/stack.compose.yml
services:
  listmonk-db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=listmonk
      - POSTGRES_PASSWORD=listmonk
      - POSTGRES_DB=listmonk
    volumes: ["listmonk_db:/var/lib/postgresql/data"]

  listmonk:
    image: listmonk/listmonk@sha256:<digest>
    depends_on: [listmonk-db]
    ports: ["9000:9000"]
    environment:
      - LISTMONK_app__address=0.0.0.0:9000
      - LISTMONK_db__host=listmonk-db
      - LISTMONK_db__user=listmonk
      - LISTMONK_db__password=listmonk
      - LISTMONK_db__database=listmonk
    command: >
      sh -c "./listmonk --install --idempotent --yes && ./listmonk --upgrade --yes && ./listmonk"

  listmonk-api-mcp:
    image: example/listmonk-api@sha256:<digest>
    depends_on: [listmonk]
    environment:
      - LISTMONK_URL=${LISTMONK_URL:?set an authenticated HTTPS endpoint}
      - LISTMONK_TOKEN=your-api-token
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  listmonk_db:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

With the platform running and credentials configured, the MCP tools and the
[`ListmonkAPI`](usage.md#as-a-python-api) client can manage lists, subscribers,
campaigns, templates, and transactional sends against your instance.
