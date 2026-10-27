FROM python:3.13-slim AS build

COPY --from=ghcr.io/astral-sh/uv:0.9.9 /uv /bin/uv
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY build.py data.py ./
COPY templates templates
COPY static static
COPY docs docs
RUN uv run --no-sync python build.py --out /app/dist


FROM nginxinc/nginx-unprivileged:1.29-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
