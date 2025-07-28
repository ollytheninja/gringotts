# Some things are required at all stages, so we'll define them up front.
FROM python:3.13-alpine as builder

# With the $PYTHONDONTWRITEBYTECODE environment variable set,
# Python will no longer write .pyc files to disk.
# https://python-docs.readthedocs.io/en/latest/writing/gotchas.html#bytecode-pyc-files-everywhere
ENV PYTHONDONTWRITEBYTECODE=1

# Ensures that the python output i.e. the stdout and stderr streams are sent straight to terminal
# without being first buffered and that you can see the output of your application (e.g. django logs) in real time.
# This also ensures that no partial output is held in a buffer somewhere and never written in case the container crashes.
ENV PYTHONUNBUFFERED=1

# We update the container and pip out of band, so this warning message isn't useful and the check slows down the build.
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install pre-requisites for building packages pip installs.
RUN apk update && \
    apk add --no-cache \
    build-base  \
    cmake  \
    gcc  \
    git  \
    python3-dev

# We're using a virtualenvironment, adding it to PATH is the equivalent of running ./venv/bin/activate
ENV PATH="/venv/bin:$PATH"
RUN python -m venv /venv

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

FROM python:3.13-alpine as runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PATH="/venv/bin:$PATH"
COPY --from=builder /venv /venv

RUN mkdir /app
WORKDIR "/app"

# Copy all the source into /app
COPY . .

# Make our entrypoint script executable and run it!
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
