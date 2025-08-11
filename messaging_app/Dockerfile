# ===== base image =====
FROM python:3.10-slim

# system deps (add build tools if your DB driver needs them)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential curl netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

# install deps first (better layer cache)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# optional: wait-for-db script if using Postgres/MySQL
# COPY ./docker/wait-for.sh /usr/local/bin/wait-for
# RUN chmod +x /usr/local/bin/wait-for

# environment (adjust for your project)
ENV DJANGO_SETTINGS_MODULE=messaging_app.settings \
  PYTHONPATH=/app

# add entrypoint to run migrations then exec gunicorn
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8000

# optional: container healthcheck (expects /healthz route)
# HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
#   CMD curl -fsS http://127.0.0.1:8000/healthz || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "90"]
