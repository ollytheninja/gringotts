FROM python:3.9-alpine as builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/venv/bin:$PATH"

RUN apk update && \
    apk add --no-cache \
    build-base  \
    cmake  \
    gcc  \
    git  \
    python3-dev

RUN python -m venv /venv

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/venv/bin:$PATH"

COPY --from=builder /venv /venv

RUN mkdir /app
WORKDIR "/app"

COPY . .

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
