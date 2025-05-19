FROM python:3.12-alpine as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    jpeg-dev \
    zlib-dev && \
    rm -rf /var/cache/apk/*

RUN pip install -U uv
COPY requirements.txt .
RUN uv pip install --no-cache-dir --system -r requirements.txt


COPY . .

FROM base as production

COPY --from=base /app /app
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 4 your_project.wsgi:application"]

FROM base as development

ENV DEBUG=True

COPY --from=base /app /app
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

COPY requirements-dev.txt .
RUN pip install --no-cache-dir --user -r requirements-dev.txt

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]